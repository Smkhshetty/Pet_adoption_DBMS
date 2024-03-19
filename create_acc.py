# create_acc.py
import streamlit as st


def create_account(conn):
    st.empty()
    st.title("Create Account")
    
    # Collect user input
    username = st.text_input("Pick a username:")
    password = st.text_input("Enter a password:", type="password")
    email = st.text_input("Enter email:")
    first_name = st.text_input("Enter first name:")
    last_name = st.text_input("Enter last name:")
    city = st.text_input("Enter city:")
    
    new_acc=st.button("CREATE NEW")
    if new_acc:
        print("something")
        cursor = conn.cursor()
        query = "INSERT INTO USERS (username, password, email, first_name, last_name, city) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (username, password, email, first_name, last_name, city)
        cursor.execute(query, data)
        conn.commit()
        cursor.close()
        st.success("Account created successfully!")





       
def update_user_details(conn, username):
    cursor = conn.cursor()

    # Fetch the user's current details
    cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
    user_data = cursor.fetchone()

    if user_data:
        st.write("## Update Your Details:")
        
        # Display the current details
        st.write(f"Current Username: {user_data[1]}")
        st.write(f"Current Email: {user_data[3]}")
        st.write(f"Current First Name: {user_data[4]}")
        st.write(f"Current Last Name: {user_data[5]}")
        st.write(f"Current City: {user_data[6]}")

        # Allow the user to input updated details
        new_username = st.text_input("New Username:", user_data[1])
        new_email = st.text_input("New Email:", user_data[3])
        new_first_name = st.text_input("New First Name:", user_data[4])
        new_last_name = st.text_input("New Last Name:", user_data[5])
        new_city = st.text_input("New City:", user_data[6])

        # Check if the form is submitted
        if st.button("Update Details"):
            # Update the user's details in the Users table
            update_query = "UPDATE Users SET username = %s, email = %s, first_name = %s, last_name = %s, city = %s WHERE username = %s"
            cursor.execute(update_query, (new_username, new_email, new_first_name, new_last_name, new_city, username))
            conn.commit()

            st.success("Details updated successfully!")

    else:
        st.warning("User not found.")
        
