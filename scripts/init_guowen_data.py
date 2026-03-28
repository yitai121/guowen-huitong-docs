"""
国文汇通资料初始化脚本
自动配置国文汇通的资料到系统
"""
import os
import sys
import json
import asyncio
import logging
from pathlib import Path
from datetime import datetime

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from storage.database.supabase_client import get_supabase_client
from coze_coding_dev_sdk.s3 import S3SyncStorage
from postgrest.exceptions import APIError

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 初始化客户端
client = get_supabase_client()
storage = S3SyncStorage(
    endpoint_url=os.getenv("COZE_BUCKET_ENDPOINT_URL"),
    access_key="",
    secret_key="",
    bucket_name=os.getenv("COZE_BUCKET_NAME"),
    region="cn-beijing",
)


def load_config():
    """加载配置文件"""
    config_file = Path(__file__).parent.parent / 'assets' / 'guowen_huitong_data.json'

    if not config_file.exists():
        logger.error(f"配置文件不存在: {config_file}")
        return None

    with open(config_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def format_file_size(size_str):
    """格式化文件大小字符串为字节数"""
    if isinstance(size_str, int):
        return size_str

    # 简单处理，实际应根据需求转换
    return 1024 * 1024  # 默认 1MB


async def download_and_upload_file(url, title):
    """从 URL 下载并上传文件"""
    try:
        logger.info(f"从 URL 下载文件: {url}")

        # 使用 S3 的 URL 上传功能
        file_key = storage.upload_from_url(url=url, timeout=60)

        logger.info(f"文件上传成功: {file_key}")
        return file_key
    except Exception as e:
        logger.error(f"文件上传失败: {str(e)}")
        return None


def document_exists(title):
    """检查文档是否已存在"""
    try:
        response = client.table('documents').select('id').eq('title', title).maybe_single().execute()
        return response is not None
    except APIError as e:
        logger.error(f"检查文档存在性失败: {e.message}")
        return False


def create_document(doc_data, config):
    """创建文档记录"""
    try:
        # 检查文档是否已存在
        if document_exists(doc_data['title']):
            logger.info(f"文档已存在，跳过: {doc_data['title']}")
            return None

        logger.info(f"创建文档: {doc_data['title']}")

        # 从 URL 下载并上传文件
        file_key = download_and_upload_file(doc_data['file_url'], doc_data['title'])

        if not file_key:
            logger.error(f"文件上传失败，跳过文档: {doc_data['title']}")
            return None

        # 准备文档数据
        document_data = {
            "title": doc_data['title'],
            "description": doc_data.get('description', ''),
            "file_name": doc_data['file_url'].split('/')[-1],
            "file_key": file_key,
            "file_size": 1024 * 1024,  # 默认 1MB，实际应从文件获取
            "file_type": "application/pdf",  # 默认 PDF 类型
            "category": doc_data['category'],
            "tags": doc_data['tags'],
            "download_count": 0
        }

        # 插入数据库
        response = client.table('documents').insert(document_data).execute()

        logger.info(f"文档创建成功: {doc_data['title']} (ID: {response.data[0]['id']})")
        return response.data[0]['id']

    except APIError as e:
        logger.error(f"创建文档失败: {e.message}")
        return None
    except Exception as e:
        logger.error(f"创建文档异常: {str(e)}")
        return None


def init_guowen_data():
    """初始化国文汇通数据"""
    logger.info("=" * 50)
    logger.info("开始初始化国文汇通资料...")
    logger.info("=" * 50)

    # 加载配置
    config = load_config()
    if not config:
        logger.error("无法加载配置文件")
        return False

    # 显示公司信息
    company = config['company']
    logger.info(f"公司名称: {company['name']}")
    logger.info(f"公司描述: {company['description']}")
    logger.info(f"官方网站: {company['website']}")
    logger.info(f"成立时间: {company['founded']}")

    # 创建文档
    documents = config['documents']
    logger.info(f"\n准备创建 {len(documents)} 个文档...")

    success_count = 0
    failed_count = 0
    skipped_count = 0

    for i, doc_data in enumerate(documents, 1):
        logger.info(f"\n[{i}/{len(documents)}] 处理文档: {doc_data['title']}")
        logger.info(f"  分类: {doc_data['category']}")
        logger.info(f"  标签: {doc_data['tags']}")
        logger.info(f"  优先级: {doc_data['priority']}")

        # 创建文档
        doc_id = create_document(doc_data, config)

        if doc_id:
            success_count += 1
        elif document_exists(doc_data['title']):
            skipped_count += 1
        else:
            failed_count += 1

    # 显示统计信息
    logger.info("\n" + "=" * 50)
    logger.info("初始化完成！")
    logger.info("=" * 50)
    logger.info(f"成功创建: {success_count} 个文档")
    logger.info(f"跳过已存在: {skipped_count} 个文档")
    logger.info(f"创建失败: {failed_count} 个文档")
    logger.info(f"总计: {len(documents)} 个文档")

    # 显示搜索关键词
    search_keywords = config.get('search_keywords', [])
    if search_keywords:
        logger.info(f"\n搜索关键词: {', '.join(search_keywords)}")

    # 显示更新计划
    update_schedule = config.get('update_schedule', {})
    if update_schedule:
        logger.info(f"\n自动更新配置:")
        logger.info(f"  自动同步: {update_schedule.get('auto_sync', {}).get('enabled', False)}")
        logger.info(f"  网络搜索: {update_schedule.get('network_search', {}).get('enabled', False)}")
        logger.info(f"  备份: {update_schedule.get('backup', {}).get('enabled', False)}")

    return success_count > 0


def main():
    """主函数"""
    try:
        success = init_guowen_data()
        if success:
            logger.info("\n✅ 国文汇通资料初始化成功！")
            return 0
        else:
            logger.error("\n❌ 国文汇通资料初始化失败！")
            return 1
    except Exception as e:
        logger.error(f"初始化异常: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
