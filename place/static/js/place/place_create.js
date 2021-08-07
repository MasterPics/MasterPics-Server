window.onload = function(){
    const target = document.querySelector('#id_images') //이미지 파일 input
    const targetHTML = document.querySelector('.images'); //이미지 필드 박스
    const fileBox = document.createElement('div'); //파일 리스트 박스를 새로 생성

    // const fileInput = document.createElement('div');
    // fileInput.classList.add('image-field-custom')
    // const fileInputContent = 
    //     '<span class="custom-file-btn"><i class="far fa-folder-open" aria-hidden="true"></i></span><span>이미지 파일을 등록해주세요.</span>'
    // fileInput.innerHTML = fileInputContent;
    // targetHTML.appendChild(fileInput);

    target.addEventListener('change',function(){
        fileList = "";
        for(i = 0; i < target.files.length; i++){
            fileList += '<p class="filename">' + target.files[i].name + '</p>';
        }
        fileBox.innerHTML = fileList;
        targetHTML.appendChild(fileBox);
    })
}