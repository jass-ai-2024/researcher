from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ChatMessageHistory
from prompt_config import SYSTEM_GUIDE, SYSTEM_ROLE, test_prompt
from tools import get_tools
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", max_tokens=4000, temperature=0.5)

CHAT_STORE = {}

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
    print("Welcome")

    print("Bot:", chat(test_prompt, session_id))
    exit()

