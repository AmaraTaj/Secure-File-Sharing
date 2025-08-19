import os
import io
from flask import Flask, request, jsonify, send_file, render_template
from werkzeug.utils import secure_filename
from cryptography.fernet import Fernet
from google.cloud import storage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BUCKET_NAME = os.getenv("BUCKET_NAME")
SECRET_KEY = os.getenv("SECRET_KEY")
GCP_KEY = os.getenv("GCP_KEY")

if not BUCKET_NAME or not SECRET_KEY or not GCP_KEY:
    raise Exception("❌ Missing .env configuration! Please set BUCKET_NAME, GCP_KEY, and SECRET_KEY.")

# Setup Fernet
fernet = Fernet(SECRET_KEY.encode())

# Setup Flask (now pointing to templates folder)
app = Flask(__name__, template_folder="templates")

# Setup GCP storage client
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GCP_KEY
storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)


# ✅ Serve index.html
@app.route("/")
def index():
    return render_template("index.html")


# ✅ Upload + Encrypt
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    filename = secure_filename(file.filename)
    file_bytes = file.read()

    # Encrypt file
    encrypted_bytes = fernet.encrypt(file_bytes)

    # Upload to GCP bucket
    blob = bucket.blob(filename + ".enc")
    blob.upload_from_string(encrypted_bytes)

    return jsonify({"message": "✅ File uploaded & encrypted successfully!", "filename": filename})


# ✅ Decrypt + Download
@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    blob = bucket.blob(filename + ".enc")

    if not blob.exists():
        return jsonify({"error": "File not found"}), 404

    encrypted_bytes = blob.download_as_bytes()
    decrypted_bytes = fernet.decrypt(encrypted_bytes)

    return send_file(
        io.BytesIO(decrypted_bytes),
        as_attachment=True,
        download_name=filename
    )


if __name__ == "__main__":
    print("✅ Secure File Sharing Backend is running at http://127.0.0.1:5000/")
    app.run(debug=True)
