import os
import streamlit as st
import random
import functions
st.set_page_config("UltraDrive",
                    page_icon="data:image/png;base64,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",
                    initial_sidebar_state='expanded',
                    layout= "wide",
                    menu_items={
    'Get Help': 'https://muiz-portfolio.streamlit.app/Contact_Me',
    'Report a bug': 'https://muiz-portfolio.streamlit.app/Contact_Me',
    'About': '''
        My UltraDrive\n
        UNLIMITED STORAGE\n
        
        Version 2.1.1\n
        The DEVS: muiznaveedrana@gmail.com\n
        ©️
    '''})

UPLOAD_DIR = "uploads"
st.title("⚡UltraDrive!⚡", help="NOT RELATED TO ULTRAMAX")
try:
    choices = ["Login", "Sign Up", "Drive", "SharePoint"]
    choice = st.sidebar.radio("Menu", choices)
    if choice == "Drive":
        if 'logged_in_user_id' not in st.session_state:
                st.error("You need to log in first!")
        else:
            # Set up a directory for uploaded files
            if not os.path.exists(UPLOAD_DIR):
                os.makedirs(UPLOAD_DIR)

            # Helper function to savaded files
            def save_uploaded_file(uploaded_file):
                file_path = os.path.join(UPLOAD_DIR,st.session_state['logged_in_user_id'],uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                return file_path
                

            # Streamlit interface
            st.subheader("Drive")
            # File uploader widget
            uploaded_file = st.file_uploader("Upload your files", type=None, help="Zipped Folders Allowed")

            if uploaded_file is not None:
                file_path = save_uploaded_file(uploaded_file)
                #st.rerun()
                #st.success(f"File {uploaded_file.name} uploaded successfully!")
                
            # List all uploaded files
            st.subheader("Uploaded Files")
            uploaded_files = os.listdir(UPLOAD_DIR + "/" +  st.session_state['logged_in_user_id'])
            #st.write(uploaded_files)
            if uploaded_files:
                for file in uploaded_files:
                    with st.expander(f"**{file}**"):
                        file_path = os.path.join(UPLOAD_DIR,st.session_state['logged_in_user_id'],file)
                        #st.write(file_path)

                        with open(file_path, "rb") as f:
                            file_content = f.read()
                        #st.write(file_path)
                        download = st.download_button("Download", file_content, file_path[7:], key=file)
                        if st.button("**PERMENANT** Delete", key=f"Hello{file}"):
                            os.remove(file_path)
                            
                            st.rerun()
            else:
                st.write("**No files uploaded yet.**")

    elif choice == "Login":
        st.subheader("Login")
        #logged_in_user = None
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        #remember_me = st.checkbox("Remember Me")
        if st.button("Login"):
            logged_in_user = functions.login(username, password)
            
            if logged_in_user:

                st.sidebar.info(f"Logged in as {username}")
        
    elif choice == "Sign Up":
        st.subheader("Create Account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        #user_id = st.text_input("Unique ID")
        if st.button("Sign Up"):
            if functions.verify_signup(username, password):
                functions.sign_up(username, password)
                logged_in_user = functions.login(username, password)
                st.session_state['logged_in_user_id'] = logged_in_user[0]
                #st.sidebar.info(f"Logged in as {functions.get_username(st.session_state['logged_in_user_id'])}")
                os.makedirs(f"uploads/{username}")
                
    elif choice == "SharePoint":
        st.subheader("SharePoint")
        shareWith = st.text_input("Username Of Sharer")
        if shareWith:
            if functions.exist(shareWith):
                uploaded_files = os.listdir(UPLOAD_DIR + "/" +  st.session_state['logged_in_user_id'])
                
                if uploaded_files:
                    for file in uploaded_files:
                        file_path = os.path.join(UPLOAD_DIR, st.session_state['logged_in_user_id'], file)

                        # Read the file content in binary mode
                        with open(file_path, "rb") as f:
                            file_content = f.read()
                        
                        # Display the file and a "Share?" button
                        if st.button(file + " " + "**Share?**", key=file):
                            # Call the add function with both file name and content
                            functions.add(f"Shared From {st.session_state['logged_in_user_id']}"+file , file_content, shareWith)
                            st.success(f"Shared {file} with {shareWith}")
            else:
                st.warning("User does not exist!")
except:
    pass