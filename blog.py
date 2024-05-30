import sqlite3

# 创建数据库连接和表
def create_connection():
    conn = sqlite3.connect('blog.db')
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS blog (
                        id INTEGER PRIMARY KEY,
                        title TEXT NOT NULL,
                        content TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# 1. 发布博客
def publish_blog(blog_id, title, content):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO blog (id, title, content) VALUES (?, ?, ?)''', (blog_id, title, content))
    conn.commit()
    conn.close()
    print("博客发布成功")

# 2. 查看博客
def view_blog(blog_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT title, content FROM blog WHERE id = ?''', (blog_id,))
    blog = cursor.fetchone()
    conn.close()
    if blog:
        print(f"标题: {blog[0]}\n内容: {blog[1]}")
    else:
        print("未找到该博客")

# 3. 删除博客
def delete_blog(blog_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''DELETE FROM blog WHERE id = ?''', (blog_id,))
    conn.commit()
    conn.close()
    print("博客删除成功")

# 4. 博客清单
def list_blogs():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT id, title FROM blog''')
    blogs = cursor.fetchall()
    conn.close()
    print("博客清单:")
    for blog in blogs:
        print(f"ID: {blog[0]}, 标题: {blog[1]}")

# 初始化数据库和表
create_table()

# 示例操作
publish_blog(1, "我的第一篇博客", "这是我的第一篇博客内容。")
publish_blog(2, "我的第二篇博客", "这是我的第二篇博客内容。")
view_blog(1)
list_blogs()
delete_blog(1)
list_blogs()