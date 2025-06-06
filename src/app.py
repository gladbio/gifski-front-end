# IMPORTANTE: Saber mais sobre a função Vsync (deprecated) e fps_mode, e se possivel adicionar opções no site
# por enquanto só funciona com gifs de framerate constante (CFR)

import secrets, os
from glob import glob
from flask import Flask, render_template, request, send_file, redirect, url_for
from markupsafe import escape

app = Flask(__name__, root_path="/home/app")
app.config['GIF_UPLOAD_FOLDER'] = "/home/app/gifs"
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024 # 20MB
app.config['USED_STORAGE'] = 0
app.config['MAX_FILESIZE'] = 1024 * 1024 * 1024 # 1GB

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/convert", methods=['POST'])
def convert():
    if 'file' not in request.files:
        # TO DO, técnicamente é requisição post feita sem o campo de arquivo
        return "Requisição POST feita sem arquivo anexado, voltando a página inicial"
    
    file = request.files['file']

    if file.filename == '':
        # TO DO
        return "Nenhum arquivo selecionado, voltando a página inicial"
    
    if(file.filename.endswith(".mp4")):
        # Checar se tem armazenamento o suficiente (Em progresso)
        # app.config['USED_STORAGE'] += file.seek(0, os.SEEK_END).tell() # Vai até o final do arquivo e vê a posição do ultimo byte
        # file.seek(0, os.SEEK_SET)
        # return app.config['USED_STORAGE']

        # Salvar o arquivo
        filename = hex(secrets.randbits(128))[2:] # Gerar uma string hexadecimal aleatória de 32 caracteres
        filepath = os.path.join(app.config['GIF_UPLOAD_FOLDER'], filename + ".mp4")
        file.save(filepath)

        # Convertendo o arquivo pra gif -- preciso fazer tratamento de erro melhor
        os.system(f"ffmpeg -i {filepath} -v 0 -f yuv4mpegpipe - | gifski-1_32_0 -o {app.config['GIF_UPLOAD_FOLDER']}/{filename}.gif -")
        

        # Deletando o arquivo original
        try:
            os.remove(filepath)
        except:
            return "Ocorreu um erro inesperado, o video original sumiu do servidor misteriosamente. Se o problema persistir entra em contato comigo no e-mail"
        return redirect(url_for('get_gif', id=filename+".gif"))
    return "Erro inesperado"

@app.route("/gif/<id>")
def get_gif(id):
    filepath = os.path.join(app.config['GIF_UPLOAD_FOLDER'], escape(id))
    fileExists = os.path.isfile(filepath)
    isGif = escape(id).endswith(".gif")

    if not fileExists or not isGif:
        return "Arquivo inválido, voltando a página inicial"

    return send_file(filepath)

if __name__ == '__main__':  
   app.run()