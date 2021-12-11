from flask import current_app

def add_to_index(index, model):
    if not current_app.elasticsearch:
        return
    
    payload = {field: getattr(model, field) for field in model.__searchable__}
    current_app.elasticsearch.index(index=index, id=model.id, document=payload)
    

def remove_from_index(index, model):
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, id=model.id)
    
    
def query_index(index, query, page, per_page):
    if not current_app.elasticsearch:
        return [], 0
    
    es = current_app.elasticsearch
    query_dsl = {'query': {'multi_match': {'query': query, 'fields': ['*']}},
                 'from': (page - 1) * per_page, 
                 'size': per_page
                 }
    search = es.search(index=index, body=query_dsl)
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']['value']