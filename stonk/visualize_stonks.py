from html_table_extractor import HtmlTableExtractor
import dotenv
from openai import OpenAI
import os
import pandas as pd

# Create Function to Load the Markdown file
def load_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

# Send markdown as prompt to LLM
def ask_llm_to_generate_code(markdown_text, data):
    prompt = f"""
You are a data analyst. Based on the following Markdown instructions, generate Python code using pandas and matplotlib to produce the requested visualizations.

Markdown Instructions:
{markdown_text}

Return only the Python code.
"""
    response = client.responses.create(
        model="gpt-4o",
        instructions=prompt,
        input=data
    )
    return response.output_text

# Save the generated code to a file
def save_code(code, filename="generated_visualizations.py"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(code)

if __name__ == '__main__':

    # Load out .env with configuration
    dotenv.load_dotenv()

    # Configure your OpenAI API key
    data_url = os.getenv("DATA_URL")
    markdown_filepath = os.getenv("VISUALIZATION_INSTRUCTIONS")

    client = OpenAI(
        api_key=os.environ.get("OPEN_API_KEY"),
    )
    
    print("--- Creating instance of HtmlTableExtractor ---")
    # Initializing the class will automatically download, parse, and write CSV
    # skip_first_rows 1 ; table has extra header row
    extractor = HtmlTableExtractor(url=data_url,
                                   output_filename="data.csv",
                                   skip_first_rows=1,
                                   first_row_is_header=1)
    print("\n--- Process converting HTML table to CSV complete ---")

    print("--- Loading Markdown Instructions and Datta ---")
    markdown_text = load_file(markdown_filepath)
    data = load_file("data.csv")
    print("--- Generating Code using provided instructions, data, and LLM ---")
    generated_code = ask_llm_to_generate_code(markdown_text, data)
    print("--- Saving Generated Code ---")
    save_code(generated_code)
    print("✅ Visualization code saved to 'generated_visualizations.py'")
    