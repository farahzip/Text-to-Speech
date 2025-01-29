from flask import Flask, render_template, request, send_file, jsonify
from gtts import gTTS
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/text_to_speech', methods=['POST'])
def text_to_speech():
    text = request.form.get('text')
    if not text:
        return jsonify({'error': 'Please enter some text.'}), 400
    
    try:
        lang = request.form.get('language', 'en')
        tts = gTTS(text=text, lang=lang, slow=False)
        filename = "output.mp3"
        tts.save(filename)
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/save_audio', methods=['POST'])
def save_audio():
    text = request.form.get('text')
    if not text:
        return jsonify({'error': 'Please enter some text.'}), 400
    
    try:
        lang = request.form.get('language', 'en')
        tts = gTTS(text=text, lang=lang, slow=False)
        filename = "output.mp3"
        tts.save(filename)
        return jsonify({'message': f'Audio saved as {filename}.'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
