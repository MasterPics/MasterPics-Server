( /* att_zone : 이미지들이 들어갈 위치 id, id_images : file tag id */
  imageView = function imageView(att_zone, id_images) {

    var attZone = document.getElementById(att_zone);
    var btnAtt = document.getElementById(id_images)
    var sel_files = [];

    btnAtt.onchange = function (e) {
      var files = e.target.files;
      var fileArr = Array.prototype.slice.call(files)
      if (existingImgCnt) {
        if (existingImgCnt - delete_list.length + sel_files.length + fileArr.length > 10) {
          alert('최대 10장까지 업로드 가능합니다.');
          e.target.value = '';
        }
        else {
          for (f of fileArr) {
            imageLoader(f);
          }
        }
      }
      else {
        if (sel_files.length + fileArr.length > 10) {
          alert('최대 10장까지 업로드 가능합니다.');
          e.target.value = '';
        }
        else {
          for (f of fileArr) {
            imageLoader(f);
          }
        }
      }
    }


    // 탐색기에서 드래그앤 드롭 사용
    attZone.addEventListener('dragenter', function (e) {
      e.preventDefault();
      e.stopPropagation();
    }, false)

    attZone.addEventListener('dragover', function (e) {
      e.preventDefault();
      e.stopPropagation();

    }, false)

    attZone.addEventListener('drop', function (e) {
      var files = {};
      e.preventDefault();
      e.stopPropagation();
      var dt = e.dataTransfer;
      files = dt.files;
      if (existingImgCnt) {
        if (existingImgCnt - delete_list.length + sel_files.length + files.length > 10) {
          alert('최대 10장까지 업로드 가능합니다.');
          files = [];
        }
        else {
          for (f of files) {
            imageLoader(f);
          }
        }
      }
      else {
        if (sel_files.length + files.length > 10) {
          alert('최대 10장까지 업로드 가능합니다.');
          files = [];
        }
        else {
          for (f of files) {
            imageLoader(f);
          }
        }
      }
    }, false)



    /*첨부된 이미지를 배열에 넣고 미리보기 */
    imageLoader = function (file) {

      sel_files.push(file);
      var reader = new FileReader();
      reader.onload = function (ee) {

        let img = document.createElement('img')
        img.setAttribute('class', 'image')
        img.src = ee.target.result;
        attZone.appendChild(makeDiv(img, file));
      }

      reader.readAsDataURL(file);
      dt = new DataTransfer();
      for (f in sel_files) {
        var file = sel_files[f];
        dt.items.add(file);
      }
      btnAtt.files = dt.files;
    }

    /*첨부된 파일이 있는 경우 checkbox와 함께 attZone에 추가할 div를 만들어 반환 */
    makeDiv = function (img, file) {
      var div = document.createElement('div')
      div.setAttribute('class', 'image-wrapper')

      var id_images = document.createElement('input')
      id_images.setAttribute('type', 'button')
      id_images.setAttribute('value', 'x')
      id_images.setAttribute('delFile', file.name);
      id_images.setAttribute('class', 'image-check');
      id_images.onclick = function (ev) {
        var ele = ev.srcElement;
        var delFile = ele.getAttribute('delFile');
        for (var i = 0; i < sel_files.length; i++) {
          if (delFile == sel_files[i].name) {
            sel_files.splice(i, 1);
          }
        }

        dt = new DataTransfer();
        for (f in sel_files) {
          var file = sel_files[f];
          dt.items.add(file);
        }
        btnAtt.files = dt.files;
        var p = ele.parentNode;
        attZone.removeChild(p)
      }
      div.appendChild(img)
      div.appendChild(id_images)
      return div
    }
  }
)('att_zone', 'id_images')