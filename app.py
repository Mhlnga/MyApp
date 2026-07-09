import streamlit as st
from datetime import datetime

st.title("Age Tracker and  Average Calculator")

# Initialize session state for storing people data
if 'people' not in st.session_state:
    st.session_state.people = []

# Input form
with st.form("person_form"):
    st.header("Add a Person")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, max_value=150, step=1)
    
    submitted = st.form_submit_button("Add to List")
    
    if submitted:
        if name and age:
            st.session_state.people.append({"name": name, "age": age})
            st.success(f"Added {name} (age {age})")
        else:
            st.error("Please enter both name and age")

# Display current list
if st.session_state.people:
    st.header("Current People")
    
    # Create two columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Names")
        for person in st.session_state.people:
            st.write(f"• {person['name']}")
    
    with col2:
        st.subheader("Ages")
        for person in st.session_state.people:
            st.write(f"• {person['age']}")
    
    # Calculate and display average
    ages = [person["age"] for person in st.session_state.people]
    average_age = sum(ages) / len(ages)
    
    st.metric(
        label=f"Average Age ({len(st.session_state.people)} people)",
        value=f"{average_age:.1f} years"
    )

else:
    st.info("No people added yet. Use the form above to get started.")

# Clear button
if st.session_state.people:
    if st.button("Clear All"):
        st.session_state.people = []
        st.rerun()
