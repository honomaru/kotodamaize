import uuid
from text_utils import transform_text, text2text, display_text
from audio_utils import transformed_text2audio
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import send_from_directory

app = Flask(__name__, static_folder='build', static_url_path='/')

@app.route('/api/audio/<path:filename>', methods=['GET'])
def get_audio(filename):
    return send_from_directory('.', filename)

@app.route('/')
def index():
    return app.send_static_file('index.html')

CORS(app) 
# dict for mapping button_id to (mode, list of "use case" of speaker)
#USE_CASE_LIST = ["video game","narration","audiobook","animation", "interactive", "news presenter", "news"]
BUTTON_ID_TO_MODE = {
    0:("radio",["interactive","video game"]),
    1:("narrative",["narrative"]),
    2:("lesson",["interactive", "interactive"]),
    3:("comedy",["video game", "video game"])
}


#TAWAMURE_PASSWORD = os.getenv("TAWAMURE_PASSWORD")

# POSTリクエストでテキストを受け取り、変換後のテキストを返す
@app.route('/api/text2audio', methods=['POST'])
def get_transformedText():
    # get JSON data from POSTrequest
    data = request.get_json()
    #password = data.get("password")
    #if password !=  TAWAMURE_PASSWORD:
    #    return jsonify({"audio_path": "","message": "Wrong password. Please check it out in our demo video!!"})

    # text that is to be transformed
    text = data.get("text")  
    if text is None:
        return jsonify({"audio_path": "","message": "Text not found"})
    # mode is a style in which the text is transformed
    button_id = data.get("ButtonID")
    mode = BUTTON_ID_TO_MODE[button_id][0]
    # number of speakers
    num_speakers = len(BUTTON_ID_TO_MODE[button_id][1])
    # use case list for selecting voice_id for each speaker
    use_case = BUTTON_ID_TO_MODE[button_id][1]

    if mode is None:
        return jsonify({"audio_path": "","message": "Please select any of Kotodamas!", "transformed_text": "Please select any of Kotodamas!"})
        
    # generate task id (unique)
    task_id = str(uuid.uuid4())
    
    # transform text
    try:
        transformed_text = text2text(text, mode)
        # format for display
    except:
        message = f'Failed to transform text style with id={task_id}'
        return jsonify({"audio_path": "","message": message,"transformed_text": message})
    # transform text to audio and save
    try:
        audio_path = transformed_text2audio(transformed_text, mode, use_case, task_id)
        message = "Success!"
        return jsonify({"audio_path": audio_path,"message": message,"transformed_text": display_text(transformed_text, mode)})

    except:
        message = f'Failed to transform text to audio...'
        return jsonify({"audio_path": "","message": message,"transformed_text":"Failed to transform text to audio..."})

if __name__ == '__main__':
    app.run(debug=True)

