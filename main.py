from api.openrouter import OpenRouterClient
from reader.OpenPDF import process_pdf
from dotenv import load_dotenv
import os


def main():
    load_dotenv()
    ENV_KEY = os.environ.get("OPENROUTER_API_KEY")
    print("[DEBUG] dotenv loaded :D")  #############
    client = OpenRouterClient(
        base_url="https://openrouter.ai/api/v1", api_key=ENV_KEY
    )  # Initialize OpenRouterClient with the base URL and API key
    print("[DEBUG] OpenRouterClient instantiated :)")  #############

    file_path = "./pdf/D&D 5E - Tasha's Cauldron of Everything - Caldeirão de Tasha para Tudo - Biblioteca do Duque.pdf"
    content = process_pdf(file_path, client)
    print(content)  # Print the response from the PDF processing


if __name__ == "__main__":
    main()
