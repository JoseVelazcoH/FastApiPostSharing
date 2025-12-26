import streamlit as st
import requests
from app.core.config import settings
from app.const.constants import MEDIA_TYPES
from app.components.post_render import get_post_render
from app.services.auth import authenticate_user, get_current_user, register_user
from app.services.post import get_feed, delete_post, upload_post

st.set_page_config(page_title="Simple Social", layout="wide")

if 'token' not in st.session_state:
    st.session_state.token = None
if 'user' not in st.session_state:
    st.session_state.user = None


def get_headers():
    if st.session_state.token:
        return {"Authorization": f"Bearer {st.session_state.token}"}
    return {}


def handle_api_response(response, success_code, success_msg=None, error_msg="Operation failed"):
    if response.status_code != success_code:
        st.error(error_msg)
        return False
    if success_msg:
        st.success(success_msg)
    return True


def login_page():
    st.title("Welcome to Social")

    email = st.text_input("Email:")
    password = st.text_input("Password:", type="password")

    if not email or not password:
        st.info("Enter your email and password above")
        return

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login", type="primary", use_container_width=True):
            response = authenticate_user(email, password)
            if not handle_api_response(response, 200, error_msg="Invalid email or password!"):
                return

            token_data = response.json()
            st.session_state.token = token_data["access_token"]

            user_response = get_current_user(st.session_state.token)
            if not handle_api_response(user_response, 200, error_msg="Failed to get user info"):
                return

            st.session_state.user = user_response.json()
            st.rerun()

    with col2:
        if st.button("Sign Up", type="secondary", use_container_width=True):
            register_response = register_user(email, password)
            if not handle_api_response(register_response, 201, success_msg="Account created! Click Login now.", error_msg="Registration failed"):
                return


def upload_page():
    st.title("📸 Share Something")
    uploaded_file = st.file_uploader("Choose media", type=MEDIA_TYPES)
    caption = st.text_area("Caption:", placeholder="What's on your mind?")

    if uploaded_file and st.button("Share", type="primary"):
        with st.spinner("Uploading..."):
            response = upload_post(
                file_name=uploaded_file.name,
                file_content=uploaded_file.getvalue(),
                file_type=uploaded_file.type,
                caption=caption,
                token=st.session_state.token
            )
            if not handle_api_response(response, 200, success_msg="Posted!"):
                return
            st.rerun()


def feed_page():
    st.title("🏠 Feed")

    response = get_feed(st.session_state.token)
    if not handle_api_response(response, 200, error_msg="Failed to load feed"):
        return

    posts = response.json()["posts"]

    if not posts:
        st.info("No posts yet! Be the first to share something.")
        return

    for post_data in posts:
        st.markdown("---")

        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"**{post_data['email']}** • {post_data['created_at'][:10]}")
        with col2:
            if post_data.get('is_owner', False):
                if st.button("🗑️", key=f"delete_{post_data['id']}", help="Delete post"):
                    delete_response = delete_post(post_data["id"], st.session_state.token)
                    if handle_api_response(delete_response, 200, success_msg="Post deleted!", error_msg="Failed to delete post!"):
                        st.rerun()

        post_class = get_post_render(post_data['file_type'])
        post = post_class(post_data)
        post.render()

        st.markdown("")


if st.session_state.user is None:
    login_page()
else:
    st.sidebar.title(f"👋 Hi {st.session_state.user['email']}!")

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.session_state.token = None
        st.rerun()

    st.sidebar.markdown("---")
    page = st.sidebar.radio("Navigate:", ["🏠 Feed", "📸 Upload"])

    pages = {
        "🏠 Feed": feed_page,
        "📸 Upload": upload_page
    }
    pages[page]()
