from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI

import os

def get_llm_chain(retriever):
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=os.environ["GOOGLE_API_KEY"]
    )

    prompt = PromptTemplate(
        template="""
        You are **MediBot**, an AI assistant for medical documents.

        Use **only the provided context** and explain what the topic about .

        Context:
        {context}

        User Question:
        {question}

        Answer:
        - Full details, Factual, calm, clear.
        - If answer not in context: "I'm sorry, but I couldn't find relevant information in the provided documents."
        """,
        input_variables=["context", "question"]
    )

    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )

