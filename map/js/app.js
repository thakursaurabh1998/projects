var map, positionLive, livePos, spots;
var markers = [];
var allMarkers = [];
var itemsProcessed;
var foursquare_client_id = "3VU3JPF4MALSI0PRWMV1VEVPWXO0HXACAEJDDNSB5GDHH0ZG";
var foursquare_client_secret = "YSBYZX0VSOEQO45P2D0MDM5OHKDFWKGSBUZ0JJXDK4S2W0AZ";
var short, searchLocation, posMarker, last, lastInfoWindow, bouncingMarker, doubleAllow=0;
  

function errorCallbackMap(){
    $("#map").text("Sorry Google Maps API can't be loaded");
}

  /****************************************/
 /* Finding places by searching location */
/****************************************/

function findArea() {
    hideAllMarkers();
    var geocoder = new google.maps.Geocoder();
    var address = $('#search-bar-text').val();
    if (address === '') {
        window.alert('You have to enter query first!');
    } else {
        geocoder.geocode({
            address: address,
        }, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                searchLocation = results[0].geometry.location;
                map.setCenter(searchLocation);
                map.setZoom(15);
                searchLocation = {
                    lat: searchLocation.lat(),
                    lng: searchLocation.lng()
                };
                createJSON(searchLocation);
            } else {
                window.alert('We could not find this location. Try something else.');
            }
        });
    }
}


   /************************************************/
  /* Creating data in JSON format by making AJAX  */
 /* calls asyncronously to the Foursquare server */
/************************************************/

function createJSON(livePos) {
    hideAllMarkers();
    allMarkers = [];
    markers = [];
    for (var i = 0; i < types.length; i++) {
        places[types[i]] = [];
    }
    var foursquareURL = `https://api.foursquare.com/v2/venues/explore?limit=5&range=3000&ll=${livePos.lat},${livePos.lng}&client_id=${foursquare_client_id}&client_secret=${foursquare_client_secret}&v=20170801&query=`;
    itemsProcessed=0;
    types.forEach(function(type) {
        $.ajax({
            url: foursquareURL + type,
            method: 'GET',
            dataType: 'json',
            success: function(response) {
                spots = response.response.groups[0].items;
                createPlaces(spots, type);
                itemsProcessed++;
                if(itemsProcessed===4)
                {
                    vm.changePlace();
                }
            }
        }).error(function(){
            Materialize.toast("Sorry, the Foursquare API service didn't responded.", 4000);
        },8000);
    });
}


  /******************************************/
 /* Finding places by geolocation location */
/******************************************/

function gps() {
    hideAllMarkers();
    for (var i = 0; i < types.length; i++) {
        places[types[i]] = [];
    }
    markers = [];
    allMarkers = [];
    navigator.geolocation.getCurrentPosition(function(position) {
        livePos = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
        };
        if (posMarker) posMarker.setMap(null);
        posMarker = new google.maps.Marker({
            position: livePos,
            title: `${position.lat} ${position.lng}`,
            icon: {
                path: google.maps.SymbolPath.CIRCLE,
                scale: 4,
                strokeColor: "skyblue"
            },
            animation: google.maps.Animation.DROP,
        });
        createJSON(livePos);
        posMarker.setMap(map);
        map.setCenter(livePos);
        map.setZoom(15);
    }, function(){
            livePos = {
            lat: 40.7413549,
            lng: -73.9980244
        };
        createJSON(livePos);
        map.setCenter(livePos);
        map.setZoom(15);
    });
    
}

  /**********************************************/
 /* Displaying markers of all the found places */
/**********************************************/

function showAllMarkers() {
    var bounds = new google.maps.LatLngBounds();
    for (var i = 0; i < allMarkers.length; i++) {
        allMarkers[i].setMap(map);
        bounds.extend(allMarkers[i].position);
    }
    map.fitBounds(bounds);
}


  /******************************************/
 /* Creating markers for all the locations */
/******************************************/

function createMarkers(type,allow) {
    hideAllMarkers();
    markers = [];
    var largeInfoWindow = new google.maps.InfoWindow();
    var bounds = new google.maps.LatLngBounds();
    for (var i = 0; i < places[type].length; i++) {
        short = places[type];
        var position = short[i].location;
        var title = short[i].name;
        var address = short[i].address;
        var marker = new google.maps.Marker({
            id: short[i].id,
            position: position,
            title: title,
            address: address,
            animation: google.maps.Animation.DROP,
        });
        markers.push(marker);
        if(allow){
            if(!allMarkers.find(function(a){
                if(a.id===marker.id)
                    return 1;
            })){
                allMarkers.push(marker);
            }
        }
        markersProperties(marker,largeInfoWindow);
        if(markers.length)
            bounds.extend(markers[i].position);
    }
}

  /********************/
 /* Initializing map */
/********************/

function initMap() {
    var defaultLocation = {
        lat: 40.7413549,
        lng: -73.9980244
    };
    var placeAutocomplete = new google.maps.places.Autocomplete(document.getElementById('search-bar-text'));
    map = new google.maps.Map(document.getElementById('map'), {
        center: defaultLocation,
        zoom: 13,
        mapTypeControl: false
    });
    var largeInfoWindow = new google.maps.InfoWindow();
    var bounds = new google.maps.LatLngBounds();
    gps();
}


