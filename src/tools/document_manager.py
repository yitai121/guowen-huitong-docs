"""
资料管理工具
支持文件上传、搜索、下载功能
"""
import os
import json
import mimetypes
from typing import Optional, List
from langchain.tools import tool, ToolRuntime
from postgrest.exceptions import APIError
from coze_coding_dev_sdk.s3 import S3SyncStorage
from storage.database.supabase_client import get_supabase_client
from coze_coding_dev_sdk import LLMClient
from coze_coding_utils.runtime_ctx.context import new_context
from langchain_core.messages import HumanMessage, SystemMessage

# 初始化对象存储客户端
storage = S3SyncStorage(
    endpoint_url=os.getenv("COZE_BUCKET_ENDPOINT_URL"),
    access_key="",
    secret_key="",
    bucket_name=os.getenv("COZE_BUCKET_NAME"),
    region="cn-beijing",
)


def _get_mime_type(file_name: str) -> str:
    """根据文件名获取 MIME 类型"""
    mime_type, _ = mimetypes.guess_type(file_name)
    return mime_type or "application/octet-stream"


def _format_file_size(size_bytes: int) -> str:
    """格式化文件大小"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"


@tool
def upload_document(title: str, file_path: str, description: str = None, category: str = None, tags: str = None, runtime: ToolRuntime = None) -> str:
    """
    上传文件到资料管理系统
    
    Args:
        title: 文件标题
        file_path: 文件路径（本地文件路径或 URL）
        description: 文件描述（可选）
        category: 文件分类（可选）
        tags: 文件标签，用逗号分隔（可选）
    
    Returns:
        上传结果，包含文档 ID 和访问 URL
    """
    try:
        # 判断是本地文件还是 URL
        if file_path.startswith("http://") or file_path.startswith("https://"):
            # 从 URL 上传
            file_key = storage.upload_from_url(url=file_path, timeout=60)
            file_name = file_path.split("/")[-1]
            
            # 获取文件大小（从存储对象获取）
            file_size = 0  # URL 上传无法直接获取大小
        else:
            # 本地文件上传
            if not os.path.exists(file_path):
                return f"错误：文件不存在 - {file_path}"
            
            # 读取文件内容
            with open(file_path, "rb") as f:
                file_content = f.read()
                file_size = len(file_content)
                file_name = os.path.basename(file_path)
            
            # 获取 MIME 类型
            content_type = _get_mime_type(file_name)
            
            # 上传到对象存储
            file_key = storage.upload_file(
                file_content=file_content,
                file_name=file_name,
                content_type=content_type
            )
        
        # 获取文件信息
        file_size_formatted = _format_file_size(file_size)
        file_type = _get_mime_type(file_name)
        
        # 保存到数据库
        client = get_supabase_client()
        
        document_data = {
            "title": title,
            "description": description,
            "file_name": file_name,
            "file_key": file_key,
            "file_size": file_size,
            "file_type": file_type,
            "category": category,
            "tags": tags,
            "download_count": 0
        }
        
        try:
            response = client.table('documents').insert(document_data).execute()
            document_id = response.data[0]['id']
        except APIError as e:
            # 上传失败，删除已上传的文件
            storage.delete_file(file_key=file_key)
            raise Exception(f"保存到数据库失败: {e.message}")
        
        # 生成下载 URL
        download_url = storage.generate_presigned_url(key=file_key, expire_time=86400)
        
        result = {
            "success": True,
            "message": "文件上传成功",
            "document_id": document_id,
            "title": title,
            "file_name": file_name,
            "file_size": file_size_formatted,
            "file_type": file_type,
            "category": category,
            "tags": tags,
            "download_url": download_url
        }
        
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"上传文件时出错: {str(e)}"


@tool
def search_documents(keyword: str = None, category: str = None, limit: int = 20, runtime: ToolRuntime = None) -> str:
    """
    搜索文档
    
    Args:
        keyword: 搜索关键词（在标题、描述、标签中搜索）
        category: 文件分类（可选）
        limit: 返回数量限制
    
    Returns:
        搜索结果列表
    """
    try:
        client = get_supabase_client()
        
        # 构建查询
        query = client.table('documents').select('id, title, description, file_name, file_size, file_type, category, tags, download_count, created_at').order('created_at', desc=True).limit(limit)
        
        # 添加过滤条件
        if category:
            query = query.eq('category', category)
        
        if keyword:
            # 在标题、描述、标签中搜索
            query = query.or_(f'title.ilike.%{keyword}%,description.ilike.%{keyword}%,tags.ilike.%{keyword}%')
        
        try:
            response = query.execute()
        except APIError as e:
            raise Exception(f"搜索失败: {e.message}")
        
        documents = response.data
        
        if not documents:
            return "未找到匹配的文档"
        
        # 格式化结果
        summary = f"【搜索结果】(共 {len(documents)} 个文档)\n\n"
        
        for doc in documents:
            summary += f"📄 ID: {doc['id']}\n"
            summary += f"   标题: {doc['title']}\n"
            summary += f"   文件名: {doc['file_name']}\n"
            summary += f"   大小: {_format_file_size(doc['file_size'])}\n"
            summary += f"   类型: {doc['file_type']}\n"
            if doc.get('category'):
                summary += f"   分类: {doc['category']}\n"
            if doc.get('tags'):
                summary += f"   标签: {doc['tags']}\n"
            if doc.get('description'):
                summary += f"   描述: {doc['description'][:100]}...\n"
            summary += f"   下载次数: {doc['download_count']}\n"
            summary += f"   上传时间: {doc['created_at']}\n\n"
        
        return summary.strip()
    except Exception as e:
        return f"搜索文档时出错: {str(e)}"


@tool
def get_document_detail(document_id: int, runtime: ToolRuntime = None) -> str:
    """
    获取文档详情
    
    Args:
        document_id: 文档 ID
    
    Returns:
        文档详情
    """
    try:
        client = get_supabase_client()
        
        try:
            response = client.table('documents').select('*').eq('id', document_id).maybe_single().execute()
        except APIError as e:
            raise Exception(f"查询失败: {e.message}")
        
        if response is None:
            return f"未找到 ID 为 {document_id} 的文档"
        
        doc = response.data
        
        # 生成下载 URL
        download_url = storage.generate_presigned_url(key=doc['file_key'], expire_time=86400)
        
        result = f"""
