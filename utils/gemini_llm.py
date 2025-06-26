import google.generativeai as genai

def init_gemini(api_key):
    genai.configure(api_key=api_key)
    # Use the fast/free Gemini model
    return genai.GenerativeModel("gemini-1.5-flash")

def generate_summary(text, model):
    prompt = f"""
You are a digital medical assistant.

Based on the following report, summarize the key findings.
Also highlight any signs of diabetes or breast cancer if present.

{text}
"""
    response = model.generate_content(prompt)
    return response.text
