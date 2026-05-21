import whisper

print("loading model...")

model = whisper.load_model("base")

print("transcribing video...")

result = model.transcribe("vid01.mp4")

print("\nTranscript:\n")
print(result["text"])