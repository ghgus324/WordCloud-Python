# 워드 클라우드에 필요한 라이브러리를 불러옵니다.
from wordcloud import WordCloud
# 한국어 자연어 처리 라이브러리를 불러옵니다.
from konlpy.tag import Twitter
# 명사의 출현 빈도를 세는 라이브러리를 불러옵니다.
from collections import Counter
# 그래프 생성에 필요한 라이브러리를 불러옵니다.
import matplotlib.pyplot as plt
# Flask 웹 서버 구축에 필요한 라이브러리를 불러옵니다.
from flask import Flask, request, jsonify
# CORS를 처리합니다.
from flask_cors import CORS
# 파일에 접근하기 위한 라이브러리를 불러옵니다.
import os

# 플라스크 웹 서버 객체 생성합니다.
app = Flask(__name__, static_folder='outputs')
CORS(app)

# 폰트 경로 설정
font_path = 'NanumGothic.ttf'


def get_tags(text):
    t = Twitter()
    nouns = t.nouns(text)
    count = Counter(nouns)
    return count


def make_cloud_image(tags, file_name):
    # 만들고자 하는 워드 클라우드의 기본 설정을 진행합니다.
    word_cloud = WordCloud(
        font_path=font_path,
        width=800,
        height=800,
        background_color="white"
    )
    word_cloud = word_cloud.generate_from_frequencies(tags)
    fig = plt.figure(figsize=(10, 10))
    plt.imshow(word_cloud)
    plt.axis("off")
    # 만들어진 이미지 객체를 파일 형태로 저장합니다.
    fig.savefig("outputs/{0}.png".format(file_name))

def process_from_text(text):
    tags = get_tags(text)
    make_cloud_image(tags,"output")

@app.route("/process", methods=['GET', 'POST'])
def process():
    # process에 접속 됬을때 사용자에게 request.json을 받아서
        content = request.json
        words = {}
        if content['words'] is not None:
            for data in content['words'].values():
                words[data['word']] = data['weight'] #단어 내용에 따라 가중치 정보를 넣는다
        #사용자가 text를 보내면 처리할 수 있도록 메소드 만듬
        process_from_text(content['text'])
        return jsonify(words)

# 실제로 프로그램이 시작 되었을때 플라스크로 작성된 이 웹서버가 정상적으로 작동하면 됨
if __name__ == '__main__':
    app.run('0.0.0.0',port=5000)