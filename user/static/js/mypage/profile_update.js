window.onload = function(){
    // 새로운 이미지 입력 시 preview
    target = document.querySelector('#id_image');
    target.onchange = function(e){
        var files = e.target.files;
        var fileArr = Array.prototype.slice.call(files)
        for(f of fileArr){
          imageLoader(f);
        }
    }
    imageLoader = function(file){
        var sel_files = [];
        sel_files.push(file);
        var reader = new FileReader();
        reader.onload = function(ee){
          target2 = document.getElementById('form__img-preview');
          target2.src = ee.target.result;
        }
        
        reader.readAsDataURL(file);
    }  



    // 기존 이미지 preview
    var cur = document.querySelector('.form__input-image').firstChild.nextSibling;

    target2 = document.getElementById('form__img-preview');
    target2.src = cur.href;


    // email 변경 불가
    var email = document.querySelector('#id_email');

    email.readOnly=true;
}