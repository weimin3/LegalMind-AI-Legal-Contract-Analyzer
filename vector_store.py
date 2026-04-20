import config
from langchain_chroma import Chroma
from knowledge_base import  KnowledgeBaseService



class VectorStoreService:
    def __init__(self,embedding,collection_name):
        self.embedding = embedding
        self.collection_name = collection_name

        self.chroma = Chroma(
            persist_directory= config.persist_directory,
            collection_name= collection_name,
            embedding_function=self.embedding
        )
        

    def get_retriever(self):
        return self.chroma.as_retriever(
            search_kwargs={"k":config.similarity_threshold}
            
        )
