var map = L.map('map'),
    trail = {
        type: 'Feature',
        properties: {
            id: 1
        },
        geometry: {
            type: 'LineString',
            coordinates: []
        }
    },
    realtime = L.realtime(function(success, error) {
        fetch('https://gist.githubusercontent.com/JakobSchoeberle/d7668de1b3e11f3012cd917f4f4c0db8/raw/473f70d01ee4af31f6f2315be23598f3589d723e/GeoJson.json')
        .then(function(response) { return response.json(); })
        .then(function(data) {
            var trailCoords = trail.geometry.coordinates;
            trailCoords.splice(0, Math.max(0, trailCoords.length - 5));
            success({
                type: 'FeatureCollection',
                features: [data, trail]
            });
        })
        .catch(error);
    }, {
        interval: 150
    }).addTo(map);
/*
L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);
*/
L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager_labels_under/{z}/{x}/{y}{r}.png', {
	attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
	subdomains: 'abcd',
	maxZoom: 20
}).addTo(map);
/*L.control.layers(null, {
    'Earthquakes 2.5+': realtime1,
    'All Earthquakes': realtime2
}).addTo(map);
*/
realtime.once('update', function() {
    map.fitBounds(realtime.getBounds(), {maxZoom: 3});
});
