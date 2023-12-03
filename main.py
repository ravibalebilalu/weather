import python_weather
from logger import logging
import asyncio
import os
from tabulate import tabulate

def print_centered_output(output):
    terminal_width = os.get_terminal_size().columns
    wrapped_output = textwrap.fill(output, width=terminal_width)
    centered_lines = [line.center(terminal_width) for line in wrapped_output.split('\n')]
    centered_output = '\n'.join(centered_lines)
    print(centered_output)

logging.info("Script started")

async def get_weather():
    async with python_weather.Client(unit=python_weather.METRIC) as client:
        location = input("Enter your location :" )
        weather = await client.get(location)
        logging.info("Weather details fetched ")

        # Create a list to hold the weather data
        table_data = []
        # Add the current temperature to the table
        table_data.append(["Current Temperature in "+ location +":  " + str(weather.current.temperature) + "°C"])

        # Add forecast data to the table
        for forecast in weather.forecasts:
            max_temp = forecast.highest_temperature
            min_temp = forecast.lowest_temperature
            description = "Not available"
            for hourly in forecast.hourly:
                if hasattr(hourly, 'description'):
                    description = hourly.description
                    break
            table_data.append([forecast.date, f"{min_temp}°C - {max_temp}°C", description])  # Include 'lowest_temperature' and 'highest_temperature'

        return table_data

if __name__ == '__main__':
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        loop = asyncio.get_event_loop()
        weather_data = loop.run_until_complete(get_weather())
        # Display weather data in tabular format
        print(tabulate(weather_data, headers=["Date", "Temperature Range", "Weather Description"]))
        logging.info("script ran successfully")
    except Exception as e:
        print("Some error occurred. Please try again!")
        logging.error(f"Error occurred: {e}")