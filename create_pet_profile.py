import streamlit as st


def add_pet_profile(conn):
    st.title("Add Pet Profile")

    # Collect pet information
    pet_name = st.text_input("Enter pet name:")
    breed = st.text_input("Enter pet breed:")
    age = st.number_input("Enter pet age:", min_value=0, step=1)
    is_lost_found = st.checkbox("Is the pet lost or found?")
    
    # Add an option to upload an image (if needed)
    # Note: You may need to adjust this based on your specific requirements
    image_file = st.file_uploader("Upload an image of the pet (optional)", type=["jpg", "jpeg", "png"])

    # Convert the image data to LONGBLOB format
    image_data = None
    if image_file is not None:
        image_data = image_file.read()

    # Add a button to submit the form
    if st.button("Add Pet Profile"):
        cursor = conn.cursor()

        # Insert pet information into the Pets table
        query = "INSERT INTO Pets (pet_name, breed, age, is_lost_found, image_data) VALUES (%s, %s, %s, %s, %s)"
        data = (pet_name, breed, age, is_lost_found, image_data)
        cursor.execute(query, data)
        conn.commit()
        cursor.close()

        st.success("Pet profile added successfully!")
        
def delete_pet_profile(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pets")
        pets = cursor.fetchall()

        if pets:
            st.write("### All Pets in the Database:")
            pet_data = [{"ID": pet[0], "Name": pet[1], "Type": pet[2], "Age": pet[3]} for pet in pets]  # Adjust column names based on your schema
            st.table(pet_data)
        else:
            st.write("No pets found in the database.")
    except Exception as e:
            st.error(f"Error displaying or deleting pets: {str(e)}")
    
    pet_id=st.text_input("Enter the pet id:")
    try:
        cursor.execute("DELETE FROM pets WHERE pet_id = %s", (pet_id,))
        conn.commit()
        st.success(f"Pet profile with ID {pet_id} deleted successfully.")
    except Exception as e:
        st.error(f"Error deleting pet profile: {str(e)}")
    finally:
        cursor.close()

    