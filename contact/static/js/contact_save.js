const onClickSave = async (contact_id) => {
    try {
        const options = {
            url: '/contact/save/',
            method: 'POST',
            data: {
                contact_id: contact_id,
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
                //modify에서는 뒤집힌 is_saved 값이 들어감
                modify(data.contact_id, data.is_saved)
            }
        }
    } catch (error) {
        console.log(error)
    }
}

const modify = (contact_id, is_saved) => {
    const save = document.querySelector(`.save-${contact_id} i`);
    const save_content = document.querySelector(`.save-${contact_id} .save__content`)
    const num = save_content.innerText; // contact.save_users.count
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