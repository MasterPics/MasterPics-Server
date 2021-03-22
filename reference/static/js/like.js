const onClickLike = async (tag_id) => {
    try {
        const options = {
            url: '/tag/like/',
            method: 'POST',
            data: {
                tag_id: tag_id,
            }
        }
        const response = await axios(options)
        const responseOK = response && response.status === 200 && response.statusText === 'OK'
        if (responseOK) {
            const data = response.data
            modifyLike(data.tag_id, data.is_liked)
        }
    } catch (error) {
        console.log(error)
    }
}

const modifyLike = (tag_id, is_liked) => {
    const like = document.querySelector(`.like-${tag_id} i`);
    const like_content = document.querySelector(`.like-${tag_id} .like__content`)
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