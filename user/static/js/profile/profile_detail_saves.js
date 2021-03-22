   
//top_button
    //Get the button:
    mybutton = document.getElementById("myBtn");

    // When the user scrolls down 20px from the top of the document, show the button
    window.onscroll = function () {
        scrollFunction()
    };

    function scrollFunction() {
        if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
            mybutton.style.display = "block";
        } else {
            mybutton.style.display = "none";
        }
    }

    // When the user clicks on the button, scroll to the top of the document
    function topFunction() {
        document.body.scrollTop = 0; // For Safari
        document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
    }


    //
    let infinite = new Waypoint.Infinite({
        element: $('.grid')[0],
        items: '.grid-item',
        onBeforePageLoad: function () {
            $('.loading').show();
        },
        onAfterPageLoad: function () {
            $('.loading').hide();
            let msnry = new Masonry('.grid', {
                itemSelector: '.grid-item',
                gutter: 10,
            })
        }
    });
    let msnry = new Masonry('.grid', {
        // optionsW
        itemSelector: '.grid-item',
        gutter: 10,
        // columnWidth: 200
    });

    //Save
    const onClickContactSave = async (contact_id) => {
        try {
            console.log("here")
            // const url = '/contact/';
            // const {
            //     data
            // } = await axios.post(url, {
            //     contact_id,
            // })
            // modify(data.contact_id, data.is_saved)

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
        const save_content = document.querySelector(`.save-${contact_id} .save__content`)
        const num = save_content.innerText; // [ {{ contact.save_users.count }} ]
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



    //Save
    const onClickPortfolioSave = async (portfolio_id) => {
        try {
            // const url = '/portfolio/';
            // const {
            //     data
            // } = await axios.post(url, {
            //     portfolio_id,
            // })
            // modify(data.portfolio_id, data.is_saved)

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
        const save_content = document.querySelector(`.save-${portfolio_id} .save__content`)
        const num = save_content.innerText; // [ {{ portfolio.save_users.count }} ]
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




    //category
    const onClickLink = (category) => {
        const categoryIdInput = document.querySelector('#category')
        categoryIdInput.value = category
        const searchForm = document.querySelector('#searchForm')
        searchForm.submit()
    }

    //search
    const searchButton = document.querySelector('.btn_search')
    searchButton.addEventListener('click', () => {
        const searchClassInput = document.querySelector('.search')
        const searchIdInput = document.querySelector('#search')
        const searchForm = document.querySelector('#searchForm')
        searchIdInput.value = searchClassInput.value
        searchForm.submit()
    })


    //sort
    const sortClassInput = document.querySelector('.sort')
    sortClassInput.addEventListener('input', (e) => {
        const sortIdInput = document.querySelector('#sort')
        const searchForm = document.querySelector('#searchForm')
        sortIdInput.value = e.target.value
        searchForm.submit()
    })