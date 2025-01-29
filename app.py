import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QComboBox, QPushButton, QTextEdit, QFileDialog, QMessageBox
)
from gtts import gTTS
from playsound import playsound
import os


class TextToSpeechApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Text-to-Speech Desktop App")
        self.setGeometry(300, 300, 500, 400)

        # Main Layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()

        # Widgets
        self.label = QLabel("Enter text to convert to speech:")
        layout.addWidget(self.label)

        self.text_input = QTextEdit()
        layout.addWidget(self.text_input)

        self.language_label = QLabel("Select Language:")
        layout.addWidget(self.language_label)

        self.language_dropdown = QComboBox()
        self.language_dropdown.addItems([
            "English (en)",
            "Spanish (es)",
            "French (fr)",
            "German (de)",
            "Italian (it)",
            "Japanese (ja)",
            "Korean (ko)"
        ])
        layout.addWidget(self.language_dropdown)

        self.play_button = QPushButton("Convert and Play")
        self.play_button.clicked.connect(self.convert_and_play)
        layout.addWidget(self.play_button)

        self.save_button = QPushButton("Convert and Save")
        self.save_button.clicked.connect(self.convert_and_save)
        layout.addWidget(self.save_button)

        # Set Layout
        self.central_widget.setLayout(layout)

    def convert_and_play(self):
        text = self.text_input.toPlainText()
        language = self.get_selected_language()

        if not text.strip():
            QMessageBox.warning(self, "Input Error", "Please enter some text to convert.")
            return

        try:
            # Generate TTS
            tts = gTTS(text=text, lang=language, slow=False)
            temp_file = "temp_audio.mp3"
            tts.save(temp_file)

            # Play the audio
            playsound(temp_file)

            # Cleanup
            os.remove(temp_file)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred:\n{str(e)}")

    def convert_and_save(self):
        text = self.text_input.toPlainText()
        language = self.get_selected_language()

        if not text.strip():
            QMessageBox.warning(self, "Input Error", "Please enter some text to convert.")
            return

        try:
            # Get Save Location
            save_path, _ = QFileDialog.getSaveFileName(self, "Save Audio File", "", "Audio Files (*.mp3)")
            if not save_path:
                QMessageBox.information(self, "Cancelled", "File save cancelled.")
                return

            # Generate TTS
            tts = gTTS(text=text, lang=language, slow=False)
            tts.save(save_path)
            QMessageBox.information(self, "Success", f"Audio saved successfully at:\n{save_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred:\n{str(e)}")

    def get_selected_language(self):
        """Extract the language code from the selected dropdown option."""
        selected_language = self.language_dropdown.currentText()
        return selected_language.split(" ")[-1][1:-1]  # Extract 'en', 'es', etc.


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TextToSpeechApp()
    window.show()
    sys.exit(app.exec())
