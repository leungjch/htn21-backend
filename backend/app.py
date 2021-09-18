from flask import Flask, request, jsonify
from ocr import gcp_ocr
from ner import ner_spacy
from summarization import summarize_t5, summarize_textrank, summarize_bart

app = Flask(__name__)


@app.route("/", methods=['GET'])
def root():
    return "Welcome to Hack the North 2021!!!"


@app.route("/process", methods=['POST'])
def process():
    """
        Payload:
            imageData: base64 image string        
    """
    # imageData base64 image string
    # Fetch image data
    data = request.get_json()
    imageData = data['imageData']

    print("hello")

    # Get OCR text using GCP
    paragraphs, lines = gcp_ocr(imageData)
    full_text = " . ".join(paragraphs)
    # Run Named Entity Recognition
    entities = ner_spacy(full_text)

    # Summarize the text
    summary = summarize_bart(full_text)

    return jsonify({"paragraphs": paragraphs, "lines": lines, "entities": entities, "summary": summary})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)