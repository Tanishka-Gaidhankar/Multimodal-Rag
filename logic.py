import os
import io
import base64
import numpy as np
from groq import Groq
from pdf2image import convert_from_path
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"), timeout=60.0)
embed_model = SentenceTransformer('all-MiniLM-L6-v2') 


current_pdf_path = None
page_embeddings = None

def build_vector_index(pdf_path):
    """Semantic Indexing: Turning 78 pages into a searchable vector space."""
    global current_pdf_path, page_embeddings
    if pdf_path == current_pdf_path:
        return
    
    reader = PdfReader(pdf_path)
    page_texts = [page.extract_text() or "" for page in reader.pages]
    

    page_embeddings = embed_model.encode(page_texts)
    current_pdf_path = pdf_path

def get_answer(pdf_path, query):
    try:
        # 1. Index the full document
        build_vector_index(pdf_path)
        
        # 2. Semantic Retrieval: Find the top 2 relevant pages
        query_vec = embed_model.encode([query])
        similarities = np.dot(page_embeddings, query_vec.T).flatten()
        top_indices = np.argsort(similarities)[-2:][::-1]
        
        # 3. Multimodal Analysis & Visual Evidence Collection
        
        retrieved_images = []
        content_list = [{"type": "text", "text": f"Analyze these pages to answer: {query}"}]
       
        temp_dir = "D:/MultiModalProject/temp_evidence"
        os.makedirs(temp_dir, exist_ok=True)

        for idx in top_indices:
            page_num = int(idx) + 1
            images = convert_from_path(pdf_path, first_page=page_num, last_page=page_num)
            
            if images:
               
                img_path = os.path.join(temp_dir, f"evidence_page_{page_num}.png")
                images[0].save(img_path, "PNG")
                retrieved_images.append(img_path)
                
             
                buffered = io.BytesIO()
                images[0].save(buffered, format="PNG")
                base64_img = base64.b64encode(buffered.getvalue()).decode('utf-8')
                content_list.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{base64_img}"}
                })

        # 4. Generate grounded response with Llama 4
        completion = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[{"role": "user", "content": content_list}]
        )
        
       
        return {
            "text": f"**Sources: Pages {[i+1 for i in top_indices]}**\n\n" + completion.choices[0].message.content,
            "images": retrieved_images
        }

    except Exception as e:
        return {"text": f"System Error: {str(e)}", "images": []}
    

   
