const sortClassInput = document.querySelector('.sort')
sortClassInput.addEventListener('input', (e) => {
    const sortIdInput = document.querySelector('#sort')
    const searchForm = document.querySelector('#searchForm')
    sortIdInput.value = e.target.value
    searchForm.submit()
})
