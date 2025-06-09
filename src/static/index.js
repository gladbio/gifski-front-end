function humanFileSize(size) {
    var i = size <= 0 ? 0 : Math.floor(Math.log(size) / Math.log(1024));
    return ((size / 1024**i).toFixed(0)) + ' ' +['Bytes', 'KB', 'MB', 'GB', 'TB'][i];
}

function checkFileSize(inputFile, maxFileSize) {
        file = inputFile.files[0];
        if (file.size > maxFileSize) {
                alert("O tamanho do arquivo excede o limite de " + humanFileSize(maxFileSize)); // To Do: um pop-up mais bonito
                inputFile.value = ''
        }
};