# chatbot_portofol_demo.py
import gradio as gr

# Përgjigjet demo për portofol
demo_pergjigje = {
    "Cili është kryeqyteti i Francës?": "Parisi",
    "Shpjego Teoremën e Pitagorës.": "Në një trekëndësh kënddrejtë, kuadrati i hipotenusës është i barabartë me shumën e katrorëve të kateteve.",
    "Jep një këshillë për organizimin e kohës.": "Bëj një listë prioritetesh dhe ndaje kohën në blloqe për secilën detyrë.",
    "Si funksionon inteligjenca artificiale?": "AI përdor modele të mësimit të makinerive për të njohur modele dhe për të dhënë përgjigje ose parashikime."
}

def pergjigje_chat(teksti):
    """
    Funksion demo për chatbot portofoli.
    Merr pyetjen si string, edhe nëse vjen nga button example.
    """
    # Kontrollo nëse vjen si listë (nga Gradio example)
    if isinstance(teksti, list):
        teksti = teksti[0]

    if not teksti.strip():
        return "Shkruaj diçka për të marrë përgjigje 😄"
    
    return demo_pergjigje.get(teksti, "Ky është një demo, nuk ka përgjigje të gjallë për këtë pyetje.")

# Pyetje shembull për butona
pyetje_shembull = [
    "Cili është kryeqyteti i Francës?",
    "Shpjego Teoremën e Pitagorës.",
    "Jep një këshillë për organizimin e kohës.",
    "Si funksionon inteligjenca artificiale?"
]

# Krijimi i ndërfaqes me Gradio
iface = gr.Interface(
    fn=pergjigje_chat,
    inputs="text",
    outputs="text",
    title="Chatbot AI për Portofol (Demo)",
    description="Shkruaj çdo pyetje dhe AI do të përgjigjet! Kliko pyetjet shembull për testim të shpejtë.",
    examples=[[q] for q in pyetje_shembull],  # butonat e pyetjeve shembull
    live=True
)

# Start interfaca
iface.launch(share=True)
