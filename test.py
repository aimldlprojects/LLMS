POST /your_index_name/_delete_by_query
{
  "query": {
    "term": {
      "field": "value"
    }
  }
}
