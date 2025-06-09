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
app.config['MAX_STORAGE_SIZE'] = 500 * 1024 * 1024 # 500MB

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

        # Convertendo o arquivo pra gif. Preciso fazer um tratamento de erro melhor
        os.system(f"ffmpeg -i {filepath} -v 0 -f yuv4mpegpipe - | gifski-1_32_0 -o {app.config['GIF_UPLOAD_FOLDER']}/{filename}.gif -")
        
        # Deletando o arquivo original
        try:
            os.remove(filepath)
        except:
            return "<h2>Ocorreu um erro inesperado, o video original sumiu do servidor misteriosamente. Se o problema persistir entra em contato comigo no e-mail<h2>"
        
        return redirect(url_for('get_gif', filename=filename+".gif"))
    return "<h2>Erro inesperado</h2>"

@app.route("/gifs/<filename>")
def get_gif(filename):
    filepath = os.path.join(app.config['GIF_UPLOAD_FOLDER'], escape(filename))
    fileExists = os.path.isfile(filepath)
    isGif = escape(filename).endswith(".gif")

    if not fileExists or not isGif:
        return "<h2>Arquivo inexistente</h2>", 404

    return send_file(filepath)

if __name__ == '__main__':  
   app.run()