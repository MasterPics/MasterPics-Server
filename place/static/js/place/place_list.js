var infinite = new Waypoint.Infinite({
    element: $('.infinite-container')[0],
    onBeforePageLoad: function () {
        $('.loading').show();
    },
    onAfterPageLoad: function ($items) {
        $('.loading').hide();
    }
});

//Save
const onClickSave = async (place_id) => {
    try {
        // const url = '/contact/';
        // const {
        //     data
        // } = await axios.post(url, {
        //     place_id,
        // })
        // modify(data.place_id, data.is_saved)

        const options = {
            url: '/place/save/',
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
            modify(data.place_id, data.is_saved)
        }
    } catch (error) {
        console.log(error)
    }
}

const modify = (place_id, is_saved) => {
    const save = document.querySelector(`.save-${place_id} i`);
    const save_content = document.querySelector(`.save-${place_id} .save__content`)
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
//category
const onClickLink = (category) => {
    const categoryIdInput = document.querySelector('#category')
    categoryIdInput.value = category
    const searchForm = document.querySelector('#searchForm')
    searchForm.submit()
}

//search
$(document).ready(function(){
    $(".page-link").on('click', function() {
        $("#page").val($(this).data("page"));
        $("#searchForm").submit();
    });

    $("#btn_search").on('click', function() {
        $("#search").val($(".search").val());
        $("#page").val(1);   //검색버튼을 클릭할 경우 1페이지부터 조회한다.
        $("#searchForm").submit();
    });
});

//sort
const sortClassInput = document.querySelector('.sort')
sortClassInput.addEventListener('input', (e) => {
    const sortIdInput = document.querySelector('#sort')
    const searchForm = document.querySelector('#searchForm')
    sortIdInput.value = e.target.value
    searchForm.submit()
})


function modal(id) {
    var zIndex = 9999;
    var modal = document.getElementById(id);

    // 모달 div 뒤에 희끄무레한 레이어
    var bg = document.createElement('div');
    bg.setStyle({
        position: 'fixed',
        zIndex: zIndex,
        left: '0px',
        top: '0px',
        width: '100%',
        height: '100%',
        overflow: 'auto',
        // 레이어 색갈은 여기서 바꾸면 됨
        backgroundColor: 'rgba(0,0,0,0.4)'
    });
    document.body.append(bg);

    // 닫기 버튼 처리, 시꺼먼 레이어와 모달 div 지우기
    modal.querySelector('.modal_close_btn').addEventListener('click', function() {
        bg.remove();
        modal.style.display = 'none';
    });

    modal.setStyle({
        position: 'fixed',
        display: 'block',
        boxShadow: '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',

        // 시꺼먼 레이어 보다 한칸 위에 보이기
        zIndex: zIndex + 1,

        // div center 정렬
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        msTransform: 'translate(-50%, -50%)',
        webkitTransform: 'translate(-50%, -50%)'
    });
}

// Element 에 style 한번에 오브젝트로 설정하는 함수 추가
Element.prototype.setStyle = function(styles) {
    for (var k in styles) this.style[k] = styles[k];
    return this;
};

document.getElementById('popup_open_btn').addEventListener('click', function() {
    // 모달창 띄우기
    modal('my_modal');
});