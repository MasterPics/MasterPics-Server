const onClickSavedContact = async(user_id) => {
    try{
        const options = {
            url: '/profile/mypage/bookmark/contact/',
            method: 'POST',
            data: {
                user_id: user_id,
            }
        }
    const response = await axios(options)
    const responseOK = response && response.status === 200 && response.statusText === 'OK'
    if (responseOK) {
        const data = response.data
        listSavedContact(data.bookmarked_contacts)
    }
    } catch (error) {
        console.log(error)
    }
}
const listSavedContact = (bookmarked_contacts) => {
    // local-bar 변경
    const postSavedPortfolio= document.querySelector('#post__saved-portfolio');
    const postSavedContact = document.querySelector('#post__saved-contact');
    const postSavedPlace = document.querySelector('#post__saved-place');
    postSavedPortfolio.className = "";
    postSavedContact.className = "post__local-sub-bar-selected";
    postSavedPlace.className = "";

    // 게시글 변경
    const postContainer = document.querySelector('.post__container');
    postContainer.innerHTML='';
    for(let i=0; i<bookmarked_contacts.length; i++){
        postContainer.innerHTML+=`<div class="post__item">`+
            `<figure class="post__image">`+
                `<img src=${bookmarked_contacts[i].thumbnail_url}>`+
                `<figcaption>`+
                    `<div class="post__info">`+
                        `<p class="post__title">${bookmarked_contacts[i].title}</p>`+
                        `<div>`+
                            `<p class="post__comment">`+
                                `<i class="far fa-comment-dots"></i>`+
                                `<span>${bookmarked_contacts[i].comment_count}</span>`+
                            `</p>`+
                            `<p class="post__bookmark save save-${bookmarked_contacts[i].id}">`+
                            `</p>`+
                        `</div>`+
                    `</div>`+
                `</figcaption>`+
            `</figure>`+
        `</div>`
    }

    // save 기능
    for(let i=0; i<bookmarked_contacts.length; i++){
        const save = document.querySelector(`.save-${bookmarked_contacts[i].id}`);
        if( bookmarked_contacts[i].is_bookmark === true ){
            save.innerHTML = `<i class="fas fa-bookmark" type="submit" onclick="onClickContactSave(${bookmarked_contacts[i].id})" name="type" value="save"></i>`
        } else {
            save.innerHTML = `<i class="far fa-bookmark" type="submit" onclick="onClickContactSave(${bookmarked_contacts[i].id})" name="type" value="save"></i>`
        }
    }
}