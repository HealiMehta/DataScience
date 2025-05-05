import csv
import urllib3
from elasticsearch import Elasticsearch

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("elastic", "fP4*PIm3Gv9r*1mnVv7F"),
    verify_certs=False
)

mapping = {
    "mappings": {
        "properties": {
            "rank": {"type": "integer"},
            "title": {"type": "text"},
            "artist": {"type": "text"},
            "year": {"type": "integer"},
            "lyrics": {"type": "text"}
        }
    }
}
es.indices.create(index="lyrics", body=mapping, ignore=400)

# Try 'utf-8', if it fails, use 'latin1' or 'cp1252'
with open("lyrics.csv", "r", encoding="latin1") as f:
    reader = csv.DictReader(f, skipinitialspace=True)
    for row in reader:
        if not row["Rank"].strip() or not row["Song"].strip() or not row["Artist"].strip() or not row["Year"].strip():
            continue
        lyrics = row.get("Lyrics", "").strip()
        try:
            doc = {
                "rank": int(row["Rank"]),
                "title": row["Song"],
                "artist": row["Artist"],
                "year": int(row["Year"]),
                "lyrics": lyrics
            }
            es.index(index="lyrics", document=doc)
        except Exception as e:
            print(f"Skipping row due to error: {e}\nRow: {row}")

print("Indexing complete!")
