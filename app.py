import gradio as gr
from logic import get_answer

def process_chat(pdf_file, user_message, chat_history):
    if not pdf_file:
        return "", chat_history, []
    
    # 1. Get the dictionary response from logic.py
   
    result = get_answer(pdf_file.name, user_message)
    
    # 2. Update Chat History
    chat_history.append({"role": "user", "content": user_message})
    chat_history.append({"role": "assistant", "content": result["text"]})
    
    # 3. Return: msg_clear, new_history, and the images for the Gallery
    return "", chat_history, result["images"]

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 📑 Advanced Multi-Modal Intelligence ")
    
    with gr.Row():
        with gr.Column(scale=1):
            file_input = gr.File(label="1. Upload Report ")
            gr.Markdown("---")
            
            summary_btn = gr.Button("📝 Generate Executive Summary", variant="secondary")
            clear = gr.ClearButton()

        with gr.Column(scale=3):
            with gr.Tabs():
                with gr.TabItem("💬 Analysis Chat"):
                    chatbot = gr.Chatbot(height=500, label="Grounded Assistant")
                    msg = gr.Textbox(placeholder="Ask about a trend, table, or chart...")
                
                with gr.TabItem("🖼️ Evidence Gallery"):
                    gr.Markdown("### Pages retrieved for the last answer:")
                    
                    gallery = gr.Gallery(label="Retrieved Pages", columns=2, height=450)

   
    msg.submit(process_chat, [file_input, msg, chatbot], [msg, chatbot, gallery])
    summary_btn.click(lambda: "Provide a detailed summary of the main findings and financial tables.", None, msg).then(
        process_chat, [file_input, msg, chatbot], [msg, chatbot, gallery]
    )

if __name__ == "__main__":
    demo.launch()
