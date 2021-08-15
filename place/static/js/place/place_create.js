//image field_파일명 추가
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

//상호무페이_pay control, 상호무페이 체크 시 0 입력 및 0 이상의 숫자 입력 불가능
const noPay = document.querySelector('#id_free');
const payField = document.querySelector('#id_pay');
noPay.addEventListener('change',function(){
    if(noPay.checked){
        payField.value = 0;
    }else{
        payField.value = '';
    }
});