from google.cloud import storage
from dotenv import load_dotenv
load_dotenv()

client = storage.Client()
buckets = list(client.list_buckets())
for bucket in buckets:
    print(bucket.name)
