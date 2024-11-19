from typing import List

from langchain_core.tools import tool


@tool
def select_ml_service(arch: str):
    """
    Useful if you a get a service architecture of project description to extract ML service information
    """
    return (f"Extract only ML service and information about models and requirements"
            f" for them from provided service arch. Don't miss details: {arch}. ML_Service:")


@tool
def generate_tasks(ml_service_information: str):
    """Useful to convert ML_service to a list of tasks for comprehensive up-to date ML research"""
    return (f"Write a detailed and focused list of research tasks for implementing machine learning service."
            f" The tasks should be tailored to the described domain,"
            f" and aim to find the most up-to-date and effective solutions."
            f"Ml Service description: {ml_service_information}. Tasks:")


@tool
def parse_list(tasks: List[str]):
    """Useful to convert ML Research tasks to a python list and send them for a further analyse"""
    for task in tasks:
        print(task)
    return ("Tasks have been converted and sent to analyse. "
            "Next you will get each task and have to use processing tool for each")



def get_tools():
    tools = [
        select_ml_service, parse_list, generate_tasks
    ]
    return tools
