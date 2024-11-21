from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ChatMessageHistory
from prompt_config import SYSTEM_GUIDE, SYSTEM_ROLE
from runner_tools import (select_ml_service_node,
                          generate_tasks_node, hf_fetch_tool, hf_summary_tool,
                          github_summary_tool, arxiv_summary_tool, google_search_tool)
from langchain_openai import ChatOpenAI


llm = ChatOpenAI(model="gpt-4o-mini", max_tokens=8000, temperature=0.3)

CHAT_STORE = {}


def get_tools():
    tools = [
        select_ml_service_node, generate_tasks_node, hf_fetch_tool,
        google_search_tool, hf_summary_tool, github_summary_tool, arxiv_summary_tool
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
    max_iterations=10,
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


def get_res(prompt: str, save_dir: str, id_: str):
    res = chat(prompt, id_)
    if "### ArXiv Papers" in res:
        res = chat("To current summary add additional summary for arxiv links", id_)

    if "### Hugging Face" in res:
        res = chat("To current summary add additional summary"
                   " for each HuggingFace link and Usefull links on GitHub found in paper", id_)

    if "### Github Links" in res:
        res = chat("To current summary add additional summary for github repositories", id_)

    print("End of execution...")
    print(res)
    with open(save_dir, 'w') as res_b:
        res_b.write(res)
        print(f"Saved Research to {save_dir}")

