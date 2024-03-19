import mysql.connector
from sql_conn import connect_to_db
import streamlit as st

def display_available_events(conn):
    cursor = conn.cursor()

    # Fetch events
    available_events_query = "SELECT * FROM Events"

    cursor.execute(available_events_query)
    available_events = cursor.fetchall()

    if available_events:
        st.write("## Available Events:")
        
        # Create a list of dictionaries for tabular display
        events_data = [{column_name: column_value for column_name, column_value in zip(cursor.column_names, event)} for event in available_events]

        # Display the table
        st.table(events_data)

    else:
        st.write("No events available.")

    cursor.close()

def create_event():
    st.write("Create Event:")

    # Event Form Inputs
    event_name = st.text_input("Event Name:")
    event_date = st.date_input("Event Date:")
    event_location = st.text_input("Event Location:")
    event_description = st.text_area("Event Description:")

    # Check if the form is submitted
    if st.button("Create Event"):
        conn = connect_to_db()
        cursor = conn.cursor()

        try:
            # Insert the event into the Events table
            insert_query = "INSERT INTO Events (event_name, event_date, event_location, event_description) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (event_name, event_date, event_location, event_description))
            conn.commit()

            st.success("Event created successfully!")
        except mysql.connector.Error as err:
            st.error(f"MySQL Error: {err}")
        finally:
            cursor.close()
            conn.close()
