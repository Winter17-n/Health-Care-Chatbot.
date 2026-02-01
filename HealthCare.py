# -------------Importing the Libraries---------------
import os
import streamlit as st
from PIL import Image
import base64
import google.generativeai as genai
from datetime import datetime


# ----------------Setting Up The Webpage------------------
st.set_page_config(page_title="Health Care Assistant", layout="wide", initial_sidebar_state='expanded')

# --- Session State Defaults ---
if "chat" not in st.session_state:
    pass 

if "transcript" not in st.session_state:
    st.session_state.transcript = []

if "saved_chats" not in st.session_state:
    st.session_state.saved_chats = []

if "last_user_message" not in st.session_state:
    st.session_state.last_user_message = ""

if "submitted_flag" not in st.session_state:
    st.session_state.submitted_flag = False

if "clear_input_pending" not in st.session_state:
    st.session_state.clear_input_pending = False


# ----------------Model Setup------------------
genai.configure(api_key=os.getenv("pyth"))
model = genai.GenerativeModel("models/gemini-2.5-flash")

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

#-------------Sidebar-------------
st.sidebar.title("Your History")

if st.session_state.saved_chats:
    for item in reversed(st.session_state.saved_chats):
        st.sidebar.markdown(f"{item['title']}")



# ----------------Styling The Header Image-----------------
img_path = "healthcar.png"
if os.path.exists(img_path):
    with open(img_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    st.markdown(f"""
    <div style="display:flex; justify-content:center; margin-bottom:20px;">
        <img src="data:image/png;base64,{b64}"
             style="
                width:1200px;
                height:200px;
                border:4px solid #5E8A8E;
                border-radius:20px;
                box-shadow:0 0 12px rgba(94,138,142,0.5);
                object-fit:fill;
             ">
    </div>
    """, unsafe_allow_html=True)

# ----------------Title--------------
st.markdown("<h2 style='text-align: center; font-family: serif; color:#390002'><u> WELCOME TO HEALTH CARE ASSISTANT</u></h2>", unsafe_allow_html=True)

# -------------Background--------------
st.markdown("""
<style>
.stApp { background-color: #D6F9FD; }
</style>
""", unsafe_allow_html=True)

# --------- CHAT HISTORY----------
if st.session_state.transcript:
    for role, msg in (st.session_state.transcript):
        if role == "You":
            st.markdown(
                f"<div style='text-align:left; color:#003153; padding:6px;'><b>You:</b> {msg}</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div style='text-align:right; color:#003153; padding:6px;'><b>Assistant:</b> {msg}</div>",
                unsafe_allow_html=True
            )


# ------------Clear input---------------
if st.session_state.clear_input_pending:
    st.session_state.user_input = ""
    st.session_state.clear_input_pending = False

def _on_submit():
    st.session_state.last_user_message = st.session_state.user_input
    st.session_state.submitted_flag = True
    st.session_state.clear_input_pending = True

st.text_input("", placeholder="♥ How can I help you?", key="user_input", on_change=_on_submit)

# ----------------Assistant Response Area-------------
response_area = st.empty()

# ----------------Handling Submission---------------
if st.session_state.submitted_flag and st.session_state.last_user_message.strip() != "":
    text = st.session_state.last_user_message.strip()

# Reset flag
    st.session_state.submitted_flag = False
    st.session_state.last_user_message = ""

# Save input into sidebar history
    st.session_state.saved_chats.append({
        "title": text if len(text) <= 40 else text[:37] + "...",
        "content": text,
        "time": datetime.now()
    })

# Build prompt
    prompt = (
        f"You are a helpful, kind and empathetic health assistant. "
        f"You can read images and response to them."
        f"Provide general wellness guidance. "
        f"you give precise answers."
        f"If user asks for tips give just 5 tips for that query but only for the tips query."
        f"you must only give response related to health and wellness."
        f"you must give elaborated response only when the user asks you for that"
        f"you must give random motivating emoji with every response."
        f"you can calculate the bmi if user asks for it."
        f"User said: {text}"
    )

    try:
        with st.spinner("Thinking..."):
            resp = st.session_state.chat.send_message(prompt)
            response_text = resp.text

 # Display and store
        response_area.write(response_text)

        st.session_state.transcript.append(("You", text))
        st.session_state.transcript.append(("Assistant", response_text))

        st.rerun()

    except Exception as e:
        response_area.error(f"Error: {e}")
