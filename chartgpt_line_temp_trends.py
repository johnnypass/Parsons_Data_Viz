import pandas as pd
import matplotlib.pyplot as plt

# Load data
url = "https://raw.githubusercontent.com/leokassio/weather-underground-data/refs/heads/master/paris-2016.csv"
data = pd.read_csv(url)

# Convert date to datetime and set as index
data['CET'] = pd.to_datetime(data['CET'])
data.set_index('CET', inplace=True)

# Plot max, mean, min temperatures
plt.figure(figsize=(12, 6))
plt.plot(data.index, data['Max TemperatureC'], label='Max Temp (°C)', color='red')
plt.plot(data.index, data['Mean TemperatureC'], label='Mean Temp (°C)', color='orange')
plt.plot(data.index, data['Min TemperatureC'], label='Min Temp (°C)', color='blue')
plt.title('Temperature Trends in Paris (2016)')
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.legend()
plt.grid(True)
plt.show()
