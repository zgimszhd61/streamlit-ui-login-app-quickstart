# 积分管理系统.
# 请为我实现一个用sqlite3进行积分管理的python程序，包含一下几个函数和功能点：
# 1.  充值：调用后，用户的积分余额就增加相应数值，接受1个参数，代表相应数值.
# 2.  消费：调用后，用户的积分余额就减少相应数值，接受1个参数，代表相应数值.会先检查用户账号里的余额是否大于这个数值，如果不大于，则返回'余额不足'，如果大于，则进行相应积分扣减.
# 3. 查看积分：调用后，返回用户当前积分余额.

## 充值（增加余额）
# 1. 现金充值到平台.
# 2. 新用户注册冷额度.
# 3. 每日任务（如签到、分享链接到社交媒体、每日活跃任务.）.
# 4. 推荐新人注册.

## 消费（减少额度）
# 1. 兑换物品.
# 2. 使用能力.

import sqlite3

# 创建数据库和表
def create_database():
    conn = sqlite3.connect('points_management.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            points INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# 初始化用户
def initialize_user(user_id):
    conn = sqlite3.connect('points_management.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (id, points) VALUES (?, ?)', (user_id, 0))
    conn.commit()
    conn.close()

# 充值积分
def recharge(user_id, amount):
    conn = sqlite3.connect('points_management.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET points = points + ? WHERE id = ?', (amount, user_id))
    conn.commit()
    conn.close()

# 消费积分
def consume(user_id, amount):
    conn = sqlite3.connect('points_management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT points FROM users WHERE id = ?', (user_id,))
    current_points = cursor.fetchone()[0]
    if current_points < amount:
        conn.close()
        return '余额不足'
    cursor.execute('UPDATE users SET points = points - ? WHERE id = ?', (amount, user_id))
    conn.commit()
    conn.close()
    return '消费成功'

# 查看积分
def check_points(user_id):
    conn = sqlite3.connect('points_management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT points FROM users WHERE id = ?', (user_id,))
    points = cursor.fetchone()[0]
    conn.close()
    return points

# 示例用法
if __name__ == '__main__':
    create_database()
    user_id = 1
    initialize_user(user_id)
    
    print("初始积分:", check_points(user_id))
    
    recharge(user_id, 100)
    print("充值100后积分:", check_points(user_id))
    
    result = consume(user_id, 50)
    print("消费50结果:", result)
    print("消费50后积分:", check_points(user_id))
    
    result = consume(user_id, 100)
    print("消费100结果:", result)
    print("消费100后积分:", check_points(user_id))