from elasticsearch import AsyncElasticsearch
from app.config import settings


class ElasticsearchClient:
    def __init__(self, index_name):
        self.index_name = index_name
        self.client = AsyncElasticsearch([{"host": settings.ELASTICSEARCH_HOST, "port": settings.ELASTICSEARCH_PORT}])
        self.mappings = {
        "properties": {
            "name": {"type": "text"},
            "description": {
                "type": "text",
                "fields": {"keyword": {"type": "keyword"}}
            },
            "quantity": {"type": "integer"},
            "price": {"type": "float"},
            "sku": {"type": "keyword"},
        }}
        
    def _ensure_index(self):
        if not self.client.indices.exists(index=self.index_name):
            self.client.indices.create(index=self.index_name, mappings=self.mappings)

    async def index_document(self, index_name: str, document: dict, document_id: str):
        await self.client.index(index=index_name, id=document_id, document=document)

    async def search_documents(self, query:str):
        search_query: dict = {
        "query": {
            "bool": {
            "must": [
                {
                "multi_match": {
                    "query": query,
                    "fields": ["name^3", "description"],
                    "fuzziness": "AUTO"
                }
                }
            ],
            }
        }
        }
        response = await self.client.search(index=self.index_name, body=search_query)
        return response

elasticsearch_client = ElasticsearchClient()