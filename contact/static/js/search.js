const searchButton = document.querySelector('.btn_search')
searchButton.addEventListener('click', () => {
    const searchClassInput = document.querySelector('.search')
    const searchIdInput = document.querySelector('#search')
    const searchForm = document.querySelector('#searchForm')
    searchIdInput.value = searchClassInput.value
    searchForm.submit()
})