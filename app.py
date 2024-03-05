from flask import Flask, render_template, request, redirect, url_for, flash
import gemini_summarize
from werkzeug.utils import secure_filename
import whisper
import os
import pytesseract
import cv2

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/uploads'
# app.config['UPLOAD_FOLDER_IMG'] = 'static/image'


@app.route('/')
def index():
    return render_template("index.html", summary="", transcription="")

# @app.route("/", methods=["POST"])
# def summary():    
#     transcript = request.form['transcript'] 
#     summary = gemini_summarize.get_summary(transcript) 
#     return render_template("index.html", summary=summary)

@app.route("/", methods=["POST"])
def summary():    
    transcript = request.form['transcript'] 
    
    # Check if the transcript is not empty before generating the summary
    if transcript:
        summary = gemini_summarize.get_summary(transcript) 
    else:
        summary = ""
    
    # Disable the summarize button if both transcript and summary are present
    disable_summarize_button = bool(transcript) and bool(summary)
    
    return render_template("index.html", summary=summary, disable_summarize_button=disable_summarize_button)

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'audio_file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['audio_file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        model = whisper.load_model("base")
        transcription = model.transcribe(file_path)
        os.remove(file_path)  # Delete the audio file
        return render_template("index.html", summary="", transcription=transcription["text"])

@app.route('/uploadImg', methods=['POST'])
def upload_image():
    if 'image_file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['image_file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        image = cv2.imread(file_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        threshold_img = cv2.threshold(gray, 178, 255, cv2.THRESH_BINARY)[1]
        text = pytesseract.image_to_string(threshold_img)
        os.remove(file_path)  # Delete the image file
        return render_template("index.html", summary="", transcription=text)

# Failed attempt at multilple image uploads
# @app.route('/uploadImg', methods=['POST'])
# def upload_image():
#     if 'image_file' not in request.files:
#         flash('No file part')
#         return redirect(request.url)
    
#     files = request.files.getlist('image_file')

#     transcriptions = []
    
#     for file in files:
#         if file.filename == '':
#             flash('No selected file')
#             return redirect(request.url)
        
#         if file:
#             filename = secure_filename(file.filename)
#             file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#             file.save(file_path)
#             image = cv2.imread(file_path)
#             gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#             threshold_img = cv2.threshold(gray, 178, 255, cv2.THRESH_BINARY)[1]
#             text = pytesseract.image_to_string(threshold_img)
#             transcriptions.append(text)
#             os.remove(file_path)  # Delete the image file
            
#         return render_template("index.html", summary="", transcriptions=transcriptions)


if __name__ == '__main__':
    app.run()