import streamlit as st
from groq import Groq
import os
import pandas as pd
import hashlib
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from dotenv import load_dotenv

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

groq_key = os.getenv("GROQ_API_KEY")

if not groq_key:
    raise ValueError("GROQ_API_KEY not found in .env")

client = Groq(api_key=groq_key)
# -----------------------
# --- Modern Sidebar and Main Content Styling ---
st.markdown("""
<style>

/* ---------- Animated App Background ---------- */

.stApp{
    background: linear-gradient(-45deg,#0f172a,#1e293b,#020617,#1e1b4b);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
    color:#e2e8f0;
}

@keyframes gradientBG{
0%{background-position:0% 50%}
50%{background-position:100% 50%}
100%{background-position:0% 50%}
}


/* ---------- Remove All White Backgrounds ---------- */

.block-container{
    background:transparent !important;
}

div[data-testid="stToolbar"],
header{
    background:transparent !important;
}

section[data-testid="stSidebar"]{
    background:#020617 !important;
}


/* ---------- Text Visibility ---------- */

h1,h2,h3,h4,h5,h6,p,span,label{
color:#e2e8f0 !important;
}


/* ---------- Sidebar ---------- */

section[data-testid="stSidebar"]{
    border-right:1px solid rgba(255,255,255,0.08);
}


/* Sidebar animation */

section[data-testid="stSidebar"]{
    animation:slideSidebar .8s ease;
}

@keyframes slideSidebar{
0%{transform:translateX(-40px);opacity:0}
100%{transform:translateX(0);opacity:1}
}


/* ---------- Cards ---------- */

.main-modern-section{

    background:rgba(15,23,42,0.75);
    backdrop-filter:blur(12px);

    border-radius:16px;
    padding:30px;

    border:1px solid rgba(255,255,255,0.08);

    box-shadow:0 8px 30px rgba(0,0,0,0.6);

    transition:all .3s ease;

    animation:fadeUp 0.8s ease;
}

@keyframes fadeUp{
0%{transform:translateY(20px);opacity:0}
100%{transform:translateY(0);opacity:1}
}

.main-modern-section:hover{
    transform:translateY(-5px) scale(1.01);
    box-shadow:0 12px 45px rgba(0,0,0,0.8);
}


/* ---------- Page Headers ---------- */

.main-modern-header{

text-align:center;
font-size:36px;
font-weight:700;

background:linear-gradient(90deg,#3b82f6,#8b5cf6,#22c55e);
background-size:200%;

-webkit-background-clip:text;
-webkit-text-fill-color:transparent;

animation:titleGlow 6s linear infinite;
}

@keyframes titleGlow{

0%{background-position:0%}
100%{background-position:200%}

}
/* Fix white background around chat/search bar */

div[data-testid="stChatFloatingInputContainer"]{
    background:#020617 !important;
    border-top:1px solid rgba(255,255,255,0.08);
}


/*------------------- Inner chat input area ---------------*/

div[data-testid="stChatInput"]{
    background:#020617 !important;
}


/* ---------------Input box----------------- */

div[data-testid="stChatInput"] textarea{
    background:#0f172a !important;
    color:#e2e8f0 !important;
    border:1px solid rgba(255,255,255,0.15) !important;
    border-radius:10px !important;
    padding:10px !important;
}


/*----------------- Placeholder text---------------- */

div[data-testid="stChatInput"] textarea::placeholder{
    color:#94a3b8 !important;
}


/*----------- Focus glow --------------*/

div[data-testid="stChatInput"] textarea:focus{
    border:1px solid #60a5fa !important;
    box-shadow:0 0 8px rgba(96,165,250,0.4);
}

/* ---------- Buttons ---------- */

.stButton button{

    background:linear-gradient(135deg,#2563eb,#7c3aed);

    border:none;

    color:white !important;

    padding:10px 18px;

    border-radius:10px;

    font-weight:600;

    transition:all .25s ease;

    box-shadow:0 5px 15px rgba(0,0,0,0.4);
}

.stButton button:hover{

    transform:translateY(-2px) scale(1.05);

    background:linear-gradient(135deg,#3b82f6,#8b5cf6);

    box-shadow:0 8px 25px rgba(124,58,237,0.6);
}


/* ---------- Inputs ---------- */

.stTextInput input,
.stNumberInput input,
.stTextArea textarea{

background:#020617 !important;

border:1px solid rgba(255,255,255,0.12) !important;

color:#f1f5f9 !important;

border-radius:8px;

padding:10px;
}

.stTextInput input:focus,
.stNumberInput input:focus,
.stTextArea textarea:focus{

border:1px solid #60a5fa !important;

box-shadow:0 0 8px rgba(96,165,250,0.5);
}


/* ---------- File uploader ---------- */

.stFileUploader{

background:#020617;

border:1px dashed rgba(255,255,255,0.2);

padding:20px;

border-radius:10px;
}
/*------------ Chat input bar -------------*/

div[data-testid="stChatInput"]{
    background: rgba(2,6,23,0.9) !important;
    border-top: 1px solid rgba(255,255,255,0.08);
    padding: 10px;
}

div[data-testid="stChatInput"] textarea{
    background:#020617 !important;
    color:#e2e8f0 !important;
    border:1px solid rgba(255,255,255,0.15) !important;
    border-radius:10px !important;
    padding:10px !important;
}

/*---------------- placeholder text-------------- */

div[data-testid="stChatInput"] textarea::placeholder{
    color:#94a3b8 !important;
}

/*---------------- focus effect ----------------*/

div[data-testid="stChatInput"] textarea:focus{
    border:1px solid #60a5fa !important;
    box-shadow:0 0 8px rgba(96,165,250,0.4);
}

/* ---------- Dataframe ---------- */

.stDataFrame{

background:#020617;

border-radius:10px;
}

/* ---------- Ultra-Clean White Chat Messages ---------- */
[data-testid="stChatMessage"] {
    background: rgba(255, 255, 255, 0.9) !important; /* Pure white with slight transparency */
    backdrop-filter: blur(10px);
    border-radius: 15px !important;
    padding: 20px !important;
    margin-bottom: 15px !important;
    border: 1px solid rgba(0, 0, 0, 0.05) !important; /* Very subtle border */
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important; /* Soft shadow */
    color: #1e293b !important; /* Dark slate text for readability */
}

/* Fix text color inside white bubbles for both User and Assistant */
[data-testid="stChatMessage"] p, [data-testid="stChatMessage"] li {
    color: #334155 !important;
}

/* ---------- Enhanced Floating Search Bar ---------- */
div[data-testid="stChatFloatingInputContainer"] {
    background: transparent !important; /* Remove the bottom bar background */
    bottom: 20px !important;
}

div[data-testid="stChatInput"] {
    background: white !important;
    border-radius: 50px !important; /* Pill shape */
    border: 1px solid rgba(0, 0, 0, 0.1) !important;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1) !important;
    padding: 5px 15px !important;
    transition: all 0.3s ease;
}

div[data-testid="stChatInput"]:focus-within {
    border: 1px solid #3b82f6 !important;
    box-shadow: 0 10px 30px rgba(59, 130, 246, 0.2) !important;
    transform: translateY(-2px);
}

/* Remove the default Streamlit styling from the inner textarea */
div[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: #1e293b !important;
    border: none !important;
    font-size: 1rem !important;
}


/* ---------- Progress Bar ---------- */

.stProgress > div > div > div{

background:linear-gradient(90deg,#3b82f6,#8b5cf6);
}


/* ---------- Toggle ---------- */

.stToggle{

color:#e2e8f0;
}


/* ---------- Scrollbar ---------- */

::-webkit-scrollbar{
width:8px;
}

::-webkit-scrollbar-track{
background:#020617;
}

::-webkit-scrollbar-thumb{
background:#334155;
border-radius:6px;
}

::-webkit-scrollbar-thumb:hover{
background:#475569;
}

</style>
""", unsafe_allow_html=True)
# Load Environment
# -----------------------
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

