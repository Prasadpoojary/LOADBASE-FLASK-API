from flask import Flask,render_template,request,jsonify
from flask_cors import CORS, cross_origin
import youtube_dl

app=Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/youtube/api", methods=['GET','OPTIONS'])
@cross_origin()
def youtube():
        url=request.args.get('url')
        ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})

        with ydl:
            source = ydl.extract_info(url,download=False)

        audio = []
        video = []
        for stream in source['formats']:
            if stream['vcodec'] == "none" and stream['acodec'] != "none":
                audio.append({'type': stream['ext'], 'url': stream['url'], 'filesize': stream['filesize'],'format': stream['format_note']})
            if stream['vcodec'] != "none" and stream['acodec'] != "none":
                video.append({'type': stream['ext'], 'url': stream['url'], 'filesize': stream['filesize'],'format': stream['format_note']})
        responce = {'audio': audio, 'video': video}
        responce=jsonify(responce)
        return responce


if __name__ == '__main__':
    app.run(debug=True)
