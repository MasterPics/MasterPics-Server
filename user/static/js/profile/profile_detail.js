//category
const onClickLink = (category) => {
    const categoryIdInput = document.querySelector('#category')
    categoryIdInput.value = category
    const searchForm = document.querySelector('#searchForm')
    searchForm.submit()
}