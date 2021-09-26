const filterCategory = document.querySelector('.filter__category')
filterCategory.addEventListener('click', (e) => {
    let selectedCategory = e.target;
    let category = 'undefined';

    // 클릭된 카테고리마다 변수 category로 넘길 string 지정
    if (selectedCategory.classList.contains('all')) {
        category = 'all';
    }
    else if (selectedCategory.classList.contains('photographer')) {
        category = 'photographer';
    }
    else if (selectedCategory.classList.contains('model')) {
        category = 'model';
    }
    else if (selectedCategory.classList.contains('hairmakeup')) {
        category = 'hairmakeup';
    }
    else if (selectedCategory.classList.contains('stylist')) {
        category = 'stylist';
    }

    // 변수 category를 받아 form submit
    if (category != 'undefined') {
        const categoryInput = document.querySelector('#category')
        categoryInput.value = category
        const searchForm = document.querySelector('#searchForm')
        searchForm.submit()
    }
})

// url에서 parameter 추출하는 함수
function getParam(sname) {
    var params = location.search.substr(location.search.indexOf("?") + 1);

    var sval = "";

    params = params.split("&");

    for (var i = 0; i < params.length; i++) {

        temp = params[i].split("=");

        if ([temp[0]] == sname) { sval = temp[1]; }

    }
    return sval;
}

// parameter와 일치하는 class명 가진 객체에 selected class명 추가하는 함수
function addClassName(param) {
    document.querySelector(`${'.' + param}`).classList.add('selected');
}

// 클릭된 카테고리가 있다면 초기화 후 클릭된 카테고리에 selected class명을 추가
if (getParam('category')) {
    document.querySelector('.all').classList.remove('selected')
    addClassName(getParam('category'));
}
