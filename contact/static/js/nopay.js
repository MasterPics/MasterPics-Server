$(function () {
    var test = localStorage.input === 'true' ? true : false;
    $('.no_pay').prop('checked', test || false);
});
$('.no_pay').on('click', function () {
    localStorage.input = $(this).is(':checked');
});
const nopayClassInput = document.querySelector('.no_pay')
const nopayIdInput = document.querySelector('#no_pay')

if (localStorage.input === 'true') {
    nopayIdInput.value = true
} else {
    nopayIdInput.value = false
}
nopayClassInput.addEventListener('click', () => {
    const nopayIdInput = document.querySelector('#no_pay')
    const searchForm = document.querySelector('#searchForm')
    if (localStorage.input === 'true') {
        nopayIdInput.value = true
    } else {
        nopayIdInput.value = false
    }
    searchForm.submit()
})