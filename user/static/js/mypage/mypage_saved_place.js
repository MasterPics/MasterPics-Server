const onClickSavedPlace = async(user_id) => {
    try{
        const options = {
            url: '/profile/mypage/bookmark/place/',
            method: 'POST',
            data: {
                user_id: user_id,
            }
        }
    const response = await axios(options)
    const responseOK = response && response.status === 200 && response.statusText === 'OK'
    if (responseOK) {
        const data = response.data
        listSavedPlace(data.bookmarked_places)
    }
    } catch (error) {
        console.log(error)
    }
}
const listSavedPlace = (bookmarked_places) => {
    // local-bar 변경
    const postSavedPortfolio= document.querySelector('#post__saved-portfolio');
    const postSavedContact = document.querySelector('#post__saved-contact');
    const postSavedPlace = document.querySelector('#post__saved-place');
    postSavedPortfolio.className = "";
    postSavedContact.className = "";
    postSavedPlace.className = "post__local-sub-bar-selected";

    // 게시글 변경
    const postContainer = document.querySelector('.post__container');
    postContainer.innerHTML='';
    for(let i=0; i<bookmarked_places.length; i++){
        postContainer.innerHTML+=`<div class="post__item">`+
        `<a href=http://127.0.0.1:8000/place/detail/${bookmarked_places[i].id}>`+
            `<figure class="post__image">`+
                `<img src=${bookmarked_places[i].thumbnail_url}>`+
                `<figcaption>`+
                    `<div class="post__info">`+
                        `<p class="post__title">${bookmarked_places[i].title}</p>`+
                        `<div>`+
                            `<p class="post__comment">`+
                                `<i class="far fa-comment-dots"></i>`+
                                `<span>${bookmarked_places[i].comment_count}</span>`+
                            `</p>`+
                            `<p class="post__like">`+
                            `<i class="fas fa-heart"></i>`+
                            `<span>${bookmarked_places[i].like_count}</span>`+
                            `</p>`+
                            `<p class="post__bookmark">`+
                                `<i class="fas fa-bookmark"></i>`+
                                `<span>${bookmarked_places[i].bookmark_count}</span>`+
                            `</p>`+
                        `</div>`+
                    `</div>`+
                `</figcaption>`+
            `</figure>`+
        `</a>`+
    `</div>`
    }

/*     // save 기능
    for(let i=0; i<bookmarked_places.length; i++){
        const save = document.querySelector(`.save-${bookmarked_places[i].id}`);
        if( bookmarked_places[i].is_bookmark === true ){
            save.innerHTML = `<i class="fas fa-bookmark" type="submit" onclick="onClickPlaceSave(${bookmarked_places[i].id})" name="type" value="save"></i>`
        } else {
            save.innerHTML = `<i class="far fa-bookmark" type="submit" onclick="onClickPlaceSave(${bookmarked_places[i].id})" name="type" value="save"></i>`
        }
    } */
}