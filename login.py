from sql_conn import connect_to_db
import streamlit as st


def login(username, password, conn):
    cursor = conn.cursor()
    query = "SELECT * FROM USERS WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    cursor.close()
    return result

def show_login_form():
    with st.form(key='login_form'):
        username_input = st.text_input("Enter username:")
        password_input = st.text_input("Enter password:", type="password")

        submit_button = st.form_submit_button("Login")

        if submit_button:
            conn = connect_to_db()
            login_result = login(username_input, password_input, conn)
            conn.close()
            return login_result
