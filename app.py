import os
import asyncio
from flask import Flask, request, send_file, redirect, url_for, Response
from werkzeug.utils import secure_filename

# Use the existing pipeline
from modules.pipeline import generate_knowledge_graph

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_HTML = os.path.join(BASE_DIR, "knowledge_graph_with_personality.html")
ALLOWED_EXTENSIONS = {"txt", "pdf"}

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.get("/")
def index() -> Response:
    # Simple inline HTML + CSS to match the attached design
    return Response(
        """
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Knowledge Graph With Personality</title>
            <style>
                :root {
                    --accent: #59c33a; /* bright green similar to screenshot */
                }
                body { font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; margin: 0; background: #fff; color: #111; }
                .container { max-width: 960px; margin: 80px auto; padding: 0 24px; text-align: center; }
                h1 { color: var(--accent); font-size: 40px; margin-bottom: 48px; font-weight: 700; }
                form { display: flex; gap: 16px; justify-content: center; align-items: stretch; }
                .input-wrap { position: relative; flex: 1; max-width: 720px; }
                input[type="text"] { width: 90%; padding: 18px 56px 18px 16px; font-size: 16px; border: 2px solid #1d1d1d; border-radius: 4px; outline: none; }
                input[type="text"]::placeholder { color: #777; }
                .upload-label { position: absolute; right: 12px; top: 50%; transform: translateY(-50%); cursor: pointer; color: #222; padding: 6px; border-radius: 4px; }
                .upload-label:hover { background: #f2f2f2; }
                .hidden-file { display: none; }
                button[type="submit"] { background: var(--accent); color: white; border: none; border-radius: 4px; padding: 0 24px; font-size: 16px; font-weight: 600; cursor: pointer; min-width: 120px; }
                button[type="submit"]:hover { filter: brightness(0.95); }
                @media (max-width: 720px) { form { flex-direction: column; } button[type="submit"] { height: 48px; } }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Knowledge Graph With Personality</h1>
                <form action="/generate" method="post" enctype="multipart/form-data">
                    <div class="input-wrap">
                        <input type="text" name="text" placeholder="Enter text" />
                        <label for="file" class="upload-label" title="Upload .txt or .pdf">
                            <!-- simple upload icon (SVG) -->
                            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                <path d="M12 16V4M12 4L8 8M12 4l4 4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                <path d="M20 16v2a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-2" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </label>
                        <input id="file" class="hidden-file" type="file" name="file" accept=".txt,.pdf" />
                    </div>
                    <button type="submit">Submit</button>
                </form>
            </div>
        </body>
        </html>
        """,
        mimetype="text/html",
    )


@app.post("/generate")
def generate():
    # Prefer file if provided, otherwise text input
    upload = request.files.get("file")
    text = request.form.get("text", "").strip()

    if upload and upload.filename and allowed_file(upload.filename):
        safe_name = secure_filename(upload.filename)
        tmp_path = os.path.join(BASE_DIR, f"upload_{os.getpid()}_{safe_name}")
        upload.save(tmp_path)
        input_payload = tmp_path
    elif text:
        input_payload = text
    else:
        # No input provided, redirect back to home
        return redirect(url_for("index"))

    # Run the async pipeline
    asyncio.run(generate_knowledge_graph(input_payload))

    # Cleanup temp file if used
    if upload and upload.filename and os.path.exists(tmp_path):
        try:
            os.remove(tmp_path)
        except Exception:
            pass

    # Serve the generated HTML directly
    if os.path.exists(OUTPUT_HTML):
        return send_file(OUTPUT_HTML)
    else:
        return Response("Failed to generate the knowledge graph.", status=500)


if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    use_reloader = os.getenv("FLASK_RELOAD", "0") == "1"
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000")),
        debug=debug,
        use_reloader=use_reloader,
    )
