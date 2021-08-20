let locationAddress = document.querySelector('#location-address');
locationAddress.placeholder = '마커를 움직이면 주소가 자동 입력됩니다.';

// 지도 생성
var mapContainer = document.getElementById('map'),
    mapOption = { 
        center: new kakao.maps.LatLng(37.54699, 127.09598), // 지도의 중심좌표
        level: 4 // 지도의 확대 레벨
    };

var map = new kakao.maps.Map(mapContainer, mapOption); 

// 마커 설정
var imageSrc = 'https://i.imgur.com/rsjHKsd.png',    
    imageSize = new kakao.maps.Size(30, 53), 
    imageOption = {offset: new kakao.maps.Point(10, 40)}; 

    var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize, imageOption);

// 마커의 드래그 설정  
var DragSrc = 'https://i.imgur.com/rsjHKsd.png', 
    DragSize = new kakao.maps.Size(30, 53), 
    DragOption = { 
        offset: new kakao.maps.Point(10, 54)
    };
var DragImage = new kakao.maps.MarkerImage(DragSrc, DragSize, DragOption);

// 마커 생성
var marker = new kakao.maps.Marker();

var geocoder = new kakao.maps.services.Geocoder();

geocoder.addressSearch(locationAddress.value, function(result, status) {
     if (status === kakao.maps.services.Status.OK) {

        var coords = new kakao.maps.LatLng(result[0].y, result[0].x);

        // 결과값으로 받은 위치를 마커로 표시
        marker.setMap(map);
        marker.setPosition(coords);
        marker.setImage(markerImage);
        marker.setDraggable(true);

        // 지도의 중심을 결과값으로 받은 위치로 이동
        map.setCenter(coords);
    } 
});   

kakao.maps.event.addListener(marker, 'dragstart', function() {
// 마커의 드래그가 시작될 때 마커 이미지를 변경
    marker.setImage(DragImage);
});

kakao.maps.event.addListener(marker, 'dragend', function() {
// 마커의 드래그가 종료될 때 마커 이미지를 원래 이미지로 변경
    marker.setImage(markerImage);

    // 마커의 드래그가 종료될 때 위치 좌표에 대한 주소정보를 표시
    searchDetailAddrFromCoords(marker.getPosition(), function(result, status) {
        if (status === kakao.maps.services.Status.OK) {
            var detailAddr = !!result[0].road_address ? result[0].road_address.address_name : result[0].address.address_name;
            locationAddress.value = detailAddr;
        }   
    });
});

function searchDetailAddrFromCoords(coords, callback) {
    // 좌표로 법정동 상세 주소 정보를 요청
    geocoder.coord2Address(coords.getLng(), coords.getLat(), callback);
}