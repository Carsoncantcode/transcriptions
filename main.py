import os
from dotenv import load_dotenv
from logic import get_transcription, getFiles, write_transcriptions_to_csv
import csv


load_dotenv()


API_KEY = os.getenv("KEY")

files = getFiles()

transcriptions = get_transcription(files)

print(transcriptions)

write_transcriptions_to_csv(transcriptions, 'transcriptions.csv')

