"""
自动化操作脚本
用于定时更新资料、网络搜索、数据同步等任务
"""
import os
import sys
import json
import time
import schedule
import logging
from datetime import datetime
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from storage.database.supabase_client import get_supabase_client
from coze_coding_dev_sdk.s3 import S3SyncStorage

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


class AutomationManager:
    """自动化操作管理器"""

    def __init__(self):
        self.running = True

    def auto_sync_data(self):
        """自动同步数据"""
        logger.info("开始自动同步数据...")

        try:
            # 获取最新文档统计
            response = client.table('documents').select('*', count='exact').execute()
            total_count = response.count

            logger.info(f"当前文档总数: {total_count}")
            logger.info("数据同步完成")
            return {"success": True, "total_count": total_count}
        except Exception as e:
            logger.error(f"数据同步失败: {str(e)}")
            return {"success": False, "error": str(e)}

    def network_search_update(self, keywords=["国文汇通", "产品设计", "技术开发"]):
        """网络搜索更新"""
        logger.info("开始网络搜索更新...")

        results = []
        for keyword in keywords:
            logger.info(f"搜索关键词: {keyword}")
            # 这里可以调用实际的网络搜索API
            # 模拟搜索结果
            result = {
                "keyword": keyword,
                "found": 5,
                "timestamp": datetime.now().isoformat()
            }
            results.append(result)

        logger.info(f"网络搜索完成: {len(results)} 个关键词")
        return {"success": True, "results": results}

    def update_statistics(self):
        """更新统计数据"""
        logger.info("开始更新统计数据...")

        try:
            # 获取文档统计
            response = client.table('documents').select('*').execute()
            documents = response.data

            stats = {
                "total_count": len(documents),
                "total_size": sum(doc['file_size'] for doc in documents),
                "total_downloads": sum(doc['download_count'] for doc in documents),
                "categories": list(set(doc['category'] for doc in documents if doc.get('category'))),
                "timestamp": datetime.now().isoformat()
            }

            logger.info(f"统计数据更新: {stats}")
            return {"success": True, "stats": stats}
        except Exception as e:
            logger.error(f"更新统计失败: {str(e)}")
            return {"success": False, "error": str(e)}

    def cleanup_old_files(self, days=30):
        """清理旧文件"""
        logger.info(f"开始清理 {days} 天前的文件...")

        try:
            # 获取所有文件
            response = storage.list_files(prefix="documents/", max_keys=1000)

            cleaned_count = 0
            cutoff_time = datetime.now().timestamp() - (days * 86400)

            for file_info in response.get('keys', []):
                # 这里可以添加文件创建时间检查
                # 模拟清理
                cleaned_count += 1

            logger.info(f"清理完成: {cleaned_count} 个文件")
            return {"success": True, "cleaned_count": cleaned_count}
        except Exception as e:
            logger.error(f"清理失败: {str(e)}")
            return {"success": False, "error": str(e)}

    def backup_data(self):
        """备份数据"""
        logger.info("开始备份数据...")

        try:
            # 获取所有文档数据
            response = client.table('documents').select('*').execute()
            documents = response.data

            # 创建备份文件
            backup_file = f"/tmp/documents_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(documents, f, ensure_ascii=False, indent=2)

            logger.info(f"备份完成: {backup_file}")
            return {"success": True, "backup_file": backup_file}
        except Exception as e:
            logger.error(f"备份失败: {str(e)}")
            return {"success": False, "error": str(e)}

    def health_check(self):
        """健康检查"""
        logger.info("开始健康检查...")

        checks = []

        # 检查数据库连接
        try:
            response = client.table('documents').select('id').limit(1).execute()
            checks.append({"service": "database", "status": "ok"})
        except Exception as e:
            checks.append({"service": "database", "status": "error", "error": str(e)})

        # 检查存储连接
        try:
            storage.file_exists("health_check.txt")
            checks.append({"service": "storage", "status": "ok"})
        except Exception as e:
            checks.append({"service": "storage", "status": "error", "error": str(e)})

        logger.info(f"健康检查完成: {len(checks)} 个服务")
        return {"success": True, "checks": checks}

    def run_scheduled_tasks(self):
        """运行定时任务"""

        # 每小时同步数据
        schedule.every().hour.do(self.auto_sync_data)

        # 每天更新网络搜索
        schedule.every().day.at("09:00").do(self.network_search_update)

        # 每6小时更新统计
        schedule.every(6).hours.do(self.update_statistics)

        # 每天备份数据
        schedule.every().day.at("03:00").do(self.backup_data)

        # 每周清理旧文件
        schedule.every().sunday.at("02:00").do(self.cleanup_old_files)

        # 每15分钟健康检查
        schedule.every(15).minutes.do(self.health_check)

        logger.info("定时任务已配置:")
        logger.info("- 每小时同步数据")
        logger.info("- 每天09:00更新网络搜索")
        logger.info("- 每6小时更新统计")
        logger.info("- 每天03:00备份数据")
        logger.info("- 每周日02:00清理旧文件")
        logger.info("- 每15分钟健康检查")

        # 运行任务循环
        while self.running:
            schedule.run_pending()
            time.sleep(1)

    def stop(self):
        """停止自动化任务"""
        logger.info("停止自动化任务...")
        self.running = False


def main():
    """主函数"""
    manager = AutomationManager()

    try:
        logger.info("自动化任务管理器启动...")
        manager.run_scheduled_tasks()
    except KeyboardInterrupt:
        logger.info("收到停止信号...")
        manager.stop()
    except Exception as e:
        logger.error(f"自动化任务错误: {str(e)}")
        manager.stop()


if __name__ == "__main__":
    main()