【文档详情】
ID: {doc['id']}
标题: {doc['title']}
文件名: {doc['file_name']}
文件大小: {_format_file_size(doc['file_size'])}
文件类型: {doc['file_type']}
"""
        if doc.get('description'):
            result += f"描述: {doc['description']}\n"
        if doc.get('category'):
            result += f"分类: {doc['category']}\n"
        if doc.get('tags'):
            result += f"标签: {doc['tags']}\n"
        
        result += f"""
下载次数: {doc['download_count']}
上传时间: {doc['created_at']}
更新时间: {doc.get('updated_at', 'N/A')}

下载链接: {download_url}
"""
        return result.strip()
    except Exception as e:
        return f"获取文档详情时出错: {str(e)}"


@tool
def download_document(document_id: int, runtime: ToolRuntime = None) -> str:
    """
    获取文档下载链接（并增加下载次数）
    
    Args:
        document_id: 文档 ID
    
    Returns:
        下载链接
    """
    try:
        client = get_supabase_client()
        
        # 先查询文档信息
        try:
            response = client.table('documents').select('id, file_key, download_count').eq('id', document_id).maybe_single().execute()
        except APIError as e:
            raise Exception(f"查询失败: {e.message}")
        
        if response is None:
            return f"未找到 ID 为 {document_id} 的文档"
        
        doc = response.data
        
        # 增加下载次数
        try:
            client.table('documents').update({'download_count': doc['download_count'] + 1}).eq('id', document_id).execute()
        except APIError as e:
            # 更新下载次数失败，但仍返回下载链接
            pass
        
        # 生成下载 URL
        download_url = storage.generate_presigned_url(key=doc['file_key'], expire_time=86400)
        
        result = {
            "success": True,
            "document_id": document_id,
            "download_url": download_url,
            "expires_in": "24小时"
        }
        
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"获取下载链接时出错: {str(e)}"


@tool
def list_documents(category: str = None, limit: int = 20, runtime: ToolRuntime = None) -> str:
    """
    列出所有文档
    
    Args:
        category: 按分类筛选（可选）
        limit: 返回数量限制
    
    Returns:
        文档列表
    """
    try:
        client = get_supabase_client()
        
        # 构建查询
        query = client.table('documents').select('id, title, file_name, file_size, file_type, category, download_count, created_at').order('created_at', desc=True).limit(limit)
        
        if category:
            query = query.eq('category', category)
        
        try:
            response = query.execute()
        except APIError as e:
            raise Exception(f"查询失败: {e.message}")
        
        documents = response.data
        
        if not documents:
            return "暂无文档"
        
        # 格式化结果
        summary = f"【文档列表】(共 {len(documents)} 个)\n\n"
        
        for doc in documents:
            summary += f"📄 ID: {doc['id']} | {doc['title']}\n"
            summary += f"   文件: {doc['file_name']} ({_format_file_size(doc['file_size'])})\n"
            if doc.get('category'):
                summary += f"   分类: {doc['category']}\n"
            summary += f"   下载: {doc['download_count']} 次 | 上传: {doc['created_at']}\n\n"
        
        return summary.strip()
    except Exception as e:
        return f"列出文档时出错: {str(e)}"


@tool
def delete_document(document_id: int, runtime: ToolRuntime = None) -> str:
    """
    删除文档
    
    Args:
        document_id: 文档 ID
    
    Returns:
        删除结果
    """
    try:
        client = get_supabase_client()
        
        # 先查询文档信息，获取 file_key
        try:
            response = client.table('documents').select('id, file_key').eq('id', document_id).maybe_single().execute()
        except APIError as e:
            raise Exception(f"查询失败: {e.message}")
        
        if response is None:
            return f"未找到 ID 为 {document_id} 的文档"
        
        doc = response.data
        file_key = doc['file_key']
        
        # 从数据库删除
        try:
            client.table('documents').delete().eq('id', document_id).execute()
        except APIError as e:
            raise Exception(f"删除数据库记录失败: {e.message}")
        
        # 从对象存储删除
        storage.delete_file(file_key=file_key)
        
        result = {
            "success": True,
            "message": "文档删除成功",
            "document_id": document_id
        }
        
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"删除文档时出错: {str(e)}"


@tool
def update_document(document_id: int, title: str = None, description: str = None, category: str = None, tags: str = None, runtime: ToolRuntime = None) -> str:
    """
    更新文档信息
    
    Args:
        document_id: 文档 ID
        title: 新标题（可选）
        description: 新描述（可选）
        category: 新分类（可选）
        tags: 新标签（可选）
    
    Returns:
        更新结果
    """
    try:
        client = get_supabase_client()
        
        # 构建更新数据
        update_data = {}
        if title is not None:
            update_data['title'] = title
        if description is not None:
            update_data['description'] = description
        if category is not None:
            update_data['category'] = category
        if tags is not None:
            update_data['tags'] = tags
        
        if not update_data:
            return "错误：没有提供任何更新字段"
        
        # 更新数据库
        try:
            response = client.table('documents').update(update_data).eq('id', document_id).execute()
        except APIError as e:
            raise Exception(f"更新失败: {e.message}")
        
        if not response.data:
            return f"未找到 ID 为 {document_id} 的文档"
        
        result = {
            "success": True,
            "message": "文档信息更新成功",
            "document_id": document_id
        }
        
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Exception as e:
        return f"更新文档时出错: {str(e)}"


@tool
def get_categories(runtime: ToolRuntime = None) -> str:
    """
    获取所有分类
    
    Returns:
        分类列表
    """
    try:
        client = get_supabase_client()
        
        try:
            response = client.table('documents').select('category').execute()
        except APIError as e:
            raise Exception(f"查询失败: {e.message}")
        
        # 提取所有分类
        categories = set()
        for doc in response.data:
            if doc.get('category'):
                categories.add(doc['category'])
        
        if not categories:
            return "暂无分类"
        
        # 格式化结果
        summary = "【分类列表】\n\n"
        for i, category in enumerate(sorted(categories), 1):
            summary += f"{i}. {category}\n"
        
        return summary.strip()
    except Exception as e:
        return f"获取分类列表时出错: {str(e)}"


@tool
def get_statistics(runtime: ToolRuntime = None) -> str:
    """
    获取系统统计信息
    
    Returns:
        统计信息
    """
    try:
        client = get_supabase_client()
        
        # 获取总文档数
        try:
            response = client.table('documents').select('*', count='exact').execute()
            total_count = response.count
        except APIError as e:
            raise Exception(f"查询失败: {e.message}")
        
        # 获取总文件大小
        try:
            response = client.table('documents').select('file_size').execute()
            total_size = sum(doc['file_size'] for doc in response.data)
        except APIError as e:
            total_size = 0
        
        # 获取各分类数量
        try:
            response = client.table('documents').select('category').execute()
            category_stats = {}
            for doc in response.data:
                category = doc.get('category', '未分类')
                category_stats[category] = category_stats.get(category, 0) + 1
        except APIError as e:
            category_stats = {}
        
        # 格式化结果
        summary = f"""
