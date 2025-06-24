## reference source url : https://milvus.io/docs/milvus_rag_with_vllm.md
## class reference source url : https://discuss.huggingface.co/t/text-input-bigger-than-max-tokens-length-for-semantic-search-embeddings/64465/2
import numpy as np
from sentence_transformers import SentenceTransformer

class Qwen3EmbeddingModel:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")            
            cls._instance.max_tokens = 1024 # Your model's max tokens limit
            cls._instance.overlap = 0 # no of tokens to be overlapped between chunks
        return cls._instance
    
    def get_embeddings(self, docs, prompt_name=None):   
        isquery= "embed a query" if prompt_name!=None else "embed documents"
        print(isquery)
        return self.model.encode(docs, prompt_name=prompt_name)
    