EMAIL = os.getenv("HR_EMAIL_ADDRESS")
PASSWORD = os.getenv("HR_EMAIL_PASSWORD")

# -----------------------
# Session States
# -----------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_histories" not in st.session_state:
    st.session_state.chat_histories = []

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True


# -----------------------
# User Database (Local CSV)
# -----------------------
# This is a simple local user store for demo purposes. In production, replace
# with a proper authentication system and hashed password storage.
USER_DB_PATH = Path(__file__).parent / "users.csv"


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def load_users() -> pd.DataFrame:
    if USER_DB_PATH.exists():
        return pd.read_csv(USER_DB_PATH)
    return pd.DataFrame(columns=["username", "email", "password_hash"])


def save_user(name, email, password, language):

    import csv

    with open("users.csv", "a", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([name, email, password, language])


def verify_user(email: str, password: str) -> dict | None:
    users = load_users()
    if users.empty:
        return None
    password_hash = _hash_password(password)
    match = users[
        (users["email"].str.lower() == email.lower()) &
        (users["password_hash"] == password_hash)
    ]
    if not match.empty:
        return match.iloc[0].to_dict()
    return None


def create_user(username: str, email: str, password: str) -> tuple[bool, str]:
    users = load_users()
    if not users[users["email"].str.lower() == email.lower()].empty:
        return False, "Email already registered."
    if not users[users["username"].str.lower() == username.lower()].empty:
        return False, "Username already taken."
    new_user = {
        "username": username,
        "email": email,
        "password_hash": _hash_password(password)
    }
    users = pd.concat([users, pd.DataFrame([new_user])], ignore_index=True)
    save_users(users)
    return True, "Account created successfully."


# -----------------------
# Login Page
# -----------------------
if not st.session_state.logged_in:

    st.markdown("""
    <style>
    body, .stApp {
        background: linear-gradient(120deg, #232946 0%, #7c3aed 100%) !important;
        min-height: 100vh;
    }
    .login-bg-anim {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: 0;
        pointer-events: none;
        overflow: hidden;
        animation: bgRotate 38s linear infinite;
    }
    @keyframes bgRotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    .login-blob {
        position: absolute;
        border-radius: 50%;
        opacity: 0.22;
        filter: blur(48px);
        animation: floatBlob 12s ease-in-out infinite alternate;
    }
    .login-blob1 {
        width: 420px; height: 420px;
        background: linear-gradient(120deg, #7c3aed 0%, #2563eb 100%);
        left: -120px; top: -80px;
        animation-delay: 0s;
    }
    .login-blob2 {
        width: 320px; height: 320px;
        background: linear-gradient(120deg, #2563eb 0%, #7c3aed 100%);
        right: -100px; bottom: -60px;
        animation-delay: 2s;
    }
    .login-blob3 {
        width: 220px; height: 220px;
        background: linear-gradient(120deg, #a5b4fc 0%, #7c3aed 100%);
        left: 50vw; top: 10vh;
        animation-delay: 4s;
    }
    .login-blob4 {
        width: 180px; height: 180px;
        background: linear-gradient(120deg, #818cf8 0%, #2563eb 100%);
        right: 40vw; bottom: 18vh;
        animation-delay: 6s;
    }
    @keyframes floatBlob {
        0% { transform: scale(1) translateY(0) translateX(0); }
        100% { transform: scale(1.13) translateY(40px) translateX(30px); }
    }
    .login-card {
        max-width: 400px;
        margin: 8vh auto 0 auto;
        background: rgba(35,41,70,0.82);
        border-radius: 22px;
        box-shadow: 0 8px 32px #0005, 0 1.5px 0 #7c3aed;
        padding: 2.5em 2.5em 2em 2.5em;
        text-align: center;
        position: relative;
        animation: fadeInCard 1.1s cubic-bezier(.4,0,.2,1);
        z-index: 2;
        backdrop-filter: blur(16px) saturate(160%);
        border: 1.5px solid #7c3aed44;
    }
    @keyframes fadeInCard {
        0% { opacity: 0; transform: translateY(-40px) scale(0.95); }
        100% { opacity: 1; transform: translateY(0) scale(1); }
    }
    .login-anim {
        width: 80px;
        margin-bottom: 1.2em;
        animation: bounceAnim 1.8s infinite cubic-bezier(.6,0,.4,1);
        filter: drop-shadow(0 4px 16px #7c3aed88);
    }
    @keyframes bounceAnim {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-18px) scale(1.08); }
    }
    .login-title { color: #fff; font-size: 2.1em; font-weight: 700; margin-bottom: 0.2em; letter-spacing: 0.5px; }
    .login-desc { color: #e0e7ff; font-size: 1.08em; margin-bottom: 1.5em; }
    .login-input input {
        background: rgba(49,46,129,0.2);
        color: #f8fafc;
        border-radius: 8px;
        border: 1.5px solid rgba(124,58,237,0.8);
        padding: 0.7em 1em;
        font-size: 1.1em;
        margin-bottom: 1.2em;
        width: 100%;
        transition: border 0.2s, background 0.2s;
        box-shadow: 0 2px 8px #0003;
    }
    .login-input input::placeholder {
        color: rgba(255,255,255,0.65);
    }
    .login-input input:focus {
        border: 2px solid #2563eb;
        outline: none;
        background: rgba(49,46,129,0.22);
    }
    .login-btn button {
        width: 100%;
        background: linear-gradient(90deg, #7c3aed 0%, #2563eb 100%);
        color: #fff;
        border: none;
        border-radius: 8px;
        padding: 0.8em 0;
        font-size: 1.15em;
        font-weight: 600;
        margin-top: 0.5em;
        box-shadow: 0 2px 8px #0002;
        transition: 0.18s;
        letter-spacing: 0.2px;
    }
    .login-btn button:hover {
        background: linear-gradient(90deg, #2563eb 0%, #7c3aed 100%);
        transform: scale(1.03);
        box-shadow: 0 4px 16px #7c3aed33;
    }
    @media (max-width: 600px) {
        .login-card {padding: 1.2em 0.5em;}
        .login-title {font-size: 1.4em;}
    }
    </style>
    <div class="login-bg-anim">
        <div class="login-blob login-blob1"></div>
        <div class="login-blob login-blob2"></div>
        <div class="login-blob login-blob3"></div>
        <div class="login-blob login-blob4"></div>
    </div>
    <div class="login-card">
        <img src="https://cdn-icons-png.flaticon.com/512/4712/4712035.png" class="login-anim" alt="login icon"/>
        <div class="login-title">AutoTask AI</div>
        <div class="login-desc">Sign in to access your AI-powered workspace.<br>Smart task automation, HR tools, and more.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='max-width:400px;margin:-2.5em auto 0 auto;position:relative;z-index:2;'>
    </div>
    """, unsafe_allow_html=True)

    # Authentication mode: Sign In / Create Account
    auth_mode = st.radio(
        "", ["Sign In", "Create Account"], index=0, horizontal=True, key="auth_mode"
    )

    st.caption("Accounts are stored locally in `users.csv`; email and password are verified against this database.")

    if auth_mode == "Sign In":
        email = st.text_input("Email", key="login_email", placeholder="you@example.com")
        password = st.text_input("Password", type="password", key="login_password", placeholder="••••••••")

        if st.button("Sign In", key="signin_btn"):
            if not email or not password:
                st.error("Enter both email and password.")
            else:
                user = verify_user(email, password)
                if user:
                    st.session_state.logged_in = True
                    st.session_state.user = user.get("username")
                    st.success(f"Welcome back, {user.get('username')}!")
                    st.rerun()
                else:
                    st.error("Invalid email or password.")

    else:
        username = st.text_input("Username", key="signup_username", placeholder="Choose a username")
        email = st.text_input("Email", key="signup_email", placeholder="you@example.com")
        password = st.text_input("Password", type="password", key="signup_password", placeholder="••••••••")
        password2 = st.text_input("Confirm Password", type="password", key="signup_password2", placeholder="••••••••")

        if st.button("Create Account", key="signup_btn"):
            if not username or not email or not password or not password2:
                st.error("All fields are required.")
            elif password != password2:
                st.error("Passwords do not match.")
            else:
                ok, msg = create_user(username, email, password)
                if ok:
                    st.success(msg + " You can now sign in.")
                else:
                    st.error(msg)

    st.stop()


# -----------------------
# Sidebar
# -----------------------

with st.sidebar:
    st.markdown('<div class="sidebar-modern">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-header"><span class="icon">🤖</span><span class="title">AutoTask AI</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="glow-btn">', unsafe_allow_html=True)
    if st.button("➕ New Chat"):
      if st.session_state.messages:
        st.session_state.chat_histories.append(st.session_state.messages.copy())
    st.session_state.messages = []
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Chat History</div>', unsafe_allow_html=True)
    st.markdown('<div class="chat-history-list">', unsafe_allow_html=True)
    if st.session_state.chat_histories:
        for idx, chat in enumerate(st.session_state.chat_histories):
            preview = next((msg["content"][:32] + ("..." if len(msg["content"]) > 32 else "")
                            for msg in chat if msg.get("role") == "user" and msg.get("content")), "(No prompt)")
            selected = (st.session_state.messages == chat)
            btn_class = "chat-history-item selected" if selected else "chat-history-item"
            if st.button(f"💬 {preview}", key=f"chat_{idx}"):
                st.session_state.messages = list(chat)
            st.markdown(f'<div class="{btn_class}"></div>', unsafe_allow_html=True)
    else:
        st.markdown("<span style='color:#aaa;font-size:0.97em;'>No conversations yet</span>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title nav-section">Features</div>', unsafe_allow_html=True)
    nav_option = st.radio(
    "Navigation",
    ["Chatbot", "Send Salary Emails", "ML Predictions", "Meeting Scheduler"],
    key="nav_radio",
    label_visibility="collapsed"
)
   
    st.markdown('<div class="settings-section">', unsafe_allow_html=True)
    st.session_state.dark_mode = st.toggle(
        "🌙 Dark Mode",
        value=st.session_state.dark_mode
    )
    
    st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# -----------------------
# Theme Switching
# -----------------------

if st.session_state.dark_mode:

    st.markdown("""
    <style>

    /* DARK MODE */

    .stApp{
        background:linear-gradient(135deg,#0f172a,#020617);
        color:#e2e8f0;
    }

    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div{
        background:#020617 !important;
    }

    .main-modern-section{
        background:#0f172a !important;
        border:1px solid rgba(255,255,255,0.08);
    }

    div[data-testid="stChatFloatingInputContainer"]{
        background:#020617 !important;
    }

    div[data-testid="stChatInput"] textarea{
        background:#0f172a !important;
        color:#e2e8f0 !important;
    }

    </style>
    """, unsafe_allow_html=True)

else:

    st.markdown("""
    <style>

    /* LIGHT MODE */

    .stApp{
        background:linear-gradient(135deg,#f1f5f9,#e2e8f0);
        color:#0f172a;
    }

    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] > div{
        background:#e2e8f0 !important;
    }

    .main-modern-section{
        background:#ffffff !important;
        border:1px solid rgba(0,0,0,0.08);
    }

    /* Fix text visibility in light mode */

section[data-testid="stSidebar"] *{
    color:#0f172a !important;
}

/* Radio button labels */

div[data-testid="stRadio"] label{
    color:#0f172a !important;
}

/* Sidebar text like "No conversations yet" */

.sidebar-modern span{
    color:#334155 !important;
}

/* General text inside main area */

.stMarkdown,
.stText,
p, span, label{
    color:#0f172a !important;
}

/* Captions */

.stCaption{
    color:#475569 !important;
}

    </style>
    """, unsafe_allow_html=True)

# -----------------------
# Email Functions
# -----------------------
def read_excel(uploaded_file):

    df = pd.read_excel(uploaded_file)

    required = {"name", "email", "salary_change", "new_salary"}

    if not required.issubset(df.columns):
        st.error("Excel must contain: name, email, salary_change, new_salary")
        return None

    return df


def generate_email(name, change, salary):

    if change > 0:

        return f"""
Dear {name},

We are pleased to inform you that your salary has increased by ₹{change}.

Your new salary will be ₹{salary} effective next month.

Best regards  
HR Department
"""

    else:

        return f"""
Dear {name},

Your salary has been adjusted by ₹{abs(change)}.

Your revised salary will be ₹{salary} effective next month.

HR Department
"""
# meeting function
import random
import string

def generate_meeting_link():
    letters = string.ascii_lowercase
    code = ''.join(random.choice(letters) for i in range(10))
    return f"https://meet.google.com/{code}"


def generate_meeting_email(name, title, date, time, link):
    return f"""
Hello {name},

You are invited to a meeting.

Title: {title}
Date: {date}
Time: {time}

Join Meeting:
{link}

Best Regards
HR Team
"""

def send_email(sender, password, receiver, body):

    msg = MIMEText(body)
    msg["Subject"] = "Meeting Invitation"
    msg["From"] = sender
    msg["To"] = receiver

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    server.login(sender, password)

    server.sendmail(sender, receiver, msg.as_string())

    server.quit()

# Salary Email Page

if nav_option == "Send Salary Emails":

    st.markdown('<div class="main-modern-section">', unsafe_allow_html=True)
    st.markdown('<div class="main-modern-header">📧 Salary Email Automation</div>', unsafe_allow_html=True)
    file = st.file_uploader("Upload Excel", type=["xlsx"])
    if file:
        df = read_excel(file)
        if df is not None:
            st.dataframe(df)
            if st.button("Send Emails"):
                progress = st.progress(0)
                for i, row in df.iterrows():
                    body = generate_email(
                        row["name"],
                        row["salary_change"],
                        row["new_salary"]
                    )
                    send_email(
                        EMAIL,
                        PASSWORD,
                        row["email"],
                        body
                    )
                    progress.progress((i + 1) / len(df))
                    time.sleep(0.2)
                st.success("Emails sent successfully")
    st.markdown('</div>', unsafe_allow_html=True)

# ML Predictions Page

elif nav_option == "ML Predictions":

    st.markdown('<div class="main-modern-section">', unsafe_allow_html=True)
    st.markdown('<div class="main-modern-header">🤖 ML Predictions</div>', unsafe_allow_html=True)
    st.subheader("Task Priority")
    skills = st.text_input("Required Skills")
    deadline = st.number_input("Deadline Days", min_value=1)
    if st.button("Predict Priority"):
        st.success("Predicted Priority: High")
    st.subheader("Employee Role")
    emp_skills = st.text_input("Employee Skills")
    exp = st.number_input("Experience", min_value=0)
    workload = st.number_input("Workload %", 0, 100)
    if st.button("Predict Role"):
        st.success("Suggested Role: Developer")
    st.subheader("Project Success")
    team = st.number_input("Team Size", min_value=1)
    days = st.number_input("Completion Days", min_value=1)
    if st.button("Predict Success"):
        st.success("Success Score: 82%")
    st.markdown('</div>', unsafe_allow_html=True)
# -----------------------
# Meeting Scheduler Page
# -----------------------

elif nav_option == "Meeting Scheduler":

    st.markdown('<div class="main-modern-section">', unsafe_allow_html=True)
    st.markdown('<div class="main-modern-header">📅 Automatic Meeting Scheduler</div>', unsafe_allow_html=True)

    title = st.text_input("Meeting Title")
    date = st.date_input("Meeting Date")
    time_val = st.time_input("Meeting Time")
    participants = st.text_area("Participants Emails (comma separated)")

    if st.button("Schedule Meeting"):

        st.write("Scheduling meeting...")

        link = generate_meeting_link()

        st.write("Meeting link generated:", link)

        emails = participants.split(",")

        for email in emails:

            email = email.strip()

            body = generate_meeting_email(
                email,
                title,
                date,
                time_val,
                link
            )

            st.write("Sending email to:", email)

            send_email(EMAIL, PASSWORD, email, body)

        st.success("Meeting Scheduled Successfully")
        st.markdown(f"### Meeting Link\n{link}")

    st.markdown('</div>', unsafe_allow_html=True)
    
    
# -----------------------
# Chatbot Page
# -----------------------
elif nav_option == "Chatbot":
    # The header stays outside or inside depending on your previous preference
    st.markdown('<div class="main-modern-header" style="margin-bottom: 20px;">💬 AI Task Assistant</div>', unsafe_allow_html=True)
    
    # Use a container to group messages together nicely
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Search bar stays at the bottom automatically
    prompt = st.chat_input("How can I help you today?")

    if prompt:

        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("AI thinking..."):

            messages = [{"role": "system", "content": "You are an autonomous AI assistant."}] + st.session_state.messages[-10:]

            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages
            )

            reply = response.choices[0].message.content

            st.session_state.messages.append({"role": "assistant", "content": reply})

            with st.chat_message("assistant"):
                st.markdown(reply)
