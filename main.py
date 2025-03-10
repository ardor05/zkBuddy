import streamlit as st
import google.generativeai as genai
from ultralytics import YOLO
from PIL import Image
import numpy as np
import zkBuddy #Import the Rust module (compiled via maturin)
 
# Set up Gemini API key
GEMINI_API_KEY = "AIzaSyDC3vNc79FsrEycm2S1_rmdJgD2U7cZpgM"
genai.configure(api_key=GEMINI_API_KEY)

# Load Gemini model
model_gemini = genai.GenerativeModel("gemini-1.5-flash")

# Load YOLO emotion detection model
model_emotion = YOLO("best.pt")

# Streamlit UI
st.title("🤖 zkBuddy: AI Chatbot with Emotion Recognition & ZK Proofs")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_emotion" not in st.session_state:
    st.session_state.user_emotion = None  # Stores detected emotion

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Emotion detection function
def predict_emotion(image):
    results = model_emotion(image)
    emotions = []
    for result in results:
        for pred in result.boxes:
            conf = pred.conf.item()
            class_name = model_emotion.names[int(pred.cls)]
            emotions.append(f"Emotion: {class_name}, Confidence: {conf:.2f}")
    
    if emotions:
        detected_emotion = model_emotion.names[int(results[0].boxes[0].cls)]
        st.session_state.user_emotion = detected_emotion  # Store emotion in session
    else:
        st.session_state.user_emotion = None  # Reset emotion if none detected

    return emotions if emotions else ["No emotions detected."]

# Chatbot function with emotion-based response and zkML proof integration
def chatbot(prompt):
    user_emotion = st.session_state.user_emotion  # Get the last detected emotion

    if user_emotion:
        prompt = f"[User seems {user_emotion}]: " + prompt

    response = model_gemini.generate_content(prompt)
    response_text = response.text

    try:
        zk_proof_result = zkBuddy.run_zkbuddy()  # Now using the updated module name
        print("[zk Proof]:", zk_proof_result)
    except Exception as e:
        print("[zk Proof Error]:", e)

    return response_text

# Image Upload Section for Emotion Recognition
st.sidebar.header("📷 Upload an Image for Emotion Detection")
uploaded_file = st.sidebar.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.sidebar.image(image, caption="Uploaded Image", use_container_width=True)
    
    img_array = np.array(image)
    
    with st.sidebar:
        if st.button("Detect Emotion"):
            emotions = predict_emotion(img_array)
            st.write("### Detected Emotions:")
            for emotion in emotions:
                st.write(emotion)

# User Input for Chatbot
user_input = st.chat_input("Type a message...")

if user_input:
    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    bot_response = chatbot(user_input)

    with st.chat_message("assistant"):
        st.markdown(bot_response)
    
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
