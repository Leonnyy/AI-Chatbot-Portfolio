
    fn=pergjigje_chat,
    inputs="text",
    outputs="text",
    title="Chatbot AI për Portofol (Demo)",
    description="Shkruaj çdo pyetje dhe AI do të përgjigjet! Kliko pyetjet shembull për testim të shpejtë.",
    examples=[[q] for q in pyetje_shembull],
    live=True
)

# Start interfaca
iface.launch(share=True)"""
🤖 Chatbot AI — Gradio 6.0 + OpenAI v1
"""

import os
import gradio as gr
import speech_recognition as sr
from openai import OpenAI

# OpenAI Client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = {
    "role": "system",
    "content": "Ti je një asistent inteligjent dhe miqësor që flet shqip. Përgjigju qartë dhe shkurt.",
}


def pergjigje_chat(mesazhi, histori):
    """Histori është listë dict-esh: [{'role': 'user'/'assistant', 'content': '...'}]"""
    if not mesazhi or not mesazhi.strip():
        return histori, ""

    if histori is None:
        histori = []

   
    messages = [SYSTEM_PROMPT] + list(histori) + [{"role": "user", "content": mesazhi}]

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=600,
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"❌ Gabim: {str(e)}"

    
    histori = histori + [
        {"role": "user", "content": mesazhi},
        {"role": "assistant", "content": reply},
    ]

    return histori, ""


def voice_to_text(audio):
    if audio is None:
        return ""
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio) as source:
            data = recognizer.record(source)
            try:
                return recognizer.recognize_google(data, language="sq-AL")
            except sr.UnknownValueError:
                return recognizer.recognize_google(data, language="en-US")
    except sr.UnknownValueError:
        return "🤔 Nuk e kuptova audion."
    except sr.RequestError as e:
        return f"❌ Gabim shërbimi: {e}"
    except Exception as e:
        return f"❌ Gabim: {e}"


def pastro():
    return [], ""



custom_css = """
.gradio-container {
    max-width: 900px !important;
    margin: 0 auto !important;
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
    min-height: 100vh;
    font-family: 'Segoe UI', system-ui, sans-serif !important;
}
body, .dark { background: #0f172a !important; }

#header {
    text-align: center;
    padding: 24px 0 8px 0;
    border-bottom: 1px solid rgba(148, 163, 184, 0.15);
    margin-bottom: 16px;
}
#header h1 { color: #f1f5f9 !important; font-size: 28px !important; font-weight: 700 !important; margin: 0 !important; }
#header p { color: #94a3b8 !important; font-size: 14px !important; margin: 6px 0 0 0 !important; }

#chatbox {
    background: #1e293b !important;
    border: 1px solid rgba(148, 163, 184, 0.15) !important;
    border-radius: 16px !important;
}

#input-box textarea {
    background: #1e293b !important;
    color: #f1f5f9 !important;
    border: 1px solid rgba(148, 163, 184, 0.25) !important;
    border-radius: 12px !important;
    padding: 14px 16px !important;
    font-size: 15px !important;
}
#input-box textarea:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15) !important;
}

#send-btn {
    background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
}

#clear-btn {
    background: transparent !important;
    color: #94a3b8 !important;
    border: 1px solid rgba(148, 163, 184, 0.25) !important;
    border-radius: 10px !important;
}

#audio-input {
    background: #1e293b !important;
    border: 1px dashed rgba(148, 163, 184, 0.3) !important;
    border-radius: 12px !important;
}

label, .label-wrap span { color: #cbd5e1 !important; font-weight: 500 !important; }
footer { display: none !important; }
"""


# UI
with gr.Blocks(title="🤖 Chatbot AI") as demo:

    gr.HTML("""
        <div id="header">
            <h1>🤖 Chatbot AI</h1>
            <p>Asistenti yt inteligjent — bisedo me tekst ose me zë 🎤</p>
        </div>
    """)

   
    state = gr.State([])

    chatbot = gr.Chatbot(
        elem_id="chatbox",
        height=520,
        show_label=False,
    )

    with gr.Row():
        txt = gr.Textbox(
            placeholder="💬 Shkruaj mesazh...",
            scale=5,
            show_label=False,
            elem_id="input-box",
            lines=1,
            max_lines=4,
        )
        btn = gr.Button("Dërgo 🚀", scale=1, elem_id="send-btn")

    with gr.Accordion("🎤 Bisedo me zë", open=False):
        audio = gr.Audio(
            sources=["microphone", "upload"],
            type="filepath",
            label="Regjistro ose ngarko audio",
            elem_id="audio-input",
        )

    clear = gr.Button("🧹 Pastro bisedën", elem_id="clear-btn")

 
    def chat_handler(mesazhi, histori_state):
        histori_e_re, txt_bosh = pergjigje_chat(mesazhi, histori_state)
        return histori_e_re, histori_e_re, txt_bosh

    def clear_handler():
        return [], [], ""

 
    btn.click(chat_handler, [txt, state], [state, chatbot, txt])
    txt.submit(chat_handler, [txt, state], [state, chatbot, txt])
    audio.change(voice_to_text, audio, txt)
    clear.click(clear_handler, None, [state, chatbot, txt])


if __name__ == "__main__":
    demo.launch(
        share=True,
        css=custom_css,
        theme=gr.themes.Base(primary_hue="blue", neutral_hue="slate"),
    )
