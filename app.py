import pyodbc

# ================= 1. 数据库连接配置 =================
SERVER = '(local)'  # 根据你的截图修改
DATABASE = 'video_mgmt'

# 适配 SQL Server 2008 老版本的连接字符串
conn_str = (
    f'DRIVER={{SQL Server}};'
    f'SERVER={SERVER};'
    f'DATABASE={DATABASE};'
    f'Trusted_Connection=yes;'
)

def get_connection():
    try:
        conn = pyodbc.connect(conn_str)
        return conn
    except Exception as e:
        print(f"❌ 数据库连接失败，请检查配置！\n错误信息：{e}")
        return None

# ================= 2. 核心功能 1：查看视频详情（调用视图） =================
def show_videos():
    conn = get_connection()
    if not conn: return
    cursor = conn.cursor()
    
    print("\n" + "="*60)
    print("🎬 视频列表 (数据来自数据库视图 v_video_detail)")
    print("="*60)
    print(f"{'ID':<5} | {'标题':<20} | {'时长(分)':<8} | {'上传者':<8} | {'标签'}")
    print("-" * 60)
    
    try:
        cursor.execute("SELECT video_id, 视频标题, 时长, 上传者, 标签列表 FROM v_video_detail")
        rows = cursor.fetchall()
        
        for row in rows:
            minutes = round(row[2] / 60) if row[2] else 0
            tags = row[4] if row[4] else "无标签"
            # 使用 <20 这种格式化，如果中文字符宽度不对，显示可能稍微有点歪，但不影响使用
            print(f"{row[0]:<5} | {row[1]:<20} | {minutes:<8} | {row[3]:<8} | {tags}")
    except Exception as e:
        print(f"查询失败: {e}")
    finally:
        print("="*60 + "\n")
        conn.close()

# ================= 3. 核心功能 2：上传新视频（调用存储过程） =================
def upload_video():
    conn = get_connection()
    if not conn: return
    cursor = conn.cursor()
    
    print("\n--- 📤 上传新视频 ---")
    title = input("请输入视频标题: ")
    duration_str = input("请输入视频时长(秒): ")
    try:
        duration = int(duration_str)
    except ValueError:
        print("❌ 时长必须是数字！操作取消。")
        return
    
    uploader_id = 1
    file_path = f"/videos/{title}.mp4"
    
    print("\n可选标签: 1-教学, 2-实验, 3-讲座, 4-代码演示, 5-校园生活")
    tag_id = input("请选择一个标签ID (如 4): ")
    
    try:
        # 调用数据库里的存储过程
        cursor.execute("EXEC sp_add_video ?, ?, ?, ?, ?", (title, file_path, duration, uploader_id, tag_id))
        conn.commit() 
        print(f"\n✅ 视频《{title}》上传成功，并已打上标签！")
    except Exception as e:
        print(f"\n❌ 上传失败，事务已回滚。错误: {e}")
    finally:
        conn.close()

# ================= 4. 主程序菜单 =================
def main():
    while True:
        print("欢迎使用 视频数据管理系统")
        print("1. 查看所有视频 (测试视图查询)")
        print("2. 上传新视频 (测试存储过程与事务)")
        print("0. 退出系统")
        choice = input("请输入选项: ")
        
        if choice == '1':
            show_videos()
        elif choice == '2':
            upload_video()
        elif choice == '0':
            print("再见！")
            break
        else:
            print("无效选项，请重新输入。\n")

if __name__ == "__main__":
    main()