function markersProperties(marker,largeInfoWindow) {
    marker.addListener('click',function(){populateInfoWindow(this, largeInfoWindow);});
    marker.addListener('click',function(){toggleBounce(this);});
}




  /**********************************************/
 /* Displaying markers for specific categories */
/**********************************************/

function showMarkers() {
    hideAllMarkers();
    var bounds = new google.maps.LatLngBounds();
    if(markers.length){
        for (var i = 0; i < markers.length; i++) {
            markers[i].setMap(map);
            bounds.extend(markers[i].position);
        }
        map.fitBounds(bounds);
    }
        
}

  /************************************/
 /* Hiding markers for all locations */
/************************************/

function hideAllMarkers() {
    for (var i = 0; i < allMarkers.length; i++) {
        allMarkers[i].setMap(null);
    }
}

  /*****************************************/
 /* Hiding markers for specific locations */
/*****************************************/

function hideMarkers() {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
    }
    hideAllMarkers();
}

  /***************************************************/
 /* Bounce animation on the markers on click events */
/***************************************************/

function toggleBounce(marker) {
    if (last) last.setAnimation(null);
    if (marker.getAnimation() !== null) {
        marker.setAnimation(null);
    } else {
        marker.setAnimation(google.maps.Animation.BOUNCE);
    }
    last = marker;
}

   /************************************************/
  /*  Populating info-window with the location's  */
 /* information acquired from the foursquare API */
/************************************************/

function populateInfoWindow(marker, infoWindow) {
    if (lastInfoWindow) lastInfoWindow.close();
    if (infoWindow.marker != marker) {
        infoWindow.marker = marker;
        infoWindow.setContent(`<div><h6>${marker.title}</h6></div><div style="max-width:150px;"><strong>Address:</strong> ${marker.address}</div>`);
        infoWindow.open(map, marker);
        infoWindow.addListener('closeclick', function() {
            infoWindow.setMarker = null;
        });
    }
    lastInfoWindow = infoWindow;
}

  /*************************/
 /* Document ready events */
/*************************/

$(function() {
    $('select').material_select();
    $('#menu').click(function() {
        $('#float').toggleClass('floating-panel-open');
    });
});

    /******************************************************************************************************/
   /*/                                   /***********************/                                      /*/
  /*/                                   /* Knockout View Model */                                      /*/
 /*/                                   /***********************/                                      /*/
/******************************************************************************************************/

var types = ['Coffee', 'Pizza', 'Icecream', 'Buffet'];
var count = 0;

  /***************************************************/
 /* Function to create objects of the data recieved */
/***************************************************/

var place = function(data) {
    this.id = count++;
    this.name = data.venue.name;
    this.location = {
        lat: data.venue.location.lat,
        lng: data.venue.location.lng
    };
    this.address = data.venue.location.formattedAddress.join(" ");
};

  /*********************************************/
 /* object for saving locations in categories */
/*********************************************/

var places = {
    Coffee: [],
    Pizza: [],
    Icecream: [],
    Buffet: []
};

  /********************************************************/
 /* pushes places in places object arrays in object form */
/********************************************************/

var createPlaces = function(data, index) {
    var createdPlaces=0;
    data.forEach(function(i) {
        places[index].push(new place(i));
        createdPlaces++;
        doubleAllow=0;
        createMarkers(index,1);
    });

};

  /****************************/
 /* Main view model function */
/****************************/

var viewModel = function() {
    var self = this;
    this.categoryList = ko.observableArray([]);
    this.categoryList = types;
    this.currentCategory = ko.observable();
    this.listPlaces = ko.observableArray([]);

      /*******************/
     /* Event listeners */
    /*******************/

    this.runGPS = function() {
        gps();
    };

    this.searchBTN = function() {
        findArea();
        self.currentCategory = ko.observable();
    };

      /****************************************************************/
     /* Animates particular marker when an object in list is clicked */
    /****************************************************************/

    this.showParticularMarker = function(marker) {
        markers.forEach(function(single) {
            if (single.title === marker) bouncingMarker = single;
        });
        toggleBounce(bouncingMarker);
        var largeInfoWindow = new google.maps.InfoWindow();
        populateInfoWindow(bouncingMarker, largeInfoWindow);
    };

      /*******************************************/
     /* populates list of places on click event */
    /*******************************************/

    this.populate = function(type) {
        if(type.currentCategory()===undefined)
            return;
        self.listPlaces.removeAll();
        for (var j = 0; j < places[type.currentCategory()].length; j++) {
            self.listPlaces.push(places[type.currentCategory()][j].name);
        }
    };

       /***************************************/
      /* If none of the categories selected, */
     /* then displays all locations in list */
    /***************************************/

    this.allList = function() {
        self.listPlaces.removeAll();
        for(var i=0;i<types.length;i++){
            for(var j=0;j<places[types[i]].length;j++) {
                if(places[types[i]][j].name!==undefined)
                    self.listPlaces.push(places[types[i]][j].name);
            }
        }
    };

      /***********************************************/
     /* Changes category on selection from dropdown */
    /***********************************************/

    this.changePlace = function() {
        hideMarkers();
        hideAllMarkers();
        if (self.currentCategory() === undefined) {
            markers = allMarkers;
            showAllMarkers();
            self.allList();
        } else {
            createMarkers(self.currentCategory(),0);
            showMarkers();
        }
    };
};

var vm = new viewModel();
ko.applyBindings(vm);
