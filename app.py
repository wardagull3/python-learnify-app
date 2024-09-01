import streamlit as st
from transformers import pipeline
from gtts import gTTS
from moviepy.editor import VideoFileClip
import os

# Access Hugging Face token from Streamlit secrets
HF_TOKEN = st.secrets["huggingface"]["token"]

# Directory where videos are stored
VIDEO_DIR = 'videos/'

# Load the text generation model
generator = pipeline('text-generation', model='distilgpt2', use_auth_token=HF_TOKEN)

# Function to generate text
def generate_text(prompt):
    response = generator(prompt, max_length=150, num_return_sequences=1)
    return response[0]['generated_text']

# Function to convert text to speech
def text_to_speech(text, filename='output_audio.mp3'):
    tts = gTTS(text)
    tts.save(filename)
    return filename

# Function to display video
def play_video(video_file):
    if os.path.exists(video_file):
        st.video(video_file)
    else:
        st.error("❌ Video file does not exist.")

# Function to map topics to videos
def get_video_for_topic(topic):
    video_mapping = {
        'variables': 'variables.mp4',
        'loop': 'loop.mp4',
        'print': 'print.mp4',
        'if-else': 'if-else.mp4',
        'break-continue': 'break-continue.mp4',
    }
    topic = topic.lower()
    for key in video_mapping.keys():
        if key in topic:
            return os.path.join(VIDEO_DIR, video_mapping[key])
    return None

# Main function to handle user input and generate content
def generate_educational_content(prompt):
    video_file = get_video_for_topic(prompt)
    if video_file:
        play_video(video_file)
    else:
        st.error("😔 Sorry, this topic is not available here. The platform is for Python beginners. "
                 "Please ask about beginner-friendly topics like `print`, `if-else`, `loops`, `variables`, "
                 "`break`, and `continue` statements.")
        
# Streamlit UI
st.set_page_config(page_title="Python Learnify", page_icon="🐍", layout="centered")
st.markdown(
    """
    <style>
        .main {
            background-color: #f0f2f6;
        }
        .reportview-container {
            background: #f0f2f6;
        }
        .stButton > button {
            background-color: #4CAF50; 
            color: white;
            border: none;
            border-radius: 12px;
            padding: 10px 24px;
            font-size: 16px;
            margin: 5px 2px;
            cursor: pointer;
        }
        .stButton > button:hover {
            background-color: #45a049;
        }
    </style>
    """, 
    unsafe_allow_html=True
)

# Header section
st.title("Python Learnify 🐍📚")
st.subheader("🔍 Discover Python Concepts Visually with Ease!")
st.write("**Ask a question or specify a topic to learn about Python:** 🎓")
st.write("This platform is dedicated to Python beginners. Feel free to explore basic topics like **variables, loops, conditional statements, and more**!")

# User input
user_input = st.text_input("📝 **Enter your question or topic:**")

# Generate button
if st.button("🚀 Generate"):
    if user_input:
        generate_educational_content(user_input)
    else:
        st.warning("⚠️ Please enter a topic or question.")
        
# Footer section
st.markdown("---")
st.markdown("**Created with ❤️ for Python Learners**")
