const onClickMapSave = async (contact_id) => {
    try {
        const options = {
            url: '/save/',
            method: 'POST',
            data: {
                contact_id: contact_id,
            }
        }
        const response = await axios(options)
        const responseOK = response && response.status === 200 && response.statusText === 'OK'
        if (responseOK) {
            const data = response.data
            //modify에서는 뒤집힌 is_saved 값이 들어감
            SaveModify(data.contact_id, data.is_saved)
        }
    } catch (error) {
        console.log(error)
    }
}

const SaveModify = (contact_id, is_saved) => {
    const save = document.querySelector(`.save-${contact_id} i`);

    if (is_saved === true) {
        save.className = "fas fa-bookmark";
    } else {
        save.className = "far fa-bookmark";
    }

}