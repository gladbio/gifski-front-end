## Sobre
**Gifski-front-end** é um aplicativo web utilizado para converter vídeos em GIFs através de um servidor local

## Requisitos
- Python (3.12+)
- FFmpeg (7.1.1+)
- Docker *(opcional)* -- Utilizado para hospedagem

## Instalação (Windows)
### FFmpeg
1. Baixe o FFMpeg através do site 
https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
2. Extraia o zip (Preferencialmente em `C:/ffmpeg`)
3. Localize o diretório bin/ e adicione ao $PATH do sistema através do Painel de Controle de acordo com o GIF abaixo

![anim](https://github.com/user-attachments/assets/f190b189-44d4-4965-a6cc-678db31ecf61)

### Python
1. Baixe Python através do site 
https://www.python.org/downloads/
2. Marque a opção "Add Python to PATH" na parte inferior da etapa inicial do instalador
3. Após a instalação, é necessário instalar os requisitos Python através do comando `pip install -r <caminho pro requirements.txt>`

## Utilização
Abra o arquivo `src/app.py` com o Python e acesse o endereço `127.0.0.1:5000` através de seu navegador
