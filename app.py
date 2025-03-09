import os
from wordcloud import WordCloud, STOPWORDS
from flask import Flask, request, render_template
import zipfile
import ijson
import shutil

app = Flask(__name__)

# Save and store uploaded files
STATIC_FOLDER = "static/wordcloud"
EXTRACT_FOLDER = "extracted_files"
UPLOAD_FOLDER = "uploads"

if os.path.exists(UPLOAD_FOLDER):
    shutil.rmtree(UPLOAD_FOLDER)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
if os.path.exists(EXTRACT_FOLDER):
    shutil.rmtree(EXTRACT_FOLDER)
os.makedirs(EXTRACT_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Handles file uploads, extracts Discord data, processes messages and uses them generates a word cloud.

    Returns:
        render_template: Renders the HTML template with the generated word cloud or an error message.
    """
    if request.method == "POST":
        # Handle the uploaded file
        file = request.files["file"]
        if not file:
            return render_template("index.html", error="File upload error")
        zip_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(zip_path)

        # Extract the zip file
        extract_folder = os.path.join(
            EXTRACT_FOLDER, os.path.splitext(file.filename)[0]
        )
        os.makedirs(extract_folder, exist_ok=True)

        with zipfile.ZipFile(zip_path, "r") as zip:
            zip.extractall(extract_folder)

        # Handling JSON files
        messages_json_paths = []

        # Define messages path
        messages_folder = os.path.join(extract_folder, "messages")
        if os.path.exists(messages_folder):
            for root, _, files in os.walk(messages_folder):
                if "messages.json" in files:
                    messages_json_paths.append(os.path.join(root, "messages.json"))

        # Handle the messages in the JSON files
        total_messages = []
        if messages_json_paths:
            for json_path in messages_json_paths:
                with open(json_path, "r", encoding="utf-8") as json_file:
                    total_messages.extend(
                        [
                            msg["Contents"].strip()
                            for msg in ijson.items(json_file, "item")
                            if msg.get("Contents", "").strip()
                        ]
                    )
            
            print("Extracted Messages:", total_messages[:10])  # Print the first 10 messages
            text_string = " ".join(total_messages)

            stopwords = {
                "i",
                "me",
                "my",
                "myself",
                "we",
                "our",
                "ours",
                "ourselves",
                "you",
                "your",
                "yours",
                "yourself",
                "yourselves",
                "he",
                "him",
                "his",
                "himself",
                "she",
                "her",
                "hers",
                "herself",
                "it",
                "its",
                "itself",
                "they",
                "them",
                "their",
                "theirs",
                "themselves",
                "what",
                "which",
                "who",
                "whom",
                "this",
                "that",
                "these",
                "those",
                "am",
                "is",
                "are",
                "was",
                "were",
                "be",
                "been",
                "being",
                "have",
                "has",
                "had",
                "having",
                "do",
                "does",
                "did",
                "doing",
                "a",
                "an",
                "the",
                "and",
                "but",
                "if",
                "or",
                "because",
                "as",
                "until",
                "while",
                "of",
                "at",
                "by",
                "for",
                "with",
                "about",
                "against",
                "between",
                "into",
                "through",
                "during",
                "before",
                "after",
                "above",
                "below",
                "to",
                "from",
                "up",
                "down",
                "in",
                "out",
                "on",
                "off",
                "over",
                "under",
                "again",
                "further",
                "then",
                "once",
                "here",
                "there",
                "when",
                "where",
                "why",
                "how",
                "all",
                "any",
                "both",
                "each",
                "few",
                "more",
                "most",
                "other",
                "some",
                "such",
                "no",
                "nor",
                "not",
                "only",
                "own",
                "same",
                "so",
                "than",
                "too",
                "very",
                "s",
                "t",
                "can",
                "will",
                "just",
                "don",
                "should",
                "now",
                "tenor",
                "https",
                "wa",
                "http",
                "wg",
                "wg wg"
            }

            # Generate and save word cloud
            custom_stopwords = STOPWORDS.union(stopwords)
            wc = WordCloud(
                prefer_horizontal=1.0,
                colormap="cividis",
                background_color="white",
                height=400,
                width=600,
                max_font_size=90,
                min_font_size=3,
                stopwords=custom_stopwords,
            ).generate(text_string)
            wordcloud_filename = "wordcloud.png"
            wordcloud_path = os.path.join(STATIC_FOLDER, wordcloud_filename)
            wc.to_file(wordcloud_path)
            return render_template("index.html", wordcloud_url=f"/{wordcloud_path}")
        return render_template(
            "index.html", error="No message files found in the ZIP file."
        )

    return render_template("index.html")


def main():
    """
    Starts the Flask web application.
    """
    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == "__main__":
    main()
