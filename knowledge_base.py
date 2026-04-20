import config
import md5_util
import os
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime
from langchain_chroma import Chroma
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

class KnowledgeBaseService:
    def __init__(self):
        os.makedirs(config.persist_directory,exist_ok = True )

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size = config.chunk_size,
            chunk_overlap = config.chunk_overlap,
            separators = config.separators,
            length_function = len
        )

    def upload_contract(self, data, filename):

        # md5
        md5_hex = md5_util.get_string_md5(data)

        if md5_util.check_md5(md5_hex):
            collection_name = self.__get_collection_name(filename)
            return collection_name, f"the {filename} has been uploaded."
        
        if len(data) > config.max_split_char_number:
            knowledge_chunks:list[str] = self.splitter.split_text(data)
        else:
            knowledge_chunks = [data]

        metadata = {
            "source" : filename,
            "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator":"admin"
        }

        collection_name = self.__get_collection_name(filename)
        self.chroma = Chroma(
            persist_directory = config.persist_directory,
            collection_name = collection_name,
            embedding_function = OllamaEmbeddings(model = config.embedding_model)

        )


        self.chroma.add_texts(
            knowledge_chunks,
            metadata = [metadata for _ in knowledge_chunks]
        )

        md5_util.save_md5(md5_hex)
        return collection_name,f"{filename} has been uploaded succesfully "
    

    def __get_collection_name(self,filename):
        import re
        name = filename.lower()
        name = name.replace(".pdf","")
        safe_name = re.sub(r'[^a-zA-Z0-9]', '_', name)
        safe_name = re.sub(r'_+', '_', safe_name).strip('_')[:10]
        hash_id = md5_util.get_string_md5(name)[:8]
        return f"{safe_name}_{hash_id}"




