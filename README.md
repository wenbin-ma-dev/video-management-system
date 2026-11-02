# 视频数据管理系统 (Video Data Management System)

本项目是《数据库原理与应用》课程设计作品。系统采用 **SQL Server 2008 + Python** 的经典 C/S 架构，实现了一个底层逻辑扎实的视频数据管理系统，并配有 Python 命令行客户端验证数据库功能。

## 🛠 技术栈
- **数据库**：Microsoft SQL Server 2008
- **开发语言**：Python 3.x
- **核心库**：`pyodbc` (用于 Python 连接 SQL Server)

## 🗄️ 数据库设计亮点
本系统设计了 4 张核心表：`user`（用户）、`video`（视频）、`tag`（标签）、`video_tag`（关联表）。

1. **多对多关系处理**：通过 `video_tag` 桥接表处理视频与标签的多对多关系，利用联合主键天然杜绝重复打标。
2. **数据完整性保障**：
   - 使用 `FOREIGN KEY` 与 `ON DELETE CASCADE` 实现级联删除，保证参照完整性。
   - 使用 `CHECK` 约束（如角色仅限 student/teacher/admin）保证域完整性。
3. **高级数据库对象应用**：
   - **视图 (`v_video_detail`)**：利用 `STUFF` 和 `FOR XML PATH` 函数，将多行标签动态拼接为单行字符串，简化应用层查询。
   - **索引**：针对高频查询字段建立非聚集索引，优化检索性能。
   - **存储过程 (`sp_add_video`)**：封装“插入视频”与“插入标签”操作，引入事务 (`TRANSACTION`) 机制保证原子性。

## 🚀 快速开始

### 1. 数据库准备
在 SQL Server 中运行 `db_setup.sql` 脚本，系统将自动创建数据库、表结构、索引、视图以及存储过程。

### 2. 运行 Python 客户端
请确保已安装 Python，并在终端中执行以下命令安装依赖：
```bash
pip install pyodbc
