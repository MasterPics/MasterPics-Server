// portfolio save
    const onClickPortfolioSave = async (portfolio_id) => {
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
                modifyPortfolio(data.portfolio_id, data.is_saved)
            }
        } catch (error) {
            console.log(error)
        }
    }

    const modifyPortfolio = (portfolio_id, is_saved) => {
        const save = document.querySelector(`.save-${portfolio_id} i`);
        if (is_saved === true) {
            save.className = "fas fa-bookmark";
        } else {
            save.className = "far fa-bookmark";
        }

    }
// contact save
    const onClickContactSave = async (contact_id) => {
        try {
            const options = {
                url: '/contact/save/',
                method: 'POST',
                data: {
                    contact_id: contact_id,
                }
            }
            const response = await axios(options)
            const responseOK = response && response.status === 200 && response.statusText === 'OK'
            if (responseOK) {
                const data = response.data
                //modify에서는 이미 뒤집힌 is_saved 값이 들어감!
                modifyContact(data.contact_id, data.is_saved)
            }
        } catch (error) {
            console.log(error)
        }
    }

    const modifyContact = (contact_id, is_saved) => {
        const save = document.querySelector(`.save-${contact_id} i`);
        if (is_saved === true) {
            save.className = "fas fa-bookmark";
        } else {
            save.className = "far fa-bookmark";
        }

    }





// place save
const onClickPlaceSave = async (place_id) => {
    try {
        const options = {
            url: '/place/bookmark/',
            method: 'POST',
            data: {
                place_id: place_id,
            }
        }
        const response = await axios(options)
        const responseOK = response && response.status === 200 && response.statusText === 'OK'
        if (responseOK) {
            const data = response.data
            //modify에서는 이미 뒤집힌 is_saved 값이 들어감!
            modifyPlace(data.place_id, data.is_bookmarked)
        }
    } catch (error) {
        console.log(error)
    }
}

const modifyPlace = (place_id, is_bookmarked) => {
    const save = document.querySelector(`.save-${place_id} i`);
    if (is_bookmarked === true) {
        save.className = "fas fa-bookmark";
    } else {
        save.className = "far fa-bookmark";
    }

}