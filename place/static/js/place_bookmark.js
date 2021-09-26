const onClickSave = async (place_id) => {
    try {
        const options = {
            url: '/place/bookmark/',
            method: 'POST',
            data: {
                place_id: place_id,
            }
        }
        const response = await axios(options)
        const responseOK = response && response.status === 200
        if (responseOK) {
            const data = response.data
            if (data.login_required === true) {
                alert('로그인 후 이용 가능합니다.');
            }
            else {
                //modify에서는 이미 뒤집힌 is_saved 값이 들어감!
                modifySave(data.place_id, data.is_bookmarked)
            }
        }
    } catch (error) {
        console.log(error)
    }
}

const modifySave = (place_id, is_bookmarked) => {
    const save = document.querySelector(`.save-${place_id} i`);
    const save_content = document.querySelector(`.save-${place_id} .save__content`)
    const num = save_content.innerText;
    if (is_bookmarked === true) {

        save.className = "fas fa-bookmark";

        const count = Number(num) + 1;
        save_content.innerHTML = count
    } else {
        save.className = "far fa-bookmark";

        const count = Number(num) - 1;
        save_content.innerHTML = count
    }

}