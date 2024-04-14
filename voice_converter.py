import requests
import os

API_KEY = os.environ.get("API_KEY")
API_URL = os.environ.get("API_URL")


class VoiceConverterError(Exception):
    pass


class VoiceConverter:
    def __init__(self, text, voice_option):
        self.parameters = {
            "key": API_KEY,
            "src": text,
            "hl": 'en-gb',
            "v": voice_option,
            "c": "mp3"
        }
        self.response = requests.get(url=API_URL, params=self.parameters)

        if self.response.status_code == 200:
            # Check if the response contains an error message
            if "ERROR" in self.response.text:
                # Extract the error message and print it
                error_message = self.response.text.strip()
                print(f"API Error: {error_message}")
                raise VoiceConverterError(error_message)
            else:
                # Write the response content to a file
                with open("music.mp3", "wb") as fout:
                    fout.write(self.response.content)
        else:
            print(f"Request failed with status code: {self.response.status_code}")
            raise VoiceConverterError(f"Request failed with status code: {self.response.status_code}")
