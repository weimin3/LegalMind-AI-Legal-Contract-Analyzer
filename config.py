
# md5_path
md5_path = "./md5.text"

# chroma database
persist_directory = "./chroma_db"
collection_name = "legal_contracts"

# text splitting 
chunk_size = 1000
chunk_overlap = 100
separators = ["\n\n","\n",".","!","?","。",""," "]
max_split_char_number = 1000

# model config
embedding_model = "nomic-embed-text"
chat_model_name = "llama3.2"

# chat_history_path
chat_history_path = "./chat_history"


#Retriever config
similarity_threshold = 5

# session config
"""
session_config = {
    "configurable":{
        "session_id":"user_123"
    }
}
"""