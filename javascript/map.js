function initAutocomplete() {
//     var map = new google.maps.Map(document.getElementById('map'), {
//   center: {
//     lat: -33.8688,
//     lng: 151.2195
//   },
//   zoom: 13,
//   mapTypeId: 'roadmap'
// });
var map = new google.maps.Map(document.getElementById('googleMaps'), {
center: {lat: 0, lng: 0},
zoom: 1,
mapTypeId: 'roadmap'
});

// Create the search box and link it to the UI element.
var input = document.getElementById('pac-input');
var searchBox = new google.maps.places.SearchBox(input);
map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

var infowindow = new google.maps.InfoWindow();
var service = new google.maps.places.PlacesService(map);
// Bias the SearchBox results towards current map's viewport.
map.addListener('bounds_changed', function() {
searchBox.setBounds(map.getBounds());
});

var markers = [];
// Listen for the event fired when the user selects a prediction and retrieve
// more details for that place.
searchBox.addListener('places_changed', function() {
var places = searchBox.getPlaces();

if (places.length == 0) {
  return;
}

// Clear out the old markers.
markers.forEach(function(marker) {
  marker.setMap(null);
});
markers = [];

// For each place, get the icon, name and location.
var bounds = new google.maps.LatLngBounds();
places.forEach(function(place) {
  if (!place.geometry) {
    console.log("Returned place contains no geometry");
    return;
  }
  service.getDetails({
    placeId: place.place_id
  }, function(place, status) {
    var marker = new google.maps.Marker({
      map: map,
      position: place.geometry.location
    });
    markers.push(marker);
    google.maps.event.addListener(marker, 'click', function() {
      infowindow.setContent('<div><strong>' + place.name + '</strong><br>' + place.formatted_address + '</div>');
      infowindow.open(map, this);
    });

  });

  if (place.geometry.viewport) {
    // Only geocodes have viewport.
    bounds.union(place.geometry.viewport);
  } else {
    bounds.extend(place.geometry.location);
  }
});
map.fitBounds(bounds);
});


}
