
var mapContainer = document.getElementById('map'), // 지도를 표시할 div 
    mapOption = { 
        center: new kakao.maps.LatLng(33.450701, 126.570667), // 지도의 중심좌표
        level: 3 // 지도의 확대 레벨
    };

// 지도를 표시할 div와  지도 옵션으로  지도를 생성합니다
var map = new kakao.maps.Map(mapContainer, mapOption); 
// 주소-좌표 변환 객체를 생성합니다
var geocoder = new kakao.maps.services.Geocoder();

// 주소로 좌표를 검색합니다

geocoder.addressSearch(address, function(result, status) {

    // 정상적으로 검색이 완료됐으면 
     if (status === kakao.maps.services.Status.OK) {

        var coords = new kakao.maps.LatLng(result[0].y, result[0].x);

        // 결과값으로 받은 위치를 마커로 표시합니다
        var marker = new kakao.maps.Marker({
            map: map,
            position: coords
        });

        // 인포윈도우로 장소에 대한 설명을 표시합니다
        /*
        var infowindow = new kakao.maps.InfoWindow({
            content: '<div style="width:150px;text-align:center;padding:6px 0;">여기에 있어요!</div>'
        });
        infowindow.open(map, marker);
        */
        // 지도의 중심을 결과값으로 받은 위치로 이동시킵니다
        map.setCenter(coords);
    } 
});  

/*
const onClickSave = async (place_id) => {
    console.log("save?");
    try {
        const url = '/place/';
        const {
        data
        } = await axios.post(url, {
        place_id,
        })
        modify(data.place_id, data.is_saved)

        const options = {
            url: '/place/save/',
            method: 'POST',
            data: {
                place_id: place_id,
            }
        }
        const response = await axios(options)
        const responseOK = response && response.status === 200 && response.statusText === 'OK'
        if (responseOK) {
            const data = response.data
            //modify에서는 이미 뒤집힌 is_saved 값이 들어감!
            modify(data.place_id, data.is_saved)
        }
    } catch (error) {
        console.log(error)
    }
}

const modify = (place_id, is_saved) => {
    const save = document.querySelector(`.save-${place_id} i`);
    const save_content = document.querySelector(`.save-${place_id} .save__content`)
    const num = save_content.innerText; // [ {{ place.save_users.count }} ]
    console.log(num)
    if (is_saved === true) {

        save.className = "fas fa-bookmark";

        const count = Number(num) + 1;
        save_content.innerHTML = count
    } else {
        save.className = "far fa-bookmark";

        const count = Number(num) - 1;
        save_content.innerHTML = count
    }

}
*/
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
    const url = `/place/comment_delete/`;

    const {
        data
    } = await axios.post(url, {
        commentId
    })
    modifyDeleteComment(data.comment_id);
}


