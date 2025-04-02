from google import genai
API_KEY = "AIzaSyCNryy6AbgxWdABJy3e3gdkqECYUdWK4wU"
MODEL = "gemini-2.0-flash"


def query_genai(query):
    client = genai.Client(api_key=API_KEY)
    response = client.models.generate_content(
    model=MODEL, contents=query)
    return response.text