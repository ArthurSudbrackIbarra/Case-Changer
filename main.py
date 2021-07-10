import json
import speech_recognition
import pyautogui
import pyperclip

# Function responsible for putting selected texts in uppercase, lowercase or titlecase.
def change_case(option):
    # Saving user's current clipboard content.
    current_clipboard_content = pyperclip.paste()
    # Copying selected text.
    pyautogui.hotkey('ctrl', 'c')
    # Erasing selected text.
    pyautogui.press('backspace')
    if option == 1:
        new_text = pyperclip.paste().upper()
    elif option == 2:
        new_text = pyperclip.paste().lower()
    else:
        new_text = pyperclip.paste().title()
    # Adding new text to user's clipboard.
    pyperclip.copy(new_text)
    # Pasting new text.
    pyautogui.hotkey('ctrl', 'v')
    # Restoring user's clipboard content.
    pyperclip.copy(current_clipboard_content)

# Recognizer object.
recognizer = speech_recognition.Recognizer()
# Microphone object.
mic = None

# Opening config.json file and extracting data.
config_file = open('config.json')
config_data = json.load(config_file)

device_index = config_data['device_index']
language = config_data['language']
lowercase_command = config_data['lowercase_command']
titlecase_command = config_data['titlecase_command']

# Setting up which microphone, language and commands to use.
if device_index == -1:
    # Microphone.
    print('You first need to choose which microphone you\'re going to use:\n')
    mic_list = speech_recognition.Microphone.list_microphone_names()
    for i, val in enumerate(mic_list):
        print(f'[{i + 1}] - {val}')
    str_device_index = input('\nYour choice (1 for 1st microphone, 2 for 2nd microphone...): ')
    while True:
        if str_device_index.isnumeric():
            numeric_device_index = int(str_device_index) - 1
            if 0 < numeric_device_index < len(mic_list):
                break
            else:
                str_device_index = input('Invalid option, try again: ')
        else:
            str_device_index = input('Invalid option, try again: ')
    mic = speech_recognition.Microphone(device_index=numeric_device_index)
    # Language and commands.
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
    # Saving configurations to config.json
    to_save = {
        'device_index': numeric_device_index,
        'language': language,
        'uppercase_command': uppercase_command,
        'lowercase_command': lowercase_command,
        'titlecase_command': titlecase_command
    }
    jsonString = json.dumps(to_save)
    with open('config.json', 'wb') as jsonFile:
        jsonFile.write(jsonString.encode('utf-8'))
        jsonFile.close()
else:
    try:
        # Microphone.
        mic = speech_recognition.Microphone(device_index=int(device_index))
    except ValueError:
        print('There was an error with config.json file, download it again at:')
        print('https://github.com/ArthurSudbrackIbarra/Case-Changer')
        exit(1)

print('\nNow listening!\n')

# Listening to user audio input.
with mic as source:
    while True:
        try:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio, language=language)
            print(f'You said: {text}')
            # Determining which case to apply.
            if text == uppercase_command:
                change_case(1)
            elif text == lowercase_command:
                change_case(2)
            elif text == titlecase_command:
                change_case(3)
        except speech_recognition.UnknownValueError:
            print('I couldn\'t understand you!')
