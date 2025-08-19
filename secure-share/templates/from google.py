from google.cloud import storage

client = storage.Client.from_service_account_json("gcp-key.json")
bucket = client.bucket("your-bucket-name")

print("Files in bucket:")
for blob in bucket.list_blobs():
    print(blob.name)
