🔒 Secure File Sharing System 
This system ensures that files are encrypted before upload and decrypted after download, providing end-to-end security. 

🚀 Features
✅ End-to-End Encryption (AES / Fernet)  
✅ Secure Upload & Download with Flask  
✅ Google Cloud Storage Integration (Signed URLs)  
✅ Simple Web UI for file sharing  

⚙️ Tech Stack
- Python (Flask)  
- Google Cloud Storage (GCS)  
- Cryptography (Fernet AES)  
- HTML, CSS, JavaScript  

 🔐 How it Works
1. User uploads a file via the web UI.  
2. File is encrypted locally before upload.  
3. Encrypted file is stored securely in Google Cloud Storage.  
5. On download, the file is decrypted and restored.  

📂 Project Structure
secure-share/
│-- app.py  # Flask backend 

│-- templates/  # HTML templates 
    └── index.html Frontend JS & CSS
│-- .env     # Environment variables (Bucket, Keys, Secret)
