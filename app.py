import gradio as gr
from logic import get_answer

def process_and_chat(pdf_file, user_message, chat_history):
    if pdf_file is None:
        chat_history.append({"role": "user", "content": user_message})
        chat_history.append({"role": "assistant", "content": "Please upload a PDF first."})
        return "", chat_history
    
    chat_history.append({"role": "user", "content": user_message})
    
    # Process multi-modal RAG via Groq
    bot_response = get_answer(pdf_file.name, user_message)
    
    chat_history.append({"role": "assistant", "content": bot_response})
    return "", chat_history

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("## ⚡ Fast Multi-Modal RAG (Groq + Llama 3.2 Vision)")
    
    with gr.Row():
        file_input = gr.File(label="Upload Financial/Policy PDF", file_types=[".pdf"])
        chatbot = gr.Chatbot(label="Analysis Chat", height=500)
    
    msg = gr.Textbox(label="Question", placeholder="Ask about the charts, tables, or text...")
    msg.submit(process_and_chat, [file_input, msg, chatbot], [msg, chatbot])

if __name__ == "__main__":
    demo.launch()