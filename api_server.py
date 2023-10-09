from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch

app = Flask(__name__)

# Make Elasticsearch connection
es = Elasticsearch(hosts=['http://localhost:9200'])

INDEX_NAME = "company_profiles"

@app.route('/search', methods=['POST'])
def search():
    query_params = request.json

    # Check if search query exists
    if not query_params.get("query"):
        return jsonify({"error": "Please provide a search query."}), 400

    # Elasticsearch query body
    body = {
        "query": {
            "multi_match": {
                "query": query_params["query"],
                "fields": ["company_commercial_name", "phone_numbers", "social_media_links.facebook"],
                "fuzziness": "AUTO"
            }
        }
    }

    response = es.search(index=INDEX_NAME, body=body)

    # If there are any hits, return the most relevant one
    if response["hits"]["hits"]:
        return jsonify(response["hits"]["hits"][0]["_source"])
    return jsonify({"error": "No matching profile found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
