import mysql.connector
import streamlit as st
from adoption_app import get_user_id_by_username


def volunteer(conn, username, event_id):
    cursor = conn.cursor()

    # Get the user_id based on the provided username
    user_id = get_user_id_by_username(conn, username)

    if user_id is not None:
        try:
            # Insert the registration into the Volunteers table
            insert_query = "INSERT INTO Volunteers (user_id, event_id) VALUES (%s, %s)"
            cursor.execute(insert_query, (user_id, event_id))
            conn.commit()

            st.success("Registration for the event successful!")
        except mysql.connector.Error as err:
            st.error(f"MySQL Error: {err}")
        finally:
            cursor.close()
    else:
        st.error("User not found.")
        
        
def show_volunteers(conn):
    cursor=conn.cursor()
    cursor.execute("Select user_id,username FROM Users WHERE user_id IN (Select user_id from volunteers)")
    users=cursor.fetchall()
    if users:
            st.write("### All usernames volunteering for events :")
            user_data = [{"ID": user[0], "username": user[1]} for user in users]  # Adjust column names based on your schema
            st.table(user_data)
    else:
            st.write("No users are volunteering")
