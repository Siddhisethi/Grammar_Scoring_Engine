import speech_recognition as sr
import language_tool_python
import os
import csv

# Print working directory to be sure
print("🔍 Working directory:", os.getcwd())

# Function to convert audio to text
def audio_to_text(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"API request error: {e}"

# Function to check grammar
def check_grammar(text):
    tool = language_tool_python.LanguageTool('en-US')
    matches = tool.check(text)
    return matches

# Function to calculate score
def score_grammar(matches):
    return max(0, 100 - len(matches) * 5)  # deduct 5 points per mistake

# Function to process an audio file
def process_audio_for_grammar(audio_path):
    transcribed_text = audio_to_text(audio_path)
    if "Could not understand audio" in transcribed_text or "API request error" in transcribed_text:
        return transcribed_text, 0, 0
    grammar_issues = check_grammar(transcribed_text)
    score = score_grammar(grammar_issues)
    return transcribed_text, len(grammar_issues), score

# ✅ Path to your train audio folder inside Dataset
train_audio_folder = os.path.join("Dataset", "audios", "train")

# ✅ Make sure Dataset/train_grammar_scores.csv is the output
output_csv_path = os.path.join("Dataset", "train_grammar_scores.csv")

# Write results to CSV
with open(output_csv_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Filename", "Transcribed Text", "Grammar Errors", "Grammar Score"])

    # Loop through audio files
    for filename in os.listdir(train_audio_folder):
        if filename.endswith(".wav"):
            audio_path = os.path.join(train_audio_folder, filename)
            print(f"🎧 Processing: {filename}")
            text, errors, score = process_audio_for_grammar(audio_path)
            writer.writerow([filename, text, errors, score])

print(f"\n✅ All done! Results saved to: {output_csv_path}")
