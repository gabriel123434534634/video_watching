from __future__ import unicode_literals
from bottle import run, route, static_file, request, template, redirect
import yt_dlp
import urllib
import shutil
import pl
import random
import os
import shutil
json2 = pl.json("index.json")
@route("/")
def index():
    return template("watching.html")
@route("/request_delete_all_videos")
def index():
    shutil.rmtree("./videos")
    json2["videos"] = {}
    json2.up()
    os.mkdir("videos")
    return "Ok"

@route("/delete_videos")
def index():
    return static_file("delete.html", root=".")
@route("/video_list")
def index():
    return str(json2["videos"])
@route("/video")
def index():
    return static_file(json2["last_video"], root="./videos")
@route("/static")
def index():
    query = request.query
    return static_file(filename=query['path'], root=".")
@route("/generate_video", method="POST")
def index():
    import requests
    import json
    data2 = request.forms.get('json')
    data2 = json.loads(data2)
    link = data2['link']
    print(link)
    from pytube import YouTube
    def download(video_url):
        filename = f"{random.randint(0, 9999999)}.mp4"
        while filename in os.listdir("videos"):
            filename = f"{random.randint(0, 9999999)}.mp4"
        json2["last_video"] = filename
        json2.up()
        ydl_opts = {'outtmpl': "videos/"+filename,
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        print("highest resolution")
        print("Download is completed successfully")
        info_dict = ydl.extract_info(video_url, download=False)
        video_title = info_dict.get('title', None)
        json2["videos"][video_title] = "videos/"+filename
        json2.up()
    download(link)
    return "redirect"
run(host="0.0.0.0", port=8080)
# import requests
# import subprocess

# # URL do vídeo que você deseja baixar
# url = 'https://www.youtube.com/watch?v=aRRJN2NbgcQ'

# # Use a biblioteca requests para fazer uma solicitação GET à página do vídeo
# response = requests.get(url)

# # Obtenha o código HTML da página do vídeo
# html = response.text

# # Procure pela URL do arquivo de vídeo na página HTML
# # Procure pela URL do arquivo de vídeo na página HTML
# start = html.find('adaptive_fmts') + len('adaptive_fmts')
# end = html.find('&', start)
# url_encoded_fmt_stream_map = html[start:end].replace('\u0026', '&')

# # Verifique se a string 'url=' está presente na variável url_encoded_fmt_stream_map
# if 'url=' in url_encoded_fmt_stream_map:
#     # Use a função split para dividir a string em uma lista de strings usando 'url=' como separador
#     split_url = url_encoded_fmt_stream_map.split('url=')
#     # Verifique se a lista tem pelo menos dois elementos antes de acessar o segundo elemento
#     if len(split_url) >= 2:
#         url = split_url[1]
#     else:
#         print('Erro: URL do vídeo não encontrada.')
# else:
#     print('Erro: URL do vídeo não encontrada.')

# # Use a biblioteca requests novamente para fazer uma solicitação GET à URL do arquivo de vídeo
# response = requests.get(url)

# # Salve o arquivo de vídeo na pasta atual
# with open('video.mp4', 'wb') as f:
#     f.write(response.content)

# # Converta o arquivo de vídeo para o formato desejado usando a biblioteca ffmpeg
# subprocess.run(['ffmpeg', '-i', 'video.mp4', '-c:v', 'copy', '-c:a', 'copy', 'video.mp3'])
