# 请为我实现一个用sqlite3进行电子虚拟交易系统的python程序，包含一下几个函数和功能点：
# 1.  上架商品：输入商品Id、商品标题、商品简介、商品价格、商品库存，存储到数据库.
# 2.  购买商品：输入商品Id、购买数量，库存减少。如果库存数量小于购买数量，则返回'无法购买，没有那么多货’而无需做实际扣减.
# 3.  查看商品清单：提供一个表格，每一行显示商品标题、商品简介、商品价格.
# 4.  下架商品：删除对应商品Id的商品。

import sqlite3

# 创建数据库连接
def create_connection():
    conn = sqlite3.connect('virtual_store.db')
    return conn

# 创建商品表
def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# 上架商品
def add_product(product_id, title, description, price, stock):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO products (id, title, description, price, stock)
        VALUES (?, ?, ?, ?, ?)
    ''', (product_id, title, description, price, stock))
    conn.commit()
    conn.close()
    print(f"商品 {title} 已上架")

# 购买商品
def purchase_product(product_id, quantity):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT stock FROM products WHERE id = ?', (product_id,))
    result = cursor.fetchone()
    if result:
        stock = result[0]
        if stock >= quantity:
            new_stock = stock - quantity
            cursor.execute('UPDATE products SET stock = ? WHERE id = ?', (new_stock, product_id))
            conn.commit()
            print(f"成功购买 {quantity} 件商品，剩余库存 {new_stock}")
        else:
            print("无法购买，没有那么多货")
    else:
        print("商品不存在")
    conn.close()

# 查看商品清单
def view_products():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT title, description, price FROM products')
    products = cursor.fetchall()
    conn.close()
    print("商品清单：")
    for product in products:
        print(f"标题: {product[0]}, 简介: {product[1]}, 价格: {product[2]}")

# 下架商品
def remove_product(product_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()
    print(f"商品 ID {product_id} 已下架")

# 初始化数据库和表
create_table()

# 示例操作
add_product(1, '商品A', '这是商品A的简介', 100.0, 50)
add_product(2, '商品B', '这是商品B的简介', 200.0, 30)
view_products()
purchase_product(1, 10)
view_products()
remove_product(2)
view_products()