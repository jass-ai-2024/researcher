from typing import List

from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ChatMessageHistory
from prompt_config import SYSTEM_GUIDE, SYSTEM_ROLE, test_prompt
from runner_tools import github_fetch_tool, select_ml_service_node, generate_tasks_node, hf_fetch_tool, arxic_fetch_tool
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool


llm = ChatOpenAI(model="gpt-4o-mini", max_tokens=4000, temperature=0.5)

CHAT_STORE = {}

TASKS = None


@tool
def parse_list_tool(tasks: List[str]):
    """Useful to convert ML Research tasks to a python list and send them for a further analyse"""
    global TASKS
    max_len = len(tasks)
    TASKS = tasks[:min(max_len, 3)]
    return "tasks were sucessfuly converted to python list"


def get_tools():
    tools = [
        parse_list_tool,github_fetch_tool, select_ml_service_node, generate_tasks_node, hf_fetch_tool, arxic_fetch_tool
    ]
    return tools


def get_chat_history(session_id: str):
    if session_id not in CHAT_STORE:
        CHAT_STORE[session_id] = ChatMessageHistory()
    return CHAT_STORE[session_id]


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_ROLE),
        ("system", SYSTEM_GUIDE),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

agent_executor = AgentExecutor(
    agent=create_tool_calling_agent(llm, get_tools(), prompt),
    tools=get_tools(),
    verbose=True,
    max_iterations=3,
    early_stopping_method="force"
)

chain_with_history = RunnableWithMessageHistory(
    agent_executor,
    get_chat_history,
    input_messages_key="input",
    history_messages_key="chat_history"
)


def chat(input, session_id):
    res = chain_with_history.invoke({"input": input},
                                    config={"configurable": {"session_id": session_id}})['output']
    return res


if __name__ == "__main__":
    # Some DeepTech solutions :D
    session_id = "demo_user"

    res = chat(test_prompt, session_id)
    print(len(TASKS))
    print(TASKS)
    if TASKS is None:
        print(res)
        # TODO return
    else:
        for task in TASKS:
            chat(f"Get useful data for this specific task only if needed: {task}", session_id)

    result_hf = chat(f"Sort tasks and results and provide top-5 most relevant for arxiv, repos, models, datasets and so on",
                     session_id)
    print(result_hf)
