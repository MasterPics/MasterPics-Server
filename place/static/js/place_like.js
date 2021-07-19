const onClickLike = async (place_id) => {
    try {
        const options = {
            url: '/place/like/',
            method: 'POST',
            data: {
                place_id: place_id,
            }
        }
        const response = await axios(options)
        const responseOK = response && response.status === 200 && response.statusText === 'OK'
        if (responseOK) {
            const data = response.data
            modifyLike(data.place_id, data.is_liked)
        }
    } catch (error) {
        console.log(error)
    }
}

const modifyLike = (place_id, is_liked) => {
    const like = document.querySelector(`.like-${place_id} i`);
    const like_content = document.querySelector(`.like-${place_id} .like__content`)
    const num = like_content.innerText
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