## 简单会员系统，
## - 登录、注册、登出等.

import streamlit as st
import sqlite3
import hashlib
import re
import datetime
import secrets
import bcrypt

# 哈希密码函数
def hash_password(password):
    salt = bcrypt.gensalt(rounds=12)  # 增加哈希成本
    return bcrypt.hashpw(password.encode(), salt).decode()

# 验证哈希密码
def verify_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode(), stored_password.encode())

# 数据库初始化
def init_db():
    with sqlite3.connect('users.db') as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (username TEXT PRIMARY KEY, password TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS sessions
                     (username TEXT, session_token TEXT, expires_at TIMESTAMP)''')
        conn.commit()

# 注册函数
def register_user(username, password):
    with sqlite3.connect('users.db') as conn:
        c = conn.cursor()
        hashed_password = hash_password(password)
        try:
            c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

# 登录函数
def login_user(username, password):
    with sqlite3.connect('users.db') as conn:
        c = conn.cursor()
        c.execute('SELECT password FROM users WHERE username=?', (username,))
        result = c.fetchone()
        if result and verify_password(result[0], password):
            return True
    return False

# 创建会话令牌
def create_session(username):
    session_token = secrets.token_hex(32)  # 增加令牌长度
    expires_at = datetime.datetime.now() + datetime.timedelta(hours=1)  # 缩短会话过期时间
    with sqlite3.connect('users.db') as conn:
        c = conn.cursor()
        c.execute('INSERT INTO sessions (username, session_token, expires_at) VALUES (?, ?, ?)', 
                  (username, session_token, expires_at))
        conn.commit()
    return session_token, expires_at

# 检查登录状态
def check_login():
    if 'session_token' in st.session_state:
        username = st.session_state.username
        session_token = st.session_state.session_token
        with sqlite3.connect('users.db') as conn:
            c = conn.cursor()
            c.execute('SELECT * FROM sessions WHERE username=? AND session_token=? AND expires_at > ?', 
                      (username, session_token, datetime.datetime.now()))
            result = c.fetchone()
            if result:
                st.session_state.logged_in = True
                return True, username
    return False, ""

# 设置登录状态
def set_login_state(username):
    session_token, expires_at = create_session(username)
    st.session_state.logged_in = True
    st.session_state.username = username
    st.session_state.session_token = session_token

# 删除会话
def delete_session(username, session_token):
    with sqlite3.connect('users.db') as conn:
        c = conn.cursor()
        c.execute('DELETE FROM sessions WHERE username=? AND session_token=?', (username, session_token))
        conn.commit()

# 登出函数
def logout_user():
    if 'session_token' in st.session_state:
        delete_session(st.session_state.username, st.session_state.session_token)
    st.session_state.clear()

# 用户个人资料页面
def list_user_profile(username):
    if username:
        st.success(f"Hello, {username}")
        if st.button("登出", key="logout_button"):
            logout_user()
            st.success("您已成功登出")
    else:
        st.warning("您还未登录，请先登录")

# 用户名和密码的基本格式验证
def validate_input(username, password):
    if not re.match("^[a-zA-Z0-9_]{3,15}$", username):
        st.warning("用户名应为3-15个字符，只能包含字母、数字和下划线")
        return False
    if len(password) < 8:
        st.warning("密码应至少包含8个字符")
        return False
    return True

# Streamlit应用
def main():
    st.title("注册和登录示例")

    menu = ["注册", "登录", "用户资料"]
    choice = st.sidebar.selectbox("菜单", menu)

    if "logged_in" not in st.session_state:
        st.session_state.logged_in, st.session_state.username = check_login()

    if st.session_state.logged_in:
        if choice == "用户资料":
            list_user_profile(st.session_state.username)
        # else:
        #     st.rerun() ## 刷新页面的意思

    if choice == "注册":
        st.subheader("创建新账户")

        new_user = st.text_input("用户名")
        new_password = st.text_input("密码", type='password')

        if st.button("注册"):
            if new_user and new_password:
                if validate_input(new_user, new_password):
                    if register_user(new_user, new_password):
                        st.success(f"欢迎 {new_user}，您已成功注册并自动登录")
                        set_login_state(new_user)
                    else:
                        st.warning("用户名已存在，请选择其他用户名")
            else:
                st.warning("请填写所有字段")

    elif choice == "登录":
        st.subheader("登录您的账户")

        username = st.text_input("用户名")
        password = st.text_input("密码", type='password')

        if st.button("登录"):
            if username and password:
                if validate_input(username, password):
                    if login_user(username, password):
                        st.success(f"欢迎 {username}")
                        set_login_state(username)
                    else:
                        st.warning("用户名或密码不正确")
            else:
                st.warning("请填写所有字段")

    elif choice == "用户资料":
        st.subheader("用户个人资料")
        if st.session_state.logged_in:
            st.success(st.session_state.username)
        else:
            st.warning("您还未登录，请先登录")

if __name__ == '__main__':
    init_db()
    main()