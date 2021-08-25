window.onload = function () {
    const pay = document.querySelector('.pay input');
    const pay_type = document.querySelector('.pay_type');

    if (pay_type.value == 2) {
        pay.readOnly = false;
        pay.style.backgroundColor = '#ffffff';
    }
    else {
        pay.value = '';
        pay.readOnly = true;
        pay.style.backgroundColor = '#e2e2e2';
    }

    // pay_type이 '페이입력'일 때, pay 입력 가능
    pay_type.addEventListener('change', function () {
        if (pay_type.value == 2) {
            pay.readOnly = false;
            pay.style.backgroundColor = '#ffffff';
        }
        else {
            pay.value = '';
            pay.readOnly = true;
            pay.style.backgroundColor = '#e2e2e2';
        }
    });
}