delete_list = [] //삭제할 이미지들 누적

function remove(el) {
    var element = el;
    delete_list.push(el.parentNode.classList[1]) //div의 class명이 삭제할 이미지의 pk
    element.parentNode.remove(); //div 제거
}

function remove_all() {
    //앞에서 누적해온 삭제할 이미지들
    for (var i = 0; i < delete_list.length; i++) {
        pk = delete_list[i]; //삭제할 이미지 pk
        $.get('/remove_all/' + pk + '/'); //해당 url에 get요청 보내서 이미지 삭제(core안 urls.py와 views.py)
    }
}