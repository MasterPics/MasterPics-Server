window.onload = function(){
    target = document.querySelector('.file_attach .form');
    target.addEventListener('change', function(){
        fileList = "";
        for(i = 0; i < target.files.length; i++){
            fileList += target.files[i].name + '<br>';
        }
        target2 = document.getElementById('showFiles');
        target2.innerHTML = "변경: " + fileList;
    });
    var cur = document.querySelector('.file_attach .form').previousSibling.previousSibling.previousSibling

    target2 = document.getElementById('showPrevFiles');
    target2.innerHTML = "현재: " + cur.textContent;
}