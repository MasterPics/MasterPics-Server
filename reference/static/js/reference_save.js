const onClickSave = async (tag_id) => {
    try {
        const options = {
            url: '/tag/save/',
            method: 'POST',
            data: {
                tag_id: tag_id,
            }
        }
        const response = await axios(options)
        const responseOK = response && response.status === 200 && response.statusText === 'OK'
        if (responseOK) {
            const data = response.data
            //modify에서는 뒤집힌 is_saved 값이 들어감
            modifySave(data.tag_id, data.is_saved)
        }
    } catch (error) {
        console.log(error)
    }
}

const modifySave = (tag_id, is_saved) => {
    const save = document.querySelector(`.save-${tag_id} i`);
    const save_content = document.querySelector(`.save-${tag_id} .save__content`)
    const num = save_content.innerText; // tag.save_users.count
    console.log(num)
    if (is_saved === true) {

        save.className = "fas fa-bookmark";

        const count = Number(num) + 1;
        save_content.innerHTML = count
    } else {
        save.className = "far fa-bookmark";

        const count = Number(num) - 1;
        save_content.innerHTML = count
    }

}