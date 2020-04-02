# Голосовой ассистент Golos 1.0 BETA
import datetime
import os
import pyttsx3
import speech_recognition as sr
from fuzzywuzzy import fuzz

# настройки
opts = {
    "alias": ('Golos', 'Voice'),
    "tbr": ('Tell', 'Tell me', 'Show me', 'How many', 'speak', 'How much', 'Play'),
    "cmds": {
        "ctime": ('What time now?', 'Time', 'Tell me time'),
        "radio": ('Play Music', 'Wanna listen music', 'play radio', 'play music from YuoTube'),
        "stupid1": ('Tell me funny story', 'make me laught', 'tell me a joke')
    }
}


# функции
def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()


def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language="eng-Eng").lower()
        print("[log] recignized: " + voice)

        if voice.startswith(opts["alias"]):
            # обращаются к Golos
            cmd = voice

            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()

            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()

            # распознаем и выполняем команду
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])

    except sr.UnknownValueError:
        print("[log] The voice is recognized!")
    except sr.RequestError as e:
        print("[log] CRAP!")


def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c, v in opts['cmd'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt

    return RC


def execute_cmd(cmd):
    if cmd == 'ctime':
        # сказать текущее время
        now = datetime.datetime.now()
        speak("Now " + str(now.hour) + ":" + str(now.minute))

    elif cmd == 'radio':
        # воспроизвести радио
        os.system("C:\\Users\\Oleg\\Desktop\\Музыка на телефон")

    elif cmd == 'stupid1':
        # рассказать анекдот
        speak("Look at your self, my boy")

    else:
        print('Please repeat!')


# запуск
r = sr.Recognizer()
m = sr.Microphone(device_index=1)

with m as source:
    r.adjust_for_ambient_noise(source)

speak_engine = pyttsx3.init()

# Только если у вас установлены голоса для синтеза речи!
voices = speak_engine.getProperty('voices')
speak_engine.setProperty('voice', voices[0].id)

# forced cmd test
speak("My boy did't teach to tell funny story, but is his job")

speak("Golos is HERE my boy")
speak("Golos is listening")

stop_listening = r.listen_in_background(m, callback)
while True: datetime.sleep(0.1) # infinity loop