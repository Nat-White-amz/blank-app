import streamlit as st
import pandas as pd
import plotly.express as px

# Set page title
st.set_page_config(page_title="Project Prioritization Matrix", layout="wide")

# Title
st.title("Project Prioritization Matrix")

# Sidebar for adding projects
st.sidebar.header("Add New Project")
project_name = st.sidebar.text_input("Project Name")
strategic_alignment = st.sidebar.slider("Strategic Alignment", 1, 5, 3)
customer_impact = st.sidebar.slider("Customer Impact", 1, 5, 3)
legal_regulatory = st.sidebar.slider("Legal & Regulatory Requirements", 1, 5, 3)
contact_volume = st.sidebar.slider("Contact Volume", 1, 5, 3)
time_savings = st.sidebar.slider("Time Savings", 1, 5, 3)
customer_satisfaction = st.sidebar.slider("Customer Satisfaction", 1, 5, 3)
internal_efficiency = st.sidebar.slider("Internal Efficiency", 1, 5, 3)

# Button to add project
if st.sidebar.button("Add Project"):
    # Create a dictionary with project details
    new_project = {
        "Project Name": project_name,
        "Strategic Alignment": strategic_alignment,
        "Customer Impact": customer_impact,
        "Legal & Regulatory Requirements": legal_requirements,
        "Contact Volume": contact_volume,
        "Time Savings": time_savings,
        "Customer Satisfaction": customer_satisfaction,
        "Internal Efficiency": internal_efficiency
    }
    
    # Add new project to session state
    if 'projects' not in st.session_state:
        st.session_state.projects = []
    st.session_state.projects.append(new_project)
    st.sidebar.success("Project added successfully!")

# Main content
if 'projects' in st.session_state and st.session_state.projects:
    # Convert projects to DataFrame
    df = pd.DataFrame(st.session_state.projects)
    
    # Define weights
    weights = {
        "Strategic Alignment": 0.25,
        "Customer Impact": 0.20,
        "Legal & Regulatory Requirements": 0.15,
        "Contact Volume": 0.10,
        "Time Savings": 0.10,
        "Customer Satisfaction": 0.15,
        "Internal Efficiency": 0.05
    }
    
    # Calculate weighted scores
    for criterion, weight in weights.items():
        df[f"{criterion} (Weighted)"] = df[criterion] * weight
    
    # Calculate total score
    df["Total Score"] = df[[f"{criterion} (Weighted)" for criterion in weights.keys()]].sum(axis=1)
    
    # Sort by total score
    df_sorted = df.sort_values("Total Score", ascending=False).reset_index(drop=True)
    
    # Display projects table
    st.subheader("Projects Prioritization Table")
    st.dataframe(df_sorted)
    
    # Create bar chart
    fig = px.bar(df_sorted, x="Project Name", y="Total Score", 
                 title="Project Priority Scores",
                 labels={"Total Score": "Priority Score", "Project Name": "Project"},
                 color="Total Score", color_continuous_scale="Viridis")
    st.plotly_chart(fig)

else:
    st.info("No projects added yet. Use the sidebar to add projects.")

# Add option to clear all projects
if st.button("Clear All Projects"):
    st.session_state.projects = []
    st.success("All projects cleared!")