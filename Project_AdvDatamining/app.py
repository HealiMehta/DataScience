from flask import Flask, request, render_template
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("elastic", "fP4*PIm3Gv9r*1mnVv7F"),
    verify_certs=False
)

@app.route("/", methods=["GET"])
def home():
    return render_template("search.html")

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "")
    body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["title", "artist", "lyrics"]
            }
        },
        "highlight": {
            "fields": {
                "lyrics": {}
            }
        }
    }
    res = es.search(index="lyrics", body=body)
    hits = []
    for hit in res["hits"]["hits"]:
        source = hit["_source"]
        snippet = hit.get("highlight", {}).get("lyrics", [""])[0]
        hits.append({
            "id": hit["_id"],
            "title": source["title"],
            "artist": source["artist"],
            "year": source["year"],
            "rank": source["rank"],
            "snippet": snippet
        })
    return render_template("results.html", hits=hits, query=query)

@app.route("/lyrics/<id>")
def lyrics(id):
    doc = es.get(index="lyrics", id=id)
    return render_template("lyrics.html", song=doc["_source"])

if __name__ == "__main__":
    app.run(debug=True)
