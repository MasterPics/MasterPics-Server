const onClickLike = async (portfolio_id) => {
    try {
        const options = {
            url: '/portfolio/like/',
            method: 'POST',
            data: {
                portfolio_id: portfolio_id,
            }
        }
        const response = await axios(options)
        const responseOK = response && response.status === 200 && response.statusText === 'OK'
        if (responseOK) {
            const data = response.data
            modifyLike(data.portfolio_id, data.is_liked)
        }
    } catch (error) {
        console.log(error)
    }
}

const modifyLike = (portfolio_id, is_liked) => {
    const like = document.querySelector(`.like-${portfolio_id} i`);
    const like_content = document.querySelector(`.like-${portfolio_id} .like__content`)
    const num = like_content.innerText; // tag.like_users.count
    console.log(num)
    if (is_liked === true) {

        like.className = "fas fa-heart";

        const count = Number(num) + 1;
        like_content.innerHTML = count
    } else {
        like.className = "far fa-heart";

        const count = Number(num) - 1;
        like_content.innerHTML = count
    }

}