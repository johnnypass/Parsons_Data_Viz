from html_table_extractor import HtmlTableExtractor
import dotenv
from openai import OpenAI
import os
import pandas as pd
import subprocess

# Create Function to Load the Markdown file
def load_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

# Send markdown as prompt to LLM
def ask_llm_to_generate_code(markdown_text, data):
    prompt = f"""
You are a data analyst. Based on the following Markdown instructions, generate Python code using pandas, Seaborn, and matplotlib to produce the requested visualizations. Use matplotlib.pyplot.table to generate requested tables as images.

Markdown Instructions:
{markdown_text}

Return only the Python code.
"""
    response = client.responses.create(
        model="gpt-4o",
        instructions=prompt,
        input=data,
        temperature=0.2
    )
    return response.output_text

# Save the generated code to a file
def save_code(code, filename="generated_visualizations.py"):
    # Remove lines starting with ```
    cleaned_code = "\n".join(
        line for line in code.splitlines() if not line.strip().startswith("```")
    )
    with open(filename, "w", encoding="utf-8") as f:
        f.write(cleaned_code)

# get current working directory 
def get_current_working_directory():
    return os.getcwd()

# check is trusted env variable 
def is_trusted_to_execute():
    user_config_trust = trust_generated_code and trust_generated_code.strip().lower() == 'true'
    is_in_venv = "VIRTUAL_ENV" in os.environ
    return user_config_trust and is_in_venv

# Run python script as a subprocess
def run_generated_code(script_path, execution_directory):
    # Execute the generated python code using subprocess.run()
    # only run if configured to trust generated code, and running in a virtual env 
    if is_trusted_to_execute():
        # Run the code 
        try:
            # 'check=True' raises an exception if the process returns a non-zero exit code (indicating an error).
            subprocess.run(["python3", script_path], cwd=execution_directory, check=True)
            print(f"Script '{script_path}' executed successfully from '{execution_directory}'.")
        except subprocess.CalledProcessError as e:
            print(f"Error executing script: {e}")
        except FileNotFoundError:
            print(f"Error: Python interpreter or script not found. Make sure 'python' is in your PATH and '{script_path}' exists.")
    else:
        print("--- Prevented from executing generated code due to lack of virtual environment or lack of trust ---")
        print("See README.md for instructions on setting up trusted mode")
        print(f"To complete the run please manually run {script_path} from the directory {execution_directory}")

if __name__ == '__main__':

    # Load out .env with configuration
    dotenv.load_dotenv()

    # Configure your OpenAI API key
    data_url = os.getenv("DATA_URL")
    markdown_filepath = os.getenv("VISUALIZATION_INSTRUCTIONS")
    trust_generated_code = os.getenv("TRUST_GENERATED_CODE")
    data_csv_file = "data.csv"
    generated_code_file = "generated_visualizations.py"

    if not data_url or not markdown_filepath:
        raise ValueError("Missing DATA_URL or VISUALIZATION_INSTRUCTIONS in .env")

    client = OpenAI(
        api_key=os.environ.get("OPEN_API_KEY"),
    )
    
    print("--- Creating instance of HtmlTableExtractor ---")
    # Save costs and enable better responses by pre-converting HTML table to CSV file
    # This class takes an web page and parses the HTML table converting to a CSV file
    # Initializing the class will automatically download, parse, and write CSV
    # Create output directory if it doesn't exist
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # only generate ouput data file when needed, skip if already present
    output_data_file = os.path.join(output_dir, data_csv_file)
    if not os.path.exists(output_data_file) or os.path.getsize(output_data_file) == 0:
        # skip_first_rows 1 ; table has header row 
        extractor = HtmlTableExtractor(url=data_url,
                                   output_filename=os.path.join(output_dir, data_csv_file),
                                   skip_first_rows=1,
                                   first_row_is_header=True)
    print("\n--- Process converting HTML table to CSV complete ---")

    print("--- Loading Markdown Instructions and Data ---")
    # These are our instructions. Change the markdown don't change the code
    markdown_text = load_file(markdown_filepath)
    # Load the data
    data = load_file(os.path.join(output_dir, data_csv_file))
    print("--- Generating Code using provided instructions, data, and LLM ---")
    # Here is the fancy part ask the LLM
    generated_code = ask_llm_to_generate_code(markdown_text, data)
    print("--- Saving Generated Code ---")
    save_code(generated_code, os.path.join(output_dir, generated_code_file))
    print(f"✅ Visualization code saved to '{os.path.join(output_dir, generated_code_file)}'")

    # CWD + output + generated_visualizations.py
    script_path = os.path.join(
        get_current_working_directory(),
        output_dir, 
        generated_code_file)

    # CWD + output 
    execution_directory = os.path.join(
        get_current_working_directory(),
        output_dir)
    
    print("--- When TRUST_GENERATED_CODE Executing Generated Code ---")
    run_generated_code(script_path, execution_directory)