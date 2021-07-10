import json
import speech_recognition
import pyautogui
import pyperclip


def change_case(option):
    pyautogui.hotkey('ctrl', 'c')
    pyautogui.press('backspace')
    if option == 1:
        new_text = pyperclip.paste().upper()
    elif option == 2:
        new_text = pyperclip.paste().lower()
    else:
        new_text = pyperclip.paste().title()
    pyperclip.copy(new_text)
    pyautogui.hotkey('ctrl', 'v')


recognizer = speech_recognition.Recognizer()
mic = None

config_file = open('config.json')
config_data = json.load(config_file)

device_index = config_data['device_index']
language = config_data['language']
uppercase_command = config_data['uppercase_command']
lowercase_command = config_data['lowercase_command']
titlecase_command = config_data['titlecase_command']

if config_data['device_index'] == -1:
    print('You first need to choose which microphone you\'re going to use:\n')
    print(f'{speech_recognition.Microphone.list_microphone_names()}\n')
    device_index = int(input('Your choice (1 for 1st microphone, 2 for 2nd microphone...): ')) - 1
    mic = speech_recognition.Microphone(device_index=device_index)
    language_option = input('\nNow choose your language, 1 for english and 2 for portuguese: ')
    if language_option == '1':
        language = 'en-US'
        uppercase_command = 'uppercase'
        lowercase_command = 'lowercase'
        titlecase_command = 'title'
    else:
        language = 'pt-BR'
        uppercase_command = 'maiúsculo'
        lowercase_command = 'minúsculo'
        titlecase_command = 'título'
    to_save = {
        'device_index': device_index,
        'language': language,
        'uppercase_command': uppercase_command,
        'lowercase_command': lowercase_command,
        'titlecase_command': titlecase_command
    }
    jsonString = json.dumps(to_save)
    jsonFile = open("config.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()
else:
    mic = speech_recognition.Microphone(device_index=config_data['device_index'])

print('\nNow listening!\n')

with mic as source:
    while True:
        try:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio, language=language)
            print(f'You said: {text}')
            if text == uppercase_command:
                change_case(1)
            elif text == lowercase_command:
                change_case(2)
            elif text == titlecase_command:
                change_case(3)
        except speech_recognition.UnknownValueError:
            print('I couldn\'t understand you!')
