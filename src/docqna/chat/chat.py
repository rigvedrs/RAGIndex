from llama_index.core.indices.base import BaseIndex
from llama_index.vector_stores.redis import RedisVectorStore
from llama_index.core import VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


def get_conversation_engine(embed_model: HuggingFaceEmbedding, 
                           vector_store: RedisVectorStore) -> BaseIndex.as_chat_engine:
    """
    
    Initialize and return a Chat engine using the provided embed model and vector store.

    Args:
    - embed_model (HuggingFaceEmbedding): An embedding model from Hugging Face to generate embeddings of the query
    - vector store (RedisVectorStore): The vector store to access from the Redis Database that was generated from the pipeline
    
    Returns:
    - Chat Engine: An initialized LLama Index Chat Engine with the provided Redis database, a ChatOpenAI language model, and a Conversation Memory.

    Notes:
    - The ChatOpenAI language model is used as the default LLM.
    - Chat Engine also does the task of keeping track of previous messages 
    """


    # Obtain the index or the type of model you want to use
    chat_engine = VectorStoreIndex.from_vector_store(
        vector_store, embed_model=embed_model
    ).as_chat_engine()


    # Return the llama index chat_engine 
    return chat_engine
