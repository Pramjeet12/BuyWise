import os

from dotenv import load_dotenv
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_groq import ChatGroq

from ShopGenie.data_ingestion import data_ingestion

# Handle LangChain import path differences across versions.
try:
    from langchain_classic.chains import create_history_aware_retriever, create_retrieval_chain
    from langchain_classic.chains.combine_documents import create_stuff_documents_chain
except ImportError:
    from langchain.chains import create_history_aware_retriever, create_retrieval_chain
    from langchain.chains.combine_documents import create_stuff_documents_chain

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.2,
    groq_api_key=GROQ_API_KEY,
)

store: dict[str, BaseChatMessageHistory] = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


def generation(vstore):
    retriever = vstore.as_retriever(search_kwargs={"k": 3})

    retriever_system_prompt = (
        "Given chat history and the latest user question, rewrite the user question "
        "as a standalone question. Do not answer the question."
    )

    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", retriever_system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ]
    )

    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    qa_system_prompt = """
You are an expert ecommerce assistant for Flipkart products.
Use the provided review context to answer.
Stay concise, relevant, and practical.
If context is insufficient, say that clearly.

CONTEXT:
{context}
"""

    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
        ]
    )

    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    chain_with_memory = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )
    return chain_with_memory


if __name__ == "__main__":
    # Use load_existing=False once for first-time ingestion, then keep it True.
    vstore, _ = data_ingestion(load_existing=True)
    conversational_rag_chain = generation(vstore)

    answer = conversational_rag_chain.invoke(
        {"input": "Can you suggest the best bluetooth earbuds from these reviews?"},
        config={"configurable": {"session_id": "flipkart_user_1"}},
    )["answer"]
    print(answer)

    answer_2 = conversational_rag_chain.invoke(
        {"input": "What was my previous question?"},
        config={"configurable": {"session_id": "flipkart_user_1"}},
    )["answer"]
    print(answer_2)
