from dotenv import load_dotenv
import os
from lida import Manager, llm, TextGenerationConfig  # Replace 'lida_lib' with the actual module name

# Load environment variables from the .env file
load_dotenv('PATH/TO/FILE')

# Get the API key from the environment variables
api_key = os.getenv('API_KEY')

# Initialize the Manager with the API key
lida = Manager(text_gen=llm("openai", api_key=api_key))  # Use the API key from the .env file
textgen_config = TextGenerationConfig(n=1, temperature=0.5, model="gpt-3.5-turbo", use_cache=True)

summary = lida.summarize("https://raw.githubusercontent.com/leokassio/weather-underground-data/refs/heads/master/paris-2016.csv", summary_method="default", textgen_config=textgen_config)
goals = lida.goals(summary, n=2, textgen_config=textgen_config)

for goal in goals:
    print(goal)
