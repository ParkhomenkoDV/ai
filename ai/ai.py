import random
import time

from fuzzywuzzy import fuzz  # Расстояние Левенштейна
import webbrowser

from speech_to_text import STT
from text_to_speech import TTS

import config


class AI:
    """Исинка"""

    __slots__ = ('stt', 'tts',
                 'sample_rate', 'device')

    def __init__(self, path: str, language: str, model_id: str, speaker: str,
                 sample_rate: int = 48_000, device: int = 1):
        self.stt = STT(path)
        self.tts = TTS(language=language, model_id=model_id, speaker=speaker)
        self.sample_rate = sample_rate
        self.device = device

    def listen(self, callback, device: int = 1):
        self.stt.listen(callback, samplerate=self.sample_rate, device=device)

    @staticmethod
    def preprocessing(text: str) -> str:
        for x in config.ALIAS: text = text.replace(x, "").strip()
        for x in config.VA_TBR: text = text.replace(x, "").strip()
        return text

    def understand(self, text: str):
        text = self.preprocessing(text)
        rc = {'cmd': '', 'percent': 0}
        for c, v in config.COMMANDS.items():
            for x in v:
                vrt = fuzz.ratio(text, x)
                if vrt > rc['percent']:
                    rc['cmd'] = c
                    rc['percent'] = vrt

        return rc

    def speak(self, text: str):
        self.tts.play(text, sample_rate=self.sample_rate)

    def do(self, command):
        if command == 'help':
            text = "Я умею: ..."
            text += "произносить время ..."
            text += "рассказывать анекдоты ..."
            text += "и открывать браузер"
            self.tts.play(text, self.sample_rate)
        elif command == 'joke':
            jokes = ('Как смеются программисты? ... ехе ехе ехе',
                     'ЭсКьюЭль запрос заходит в бар, подходит к двум столам и спрашивает .. «м+ожно присоединиться?»',
                     'Программист это машина для преобразования кофе в код')
            joke = random.choice(jokes)
            self.tts.play(joke, self.sample_rate)
        elif command == 'cdate':
            now = time.strftime('%Y.%m.%d.%H.%M.%S', time.localtime())
            year, month, day, hour, minute, second = map(int, now.split('.'))
            text = f"Сейч+ас {year} год {month} месяц {day} день"
            self.tts.play(text, self.sample_rate)
        elif command == 'ctime':
            now = time.strftime('%Y.%m.%d.%H.%M.%S', time.localtime())
            year, month, day, hour, minute, second = map(int, now.split('.'))
            text = f"Сейч+ас {hour} часов {minute} минут {second} секунд"
            self.tts.play(text, self.sample_rate)
        elif command == 'open_browser':
            chrome_path = 'C:/Program Files/Mozilla Firefox/firefox.exe %s'
            webbrowser.get(chrome_path).open("http://python.org")


if __name__ == '__main__':
    path = 'models/RUSSIAN_small'
    language = 'ru'
    model_id = 'ru_v3'
    speaker = 'xenia'
    sample_rate = 48_000
    device = 1
    ai = AI(path, language=language, model_id=model_id, speaker=speaker, sample_rate=sample_rate, device=device)


    def respond(voice: str):
        print(voice)
        if voice.startswith(config.ALIAS):
            command = ai.understand(voice)

            if command['cmd'] not in config.COMMANDS.keys():
                ai.speak("Что?")
            else:
                ai.do(command['cmd'])


    ai.listen(respond)
