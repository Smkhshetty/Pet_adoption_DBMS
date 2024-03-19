# adoption.py
import mysql.connector
import streamlit as st


def display_available_pets(conn):
    cursor = conn.cursor()

    # Fetch pets available for adoption
    available_pets_query = "SELECT * FROM pets WHERE is_lost_found = 0 AND adoption_status = 0"

    try:
        cursor.execute(available_pets_query)
        available_pets = cursor.fetchall()

        if available_pets:
            st.write("## Available Pets for Adoption:")
            
            # Create a list of dictionaries for tabular display
            pets_data = [{column_name: column_value for column_name, column_value in zip(cursor.column_names, pet)} for pet in available_pets]

            # Display the table
            st.table(pets_data)

        else:
            st.write("No pets available for adoption.")

    except mysql.connector.Error as err:
        st.error(f"MySQL Error: {err}")

    cursor.close()





def get_user_id_by_username(conn, username):
    cursor = conn.cursor()
    query = "SELECT user_id FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else None



def create_adoption_application(conn, username, pet_id):
    cursor = conn.cursor()

    try:
        # Call the stored procedure
        cursor.callproc("create_adoption_application_and_update_status", (username, pet_id))
        conn.commit()

        result = cursor.fetchone()
        if result == 'Success':
            st.success("Adoption application created and pet profile status updated successfully!")
        elif result == 'Error':
            st.error("Error creating adoption application or pet not available for adoption.")

    except mysql.connector.Error as err:
        st.error(f"MySQL Error: {err}")

    cursor.close()

