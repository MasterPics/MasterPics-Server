var mapContainer = document.getElementById('map'), // 지도를 표시할 div 
    mapOption = { 
        center: new kakao.maps.LatLng(33.450701, 126.570667), // 지도의 중심좌표
        level: 3 // 지도의 확대 레벨
    };

// 지도를 표시할 div와  지도 옵션으로  지도를 생성합니다
var map = new kakao.maps.Map(mapContainer, mapOption); 
// 주소-좌표 변환 객체를 생성합니다
var geocoder = new kakao.maps.services.Geocoder();

let userMarkerSrc = 'https://i.imgur.com/rsjHKsd.png', // 출발 마커이미지의 주소입니다    
    userMarkerSize = new kakao.maps.Size(35, 60), // 출발 마커이미지의 크기입니다 
    userMarkerOption = { 
    offset: new kakao.maps.Point(17, 43) // 출발 마커이미지에서 마커의 좌표에 일치시킬 좌표를 설정합니다 (기본값은 이미지의 가운데 아래입니다)
};

let userMarkerImage = new kakao.maps.MarkerImage(userMarkerSrc, userMarkerSize, userMarkerOption);

// 주소로 좌표를 검색합니다
geocoder.addressSearch(address, function(result, status) {

    // 정상적으로 검색이 완료됐으면 
     if (status === kakao.maps.services.Status.OK) {

        var coords = new kakao.maps.LatLng(result[0].y, result[0].x);

        // 결과값으로 받은 위치를 마커로 표시합니다
        var marker = new kakao.maps.Marker({
            position: coords,
            image: userMarkerImage
        });
        // 지도의 중심을 결과값으로 받은 위치로 이동시킵니다
        marker.setMap(map);
        map.setCenter(coords);
    } 
});  


const modifyNewComment = (place_id, comment_id, value) => {
    const CommentContainer = document.querySelector(`.comments-${place_id}`);
    console.log(CommentContainer)

    const tempContainer = document.createElement("div");
    tempContainer.className = `comment comment-${comment_id}`;

    const commentContent = document.createElement("div")
    commentContent.className = `comment-content`;

    const commentImage = document.createElement("div")
    commentImage.className = `comment-image`;
    const commentUserImage = document.createElement("img")
    commentUserImage.setAttribute('src',userImage);
    commentImage.appendChild(commentUserImage);

    const commentInfo = document.createElement("div")
    const commentWriter =  document.createElement("span")
    commentWriter.className = `comment-writer`;
    commentWriter.textContent = writer;

    const commentCreated =  document.createElement("span")
    commentCreated.className = `comment-created`;
    commentCreated.textContent = "방금 전";

    const commentText =  document.createElement("p")
    commentText.className = `comment-text`;
    commentText.textContent = value;

    const deleteBtn = document.createElement("input");
    deleteBtn.className = "delete";
    deleteBtn.setAttribute("type", "submit");
    deleteBtn.setAttribute("value", "삭제");
    deleteBtn.setAttribute("onclick", `onClickDeleteComment(${comment_id})`)

    commentInfo.appendChild(commentWriter)
    commentInfo.appendChild(commentCreated)
    commentInfo.appendChild(commentText)

    commentContent.appendChild(commentImage)
    commentContent.appendChild(commentInfo)

    tempContainer.appendChild(commentContent)
    tempContainer.appendChild(deleteBtn);
    CommentContainer.appendChild(tempContainer);
}

const onClickNewComment = async (id) => {
    try{
        const url = `/place/comment_create/`;
        const value = document.querySelector(`.createComment-${id} .comment__value`);
        const value_text = value.value
        const {
            data
        } = await axios.post(url, {
            id,
            value: value_text
        })

        modifyNewComment(id, data.comment_id, data.value);

        const cmt = document.querySelector('.comment__value')
        cmt.value = ''
    }   catch (error) {
        console.log(error)
    }

}

const modifyDeleteComment = (comment_id) => {
    const targetCommentContainer = document.querySelector(`.comment-${comment_id}`);
    targetCommentContainer.remove();
}

const onClickDeleteComment = async (commentId) => {
    alert('start');
    if(confirm("댓글을 삭제하시겠습니까?")){
        alert("1");
        const url = `/place/comment_delete/`;
        alert("2");
        const {
            data
        } = await axios.post(url, {
            commentId
        })
        alert("3");
        modifyDeleteComment(data.comment_id);
    }else{
        alert("ohno");
        return;
    }
    
}

//enter event
// document.getElementById("comment_submit").onkeyup = function(id) {
//     onClickNewComment(id);
// }
