from flask import Flask, render_template, request, send_file
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import nltk
import json
import os
import io

# PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

nltk.download('stopwords', quiet=True)

# ----------------------------
# Load Dataset
# ----------------------------
file_path = "data/thirukkural.csv"

df = pd.read_csv(file_path, encoding='utf-8')

df.rename(columns={
    "Unnamed: 0": "NUMBER",
    "தமிழ் குறள்": "TAMIL_VERSE",
    "ENGLISH VERSE": "ENGLISH_VERSE",
    "தமிழ் விளக்கம்": "TAMIL_EXPLANATION",
    "ENGLISH EXPLANATION": "ENGLISH_EXPLANATION"
}, inplace=True)

df = df[[
    "NUMBER",
    "TAMIL_VERSE",
    "ENGLISH_VERSE",
    "TAMIL_EXPLANATION",
    "ENGLISH_EXPLANATION"
]]

df.fillna("", inplace=True)

# ----------------------------
# Chat History
# ----------------------------
HISTORY_FILE = "data/chat_history.json"

if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)

def load_history():
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_history(data):
    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ----------------------------
# NLP
# ----------------------------
tamil_stop_words = ["இது", "அது", "ஒரு", "என்", "உங்கள்", "உடன்"]

def preprocess_tamil_text(text):
    text = str(text)
    text = re.sub(r'\W', ' ', text).lower()
    return " ".join([w for w in text.split() if w not in tamil_stop_words])

def preprocess_english_text(text):
    text = str(text)
    text = re.sub(r'\W', ' ', text).lower()
    stopwords = nltk.corpus.stopwords.words('english')
    return " ".join([w for w in text.split() if w not in stopwords])

df["PROCESSED"] = (
    df["ENGLISH_EXPLANATION"].apply(preprocess_english_text) + " " +
    df["TAMIL_VERSE"].apply(preprocess_tamil_text)
)

vectorizer = TfidfVectorizer(ngram_range=(1, 3))
matrix = vectorizer.fit_transform(df["PROCESSED"])

def search(query):
    if any("\u0B80" <= c <= "\u0BFF" for c in query):
        query = preprocess_tamil_text(query)
    else:
        query = preprocess_english_text(query)

    vec = vectorizer.transform([query])
    idx = cosine_similarity(vec, matrix).argmax()
    return df.iloc[idx]

# ----------------------------
# Flask
# ----------------------------
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html", history=load_history())

@app.route('/get_verse', methods=['POST'])
def get_verse():
    query = request.form['query']

    try:
        if query.isdigit():
            result = df[df["NUMBER"] == int(query)].iloc[0]
        else:
            result = search(query)

        entry = {
            "query": query,
            "verse_number": int(result["NUMBER"]),
            "tamil": result["TAMIL_VERSE"],
            "english": result["ENGLISH_VERSE"],
            "tamil_explanation": result["TAMIL_EXPLANATION"],
            "english_explanation": result["ENGLISH_EXPLANATION"]
        }

        history = load_history()
        history.append(entry)
        save_history(history)

        return render_template("index.html", history=history)

    except Exception as e:
        return render_template("index.html", error=str(e), history=load_history())

# ----------------------------
# Clear History
# ----------------------------
@app.route('/clear_history', methods=['POST'])
def clear_history():
    save_history([])
    return render_template("index.html", history=[])

# ----------------------------
# Export JSON
# ----------------------------
@app.route('/export_history')
def export_history():
    data = load_history()
    return send_file(
        io.BytesIO(json.dumps(data, indent=2, ensure_ascii=False).encode()),
        as_attachment=True,
        download_name="chat_history.json",
        mimetype="application/json"
    )

# ----------------------------
# Export PDF
# ----------------------------
@app.route('/export_pdf')
def export_pdf():
    history = load_history()

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    content = []

    for item in history:
        content.append(Paragraph(f"<b>Query:</b> {item['query']}", styles["Normal"]))
        content.append(Paragraph(f"<b>Verse #{item['verse_number']}</b>", styles["Normal"]))
        content.append(Paragraph(item['tamil'], styles["Normal"]))
        content.append(Paragraph(item['english'], styles["Normal"]))
        content.append(Paragraph(item['tamil_explanation'], styles["Normal"]))
        content.append(Paragraph(item['english_explanation'], styles["Normal"]))
        content.append(Spacer(1, 15))

    doc.build(content)
    buffer.seek(0)

    return send_file(buffer, as_attachment=True,
                     download_name="chat.pdf",
                     mimetype="application/pdf")

# ----------------------------
# Run
# ----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
