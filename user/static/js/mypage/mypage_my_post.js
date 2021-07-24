const onClickMyPost = async(user_id) => {
    try{
        const options = {
            url: '/profile/mypage/post/contact/',
            method: 'POST',
            data: {
                user_id: user_id,
            }
        }
    const response = await axios(options)
    const responseOK = response && response.status === 200 && response.statusText === 'OK'
    if (responseOK) {
        const data = response.data
        listMyPost(data.contacts)
    }
    } catch (error) {
        console.log(error)
    }
}
const listMyPost = (contacts) => {
        // local-bar 변경
        const postPortfolio = document.querySelector('#post__portfolio');
        const postMyPost = document.querySelector('#post__my-post');
        const postSavedPost = document.querySelector('#post__saved-post');
        const postPortfolioSelected = document.querySelector('#post__portfolio-selected');
        const postMyPostSelected = document.querySelector('#post__my-post-selected');
        const postSavedPostSelected = document.querySelector('#post__saved-post-selected');
        const postMyContact = document.querySelector('#post__my-contact');
        const postMyPlace = document.querySelector('#post__my-place');
        postPortfolio.className = "";
        postMyPost.className = "post__local-bar-selected";
        postSavedPost.className = "";
        postPortfolioSelected.className = "post__not-selected";
        postMyPostSelected.className = "";
        postSavedPostSelected.className = "post__not-selected";
        postMyContact.className = "post__local-sub-bar-selected";
        postMyPlace.className = "";

        // 게시글 변경
        const postContainer = document.querySelector('.post__container');
        postContainer.innerHTML='';
        for(let i=0; i<contacts.length; i++){
            postContainer.innerHTML+=`<div class="post__item">`+
                `<a href=http://127.0.0.1:8000/contact/detail/${contacts[i].id}>`+
                    `<figure class="post__image">`+
                        `<img src=${contacts[i].thumbnail_url}>`+
                        `<figcaption>`+
                            `<div class="post__info">`+
                                `<p class="post__title">${contacts[i].title}</p>`+
                                `<div>`+
                                    `<p class="post__comment">`+
                                        `<i class="far fa-comment-dots"></i>`+
                                        `<span>${contacts[i].comment_count}</span>`+
                                    `</p>`+
                                    `<p class="post__bookmark">`+
                                        `<i class="fas fa-bookmark"></i>`+
                                        `<span>${contacts[i].bookmark_count}</span>`+
                                    `</p>`+
                                `</div>`+
                            `</div>`+
                        `</figcaption>`+
                    `</figure>`+
                `</a>`+
            `</div>`
        }
}