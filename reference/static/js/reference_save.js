const onClickSave = async (portfolio_id) => {
    try {
        const options = {
            url: window.location.origin + 'portfolio/save/',
            method: 'POST',
            data: {
                portfolio_id: portfolio_id,
            }
        }
        const response = await axios(options)
        const responseOK = response && response.status === 200
        if (responseOK) {
            const data = response.data
            //modify에서는 뒤집힌 is_saved 값이 들어감
            modifySave(data.portfolio_id, data.is_saved)
        }
    } catch (error) {
        console.log(error)
    }
}

// TODO: bookmark count 필요없으면 밑의 주석 삭제하기. 필요하면 해당 count 띄워주는 html 태그 만들고 주석 해제하기
const modifySave = (portfolio_id, is_saved) => {
    console.log(is_saved)
    const save = document.querySelector(`.save-${portfolio_id} i`);
    // const save_content = document.querySelector(`.save-${portfolio_id} .save__content`)
    // const num = save_content.innerText; // tag.save_users.count
    // console.log(num)
    if (is_saved === true) {
        console.log(is_saved)

        save.className = "fas fa-bookmark";

        // const count = Number(num) + 1;
        // save_content.innerHTML = count
    } else {
        console.log(is_saved)
        save.className = "far fa-bookmark";

        // const count = Number(num) - 1;
        // save_content.innerHTML = count
    }

}