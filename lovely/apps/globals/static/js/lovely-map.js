
function initializeMap() {
    var mapDiv = document.getElementById('info-section-map');
    var map = new google.maps.Map(mapDiv, {
      center: new google.maps.LatLng(25.038988, 121.553783),
      zoom: 16,
      disableDefaultUI: true,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    });

    return map;
}

function initializeMarker(map){
    var latLng = new google.maps.LatLng(25.038988, 121.553783);
    var marker = new google.maps.Marker({
      position: latLng,
      map: map
    });
    return marker;
}

$(document).ready(function(){
    initializeMarker(initializeMap());
});
