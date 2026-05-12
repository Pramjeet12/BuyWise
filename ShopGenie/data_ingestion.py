import os
from dotenv import load_dotenv
from langchain_astradb import AstraDBVectorStore
from langchain_huggingface import HuggingFaceEndpointEmbeddings

from ShopGenie.data_converter import dataconverter

load_dotenv()

ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_KEYSPACE = os.getenv("ASTRA_DB_KEYSPACE", "default_keyspace")
COLLECTION_NAME = os.getenv("ASTRA_COLLECTION", "flipkart")
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

embeddings = HuggingFaceEndpointEmbeddings(
    model="BAAI/bge-base-en-v1.5",
    task="feature-extraction",
    huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN
)


def data_ingestion(load_existing: bool = True):
    vstore = AstraDBVectorStore(
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        api_endpoint=ASTRA_DB_API_ENDPOINT,
        token=ASTRA_DB_APPLICATION_TOKEN,
        namespace=ASTRA_DB_KEYSPACE,
    )

    insert_ids = []
    if not load_existing:
        docs = dataconverter()
        insert_ids = vstore.add_documents(docs)

    return vstore, insert_ids


if __name__ == "__main__":
    vstore, insert_ids = data_ingestion(load_existing=False)
    print(f"\nInserted {len(insert_ids)} docs into collection '{COLLECTION_NAME}'")
    results = vstore.similarity_search("Can you tell me the low budget sound basshead?")
    for res in results:
        print(f"\n{res.page_content} [{res.metadata}]")
