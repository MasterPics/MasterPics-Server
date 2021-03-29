const onClickSave = async (portfolio_id) => {
    try {
        const options = {
            url: '/portfolio/save/',
            method: 'POST',
            data: {
                portfolio_id: portfolio_id,
            }
        }
        const response = await axios(options)
        const responseOK = response && response.status === 200 && response.statusText === 'OK'
        if (responseOK) {
            const data = response.data
            //modify에서는 이미 뒤집힌 is_saved 값이 들어감!
            modifySave(data.portfolio_id, data.is_saved)
        }
    } catch (error) {
        console.log(error)
    }
}

const modifySave = (portfolio_id, is_saved) => {
    const save = document.querySelector(`.save-${portfolio_id} i`);
    const save_content = document.querySelector(`.save-${portfolio_id} .save__content`)
    const num = save_content.innerText; // portfolio.save_users.count
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