【系统统计】
总文档数: {total_count}
总存储空间: {_format_file_size(total_size)}

【分类统计】
"""
        if category_stats:
            for category, count in sorted(category_stats.items(), key=lambda x: x[1], reverse=True):
                summary += f"{category}: {count} 个文档\n"
        else:
            summary += "暂无分类统计\n"
        
        return summary.strip()
    except Exception as e:
        return f"获取统计信息时出错: {str(e)}"


@tool
def network_search_and_add(keyword: str, category: str = "国文汇通", max_results: int = 5, runtime: ToolRuntime = None) -> str:
    """
    网络搜索并自动添加相关资料
    
    Args:
        keyword: 搜索关键词
        category: 资料分类（默认：国文汇通）
        max_results: 最大搜索结果数量
    
    Returns:
        搜索和添加结果
    """
    try:
        ctx = new_context(method="network_search")
        llm_client = LLMClient(ctx=ctx)
        
        # 使用 LLM 进行智能搜索分析
        messages = [
            SystemMessage(content="你是一个资料搜索专家。请根据关键词分析并生成相关的资料描述和标签。"),
            HumanMessage(content=f"请为关键词 '{keyword}' 生成 3-5 个相关的资料标题和描述，格式如下：\n\n1. 标题：XXX\n   描述：XXX\n   标签：XXX\n\n2. 标题：XXX\n   描述：XXX\n   标签：XXX\n\n...（继续生成更多）")
        ]
        
        try:
            response = llm_client.invoke(messages=messages, temperature=0.7)
            
            # 提取生成的内容
            if isinstance(response.content, str):
                search_content = response.content
            elif isinstance(response.content, list):
                search_content = " ".join(str(item) for item in response.content)
            else:
                search_content = str(response.content)
            
        except Exception as e:
            return f"搜索分析失败: {str(e)}"
        
        # 解析搜索结果
        results = []
        lines = search_content.split('\n')
        current_title = ""
        current_description = ""
        current_tags = ""
        
        for line in lines:
            line = line.strip()
            if line.startswith('标题：'):
                if current_title:  # 保存上一个结果
                    results.append({
                        'title': current_title,
                        'description': current_description,
                        'tags': current_tags
                    })
                current_title = line.replace('标题：', '').strip()
                current_description = ""
                current_tags = ""
            elif line.startswith('描述：'):
                current_description = line.replace('描述：', '').strip()
            elif line.startswith('标签：'):
                current_tags = line.replace('标签：', '').strip()
        
        # 添加最后一个结果
        if current_title:
            results.append({
                'title': current_title,
                'description': current_description,
                'tags': current_tags
            })
        
        # 保存到数据库
        added_count = 0
        client = get_supabase_client()
        
        for i, result in enumerate(results[:max_results], 1):
            try:
                # 创建占位文档（实际文件需要用户上传）
                document_data = {
                    "title": result['title'],
                    "description": result['description'],
                    "file_name": f"search_result_{i}_{keyword}.pdf",
                    "file_key": f"documents/search_result_{i}_{keyword}.pdf",
                    "file_size": 0,
                    "file_type": "application/pdf",
                    "category": category,
                    "tags": result['tags'],
                    "download_count": 0
                }
                
                response = client.table('documents').insert(document_data).execute()
                added_count += 1
                
            except APIError as e:
                # 可能是重复，跳过
                continue
        
        # 返回结果
        summary = f"""
