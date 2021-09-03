const onClickSavedPost = async(user_id) => {
    try{
        const options = {
            url: '/profile/mypage/bookmark/portfolio/',
            method: 'POST',
            data: {
                user_id: user_id,
            }
        }
    const response = await axios(options)
    const responseOK = response && response.status === 200 && response.statusText === 'OK'
    if (responseOK) {
        const data = response.data
        listSavedPost(data.bookmarked_portfolios)
    }
    } catch (error) {
        console.log(error)
    }
}
const listSavedPost = (bookmarked_portfolios) => {
    // local-bar 변경
    const postPortfolio = document.querySelector('#post__portfolio');
    const postMyPost = document.querySelector('#post__my-post');
    const postSavedPost = document.querySelector('#post__saved-post');
    const postPortfolioSelected = document.querySelector('#post__portfolio-selected');
    const postMyPostSelected = document.querySelector('#post__my-post-selected');
    const postSavedPostSelected = document.querySelector('#post__saved-post-selected');
    const postSavedPortfolio= document.querySelector('#post__saved-portfolio');
    const postSavedContact = document.querySelector('#post__saved-contact');
    const postSavedPlace = document.querySelector('#post__saved-place');
    postPortfolio.className = "";
    postMyPost.className = "";
    postSavedPost.className = "post__local-bar-selected";
    postPortfolioSelected.className = "post__not-selected";
    postMyPostSelected.className = "post__not-selected";
    postSavedPostSelected.className = "";
    postSavedPortfolio.className = "post__local-sub-bar-selected";
    postSavedContact.className = "";
    postSavedPlace.className = "";

    // 게시글 변경
    const postContainer = document.querySelector('.post__container');
    postContainer.innerHTML='';
    for(let i=0; i<bookmarked_portfolios.length; i++){
        postContainer.innerHTML+=`<div class="post__item">`+
            `<a href=http://127.0.0.1:8000/portfolio/${bookmarked_portfolios[i].id}>`+
                `<figure class="post__image">`+
                    `<img src=${bookmarked_portfolios[i].thumbnail_url}>`+
                    `<figcaption>`+
                        `<div class="post__info">`+
                            `<p class="post__title">${bookmarked_portfolios[i].title}</p>`+
                            `<div>`+
                                `<p class="post__comment">`+
                                `<i class="far fa-comment"></i>`+
                                `<span>${bookmarked_portfolios[i].comment_count}</span>`+
                                `</p>`+
                                `<p class="post__view">`+
                                    `<i class="far fa-eye"></i>`+
                                    `<span>${bookmarked_portfolios[i].view_count}</span>`+
                                `</p>`+
                                `<p class="post__like">`+
                                    `<i class="fas fa-heart"></i>`+
                                    `<span>${bookmarked_portfolios[i].like_count}</span>`+
                                `</p>`+
                                `<p class="post__bookmark">`+
                                    `<i class="fas fa-bookmark"></i>`+
                                    `<span>${bookmarked_portfolios[i].bookmark_count}</span>`+
                                `</p>`+
                            `</div>`+
                        `</div>`+
                    `</figcaption>`+
                `</figure>`+
            `</a>`+
        `</div>`
    }

    // // save 기능
    // for(let i=0; i<bookmarked_portfolios.length; i++){
    //     const save = document.querySelector(`.save-${bookmarked_portfolios[i].id}`);
    //     if( bookmarked_portfolios[i].is_bookmark === true ){
    //         save.innerHTML = `<i class="fas fa-bookmark" type="submit" onclick="onClickPortfolioSave(${bookmarked_portfolios[i].id})" name="type" value="save"></i>`
    //     } else {
    //         save.innerHTML = `<i class="far fa-bookmark" type="submit" onclick="onClickPortfolioSave(${bookmarked_portfolios[i].id})" name="type" value="save"></i>`
    //     }
    // }
}