import streamlit as st
from utils.pdf_processor import ingest_pdf, retrieve_context
from utils.redis_client import RedisClient
import os
import uuid
import google.generativeai as genai

def generate_answer(context, prompt):
    """Generate an answer using Gemini API."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY not set."
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    try:
        response = model.generate_content(f"Context: {context}\nQuestion: {prompt}\nAnswer concisely:")
        return response.text
    except Exception as e:
        return f"Error generating answer: {str(e)}"

st.title("Multi-User PDF Q&A")
st.write("Upload your PDF")

redis_client = RedisClient(host=os.getenv("REDIS_HOST", "redis-service"), port=int(os.getenv("REDIS_PORT", 6379)))
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())
user_id = st.session_state.user_id

uploaded_file = st.file_uploader("Upload your PDF", type="pdf")
if uploaded_file:
    with st.spinner("Processing PDF..."):
        ingest_pdf(uploaded_file, user_id, redis_client)
    st.success("PDF uploaded and processed successfully.")

st.write("Chat with your PDF")
prompt = st.chat_input("Ask a question about the PDF")
if prompt:
    with st.spinner("Generating response..."):
        context = retrieve_context(user_id, prompt, redis_client)
        response = generate_answer(context, prompt)
        redis_client.append_to_list(f"history:{user_id}", {"question": prompt, "answer": response})
        st.chat_message("user").write(prompt)
        st.chat_message("assistant").write(response)

# Display chat history, excluding the latest message if just added
chat_history = redis_client.get_list(f"history:{user_id}")
if prompt:
    # Skip the last message since it was just displayed
    chat_history = chat_history[:-1]
for message in chat_history:
    if "question" in message:
        st.chat_message("user").write(message["question"])
    if "answer" in message:
        st.chat_message("assistant").write(message["answer"])