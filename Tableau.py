import streamlit as st
import tableauserverclient as TSC

# Streamlit App Title
st.title("Tableau Extract Refresh Utility")

# Sidebar for General Information
st.sidebar.header("Instructions")
st.sidebar.write("""
- Fill in the Tableau Server details below.
- Provide the name of the datasource to refresh.
- Click 'Refresh Extract' to trigger the operation.
""")

# Create a Form for User Inputs
with st.form("tableau_form"):
    st.header("Enter Tableau Server Details")
    
    # Input Fields for Tableau Server Connection Details
    server_url = st.text_input("Server URL", value="https://prod-apnortheast-a.online.tableau.com/", help="Enter the Tableau Server or Tableau Online URL.")
    username = st.text_input("Username", value="", placeholder="Enter your Tableau username", help="Your Tableau username or email address.")
    password = st.text_input("Password", value="", placeholder="Enter your Tableau password", type="password", help="Your Tableau password.")
    site_id = st.text_input("Site ID", value="mohdsajjadsheikh-8334074aaa", help="Enter the Tableau Site ID. Leave blank for the default site.")
    
    # Input for Datasource Name
    datasource_name = st.text_input("Datasource Name", value="", placeholder="Enter the datasource name", help="The exact name of the datasource to refresh.")
    
    # Submit Button
    submit_button = st.form_submit_button("Refresh Extract")

# Perform the Extract Refresh When Form is Submitted
if submit_button:
    if not (server_url and username and password and datasource_name):
        st.error("Please fill in all the required fields.")
    else:
        # Connect to Tableau Server
        tableau_auth = TSC.TableauAuth(username, password, site_id)
        server = TSC.Server(server_url)
        server.use_server_version()

        try:
            with server.auth.sign_in(tableau_auth):
                # Get the list of all datasources
                all_datasources, pagination_item = server.datasources.get()

                # Find the specific datasource to refresh
                datasource = next((ds for ds in all_datasources if ds.name == datasource_name), None)

                if datasource:
                    # Trigger a refresh
                    st.info(f"Refreshing extract for datasource: {datasource.name}")
                    job = server.datasources.refresh(datasource)

                    # Display success message
                    st.success(f"Refresh job {job.id} has been triggered successfully.")
                else:
                    st.error(f"Datasource '{datasource_name}' not found.")

        except Exception as e:
            st.error(f"An error occurred: {e}")
