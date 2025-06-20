# MoodyBuddy - Tamil Mood Music Recommender + Personal Diary (Streamlit App with Login)

import streamlit as st
import json
import os
import datetime

# ------------------------------
# Song suggestions based on mood
# ------------------------------
song_data = {
    "Happy": [
        ("Vthisaathi Coming", "https://open.spotify.com/track/0u2XOjUhTaUR2cw5C5u5uZ"),
        ("Jimikki Ponnu", "https://open.spotify.com/track/1ywVjkY1vVqBkSHB0qqyjs"),
        ("Aaluma Doluma", "https://open.spotify.com/track/5pqLiyab2B1kGdKFiT4uKY")
    ],
    "Sad": [
        ("Nenjukulle", "https://open.spotify.com/track/4h0NGS8F39vYrJnRR0g79g"),
        ("Unakkena Venum Sollu", "https://open.spotify.com/track/4jeH3v9kEeYujkVFCrcMHT"),
        ("Oru Kal Oru Kannadi", "https://open.spotify.com/track/3c2NG6VvlKxKZAw0gYZq7m")
    ],
    "Chill": [
        ("Thuli Thuli", "https://open.spotify.com/track/5XMf7QAdUBvQInOyIV5Zt1"),
        ("Vaseegara", "https://open.spotify.com/track/1Tg0EPIyqTiEoB9dZntYJl"),
        ("Munbe Vaa", "https://open.spotify.com/track/3hZZNs1lTclGLn5iNc3K8J")
    ],
    "Energetic": [
        ("Marana Mass", "https://open.spotify.com/track/6M3Xw1ab7nUxJBKDNzL73N"),
        ("Arabic Kuthu", "https://open.spotify.com/track/2QUPtM2rTDwytAY3etMd3f"),
        ("Sodakku", "https://open.spotify.com/track/0fncu09KVDNgWBZlbtTNCU")
    ]
}

# ------------------------------
# File paths
# ------------------------------
users_file = "users.json"
diary_folder = "diaries"

if not os.path.exists(users_file):
    with open(users_file, "w") as f:
        json.dump({}, f)

if not os.path.exists(diary_folder):
    os.makedirs(diary_folder)

with open(users_file, "r") as f:
    users = json.load(f)

# ------------------------------
# User Authentication System
# ------------------------------
def register_user(username, password):
    if username in users:
        return False
    users[username] = password
    with open(users_file, "w") as f:
        json.dump(users, f)
    return True

def login_user(username, password):
    return users.get(username) == password

# ------------------------------
# Diary Functions
# ------------------------------
def get_diary_path(username):
    return os.path.join(diary_folder, f"{username}_diary.json")

def load_diary(username):
    diary_path = get_diary_path(username)
    if os.path.exists(diary_path):
        with open(diary_path, "r") as f:
            return json.load(f)
    return {}

def save_diary(username, diary):
    diary_path = get_diary_path(username)
    with open(diary_path, "w") as f:
        json.dump(diary, f)

# ------------------------------
# Streamlit UI
# ------------------------------
st.set_page_config(page_title="MoodyBuddy - Tamil Mood Songs", page_icon="🎵")
st.title("🎵 MoodyBuddy")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Register":
    st.sidebar.subheader("Create New Account")
    new_user = st.sidebar.text_input("Username", key="register_user")
    new_password = st.sidebar.text_input("Password", type='password', key="register_pass")
    if st.sidebar.button("Register"):
        if register_user(new_user, new_password):
            st.sidebar.success("Account created successfully!")
        else:
            st.sidebar.warning("Username already exists.")

elif choice == "Login":
    st.sidebar.subheader("Login to Your Account")
    username = st.sidebar.text_input("Username", key="login_user")
    password = st.sidebar.text_input("Password", type='password', key="login_pass")
    if st.sidebar.button("Login"):
        if login_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.experimental_rerun()  # Fix: Force rerun after successful login
        else:
            st.sidebar.error("Invalid Username or Password")

# ------------------------------
# Main App Content (after login)
# ------------------------------
if st.session_state.logged_in:
    username = st.session_state.username

    st.subheader("Choose your mood and get Tamil song suggestions 🎶")
    mood = st.selectbox("Select your mood:", list(song_data.keys()))

    if mood:
        st.markdown(f"### Suggested Tamil Songs for {mood} Mood:")
        for song, link in song_data[mood]:
            st.markdown(f"- [{song}]({link})")

    st.markdown("---")

    # Personal Diary
    st.subheader("📝 Your Personal Diary")
    diary = load_diary(username)
    today = str(datetime.date.today())
    entry = diary.get(today, "")

    new_entry = st.text_area("Today's Entry:", value=entry, height=200, key="diary_input")
    if st.button("Save Diary Entry"):
        diary[today] = new_entry
        save_diary(username, diary)
        st.success("Diary entry saved!")

    if st.checkbox("Show Past Entries"):
        for date in sorted(diary.keys(), reverse=True):
            st.markdown(f"**{date}**\n{diary[date]}")

    st.markdown("---")
    st.caption("Made with ❤️ for Tamil music lovers")
