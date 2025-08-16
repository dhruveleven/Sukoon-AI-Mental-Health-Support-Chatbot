import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def get_gemini_response(prompt):
    """Gets a response from the Gemini API."""
    try:
        model = genai.GenerativeModel('gemini-2.5-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error getting Gemini response: {e}")
        return "Sorry, I encountered an error. Please try again later."

if __name__ == "__main__":
    #Example usage.
    example_prompt = "Explain the importance of mindfulness in daily life."
    response = get_gemini_response(example_prompt)
    print(response)