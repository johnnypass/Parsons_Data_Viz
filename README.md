ASSIGNMENT #3

Use an AI tool and everything you learned in the lecture to make a well-designed visualization of the weather in your favorite city. Post your visualization (static image) and write a short reflection on that experience of creating with AI. Will AI takeover? It doesn't need to be perfect, but see how far you can get to a decent visualization. Be sure to post the prompts used, tools, and document the process you went through to create it.

I got excited about trying a few different things to visualize data. I decided to start with Lida

    https://microsoft.github.io/lida/

I installed lida on my MacBook, got a key from OpenAI to access its AI tools for data analytics, and wrote two python scripts that use data from a Git repo of weather underground data, specifically the weather in Paris from 2016, to anayltlics and visualize the data.  

    https://github.com/leokassio/weather-underground-data

I wrote a summarization script (summarize_goals_weather.py) that accessed Open AI's llm, which provided me with two questions I may want to answer with the data set provided. The two prompts Open AI returned were:

Question
What is the distribution of Max Temperature in Paris in 2016?

visualization='Bar chart of Max_TemperatureC', rationale='By visualizing the distribution of maximum temperatures,          we can understand the range and frequency of high temperatures experienced in Paris throughout 2016. This can help          in identifying patterns and anomalies in temperature data.', index=0)

Question
How does the mean visibility vary in Paris in 2016?

visualization='Line chart of _Mean_VisibilityKm over time (CET)', rationale='Tracking the mean visibility over time         can provide insights into the atmospheric conditions in Paris throughout the year. This visualization can help in           understanding trends in visibility and potential correlations with other weather parameters.', index=1)

I used the prompts above in another script that generated visualizations as both bar and line charts (available in the attached repository). This process was interesting as a proof of concept. Lida can do a lot of things, including natural language-based visualization refinement, visualization explanations and accessibility, self-evaluation and repair of visualization code, and even recommending visualizations. I only scratched the surface of what it's capable of.





