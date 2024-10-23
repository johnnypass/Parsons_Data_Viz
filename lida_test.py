import os
from dotenv import load_dotenv
import lida
from lida import Manager, TextGenerationConfig, llm 
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# Load environment variables from openapi.env file
load_dotenv(dotenv_path='openapi.env')

# Ensure the API key is set in the environment
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

# Initialize the Manager
lida = Manager(text_gen=llm("openai"))

def main():
    textgen_config = TextGenerationConfig(n=1, temperature=0.5, model="gpt-3.5-turbo", use_cache=True)

    summary = lida.summarize("https://raw.githubusercontent.com/LearnDataSci/articles/refs/heads/master/Python%20Pandas%20Tutorial%20A%20Complete%20Introduction%20for%20Beginners/IMDB-Movie-Data.csv", summary_method="default", textgen_config=textgen_config)  
    goals = lida.goals(summary, n=2, textgen_config=textgen_config)

    for goal in goals:
        print(goal)

    # Visualization code
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

    # Load the data into a DataFrame
    data_url = "https://raw.githubusercontent.com/LearnDataSci/articles/refs/heads/master/Python%20Pandas%20Tutorial%20A%20Complete%20Introduction%20for%20Beginners/IMDB-Movie-Data.csv"
    data = pd.read_csv(data_url)

    # Create a bar chart of the distribution of movie ratings
    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 6))
    sns.histplot(data=data, x='Rating', bins=20, kde=True, color='skyblue', edgecolor='black')
    plt.axvline(data['Rating'].mean(), color='red', linestyle='dashed', linewidth=1.5, label=f'Mean Rating: {data["Rating"].mean():.2f}')
    plt.legend()
    plt.xlabel('Rating')
    plt.ylabel('Frequency')
    plt.title('How does the distribution of movie ratings look like?', wrap=True)

    # Show the plot
    plt.show()

if __name__ == "__main__":
    main()