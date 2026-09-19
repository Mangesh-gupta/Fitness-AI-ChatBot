import streamlit as st
import os
import sys
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from frontend.api_client import FitnessAPIClient
from frontend.components.ui import (
    inject_custom_css,
    render_sources_accordion,
    render_thinking_expander
)


# Page Configuration
st.set_page_config(
    page_title="Fitness AI-Chatbot",
    page_icon="🏋️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize API Client
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
api = FitnessAPIClient(base_url=BACKEND_URL)

# Inject Custom CSS
inject_custom_css()

# ==================== Session State Initialization ====================
if "token" not in st.session_state:
    st.session_state.token = None
if "user" not in st.session_state:
    st.session_state.user = None
if "profile" not in st.session_state:
    st.session_state.profile = None
if "sessions" not in st.session_state:
    st.session_state.sessions = []
if "active_session_id" not in st.session_state:
    st.session_state.active_session_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "prompt_to_send" not in st.session_state:
    st.session_state.prompt_to_send = None

def refresh_profile_and_sessions():
    """Fetch latest profile and sessions from backend"""
    if st.session_state.token:
        try:
            st.session_state.profile = api.get_profile(st.session_state.token)
            st.session_state.sessions = api.list_sessions(st.session_state.token)
        except Exception as e:
            st.error(f"Error syncing with server: {e}")

def load_session_messages(session_id: str):
    """Load messages for the selected session"""
    if st.session_state.token and session_id:
        try:
            session_data = api.get_session(st.session_state.token, session_id)
            st.session_state.active_session_id = session_id
            st.session_state.messages = session_data.get("messages", [])
        except Exception as e:
            st.error(f"Error loading session: {e}")

# ==================== Authentication Screen ====================
if not st.session_state.token:
    st.markdown("""
    <div class="hero-container" style="text-align:center;">
        <div class="hero-title" style="justify-content:center;">🏋️‍♂️ Fitness AI-Chatbot</div>
        <div class="hero-subtitle">
            Your intelligent personal fitness coach delivering science-backed workout and nutrition guidance.
        </div>
    </div>

    """, unsafe_allow_html=True)

    auth_col1, auth_col2, auth_col3 = st.columns([1, 2, 1])
    with auth_col2:
        tab_login, tab_register = st.tabs(["🔑 Log In", "📝 Create Account"])

        with tab_login:
            with st.form("login_form"):
                st.subheader("Welcome Back")
                username_or_email = st.text_input("Username or Email")
                password = st.text_input("Password", type="password")
                submit_login = st.form_submit_button("Sign In", use_container_width=True)

                if submit_login:
                    if not username_or_email or not password:
                        st.warning("Please fill in both fields.")
                    else:
                        try:
                            auth_res = api.login(username_or_email, password)
                            st.session_state.token = auth_res["access_token"]
                            st.session_state.user = {
                                "id": auth_res["user_id"],
                                "username": auth_res["username"],
                                "email": auth_res["email"]
                            }
                            refresh_profile_and_sessions()
                            # Select first session if exists, else create one
                            if st.session_state.sessions:
                                load_session_messages(st.session_state.sessions[0]["id"])
                            else:
                                new_sess = api.create_session(st.session_state.token, "Initial Consultation")
                                st.session_state.sessions = [new_sess]
                                load_session_messages(new_sess["id"])
                            st.success(f"Welcome back, {auth_res['username']}!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Login failed: {str(e)}")

        with tab_register:
            with st.form("register_form"):
                st.subheader("Start Your Fitness Journey")
                reg_username = st.text_input("Username (3+ chars)")
                reg_email = st.text_input("Email Address")
                reg_password = st.text_input("Password (6+ chars)", type="password")
                submit_reg = st.form_submit_button("Create Account", use_container_width=True)

                if submit_reg:
                    if not reg_username or not reg_email or not reg_password:
                        st.warning("Please provide username, email, and password.")
                    else:
                        try:
                            reg_res = api.register(reg_username, reg_email, reg_password)
                            st.session_state.token = reg_res["access_token"]
                            st.session_state.user = {
                                "id": reg_res["user_id"],
                                "username": reg_res["username"],
                                "email": reg_res["email"]
                            }
                            refresh_profile_and_sessions()
                            new_sess = api.create_session(st.session_state.token, "Initial Consultation")
                            st.session_state.sessions = [new_sess]
                            load_session_messages(new_sess["id"])
                            st.success("Account created successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Registration failed: {str(e)}")

    st.stop()

# ==================== Authenticated App Layout ====================

# Sidebar: User Profile & Chat Sessions
with st.sidebar:
    st.markdown("### 🏋️‍♂️ Fitness AI-Chatbot")
    st.markdown(f"Welcome, **{st.session_state.user['username']}**")

    # Profile & Goals Drawer
    with st.expander("⚙️ My Fitness Profile & Goals", expanded=False):
        with st.form("profile_form"):
            curr_p = st.session_state.profile or {}
            col_a, col_b = st.columns(2)
            with col_a:
                age_val = st.number_input("Age", min_value=12, max_value=100, value=int(curr_p.get("age") or 25))
                height_val = st.number_input("Height (cm)", min_value=100.0, max_value=240.0, value=float(curr_p.get("height_cm") or 175.0))
            with col_b:
                gender_val = st.selectbox("Gender", ["male", "female", "other"], index=0 if curr_p.get("gender") != "female" else 1)
                weight_val = st.number_input("Weight (kg)", min_value=30.0, max_value=250.0, value=float(curr_p.get("weight_kg") or 75.0))

            goal_options = ["muscle_gain", "fat_loss", "endurance", "general_fitness"]
            curr_goal = curr_p.get("fitness_goal") or "muscle_gain"
            goal_idx = goal_options.index(curr_goal) if curr_goal in goal_options else 0
            goal_val = st.selectbox("Fitness Goal", goal_options, index=goal_idx, format_func=lambda x: x.replace("_", " ").title())

            act_options = ["sedentary", "light", "moderate", "very_active"]
            curr_act = curr_p.get("activity_level") or "moderate"
            act_idx = act_options.index(curr_act) if curr_act in act_options else 2
            act_val = st.selectbox("Activity Level", act_options, index=act_idx, format_func=lambda x: x.replace("_", " ").title())

            diet_options = ["none", "vegan", "vegetarian", "keto", "paleo"]
            curr_diet = curr_p.get("dietary_preference") or "none"
            diet_idx = diet_options.index(curr_diet) if curr_diet in diet_options else 0
            diet_val = st.selectbox("Dietary Preference", diet_options, index=diet_idx, format_func=lambda x: x.title())

            injuries_val = st.text_input("Injuries/Limitations (optional)", value=curr_p.get("injuries_limitations") or "")

            save_profile = st.form_submit_button("Save Profile & Goals", use_container_width=True)
            if save_profile:
                update_payload = {
                    "age": age_val,
                    "gender": gender_val,
                    "height_cm": height_val,
                    "weight_kg": weight_val,
                    "fitness_goal": goal_val,
                    "activity_level": act_val,
                    "dietary_preference": diet_val,
                    "injuries_limitations": injuries_val
                }
                try:
                    updated = api.update_profile(st.session_state.token, update_payload)
                    st.session_state.profile = updated
                    st.success("Profile updated!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Update failed: {e}")

    st.markdown("---")

    # New Chat Button
    st.markdown('<div class="new-chat-btn">', unsafe_allow_html=True)
    if st.button("➕ New Consultation", use_container_width=True):
        try:
            new_s = api.create_session(st.session_state.token, "New Consultation")
            st.session_state.sessions.insert(0, new_s)
            load_session_messages(new_s["id"])
            st.rerun()
        except Exception as e:
            st.error(f"Error creating session: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

    # Sessions List
    st.markdown("#### 💬 Consultations")
    if not st.session_state.sessions:
        st.caption("No consultations yet. Start one above!")
    else:
        for s in st.session_state.sessions:
            s_id = s["id"]
            s_title = s.get("title", "Consultation")
            is_active = s_id == st.session_state.active_session_id

            col_s1, col_s2 = st.columns([0.82, 0.18], vertical_alignment="center")
            with col_s1:
                btn_label = f"{'🟢 ' if is_active else '💬 '}{s_title}"
                if is_active:
                    st.markdown('<div class="active-session-btn">', unsafe_allow_html=True)
                if st.button(btn_label, key=f"sess_btn_{s_id}", use_container_width=True):
                    load_session_messages(s_id)
                    st.rerun()
                if is_active:
                    st.markdown('</div>', unsafe_allow_html=True)
            with col_s2:
                if st.button("🗑️", key=f"del_btn_{s_id}", help="Delete consultation", use_container_width=True):
                    api.delete_session(st.session_state.token, s_id)
                    st.session_state.sessions = [x for x in st.session_state.sessions if x["id"] != s_id]
                    if st.session_state.active_session_id == s_id:
                        if st.session_state.sessions:
                            load_session_messages(st.session_state.sessions[0]["id"])
                        else:
                            st.session_state.active_session_id = None
                            st.session_state.messages = []
                    st.rerun()

    st.markdown("---")
    st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
    if st.button("🔒 Log Out", use_container_width=True):
        st.session_state.token = None
        st.session_state.user = None
        st.session_state.profile = None
        st.session_state.sessions = []
        st.session_state.active_session_id = None
        st.session_state.messages = []
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== Main Chat Interface ====================

# Ensure an active session exists
if not st.session_state.active_session_id:
    if st.session_state.sessions:
        load_session_messages(st.session_state.sessions[0]["id"])
    else:
        new_sess = api.create_session(st.session_state.token, "Initial Consultation")
        st.session_state.sessions = [new_sess]
        load_session_messages(new_sess["id"])

# Find active session title
active_session_title = "Consultation"
for s in st.session_state.sessions:
    if s["id"] == st.session_state.active_session_id:
        active_session_title = s.get("title", "Consultation")
        break

# Header
st.markdown(f"### 💬 {active_session_title}")

# Empty State Hero & Starter Prompts
if not st.session_state.messages:
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">👋 Hey there! I'm your Fitness AI-Chatbot.</div>
        <div class="hero-subtitle">
            I provide personalized workout programming, precision nutrition guidance, science-backed supplement advice, and gear recommendations tailored to your goals.
        </div>
    </div>

    """, unsafe_allow_html=True)

    st.markdown("##### 🚀 Quick Start Topics")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏋️ Design a 4-day Upper/Lower Hypertrophy Split", use_container_width=True):
            st.session_state.prompt_to_send = "Design a 4-day Upper/Lower Hypertrophy Split with sets, reps, and RIR recommendations based on my profile."
        if st.button("🥗 Build a high-protein nutrition & meal plan for fat loss", use_container_width=True):
            st.session_state.prompt_to_send = "Provide a science-backed, high-protein meal plan and nutrition guidelines for fat loss tailored to my profile."
    with col2:
        if st.button("💊 What are the evidence-based benefits of Creatine?", use_container_width=True):
            st.session_state.prompt_to_send = "What are the evidence-based benefits, dosing protocol, and safety profile of Creatine Monohydrate?"
        if st.button("🦵 How to protect my knees and maintain form during deep squats?", use_container_width=True):
            st.session_state.prompt_to_send = "How do I protect my knees and maintain proper biomechanics during deep barbell squats?"


# Render Chat History
for msg in st.session_state.messages:
    role = msg.get("role")
    content = msg.get("content", "")
    reasoning = msg.get("reasoning_content")
    sources = msg.get("sources")

    if role == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(content)
    elif role == "assistant":
        with st.chat_message("assistant", avatar="🏋️‍♂️"):
            # Collapsible thinking process
            if reasoning:
                render_thinking_expander(reasoning)

            # Markdown content
            st.markdown(content)

            # Sources from ChromaDB RAG
            if sources:
                render_sources_accordion(sources)

# Handle Triggered Quick-Start Prompts
prompt = None
if st.session_state.prompt_to_send:
    prompt = st.session_state.prompt_to_send
    st.session_state.prompt_to_send = None
else:
    prompt = st.chat_input("Message Fitness AI-Chatbot...")

if prompt:
    # 1. Display User Message
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Append to local message state
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Stream Assistant Response
    with st.chat_message("assistant", avatar="🏋️‍♂️"):
        thinking_placeholder = st.empty()
        content_placeholder = st.empty()
        sources_placeholder = st.empty()

        accumulated_thinking = ""
        accumulated_content = ""
        retrieved_sources = []

        try:
            for chunk in api.stream_chat(st.session_state.token, st.session_state.active_session_id, prompt):
                event_type = chunk.get("event")

                if event_type == "meta":
                    retrieved_sources = chunk.get("sources", [])

                elif event_type == "thinking":
                    accumulated_thinking += chunk.get("text", "")
                    with thinking_placeholder.container():
                        render_thinking_expander(accumulated_thinking)

                elif event_type == "content":
                    accumulated_content += chunk.get("text", "")
                    content_placeholder.markdown(accumulated_content + "▌")

                elif event_type == "done":
                    break

            # Finalize display without streaming cursor
            content_placeholder.markdown(accumulated_content)

            if retrieved_sources:
                with sources_placeholder.container():
                    render_sources_accordion(retrieved_sources)

            # Append to session state
            st.session_state.messages.append({
                "role": "assistant",
                "content": accumulated_content,
                "reasoning_content": accumulated_thinking if accumulated_thinking else None,
                "sources": retrieved_sources
            })

            # Refresh session list in case title was updated
            st.session_state.sessions = api.list_sessions(st.session_state.token)

        except Exception as e:
            st.error(f"Error communicating with AI coach: {e}")

