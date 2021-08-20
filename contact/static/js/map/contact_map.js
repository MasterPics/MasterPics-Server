/////////////////////////////////// result ///////////////////////////////////////
var locationValue = document.querySelector('#result__location-value');
var postValue = document.querySelector('#result__post-value');

/////////////////////////////////// map ///////////////////////////////////////
var geocoder = new kakao.maps.services.Geocoder();

var markers = [];

// 인포윈도우 생성
var infowindow = new kakao.maps.InfoWindow({zIndex:1});

// 지도 생성
var mapContainer = document.getElementById('map'), 
    mapOption = {
        center: new kakao.maps.LatLng(37.566826, 126.9786567),
        level: 3 
    };  

var map = new kakao.maps.Map(mapContainer, mapOption);  

// contact의 위치
var positions = [];

contactPlaces();

function contactPlaces() {
    
    for (var i=0; i<contacts.length; i++) {
        positions.push(
            {
                pk: contacts[i].pk,
                title: contacts[i].title,
                thumbnail:contacts[i].thumbnail,
                is_saved:contacts[i].is_saved,
                address: contacts[i].address, 
                pay_type : contacts[i].pay_type,
                pay : contacts[i].pay,
                startDate : contacts[i].start_date,
                endDate : contacts[i].end_date,
                writer:contacts[i].writer,
                writer_thumbnail:contacts[i].writer_thumbnail,
                writer_category:contacts[i].writer_category,
                latlng: ''
            }
        );   
    }

    positions.forEach(function(element) {
        geocoder.addressSearch(element.address, function(result, status) { 

             if (status === kakao.maps.services.Status.OK) {
        
                var coords = new kakao.maps.LatLng(result[0].y, result[0].x);
                element.latlng = coords;
            }

        });
    });
}

// 현위치 주변 검색
function searchCurrentPosition(){
    if (navigator.geolocation) {
    
        // GeoLocation을 이용해서 접속 위치를 얻어옵니다
        navigator.geolocation.getCurrentPosition(function(position) {
            
            var lat = position.coords.latitude, // 위도
                lon = position.coords.longitude; // 경도
                
            var locPosition = new kakao.maps.LatLng(lat, lon);
             
            searchDetailAddrFromCoords(locPosition, function(result, status) {
                if (status === kakao.maps.services.Status.OK) {
                    var detailAddr = !!result[0].road_address ? result[0].road_address.address_name : result[0].address.address_name;
                    
                    var keywordInput = document.getElementById('keyword');
                    
                    keywordInput.value = detailAddr;
    
                    // 마커와 인포윈도우를 표시
                    displayPlaces(detailAddr);
                    // displayPagination(pagination);  
                }   
            });
          });
    }
}

function searchDetailAddrFromCoords(coords, callback) {
    // 좌표로 법정동 상세 주소 정보를 요청
    geocoder.coord2Address(coords.getLng(), coords.getLat(), callback);
}
  
// 장소 검색
searchPlaces();

function searchPlaces() {
    var keyword = document.getElementById('keyword').value;

    // 검색 결과 검색어 result에 보냄
    locationValue.innerHTML = keyword;

    // if (!keyword.replace(/^\s+|\s+$/g, '')) {
    //     alert('키워드를 입력해주세요!');
    //     return false;
    // }

    // 검색 결과 목록, 마커 표출
    displayPlaces(keyword);

    // 페이지 번호 표출
    // displayPagination(pagination);
}

// 검색 결과 목록, 마커 표출
function displayPlaces(keyword) {

    places=[];

    for (var i=0; i<positions.length; i++){
        var contactAddress = positions[i].address,
        keywordAddress = keyword;

        if (contactAddress.includes(keywordAddress)){
            places.push(positions[i]);
        }
    }

    // 검색 결과 places 개수 result에 보냄
    postValue.innerHTML = places.length;

    var listEl = document.getElementById('placesList'), 
    contentEl = document.getElementById('content'),
    fragment = document.createDocumentFragment(), 
    bounds = new kakao.maps.LatLngBounds();
    
    // 검색 결과 목록 제거
    removeAllChildNods(listEl);

    // 마커 제거
    removeMarker();
    
    for ( var i=0; i<places.length; i++ ) {

        // 마커 생성
        var placePosition = places[i].latlng,
            marker = addMarker(placePosition, i), 
            itemEl = getListItem(i, places[i]); 

        // 검색된 장소 위치를 기준으로 지도 범위를 재설정
        bounds.extend(placePosition);

        // 인포윈도우 설정
        (function(marker, title) {
            kakao.maps.event.addListener(marker, 'mouseover', function() {
                displayInfowindow(marker, title);
            });

            kakao.maps.event.addListener(marker, 'mouseout', function() {
                infowindow.close();
            });

            itemEl.onmouseover =  function () {
                displayInfowindow(marker, title);
            };

            itemEl.onmouseout =  function () {
                infowindow.close();
            };
        })(marker, places[i].title);

        fragment.appendChild(itemEl);
    }

    // 검색결과 항목들을 검색결과 목록 Elemnet에 추가
    listEl.appendChild(fragment);
    contentEl.scrollTop = 0;

    // 검색된 장소 위치를 기준으로 지도 범위를 재설정
    map.setBounds(bounds);
}

