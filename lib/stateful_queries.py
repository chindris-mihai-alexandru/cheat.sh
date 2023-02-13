"""
Support for the stateful queries
"""

import cache

def save_query(client_id, query):
    """
    Save the last query `query` for the client `client_id`
    """
    cache.put(f"l:{client_id}", query)

def last_query(client_id):
    """
    Return the last query for the client `client_id`
    """
    return cache.get(f"l:{client_id}")
