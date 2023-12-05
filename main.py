from dotenv import load_dotenv
import os
import requests
import json


# Load environment variables from .env file
load_dotenv()


OpenAIKey = os.getenv("OPENAI_KEY")
OpenWeatherAPI = os.getenv("OPENWEATHER")

# Make the HTTP request to the OpenWeatherMap API
response = requests.get("http://api.openweathermap.org/data/2.5/weather?q=Dublin,ie&appid="+OpenWeatherAPI)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response
    data = json.loads(response.text)

    # Extract the weather information
    weather_data = data.get('weather')

    if weather_data and isinstance(weather_data, list) and len(weather_data) > 0:
        weather = weather_data[0].get('description')
        temperature = data.get('main', {}).get('temp')
        humidity = data.get('main', {}).get('humidity')

        # Print the weather information
        print("Weather in Dublin, Ireland:")
        print("Description:", weather)
        print("Temperature:", temperature, "K")
        print("Humidity:", humidity, "%")
    else:
        print("No weather data available.")
else:
    print(f"Error: {response.status_code}")


if OpenAIKey is None:
    raise ValueError("OPENAI_KEY environment variable is not set.")

import autogen
config_list = [
    {
        'model': 'gpt-3.5-turbo',
        'api_key': OpenAIKey
    }
]
llm_config={
    "request_timeout": 600,
    "seed": 42,
    "config_list": config_list,
    "temperature": 0,
}
# create an AssistantAgent instance named "assistant"
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config=llm_config
)
# create a UserProxyAgent instance named "user_proxy"
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="Always",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "web"},
    llm_config=llm_config,
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
Otherwise, reply CONTINUE, or the reason why the task is not solved yet."""
)
# the assistant receives a message from the user, which contains the task description
user_proxy.initiate_chat(
    assistant,
    message="""
What is the weather in Dublin, Ireland today? 
""",
)