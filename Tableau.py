import streamlit as st
import tableauserverclient as TSC

# Streamlit App Title
st.title("Tableau Extract Refresh Utility")

# Input Fields for Tableau Connection Details
st.sidebar.header("Tableau Server Connection Details")
server_url = st.sidebar.text_input("Server URL", value="https://prod-apnortheast-a.online.tableau.com/")
username = st.sidebar.text_input("Username", value="", placeholder="Enter your Tableau username")
password = st.sidebar.text_input("Password", value="", placeholder="Enter your Tableau password", type="password")
site_id = st.sidebar.text_input("Site ID", value="mohdsajjadsheikh-8334074aaa", placeholder="Enter the Tableau site ID (leave blank for default site)")

# Input for Datasource Name
datasource_name = st.text_input("Datasource Name", value="", placeholder="Enter the name of the datasource to refresh")

# Button to Trigger Refresh
if st.button("Refresh Extract"):
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
