const onClickPortfolio = async(user_id) => {
    try{
        const options = {
            url: '/profile/mypage/portfolio/',
            method: 'POST',
            data: {
                user_id: user_id,
            }
        }
    const response = await axios(options)
    const responseOK = response && response.status === 200 && response.statusText === 'OK'
    if (responseOK) {
        const data = response.data
        listMyPortfolio(data.portfolios)
    }
    } catch (error) {
        console.log(error)
    }
}
const listMyPortfolio = (portfolios) => {
    // local-bar 변경
    const postPortfolio = document.querySelector('#post__portfolio');
    const postMyPost = document.querySelector('#post__my-post');
    const postSavedPost = document.querySelector('#post__saved-post');
    const postPortfolioSelected = document.querySelector('#post__portfolio-selected');
    const postMyPostSelected = document.querySelector('#post__my-post-selected');
    const postSavedPostSelected = document.querySelector('#post__saved-post-selected');
    postPortfolio.className = "post__local-bar-selected";
    postMyPost.className = "";
    postSavedPost.className = "";
    postPortfolioSelected.className = "";
    postMyPostSelected.className = "post__not-selected";
    postSavedPostSelected.className = "post__not-selected";

    // 게시글 변경
    const postContainer = document.querySelector('.post__container');
    postContainer.innerHTML='';
    for(let i=0; i<portfolios.length; i++){
        postContainer.innerHTML+=`<div class="post__item">`+
            `<a href=http://127.0.0.1:8000/portfolio/${portfolios[i].id}>`+
                `<figure class="post__image">`+
                    `<img src=${portfolios[i].thumbnail_url}>`+
                    `<figcaption>`+
                        `<div class="post__info">`+
                            `<p class="post__title">${portfolios[i].title}</p>`+
                            `<div>`+
                                `<p class="post__like">`+
                                    `<i class="fas fa-heart"></i>`+
                                    `<span>${portfolios[i].like_count}</span>`+
                                `</p>`+
                                `<p class="post__view">`+
                                    `<i class="far fa-eye"></i>`+
                                    `<span>${portfolios[i].view_count}</span>`+
                                `</p>`+
                            `</div>`+
                        `</div>`+
                    `</figcaption>`+
                `</figure>`+
            `</a>`+
        `</div>`
    }
}