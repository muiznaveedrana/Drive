import streamlit as st
import re
import pandas as pd
import os
import hashlib
USER_DATA_FILE = 'users.csv'
UPLOAD_DIR = "uploads"

def exist(username):
    users_df = pd.read_csv(USER_DATA_FILE)
    if users_df['username'].isin([username]).any():
        return True
    return False

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to check if ID is unique
def is_id_unique(user_id):
    if not os.path.exists(USER_DATA_FILE):
        return True
    users_df = pd.read_csv(USER_DATA_FILE)
    return user_id not in users_df['user_id'].values

def verify_signup(username, password):
    if len(username) < 5:
        st.error("Username Too Short.")
        return False
    if len(password) < 6 or not re.search(r'[A-Z]', password) or not re.search(r'[0-9]', password):
        st.error("Password must be at least 6 characters long, contain an uppercase letter and a number")
        return False
    if username.lower() in password.lower():
        st.error("Password cannot contain username.")
        return False
    if not re.match(r'^[A-Za-z0-9_]+$', username):
        st.error("Username can only contain letters, numbers, and underscores.")
        return False
    return True

# Function to verify user credentials
def verify_user(username, password):
    if not os.path.exists(USER_DATA_FILE):
        return False, None
    users_df = pd.read_csv(USER_DATA_FILE)
    hashed_password = hash_password(password)
    user = users_df[(users_df['username'] == username) & (users_df['password'] == hashed_password)]
    return not user.empty

def save_uploaded_file(uploaded_file, username):
            file_path = os.path.join(UPLOAD_DIR,username,uploaded_file)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            return file_path

# Function to get username from user_id
def add(filename, file_content, recipient):
    # Define where to save the shared file (for example, in a shared folder)
    shared_folder = os.path.join("uploads", recipient)

    # Make sure the recipient's folder exists
    if not os.path.exists(shared_folder):
        os.makedirs(shared_folder)

    # Save the shared file in the recipient's folder
    shared_file_path = os.path.join(shared_folder, filename)
    
    with open(shared_file_path, "wb") as f:
        f.write(file_content)
    
    #print(f"File {filename} shared with {recipient}.")
# Sign-up system
def sign_up(username, password,):
    if not os.path.exists(USER_DATA_FILE):
        users_df = pd.DataFrame(columns=['username', 'password'])
    else:
        users_df = pd.read_csv(USER_DATA_FILE)
        
    if username in users_df['username'].values:
        st.error('Username already exists. Please choose another.')
    
    else:
        hashed_password = hash_password(password)
        new_user = pd.DataFrame([[username, hashed_password]], columns=['username', 'password'])
        users_df = pd.concat([users_df, new_user], ignore_index=True)
        users_df.to_csv(USER_DATA_FILE, index=False)
        st.success('Sign-up successful!')
        
# Login system
def login(username, password):
    valid = verify_user(username, password)
    if valid:
        st.session_state['logged_in_user_id'] = username
        st.success(f'Login successful! Welcome {username}')
        return username
    else:
        st.error('Invalid username or password.')
        return None

