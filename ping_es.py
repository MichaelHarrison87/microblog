import os
from dotenv import load_dotenv
from elasticsearch import Elasticsearch, RequestsHttpConnection
from pprint import pprint

load_dotenv()

ELASTICSEARCH_USER = os.getenv('ELASTICSEARCH_USER')
ELASTICSEARCH_PW = os.getenv('ELASTICSEARCH_PW')

es = Elasticsearch(['localhost'],
                   port=9200,
                   connection_class=RequestsHttpConnection,
                   http_auth=(ELASTICSEARCH_USER, ELASTICSEARCH_PW)
                   )
print("Cluster Running:", es.ping())

es.index(index='my_index', id=1, document={'text': 'this is a test'})
es.index(index='my_index', id=2, document={'text': 'a second test'})
res = es.search(index='my_index', query={'match': {'text': 'second'}})
print("Elasticsearch Result:")
pprint(res)
es.indices.delete(index='my_index')