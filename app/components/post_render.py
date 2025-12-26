import streamlit as st
from app.services.imagekit_service import create_transformed_url

class Post:
    def __init__(self, post_data):
        self.data = post_data

    def render(self):
        pass

class ImagePost(Post):
    def render(self):
        caption = self.data.get('caption', '')
        uniform_url = create_transformed_url(self.data['url'], "", caption)
        st.image(uniform_url, width=300)

class VideoPost(Post):
    def render(self):
        uniform_video_url = create_transformed_url(self.data['url'], "w-400,h-200,cm-pad_resize,bg-blurred")
        st.video(uniform_video_url)
        st.caption(self.data.get('caption', ''))

def get_post_render(file_type):
    renderers = {
        'image': ImagePost,
        'video': VideoPost
    }
    return renderers.get(file_type, Post)
