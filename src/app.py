# TODO: multithreading (pra cada usuário), compartilhamento de recurso (a conversão ta sendo feita nas mesmas threads q o aplicativo roda), tratamento de erro

import secrets, os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, send_file, redirect, url_for
from pathlib import PureWindowsPath, PurePosixPath

app = Flask(__name__)
app.config['GIF_UPLOAD_FOLDER'] = "./gifs"
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024 # 20MB
app.config['USED_STORAGE'] = 0
app.config['MAX_STORAGE_SIZE'] = 500 * 1024 * 1024 # 500MB

def videoToGif(videoFilePath, convertedFilename):
    if(os.name == "posix"):
        os.system( str( PurePosixPath(f"ffmpeg -i {videoFilePath} -v 0 -f yuv4mpegpipe - | gifski-1_32_0 -o {app.config['GIF_UPLOAD_FOLDER']}/{convertedFilename}.gif -")))
    elif(os.name == "nt"):
        os.system( str( PureWindowsPath(f"ffmpeg -i {videoFilePath} -v 0 -f yuv4mpegpipe - | ../bin/gifski-1_32_0.exe -o {app.config['GIF_UPLOAD_FOLDER']}/{convertedFilename}.gif -")))
    else:
        raise SystemError('Lista de sistemas compatíveis: Unix/Linux e Windows NT')

@app.route("/")
def index():
    return render_template("index.html", maxFileSize=app.config['MAX_CONTENT_LENGTH'])

@app.route("/convert", methods=['POST'])
def convert():
    if 'file' not in request.files:
        return "Requisição POST feita sem arquivo anexado",
    
    file = request.files['file']

    if file.filename == '':
        return render_template("redirect.html", reason="Nenhum arquivo selecionado, voltando a página inicial...")
    
    if(file.filename.endswith(".mp4")):
        # Checar se tem armazenamento o suficiente (Em progresso)
        # app.config['USED_STORAGE'] += file.seek(0, os.SEEK_END).tell() # Vai até o final do arquivo e vê a posição do ultimo byte
        # file.seek(0, os.SEEK_SET)
        # return app.config['USED_STORAGE']

        # Salvar o arquivo
        filename = hex(secrets.randbits(64))[2:] # Gerar uma string hexadecimal aleatória de 16 caracteres
        filepath = os.path.join(app.config['GIF_UPLOAD_FOLDER'], filename + ".mp4")
        file.save(filepath)
        videoToGif(filepath, filename)

        # Deleta o arquivo original
        try:
            os.remove(filepath)
        except:
            return "<h2>Ocorreu um erro inesperado, o video original sumiu do servidor misteriosamente. Se o problema persistir entra em contato comigo no e-mail<h2>"
        
        return redirect(url_for('get_gif', filename=filename+".gif"))
    
    return "<h2>Tipo de arquivo inválido</h2>"

@app.route("/gifs/<filename>")
def get_gif(filename):
    filepath = os.path.join(app.config['GIF_UPLOAD_FOLDER'], secure_filename(filename))
    fileExists = os.path.isfile(filepath)
    isGif = secure_filename(filename).endswith(".gif")

    if not fileExists or not isGif:
        return "<h2>Arquivo inexistente</h2>", 404

    return send_file(filepath, mimetype="image/gif")

if __name__ == '__main__':
    app.run()