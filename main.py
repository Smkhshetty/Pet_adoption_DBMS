import streamlit as st
from lost_pet import display_lost_pets,if_found
from login import show_login_form
from sql_conn import connect_to_db
from adoption_app import display_available_pets, create_adoption_application
from create_acc import create_account,update_user_details
from event import create_event,display_available_events
from volunteer import volunteer,show_volunteers
from create_pet_profile import add_pet_profile,delete_pet_profile

def show_options_menu():
    conn = connect_to_db()
    username = st.session_state.username
    st.write("## Options Menu:")
    if st.session_state.user_authenticated and st.session_state.role == "ADMIN":
        option = st.selectbox("Select an option:", ["", "Looking to Adopt", "Looking to Volunteer",  "Looking for lost Pet", "Create Event","Add Pet Profile","Delete Pet Profile","Show all volunteers"])
    else:
        option = st.selectbox("Select an option:", ["", "Looking to Adopt", "Looking to Volunteer", "Looking for lost Pet","Update my Details"])

    if option:
        st.write(f"You selected: {option}")

        # Implement further logic based on the selected option
        if option == "Looking to Adopt":
            st.write("Displaying available pets for adoption:")
            display_available_pets(conn)
            pet_id_input = st.text_input("Enter the pet ID you want to adopt:")
            if st.button("Submit Adoption Application"):
                create_adoption_application(conn, username, pet_id_input)
                st.success("Adoption application submitted successfully.")

        elif option == "Looking for lost Pet":
            display_lost_pets(conn)
            lost_pet_id = st.text_input("Found your Pet? Enter his ID here:")
            if_found(conn,lost_pet_id)

        elif option == "Looking to Volunteer":
            display_available_events(conn)
            event_id = st.text_input("Enter the event id of the event you would like to volunteer for :")
            volunteer(conn,username,event_id)
        
        elif option == "Update my Details":
           update_user_details(conn,username)

        elif option == "Add Pet Profile":
            add_pet_profile(conn)
        
        elif option == "Delete Pet Profile":
            delete_pet_profile(conn)
        
        elif option == "Show all volunteers":
            show_volunteers(conn)       
        elif option == "Create Event":
            create_event()
        # Add a button to refresh the page
        if st.button("Refresh Page"):
            st.rerun()



def main():
    conn=connect_to_db()
    st.title("Login Page")

    # Create a session state to manage user authentication and options
    if 'user_authenticated' not in st.session_state:
        st.session_state.user_authenticated = False
        st.session_state.username = None

    # Check if the user is authenticated before displaying the dashboard
    if st.session_state.user_authenticated:
        st.title(f"Welcome, {st.session_state.name}, from {st.session_state.location}!")
        st.empty()
        show_options_menu()

    else:

        login_result = show_login_form()
        create_acc_button = st.button("Create Acc")
        if login_result:
            st.session_state.user_authenticated = True
            st.session_state.username = login_result[1]# Assuming username is in the second column
            st.session_state.name=login_result[4]
            st.session_state.location = login_result[6]
            st.session_state.role = login_result[7]  
        if create_acc_button:
                st.empty()
                create_account(conn)
                
if __name__ == "__main__":
    main()