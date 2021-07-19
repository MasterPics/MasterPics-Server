( /* att_zone : 이미지들이 들어갈 위치 id, images : file tag id */
  imageView = function imageView(att_zone, images){

    var attZone = document.getElementById(att_zone);
    var btnAtt = document.querySelector(".images .form")
    var sel_files = [];
    
    // 이미지와 체크 박스를 감싸고 있는 div 속성
    var div_style = 'display:inline-block;position:relative;padding:3px;overflow:hidden;';
    // 미리보기 이미지 속성
    var img_style = 'width:68px;height:68px;margin-right:1px;margin-bottom:4px;z-index:none;object-fit:cover;';
    // 이미지안에 표시되는 체크박스의 속성
    var chk_style = 'width:14px;height:14px;position:absolute;right:10px;top:10px;'
                  + 'font-size:10px;z-index:999;background-color:#c4c4c4;color:#ffffff;border:0;border-radius:100%;';
  
    btnAtt.onchange = function(e){
      var files = e.target.files;
      var fileArr = Array.prototype.slice.call(files)
      for(f of fileArr){
        imageLoader(f);
      }
    }  
    
  
    // 탐색기에서 드래그앤 드롭 사용
    attZone.addEventListener('dragenter', function(e){
      e.preventDefault();
      e.stopPropagation();
    }, false)
    
    attZone.addEventListener('dragover', function(e){
      e.preventDefault();
      e.stopPropagation();
      
    }, false)
  
    attZone.addEventListener('drop', function(e){
      var files = {};
      e.preventDefault();
      e.stopPropagation();
      var dt = e.dataTransfer;
      files = dt.files;
      for(f of files){
        imageLoader(f);
      }
      
    }, false)
    

    
    /*첨부된 이미리즐을 배열에 넣고 미리보기 */
    imageLoader = function(file){
      sel_files.push(file);
      var reader = new FileReader();
      reader.onload = function(ee){
        let img = document.createElement('img')
        img.setAttribute('style', img_style)
        img.src = ee.target.result;
        attZone.appendChild(makeDiv(img, file));
      }
      
      reader.readAsDataURL(file);
    }
    
    /*첨부된 파일이 있는 경우 checkbox와 함께 attZone에 추가할 div를 만들어 반환 */
    makeDiv = function(img, file){
      var div = document.createElement('div')
      div.setAttribute('style', div_style)
      
      var images = document.createElement('input')
      images.setAttribute('type', 'button')
      images.setAttribute('value', 'x')
      images.setAttribute('delFile', file.name);
      images.setAttribute('style', chk_style);
      images.onclick = function(ev){
        var ele = ev.srcElement;
        var delFile = ele.getAttribute('delFile');
        for(var i=0 ;i<sel_files.length; i++){
          if(delFile== sel_files[i].name){
            sel_files.splice(i, 1);      
          }
        }
        
        dt = new DataTransfer();
        for(f in sel_files) {
          var file = sel_files[f];
          dt.items.add(file);
        }
        btnAtt.files = dt.files;
        var p = ele.parentNode;
        attZone.removeChild(p)
      }
      div.appendChild(img)
      div.appendChild(images)
      return div
    }
  }
)('att_zone', 'images')