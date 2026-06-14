import os
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from ingest import ingest_file
from chat import answer
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "./uploads"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024
os.makedirs("./uploads", exist_ok=True)

ALLOWED = {"pdf", "txt", "md"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    file = request.files["file"]
    if file.filename == "" or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Use PDF, TXT, or MD"}), 400
    filename = secure_filename(file.filename)
    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(path)
    chunks = ingest_file(path, filename)
    return jsonify({"message": f"Ingested {chunks} chunks from {filename}", "filename": filename})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "question" not in data:
        return jsonify({"error": "No question provided"}), 400
    result = answer(data["question"])
    return jsonify(result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)