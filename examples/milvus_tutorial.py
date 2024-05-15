"""Script that demonstrates how to use the RAG model with Milvus to implement rule-based retrieval."""

import os

from pymilvus import DataType

from src.whyhow_rbr.rag_milvus import ClientMilvus

# Set up your Milvus Client information
YOUR_MILVUS_LITE_FILE_PATH = "./milvus_demo.db" # random name for milvus lite local db


# Initialize the ClientMilvus
milvus_client = ClientMilvus(
    milvus_uri=YOUR_MILVUS_LITE_FILE_PATH,
)


# Define collection name
COLLECTION_NAME = "YOUR_COLLECTION_NAME"  # take your own collection name


# Create necessary schema to store data
DIMENSION = 1536  # decide by the model you use

schema = milvus_client.create_schema(auto_id=True)  # Enable id matching

schema = milvus_client.add_field(
    schema=schema, field_name="id", datatype=DataType.INT64, is_primary=True
)
schema = milvus_client.add_field(
    schema=schema,
    field_name="embedding",
    datatype=DataType.FLOAT_VECTOR,
    dim=DIMENSION,
)


# Start to indexing data field
index_params = milvus_client.prepare_index_params()
index_params = milvus_client.add_index(
    index_params=index_params,  # pass in index_params object
    field_name="embedding",
    index_type="AUTOINDEX",  # use autoindex instead of other complex indexing method
    metric_type="COSINE",  # L2, COSINE, or IP
)


# Create Collection
milvus_client.create_collection(
    collection_name=COLLECTION_NAME, schema=schema, index_params=index_params
)


# Create a Partition, list it out
milvus_client.crate_partition(
    collection_name=COLLECTION_NAME,
    partition_name="xxx",  # Put in your own partition name, better fit the document you upload
)

partitions = milvus_client.list_partition(collection_name=COLLECTION_NAME)
print(partitions)


# Uploading the PDF document
# get pdfs
pdfs = ["harry-potter.pdf", "game-of-thrones.pdf"]  # replace to your pdfs path

milvus_client.upload_documents(
    collection_name=COLLECTION_NAME, partition_name="xxx", documents=pdfs
)


# add your rules:
filter = ""
partition_names = None


# Search data and implement RAG!
res = milvus_client.search(
    question="Tell me about the greedy method",
    collection_name=COLLECTION_NAME,
    filter=filter,
    partition_names=None,
    anns_field="embedding",
    output_fields="text",
)
print(res["answer"])
print(res["matches"])


# Clean up
milvus_client.drop_collection(collection_name=COLLECTION_NAME)
