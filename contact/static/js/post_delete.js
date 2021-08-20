function postDelete() {
    const postDelete = document.querySelector('#postDelete');

    if (confirm("게시물을 삭제하시겠습니까?") == true){    //확인
   
        postDelete.submit();
   
    } else{   //취소
        
        return ;
   
    }   
}