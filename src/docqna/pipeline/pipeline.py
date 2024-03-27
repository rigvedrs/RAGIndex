import toml

from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.ingestion import (
    DocstoreStrategy,
    IngestionPipeline,
    IngestionCache,
)
from llama_index.storage.kvstore.redis import RedisKVStore as RedisCache
from llama_index.storage.docstore.redis import RedisDocumentStore
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.redis import RedisVectorStore


# Load parameters from the TOML file
with open('../config.toml', 'r') as f:
    params = toml.load(f)



def get_pipeline() -> dict:
    """
    Initialize and return the embedding model and LLama-Index IngestionPipeline 

    Returns:
    - Dict: A dictionory of the embedding model and LLama-Index IngestionPipeline 

    Notes:
    - The SentenceTransformerEmbeddings model used is "Suva/bge-base-finetune-v2", and its cached data is stored in "./store/models".
      
      The Ingestion pipeline contains the following features:
    - Splitting: The function uses the SentenceSplitter with a chunk size of 1,000 characters and an overlap of 100 characters.
    - DocumentStore: For passing the location for storing the documents. Uses RedisDocumentStore for storage and doc tracking
    - VectorStore: For passing the location for storing the vectors. Uses RedisVectorStore for storage 
    - IngestionCache: All node + transformation combinations will have their outputs cached, which will save time on duplicate runs.
    - Docstore Strategy: The strategy to track and update documents. Uses DUPLICATES_ONLY strategy that checks for existence 
                         of any duplicate file and prevents it from being ingested again.
    """

    # Define the embedding model from the HuggingFace Library
    embed_model = HuggingFaceEmbedding(
        model_name=params['embed_model']['model_name'], 
        cache_folder= params['embed_model']['cache_folder'], 
        embed_batch_size= params['embed_model']['embed_batch_size']
    )

    # Initialising the Ingestion Pipeline for Document Ingestion
    pipeline = IngestionPipeline(
        transformations=[
            SentenceSplitter(chunk_size=params['transformations']['chunk_size'], chunk_overlap=params['transformations']['chunk_overlap']),
            embed_model,
        ],
        docstore=RedisDocumentStore.from_host_and_port(
            "localhost", params['redis']['port_no'], namespace=params['redis']['doc_store_name']
        ), 
        vector_store=RedisVectorStore(
            index_name=params['redis']['vector_index_name'],
            index_prefix=params['redis']['vector_index_prefix'],
            redis_url="redis://localhost:"+str(params['redis']['port_no']),
            # index_args = {'dims:': 3072}
        ),
        cache=IngestionCache(
            cache=RedisCache.from_host_and_port("localhost", params['redis']['port_no']),
            collection=params['redis']['cache_name'],
        ),
        docstore_strategy=DocstoreStrategy.DUPLICATES_ONLY,
    )


    # Return Embed model and Ingestion Pipeline
    return {'pipeline': pipeline, 'embed_model': embed_model}
