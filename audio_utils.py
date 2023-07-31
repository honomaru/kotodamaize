import requests
import re
import pydub
from pydub import AudioSegment
import os
import random


#voice_dict={"A: ":'21m00Tcm4TlvDq8ikWAM', "B: ":"GBv7mTt0atIp3Br8iCZE"}

API_KEY = os.getenv("ELEVEN_API_KEY")

def transformed_text2audio(transformed_text, mode, use_case, task_id):
    """
    Transform transformed_text to audio & Save to specified file_path and return error if exists
    Params: 
        transformed_text(str): output of LLM
        mode: (str): 
        task_id (int): used to make unique file path for each work
    Returns:
        path (str): file path of audio consisting of each speech
    """

    # set speaker's voice by "use_case" list
    voice_dict = create_voice_dict(use_case)
    # get speaker_marks used in func. split_text_by_keywords as keywords
    speaker_marks = voice_dict.keys()

    try:
        # get speech list list of tuple ("speaker: ","content")
        speech_list = split_text_by_keywords(transformed_text,keywords =speaker_marks )
    except SomeException as e:
        print("Failed to retrieve audio data. Please verify if text conversion was performed.")

    # save file
    file_list = []
    for i, speech_tuple in enumerate(speech_list):
        # set voice_id by Voice_dict
        voice_id = voice_dict[speech_tuple[0]]
        # set file_path to each piece of speech
        file_path = f'./{task_id}_{i}.mp3'
        # vocalize and save each voices
        err = vocalization(speech_tuple[1], file_path, voice_id)
        if err != "":
            print("Failed to transform text: "+err)
        file_list.append(file_path)
        
    path = f'./audio_id_{task_id}.mp3'
    audio_path = concat_audio(file_list, path, silence_duration=1000)
    return audio_path
"""
Transform text to audio and save to specified file_path and return error if exists

Params: 
    text (str): text to be transformed to audio
    filepath (str): file_path where audio to be saved 

Returns:
    err(str): error message (return "" when error does not occurs) 

"""
def vocalization(text, filepath, voice_id='21m00Tcm4TlvDq8ikWAM',latency='0'):
    base_url = 'https://api.elevenlabs.io/v1/text-to-speech/'
    params = f'{voice_id}?optimize_streaming_latency={latency}'
    url = base_url + params
    headers = {
        'accept': 'audio/mpeg',
        "xi-api-key": API_KEY,
        'Content-Type': 'application/json'
    }

    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0,
            "similarity_boost": 0,
            "style": 0.5,
            "use_speaker_boost": True
        }
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        with open(filepath, 'wb') as f:
            f.write(response.content)
        err = ""
        return err
    elif response.status_code == 422:
        err = f"Request failed with status code: {response.status_code}."
        return err
    elif response.status_code == 401:
        err = f"Request failed with status code: {response.status_code}.\n Make sure your api call limit"
        return err
    else:
        err = f"Request failed with status code: {response.status_code}. "
        return err


def split_text_by_keywords(text, keywords=["A: ","B: "]):
    """
    Params:
        text (list of str): LLMから帰ってきた文字列を想定
        voice (dict): 登場人物をキーとして、ボイスIDを指定する。"MC"と"Guest"
    Returns:
        result_list(list of tuple): list of tuples ("speaker: ","content")
    """
   
    # Join the keywords into a single regular expression pattern with the '|' (OR) operator
    pattern = '|'.join(map(re.escape, keywords))

    # Split the text using the regular expression pattern
    # LLM output begins with "A: " because of prompt, so the element located index=0 must be removed
    split_list = re.split(f"({pattern})", text)[1:]

    # Create a dictionary with trigger keywords as keys and the resulting substrings as values
    result_list = []

    for i in range(0, len(split_list), 2):
        if split_list[i] in keywords:
            result_list.append((split_list[i],split_list[i+1]))
  
    return result_list


def concat_audio(file_list, merged_file_path, silence_duration=300):
    """
    Concatenate the audio and store the silence between each audio file

    Params:
        file_list (list of str): list of file path to be merged
        merged_file_path(str): file path for save 
        silence_duration (int [Defalt:1000]): Specify the duration of silence to be inserted (in ms) (1000 ms = 1 sec)
    Returns:
        merged_fila_path (str): Path of merged audio file
    """
    # Create silent audio segment for the specified duration
    silence = AudioSegment.silent(duration=silence_duration)

    # Initialize the 'speech' variable to hold the combined audio data
    speech = AudioSegment.empty()

    for i, f in enumerate(file_list):
        speech += silence+AudioSegment.from_mp3(f)
        # remove file of each speech 
        os.remove(f)
    
    # save speech as a mp3 file
    speech.export(merged_file_path, format="mp3")

    return merged_file_path

def create_voice_dict(use_case):
    """
    Make voice_dict to determine each speaker's voice

    Params:
        use_case (list of str): use_case("narration"/"video game" etc. ) for each speaker
    Returns:
        voice_dict(dict): {"A: ", voice_id}, "A: ", "B: " is marks of speakers

    """
    # get voice_id list by param=use_case
    def get_voice_id_list(use_case):
        url = 'https://api.elevenlabs.io/v1/voices'
        params = {'use case': use_case}
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print("Failed to get voice list ")
            return voice_dict
        data = response.json()
        # get voice_id list which has the use case(=u)
        voice_id_list = [item['voice_id'] for item in data['voices']]
        return voice_id_list

    voice_dict = {}
    # for the case that speakers have the same use_case of their voice
    # to prevent from a case that speakers' voice ids are the same.

    if (len(use_case)!= 1) and (use_case[0]==use_case[1]):
        voice_id_list = get_voice_id_list(use_case[0])

        # create two random indexes
        numbers = list(range(len(voice_id_list)))
        random_numbers = random.sample(numbers, len(numbers))

        # create voice_dict keys
        letters = [chr(ord('A') + i) for i in range(len(use_case))]
        speaker_marks = [f"{letter}: " for letter in letters]

        # make voice_dict
        voice_dict[speaker_marks[0]] = voice_id_list[random_numbers[0]]
        voice_dict[speaker_marks[1]] = voice_id_list[random_numbers[1]]
        return voice_dict
    else:
        for i, u in enumerate(use_case):
            # get voice_id list which has the use case(=u)
            voice_id_list = get_voice_id_list(u)

            # select voice randomly
            random_index = random.randint(0, len(voice_id_list)-1)
            voice_id = voice_id_list[random_index]

            # set speaker mark ("A: ", "B: "...etc.) corresponds to index of use_case
            letter = chr(ord('A') + i)
            speaker_mark = f"{letter}: "

            # set voice_dict 
            voice_dict[speaker_mark] = voice_id_list[random_index]
        print(voice_dict)
        return voice_dict
def main():
    transformed_text = ""
    mode = "radio"
    mode = "comedy"
    use_case = ["interactive","video game"]
    use_case = ["interactive"]
    #use_case = ["interactive","interactive"]
    task_id = "11"
    path = transformed_text2audio(transformed_text, mode, use_case, task_id)
    print(path)

if __name__ == "__main__":
    main()
