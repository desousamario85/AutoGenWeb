from dotenv import load_dotenv
import os
import requests
import json


# Load environment variables from .env file
load_dotenv()


OpenAIKey = os.getenv("OPENAI_KEY")
OpenWeatherAPI = os.getenv("OPENWEATHER")

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
What is the weather in Dublin, Ireland today? this is my API Key: b3bfefde9a3b6606d2ce230660e6d09c
""",
)

# Check if the user is asking about the weather
if "weather" in user_input.lower():
    # Add the OpenWeatherAPI variable to the user's message
    user_input += f"\nOpenWeatherAPI: {OpenWeatherAPI}"

# The assistant receives a message from the user, which contains the task description
user_proxy.initiate_chat(assistant, message=user_input)