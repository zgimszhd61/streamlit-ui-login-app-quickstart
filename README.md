# streamlit-ui-login-app-quickstart
```
import streamlit as st
import sqlite3

# 数据库连接和用户表创建
conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users
             (username TEXT PRIMARY KEY, password TEXT)''')
conn.commit()

# 注册函数
def register_user(username, password):
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()

# 登录函数
def login_user(username, password):
    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    return c.fetchone()

# Streamlit应用
def main():
    st.title("注册和登录示例")

    menu = ["注册", "登录"]
    choice = st.sidebar.selectbox("菜单", menu)

    if choice == "注册":
        st.subheader("创建新账户")

        new_user = st.text_input("用户名")
        new_password = st.text_input("密码", type='password')

        if st.button("注册"):
            register_user(new_user, new_password)
            st.success("您已成功注册")
            st.info("请返回登录菜单进行登录")

    elif choice == "登录":
        st.subheader("登录您的账户")

        username = st.text_input("用户名")
        password = st.text_input("密码", type='password')

        if st.button("登录"):
            result = login_user(username, password)
            if result:
                st.success(f"欢迎 {username}")
            else:
                st.warning("用户名或密码不正确")

if __name__ == '__main__':
    main()

```
