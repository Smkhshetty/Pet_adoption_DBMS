import mysql.connector
import streamlit as st

def display_lost_pets(conn):
    cursor = conn.cursor()

    # Fetch pets available for adoption
    available_pets_query = "SELECT * FROM pets WHERE is_lost_found = 1"

    try:
        cursor.execute(available_pets_query)
        available_pets = cursor.fetchall()

        if available_pets:
            st.write("Lost pets  reported")
            
            # Create a list of dictionaries for tabular display
            pets_data = [{column_name: column_value for column_name, column_value in zip(cursor.column_names, pet)} for pet in available_pets]

            # Display the table
            st.table(pets_data)

        else:
            st.write("All lost pets have been found!")

    except mysql.connector.Error as err:
        st.error(f"MySQL Error: {err}")

    cursor.close()
    
def if_found(conn,lost_pet_id):
    cursor = conn.cursor()
    try:
        # Check if the pet with the given lost_pet_id exists
        cursor.execute("SELECT * FROM pets WHERE pet_id = %s", (lost_pet_id,))
        pet_result = cursor.fetchone()

        if pet_result:
            # Pet found, update the pet profile
            update_query = "UPDATE pets SET adoption_status = 1, is_lost_found = 0 WHERE pet_id = %s"
            cursor.execute(update_query, (lost_pet_id,))
            conn.commit()

            # Display a success message with a phone number
            st.success(f"Pet with ID {lost_pet_id} found! Contact us at: +123456789")

        else:
            # Pet not found
            st.warning("Pet not found. Please check the ID and try again.")

    except mysql.connector.Error as err:
        # Handle MySQL errors
        st.error(f"MySQL Error: {err}")