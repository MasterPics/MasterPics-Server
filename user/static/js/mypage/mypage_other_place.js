const onClickMyPlace = async(user_id) => {
    try{
        const options = {
            url: '/profile/mypage/post/place/',
            method: 'POST',
            data: {
                user_id: user_id,
            }
        }
    const response = await axios(options)
    const responseOK = response && response.status === 200 && response.statusText === 'OK'
    if (responseOK) {
        const data = response.data
        listMyPlace(data.places)
    }
    } catch (error) {
        console.log(error)
    }
}
const listMyPlace = (places) => {
        // local-bar 변경
        const postMyContact = document.querySelector('#post__my-contact');
        const postMyPlace = document.querySelector('#post__my-place');
        postMyContact.className = "";
        postMyPlace.className = "post__local-sub-bar-selected";

        // 게시글 변경
        const postContainer = document.querySelector('.post__container');
        postContainer.innerHTML='';
        for(let i=0; i<places.length; i++){
            postContainer.innerHTML+=`<div class="post__item">`+
                `<a href=http://127.0.0.1:8000/place/detail/${places[i].id}>`+
                    `<figure class="post__image">`+
                        `<img src=${places[i].thumbnail_url}>`+
                        `<figcaption>`+
                            `<div class="post__info">`+
                                `<p class="post__title">${places[i].title}</p>`+
                                `<div>`+
                                    `<p class="post__comment">`+
                                        `<i class="far fa-comment-dots"></i>`+
                                        `<span>${places[i].comment_count}</span>`+
                                    `</p>`+
                                    `<p class="post__like">`+
                                    `<i class="fas fa-heart"></i>`+
                                    `<span>${places[i].like_count}</span>`+
                                    `</p>`+
                                    `<p class="post__bookmark">`+
                                        `<i class="fas fa-bookmark"></i>`+
                                        `<span>${places[i].bookmark_count}</span>`+
                                    `</p>`+
                                `</div>`+
                            `</div>`+
                        `</figcaption>`+
                    `</figure>`+
                `</a>`+
            `</div>`
        }
}