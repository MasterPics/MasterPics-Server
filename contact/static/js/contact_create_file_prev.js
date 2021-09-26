// window.onload = function () {
target = document.querySelector('.file_attach .form');
target.addEventListener('change', function () {
    let fileList = "";
    for (i = 0; i < target.files.length; i++) {
        fileList += target.files[i].name + '<br>';
    }
    target2 = document.getElementById('showFiles');
    target2.innerHTML = "파일명: " + fileList;
});
// }