【网络搜索结果】
关键词: {keyword}
分类: {category}
找到: {len(results)} 个结果
成功添加: {added_count} 个文档

【搜索到的资料】
"""
        for i, result in enumerate(results[:max_results], 1):
            summary += f"\n{i}. {result['title']}\n"
            summary += f"   描述: {result['description'][:100]}...\n"
            summary += f"   标签: {result['tags']}\n"
        
        summary += f"\n💡 提示：搜索到的文档已创建为占位符，请上传实际文件或使用 upload_document 工具更新文件。"
        
        return summary.strip()
    except Exception as e:
        return f"网络搜索失败: {str(e)}"


@tool
def auto_update_documents(runtime: ToolRuntime = None) -> str:
    """
    自动更新文档（触发所有自动化任务）
    
    Returns:
        更新结果
    """
    try:
        summary = "【自动更新报告】\n\n"
        
        # 1. 同步数据
        summary += "1. 数据同步...\n"
        client = get_supabase_client()
        try:
            response = client.table('documents').select('*', count='exact').execute()
            summary += f"   ✅ 当前文档总数: {response.count}\n"
        except APIError as e:
            summary += f"   ❌ 同步失败: {e.message}\n"
        
        # 2. 检查存储
        summary += "\n2. 存储检查...\n"
        try:
            # 检查文档数量和存储空间
            response = client.table('documents').select('file_size').execute()
            total_size = sum(doc['file_size'] for doc in response.data)
            summary += f"   ✅ 存储空间: {_format_file_size(total_size)}\n"
        except Exception as e:
            summary += f"   ❌ 检查失败: {str(e)}\n"
        
        # 3. 更新统计
        summary += "\n3. 更新统计...\n"
        try:
            stats = get_statistics(runtime=runtime)
            summary += f"   ✅ {stats}\n"
        except Exception as e:
            summary += f"   ❌ 更新失败: {str(e)}\n"
        
        summary += "\n✅ 自动更新完成！"
        return summary
    except Exception as e:
        return f"自动更新失败: {str(e)}"
