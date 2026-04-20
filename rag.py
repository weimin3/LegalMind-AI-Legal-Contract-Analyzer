from langchain_ollama import ChatOllama
from file_history_store import get_history

import vector_store
import config
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableLambda, RunnableWithMessageHistory, chain
from langchain_core.output_parsers import StrOutputParser

def print_prompt(prompt):
    print("=" * 20)
    print(prompt.to_string())
    print("=" * 20)

    return prompt

class RagService(object):
    def __init__(self,collection_name):
        self.vector_service = vector_store.VectorStoreService(
            OllamaEmbeddings(model = config.embedding_model),
            collection_name)

        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system","""
                        You are an expert legal contract analyst. 
                        Your job is to help users understand legal contracts,identify key clauses, and assess potiential risks.
                        Always answer based on the following contract context:{context}

                        When analyzing contracts, focus on:
                        - Key parties and their obligations
                        - Important dates and deadlines
                        - Payment terms and penalties
                        - Termination conditions
                        - Liability and indemnification clauses
                        - Intellectual property rights
                        - Risk factors for each party
                        If the context does not contain enough information to answer, say so clearly rather than making assumptions
                 """),
                ("system", "Here is the conversation history for context:"),
                MessagesPlaceholder("history"),
                ("user","{input}")
            ]

        )

        self.chat_model = ChatOllama(model= config.chat_model_name)

        self.chain = self.__get_chain()


    def __get_chain(self):
        retriever = self.vector_service.get_retriever()
        def format_for_retriever(value):
            return value["input"]
        
        def format_document(docs):
            if not docs:
                return "No relevant cotract sections found"
            
            formatted = ""
            for i, doc in enumerate(docs):
                formatted += f"---Section {i+1} ----\n"
                formatted += f"Source: {doc.metadata.get('source', 'Unknown')} \n"
                formatted += f"Content: {doc.page_content}\n\n"
            return formatted
        
        def format_for_prompt(value):
            return {
                "input": value["input"]["input"],
                "context" : value["context"],
                "history" : value["input"]["history"]
            }

        
        chain = (
            {
                "input" : RunnablePassthrough(),
                "context":RunnableLambda(format_for_retriever)|retriever|format_document
            }
            |RunnableLambda(format_for_prompt)
            |self.prompt_template
            |print_prompt
            |self.chat_model
            |StrOutputParser()
        )

        conversation_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history"
        )

        return conversation_chain