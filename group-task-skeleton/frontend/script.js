document.addEventListener('DOMContentLoaded', () => {

    const jsonOutputTextarea = document.getElementById('json-output');
    const statusMessageDiv = document.getElementById('status-message');

    // --- MAPA ---
    var map = L.map('map').setView([51.1079, 17.0385], 13); // Wroclaw center
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    let startMarker = null;
    let endMarker = null;
    let nextMarkerType = 'start'; // 'start' or 'end'

    // Custom icons
    const startIcon = L.icon({
        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
    });

    const endIcon = L.icon({
        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
    });

    function setInputFromMarker(marker, inputId) {
        const latlng = marker.getLatLng();
        document.getElementById(inputId).value = latlng.lat.toFixed(6) + ',' + latlng.lng.toFixed(6);
    }

    function createMarker(latlng, type) {
        const icon = type === 'start' ? startIcon : endIcon;
        const marker = L.marker(latlng, {draggable: true, icon: icon}).addTo(map);
        marker.bindPopup(type === 'start' ? 'Start Point' : 'Destination');
        
        marker.on('dragend', function() {
            setInputFromMarker(marker, type === 'start' ? 'start-coord' : 'end-coord');
        });
        
        return marker;
    }

    map.on('click', function(e) {
        if (nextMarkerType === 'start') {
            if (startMarker) {
                map.removeLayer(startMarker);
            }
            startMarker = createMarker(e.latlng, 'start');
            setInputFromMarker(startMarker, 'start-coord');
            nextMarkerType = 'end';
        } else {
            if (endMarker) {
                map.removeLayer(endMarker);
            }
            endMarker = createMarker(e.latlng, 'end');
            setInputFromMarker(endMarker, 'end-coord');
            nextMarkerType = 'start';
        }
    });

    // Allow manual input
    document.getElementById('start-coord').addEventListener('change', function() {
        const val = this.value.split(',');
        if (val.length === 2 && !isNaN(val[0]) && !isNaN(val[1])) {
            const latlng = [parseFloat(val[0]), parseFloat(val[1])];
            if (startMarker) {
                startMarker.setLatLng(latlng);
            } else {
                startMarker = createMarker(latlng, 'start');
            }
            map.panTo(latlng);
        }
    });
    
    document.getElementById('end-coord').addEventListener('change', function() {
        const val = this.value.split(',');
        if (val.length === 2 && !isNaN(val[0]) && !isNaN(val[1])) {
            const latlng = [parseFloat(val[0]), parseFloat(val[1])];
            if (endMarker) {
                endMarker.setLatLng(latlng);
            } else {
                endMarker = createMarker(latlng, 'end');
            }
            map.panTo(latlng);
        }
    });

    // Add buttons to switch marker selection mode
    document.getElementById('start-coord').addEventListener('focus', function() {
        nextMarkerType = 'start';
        displayStatus('Click on map to set start point (green marker)', 'text-green-600');
    });
    
    document.getElementById('end-coord').addEventListener('focus', function() {
        nextMarkerType = 'end';
        displayStatus('Click on map to set destination (red marker)', 'text-red-600');
    });

    // --- FORMULARZ ---
    document.getElementById('search-form').addEventListener('submit', function(e) {
        e.preventDefault();
        jsonOutputTextarea.value = '';
        displayStatus('Searching for departures... (API integration needed)', 'text-blue-600');
        // Tu docelowo wywołanie API
    });

    function displayStatus(message, colorClass) {
        statusMessageDiv.textContent = message;
        statusMessageDiv.className = `mt-4 text-center text-sm font-semibold ${colorClass}`;
    }
});
