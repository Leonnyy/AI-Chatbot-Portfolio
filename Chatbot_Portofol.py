# chatbot_portofol.py
import gradio as gr

# API key vendoset në kompjuterin tënd si environment variable për siguri
# import openai
# openai.api_key = os.getenv("OPENAI_API_KEY")

def chat_response(message):
    """
    Funksion demo për Chatbot për portofol.
    Përdor përgjigje të përgatitura për screenshot/demo.
    """
    demo_answers = {
        "Cili është kryeqyteti i Francës?": "Parisi",
        "Shpjego Teoremën e Pitagorës.": "Në një trekëndësh kënddrejtë, kuadrat i hipotenusës është i barabartë me shumën e katrorëve të kateteve.",
        "Jep një këshillë për organizimin e kohës.": "Bëj një listë prioritetesh dhe ndaje kohën në blloqe për secilën detyrë.",
        "Si funksionon inteligjenca artificiale?": "AI përdor modele të mësimit të makinerive për të njohur modele dhe për të bërë parashikime ose përgjigje."
    }
    
    if not message.strip():
        return "Shkruaj diçka për të marrë përgjigje 😄"
    
    # Kthe përgjigjen demo nëse pyetja ekziston
    return demo_answers.get(message, "Ky është një demo, nuk ka përgjigje të gjallë për këtë pyetje.")

# Pyetje shembull për screenshot
example_questions = [
    "Cili është kryeqyteti i Francës?",
    "Shpjego Teoremën e Pitagorës.",
    "Jep një këshillë për organizimin e kohës.",
    "Si funksionon inteligjenca artificiale?"
]

# Krijimi i ndërfaqes me Gradio
iface = gr.Interface(
    fn=chat_response,
    inputs="text",
    outputs="text",
    title="Chatbot AI për Portofol",
    description="Shkruaj çdo pyetje dhe AI do të përgjigjet! Kliko pyetjet shembull për testim të shpejtë.",
    examples=[[q] for q in example_questions]
)

# Launch me link publik për demo
iface.launch(share=True)