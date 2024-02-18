import os
from dotenv import load_dotenv
import csv


from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)

load_dotenv()


API_KEY = os.getenv("KEY")

def getFiles():
    folder = 'videos'

    files = os.listdir(folder)

    print(files)

    return files

def get_transcription(paths):
    transcriptions = []

    for path in paths:
        try:
            AUDIO_FILE = os.path.join("videos", path)

            # STEP 1 Create a Deepgram client using the API key
            deepgram = DeepgramClient(API_KEY)

            with open(AUDIO_FILE, "rb") as file:
                buffer_data = file.read()

            payload: FileSource = {
                "buffer": buffer_data,
            }

            #STEP 2: Configure Deepgram options for audio analysis
            options = PrerecordedOptions(
                model="nova-2",
                smart_format=True,
            )

            # STEP 3: Call the transcribe_file method with the text payload and options
            response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)

            # STEP 4: Print the response
            print(response.to_json(indent=4))

            transcription = response['results']['channels'][0]['alternatives'][0]['transcript']
            row = ({path: transcription})

            transcriptions.append(row)


            print(row)

        except Exception as e:
            print(f"Exception: {e}")
    
    return transcriptions

def write_transcriptions_to_csv(transcriptions, csv_file_name):
    
    with open(csv_file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(['Video Name', 'Transcription'])

        for transcription in transcriptions:
            for video_name, text in transcription.items():
                writer.writerow([video_name, text])

