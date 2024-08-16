from flask import Flask, request, redirect, url_for, render_template, send_from_directory
import os
import urllib.parse

app = Flask(__name__)

# Set the upload folder and allowed extensions
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        print("No file part in request")
        return redirect(request.url)
    
    file = request.files['file']
    
    if file.filename == '':
        print("No selected file")
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = file.filename
        safe_filename = urllib.parse.quote(filename)  # URL encode the filename
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        try:
            file.save(save_path)
            print("File saved successfully at:", save_path)
        except Exception as e:
            print(f"Error saving file: {e}")
            return "There was an error saving the file."
        
        return render_template('success.html', filename=safe_filename)
    else:
        print("File type not allowed")
        return "File type not allowed"

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    decoded_filename = urllib.parse.unquote(filename)  # URL decode the filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], decoded_filename)
    print(f"Serving file from: {file_path}")
    return send_from_directory(app.config['UPLOAD_FOLDER'], decoded_filename)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