// 검색결과 항목을 Element로 반환
function getListItem(index, places) {
    console.log(places);
    
    let itemSave;
    let itemPay;

    if (places.is_saved){
        itemSave = `<i class="fas fa-bookmark" type="submit" onclick="onClickMapSave(${places.pk})" name="type" value="save"></i>`;
    } else {
        itemSave = `<i class="far fa-bookmark" type="submit" onclick="onClickMapSave(${places.pk})" name="type" value="save"></i>`;
    }

    if (places.pay_type === 0){
        itemPay = "상호무페이";
    }
    else if (places.pay_type === 1){
        itemPay = places.pay + "원";
    }
    else {
        itemPay = "페이협의";
    }

    var el = document.createElement('li'),


    itemStr =   '<div class="info">' +
                `<div class="save save-${places.pk}">`+ itemSave + `</div>`+
                '<div class="content">'+
                    `<a href="http://127.0.0.1:8000/contact/detail/${places.pk}">`+'<div class="place-title">' + places.title + '</div>'+`</a>`+
                    '<div class="address">' + places.address + '</div>'+
                    '<div class="pay-date">'+
                        '<div class="pay">' + itemPay + '</div>'+
                        '<div class="date-wrapper">'+
                            '<div>' + places.startDate  + '</div>'+
                            '<div>' + '~'  + '</div>'+
                            '<div>' + places.endDate  + '</div>'+
                        '</div>'+
                    '</div>'+
                    '<div class="user-wrapper">'+
                        `<img src=${places.writer_thumbnail}>`+
                        '<div>'+
                            '<div class="writer">' + places.writer  + '</div>'+
                            '<div class="writer__category">' + places.writer_category  + '</div>'+
                        '</div>'+
                    '</div>'+
                '</div>'+
                '<div class="thumbnail">'+
                `<a href="http://127.0.0.1:8000/contact/detail/${places.pk}">`+`<img src=${places.thumbnail} />`+`</a>`+
                '</div>'+
            '</div>';         

    el.innerHTML = itemStr;
    el.className = 'item';

    return el;
}

// 마커 생성
function addMarker(position, idx, title) {
    var imageSrc = 'https://i.imgur.com/rsjHKsd.png',
        imageSize = new kakao.maps.Size(30, 53),
        imgOptions =  {
            spriteSize : new kakao.maps.Size(30, 53), // 스프라이트 이미지의 크기
            offset: new kakao.maps.Point(10, 40) // 마커 좌표에 일치시킬 이미지 내에서의 좌표
        },
        markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize, imgOptions),
            marker = new kakao.maps.Marker({
            position: position, 
            image: markerImage 
        });

    marker.setMap(map);
    markers.push(marker);  // 배열에 생성된 마커를 추가

    return marker;
}

// 지도 위에 표시되고 있는 마커를 모두 제거
function removeMarker() {
    for ( var i = 0; i < markers.length; i++ ) {
        markers[i].setMap(null);
    }   
    markers = [];
}

// 검색결과 목록 하단에 페이지번호 표시
// function displayPagination(pagination) {
//     var paginationEl = document.getElementById('pagination'),
//         fragment = document.createDocumentFragment(),
//         i; 

//     // 기존에 추가된 페이지번호 삭제
//     while (paginationEl.hasChildNodes()) {
//         paginationEl.removeChild (paginationEl.lastChild);
//     }

//     for (i=1; i<=pagination.last; i++) {
//         var el = document.createElement('a');
//         el.href = "#";
//         el.innerHTML = i;

//         if (i===pagination.current) {
//             el.className = 'on';
//         } else {
//             el.onclick = (function(i) {
//                 return function() {
//                     pagination.gotoPage(i);
//                 }
//             })(i);
//         }

//         fragment.appendChild(el);
//     }
//     paginationEl.appendChild(fragment);
// }

// 인포윈도우에 장소명을 표시
function displayInfowindow(marker, title) {
    var content = '<div style="padding:5px;z-index:1;">' + title + '</div>';

    infowindow.setContent(content);
    infowindow.open(map, marker);
}

 // 검색결과 목록의 자식 Element를 제거
function removeAllChildNods(el) {   
    while (el.hasChildNodes()) {
        el.removeChild (el.lastChild);
    }
}

