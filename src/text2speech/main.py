import pandas as pd
import requests
from pydub import AudioSegment
from settings import AUTH_TOKEN
from settings import FOLDER_ID

if __name__ == '__main__':
    df = pd.read_csv("questions.csv")
    questions = list(df['explicit_questions_known'])
    for q in questions:
        if '?' not in q:
            q = q + '?'
        headers = {'Authorization': 'Bearer {}'.format(AUTH_TOKEN)}
        resp = requests.post('https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize',
                             data={'lang': 'ru-RU', 'folderId': FOLDER_ID, 'text': q}, headers=headers)
        filename = "{}.ogg".format(q)
        with open(filename, "wb") as f:
            f.write(resp.content)
        ogg_version = AudioSegment.from_ogg(filename)
        ogg_version.export("{}.wav".format(q), format="wav")
