import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from lida import Manager, llm, TextGenerationConfig
import os
from dotenv import load_dotenv

# Assuming summary and goals are defined somewhere in your code
summary = "Paris 2016 weather data summary"
goals = ["Goal 1: Distribution of Max Temperature", "Goal 2: Mean Visibility over time"]# Assuming Manager, llm, and TextGenerationConfig are part of a library, import them
# from your_library import Manager, llm, TextGenerationConfig

# Mock definitions for Manager, llm, and TextGenerationConfig for demonstration purposes
# Mock definitions for Manager, llm, and TextGenerationConfig for demonstration purposes
class Manager:
    def __init__(self, text_gen):
        pass

    def summarize(self, url, summary_method, textgen_config):
        return "summary"

    def goals(self, summary, n, textgen_config):
        return [
            {
                "question": "What is the distribution of Max Temperature in Paris in 2016?",
                "visualization": "Bar chart of Max_TemperatureC",
                "rationale": "By visualizing the distribution of maximum temperatures, we can understand the range and frequency of high temperatures experienced in Paris throughout 2016. This can help in identifying patterns and anomalies in temperature data.",
                "index": 0
            },
            {
                "question": "How does the mean visibility vary in Paris in 2016?",
                "visualization": "Line chart of _Mean_VisibilityKm over time (CET)",
                "rationale": "Tracking the mean visibility over time can provide insights into the atmospheric conditions in Paris throughout the year. This visualization can help in understanding trends in visibility and potential correlations with other weather parameters.",
                "index": 1
            }
        ]

    def visualize(self, summary, goal, textgen_config, library):
        return [plt.figure()]

def llm(api_name):
    return "llm_instance"

class TextGenerationConfig:
    def __init__(self, n, temperature, model=None, use_cache=False):
        self.n = n
        self.temperature = temperature
        self.model = model
        self.use_cache = use_cache

# Load environment variables from openapi.env file
load_dotenv(dotenv_path='openapi.env')

# Ensure the API key is set in the environment
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

# Initialize the Manager
lida = Manager(text_gen=llm("openai"))

def create_bar_chart(data):
    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 6))
    sns.histplot(data=data, x='Max TemperatureC', bins=20, kde=True, color='skyblue', edgecolor='black')
    plt.axvline(data['Max TemperatureC'].mean(), color='red', linestyle='dashed', linewidth=1.5, label=f'Mean Max Temperature: {data["Max TemperatureC"].mean():.2f}')
    plt.legend()
    plt.xlabel('Max Temperature (°C)')
    plt.ylabel('Frequency')
    plt.title('What is the distribution of Max Temperature in Paris in 2016?', wrap=True)
    plt.show()

def create_line_chart(data):
    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=data, x='CET', y=' Mean VisibilityKm', color='blue')
    plt.xlabel('Date')
    plt.ylabel('Mean Visibility (Km)')
    plt.title('How does the mean visibility vary in Paris in 2016?', wrap=True)
    plt.show()

def main():
    textgen_config = TextGenerationConfig(n=1, temperature=0.5, model="gpt-3.5-turbo", use_cache=True)

    summary = lida.summarize("https://raw.githubusercontent.com/leokassio/weather-underground-data/refs/heads/master/paris-2016.csv", summary_method="default", textgen_config=textgen_config)  
    goals = lida.goals(summary, n=2, textgen_config=textgen_config)

    for goal in goals:
        print(goal)

    # Visualization code for the first goal
   # Visualization code for the first goal
i = 0
library = "seaborn"
textgen_config = TextGenerationConfig(n=1, temperature=0.2, use_cache=True)
charts = lida.visualize(summary=summary, goal=goals[i], textgen_config=textgen_config, library=library)  

# Check if charts are generated
if not charts:
    print("No charts were generated.")
else:
    # Display the first chart
    charts[0].show()

# Visualization code for the second goal
i = 1
charts = lida.visualize(summary=summary, goal=goals[i], textgen_config=textgen_config, library=library)  

# Check if charts are generated
if not charts:
    print("No charts were generated.")
else:
    # Display the first chart
    charts[0].show()

    # Load the data into a DataFrame
    data_url = "https://raw.githubusercontent.com/leokassio/weather-underground-data/refs/heads/master/paris-2016.csv"
    data = pd.read_csv(data_url)

# Create a bar chart of the distribution of Max Temperature in Paris in 2016
create_bar_chart(data)

# Visualization code for the second goal
i = 1
charts = lida.visualize(summary=summary, goal=goals[i], textgen_config=textgen_config, library=library)  

# Check if charts are generated
if not charts:
    print("No charts were generated.")
else:
    # Display the first chart
    charts[0].show()

# Create a line chart of Mean Visibility in Paris in 2016
create_line_chart(data)

# Keep the plots open
plt.show()

if __name__ == "__main__":
    main()
