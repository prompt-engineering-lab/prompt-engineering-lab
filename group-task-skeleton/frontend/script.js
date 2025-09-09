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

    function setInputFromMarker(marker, inputId) {
        const latlng = marker.getLatLng();
        document.getElementById(inputId).value = latlng.lat.toFixed(6) + ',' + latlng.lng.toFixed(6);
    }

    map.on('click', function(e) {
        if (!startMarker) {
            startMarker = L.marker(e.latlng, {draggable: true}).addTo(map);
            setInputFromMarker(startMarker, 'start-coord');
            startMarker.on('dragend', function() {
                setInputFromMarker(startMarker, 'start-coord');
            });
        } else if (!endMarker) {
            endMarker = L.marker(e.latlng, {draggable: true, icon: L.icon({iconUrl: 'https://cdn-icons-png.flaticon.com/512/684/684908.png', iconSize: [25, 41], iconAnchor: [12, 41]})}).addTo(map);
            setInputFromMarker(endMarker, 'end-coord');
            endMarker.on('dragend', function() {
                setInputFromMarker(endMarker, 'end-coord');
            });
        }
    });

    // Allow manual input
    document.getElementById('start-coord').addEventListener('change', function() {
        const val = this.value.split(',');
        if (val.length === 2 && !isNaN(val[0]) && !isNaN(val[1])) {
            const latlng = [parseFloat(val[0]), parseFloat(val[1])];
            if (startMarker) { startMarker.setLatLng(latlng); } else { startMarker = L.marker(latlng, {draggable: true}).addTo(map); }
            map.panTo(latlng);
        }
    });
    document.getElementById('end-coord').addEventListener('change', function() {
        const val = this.value.split(',');
        if (val.length === 2 && !isNaN(val[0]) && !isNaN(val[1])) {
            const latlng = [parseFloat(val[0]), parseFloat(val[1])];
            if (endMarker) { endMarker.setLatLng(latlng); } else { endMarker = L.marker(latlng, {draggable: true, icon: L.icon({iconUrl: 'https://cdn-icons-png.flaticon.com/512/684/684908.png', iconSize: [25, 41], iconAnchor: [12, 41]})}).addTo(map); }
            map.panTo(latlng);
        }
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
