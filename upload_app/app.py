from flask import Flask, jsonify, request, render_template, make_response
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_cors import CORS
import os
import gdown
from tensorflow.keras.models import load_model

# Flask setup
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__, static_url_path='/static')
CORS(app)
app.secret_key = 'dave_server'

login_manager = LoginManager()
login_manager.init_app(app)

# Google Drive file ID and destination
FILE_ID = 'your_google_drive_file_id_here'
MODEL_DEST = 'model.h5'

# Download the model if it doesn't exist
if not os.path.exists(MODEL_DEST):
    gdown.download(f"https://drive.google.com/uc?id=1g-AB4ZK96MfYIUhGsJ4AM4fncXs4MoMM", MODEL_DEST, quiet=False)

# Load the model
model = load_model(MODEL_DEST)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        # Process and use your model here
        # Example: Make a prediction and return the result
        return jsonify({"message": "File received and processed"}), 200

    return jsonify({"error": "Invalid file type"}), 400

if __name__ == '__main__':
    app.run(debug=True)
