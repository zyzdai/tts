# encoding=utf-8
import hashlib
import os
from flask import Flask, request, jsonify, make_response, send_from_directory
import re
import time
import uuid
app = Flask(__name__)
# tts
voiceMap = {
    "xiaoxiao": "zh-CN-XiaoxiaoNeural",
    "xiaoyi": "zh-CN-XiaoyiNeural",
    "yunjian": "zh-CN-YunjianNeural",
    "yunxi": "zh-CN-YunxiNeural",
    "yunxia": "zh-CN-YunxiaNeural",
    "yunyang": "zh-CN-YunyangNeural",
    "xiaobei": "zh-CN-liaoning-XiaobeiNeural",
    "xiaoni": "zh-CN-shaanxi-XiaoniNeural",
    "hiugaai": "zh-HK-HiuGaaiNeural",
    "hiumaan": "zh-HK-HiuMaanNeural",
    "wanlung": "zh-HK-WanLungNeural",
    "hsiaochen": "zh-TW-HsiaoChenNeural",
    "hsioayu": "zh-TW-HsiaoYuNeural",
    "yunjhe": "zh-TW-YunJheNeural",
}

def getVoiceById(voiceId):
    return voiceMap.get(voiceId)

# 删除html标签
def remove_html(string):
    regex = re.compile(r'<[^>]+>')
    return regex.sub('', string)


def createAudio(text, voiceId, rate):
    new_text = remove_html(text)
    voice = getVoiceById(voiceId)
    rate = f"+{rate}%"
    if not voice:
        return "error params"
    data_md5 = hashlib.md5((text+voiceId+rate).encode('utf-8')).hexdigest()
    file_name = f'{data_md5}.mp3'
    if os.path.exists(file_name):
        pwdPath = os.getcwd()
        filePath = pwdPath + "/" + file_name
        return filePath
    pwdPath = os.getcwd()
    filePath = pwdPath + "/" + file_name
    dirPath = os.path.dirname(filePath)
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)
    if not os.path.exists(filePath):
        # 用open创建文件 兼容mac
        open(filePath, 'a').close()
    script = 'edge-tts --rate=' + rate + ' --voice ' + voice + ' --text "' + new_text + '" --write-media ' + filePath
    os.system(script)
    return filePath

@app.route('/tts', methods=['POST', 'GET'])
def tts():
    clear_tmp_file()
    text = request.args.get('text')
    if len(text) <= 0:
        return jsonify({"code": "异常", "message": "text参数不能为空"})
    voice = request.args.get('voice')
    rate = request.args.get('rate')
    print(text, voice, rate)
    filePath = createAudio(text, voice, rate)
    r = os.path.split(filePath)
    print(r)
    try:
        response = make_response(
            send_from_directory(r[0], r[1], as_attachment=True))
        return response
    except Exception as e:
        return jsonify({"code": "异常", "message": "{}".format(e)})



def clear_tmp_file(sec=120):
    zip_file_list = os.listdir(os.getcwd())
    for file in zip_file_list:
        if file.endswith('.zip') or file.endswith('mp3') or file.endswith('jpg'):
            zip_file_time = os.path.getmtime(file)
            if (time.time() - zip_file_time) > sec:
                os.remove(file)

@app.route('/', methods=['GET', 'POST'])
def index():
    return 'OK'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9898)