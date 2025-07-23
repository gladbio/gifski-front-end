# TODO: multithreading (pra cada usuário), compartilhamento de recurso (a conversão ta sendo feita nas mesmas threads q o aplicativo roda), tratamento de erro (importante pq ta péssimo)

import secrets, os, subprocess, sys
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, send_file, redirect, url_for
from pathlib import Path

app = Flask(__name__)
app.config['GIF_UPLOAD_FOLDER'] = "./gifs"
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024 # 20MB
app.config['USED_STORAGE'] = 0
app.config['MAX_STORAGE_SIZE'] = 500 * 1024 * 1024 # 500MB
GIFSKI_PATH = "gifski-1_32_0" if os.name == "posix" else "..\\bin\\gifski-1_32_0.exe"
BASE_DIR = Path(__file__).resolve().parent

def abort_app(text: str):
    print(text)

    input("Pressione Enter para sair. . .")
    sys.exit(1)

def videoToGif(videoPath: Path, outputName: str):
    if not videoPath.is_file():
        raise FileNotFoundError(f"Vídeo não encontrado: {videoPath!s}")
    
    outputPath = os.path.join(app.config["GIF_UPLOAD_FOLDER"], outputName+".gif")
    cmd = [
        "ffmpeg",
        "-i", str(videoPath),
        "-v", "0",
        "-f", "yuv4mpegpipe",
        "-",
        "|",
        GIFSKI_PATH,
        "-o", outputPath,
        "-"
    ]

    cmd_str = " ".join(cmd)
    result = subprocess.run(cmd_str, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"Erro na conversão do vídeo para gif\n"
            f"COMANDO: {cmd_str}\n"
            f"STDOUT: {result.stdout}\n"
            f"STDERR: {result.stderr}"
        )

    return os.path.abspath(outputPath)

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
        filepath = Path(os.path.join(app.config['GIF_UPLOAD_FOLDER'], filename + ".mp4"))
        file.save(filepath)
        videoToGif(filepath, filename)

        # Deleta o arquivo original
        try:
            os.remove(filepath)
        except FileNotFoundError:
            app.logger.warning(f'Vídeo não encontrado ao tentar remover: {os.path.abspath(filepath)}')
            return "<h2>Ocorreu um erro inesperado: o vídeo original sumiu do servidor misteriosamente. Se o problema persistir, entre em contato comigo pelo e‑mail.</h2>"
        
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
    os.chdir(BASE_DIR)

    if not os.name.startswith(("nt", "posix")):
        abort_app('Sistema incompatível. Lista de sistemas compatíveis: Unix/Linux e Windows NT')

    if not os.path.exists(app.config['GIF_UPLOAD_FOLDER']):
        try:
            os.makedirs(app.config['GIF_UPLOAD_FOLDER'])
        except OSError as e:
            abort_app(f'Não foi possível criar o diretório "{app.config['GIF_UPLOAD_FOLDER']}": {e.strerror}. Verifique as permissões.')
        
    app.run()
