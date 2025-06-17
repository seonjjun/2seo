import weaviate
import os

client = weaviate.Client(
    url=os.getenv("WEAVIATE_URL"),
    auth_client_secret=weaviate.AuthApiKey(os.getenv("WEAVIATE_API_KEY")),
)

structure_schema = {
    "class": "Structure",
    "vectorizer": "none",
    "vectorIndexType": "hnsw",
    "properties": [
        {"name": "symbol", "dataType": ["text"]},
        {"name": "description", "dataType": ["text"]},
        {"name": "success", "dataType": ["boolean"]},
        {"name": "time", "dataType": ["text"]},
        {"name": "image", "dataType": ["text"]},
        {"name": "rsi", "dataType": ["number"]},
        {"name": "obv", "dataType": ["number"]},
        {"name": "volume", "dataType": ["number"]}
    ]
}

client.schema.create_class(structure_schema)
print("✅ Structure 클래스 등록 완료")
