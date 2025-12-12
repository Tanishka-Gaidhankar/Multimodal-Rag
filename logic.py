import os
import io
import base64
import time
from groq import Groq
from pdf2image import convert_from_path
from dotenv import load_dotenv

load_dotenv()
# Use your key from .env or hardcode it here for a final test
client = Groq(api_key=os.getenv("GROQ_API_KEY"), timeout=30.0)

def get_answer(pdf_path, query):
    try:
        # 1. Convert PDF to Image (Ensures Poppler is working)
        # We only take the first page to keep the request size small (<4MB)
        pages = convert_from_path(pdf_path, first_page=1, last_page=1)
        if not pages:
            return "Error: Could not extract pages from PDF."
        
        # 2. Encode Image to Base64 (Fixes the NameError)
        buffered = io.BytesIO()
        pages[0].save(buffered, format="PNG")
        base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

        # 3. Call Groq with ONLY 'user' role to prevent API hangs
        # model="llama-3.2-11b-vision-preview" 
        completion = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"Context: Document Page 1. Question: {query}"},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{base64_image}"}
                        }
                    ]
                }
            ],
            max_tokens=1000
        )
        
        return completion.choices[0].message.content

    except Exception as e:
        return f"Request Error: {str(e)}"