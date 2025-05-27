import os
import google.generativeai as genai

# Configure with a placeholder API key
genai.configure(api_key=os.getenv('GEMINI_API_KEY', 'your-real-key'))

def query_gemini(prompt, context):
    try:
        response = genai.generate_content(
            f"Context: {context}\n\nQuestion: {prompt}\n\nAnswer:"
        )
        return response.text
    except Exception as e:
        return f"Error querying Gemini API: {str(e)}"