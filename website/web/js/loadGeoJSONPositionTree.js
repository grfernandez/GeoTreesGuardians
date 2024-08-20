 // Inicializa el mapa centrado en Formosa, Argentina
 const map = L.map('map').setView([-26.1775, -58.1781], 13);

 // Agrega la capa de OpenStreetMap
 L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
     attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
 }).addTo(map);

 // Añadir un marcador como ejemplo
 L.marker([-26.1775, -58.1781]).addTo(map)
     .bindPopup('Formosa.<br> Imprerio del Verde.')
     .openPopup();

// Función para cargar GeoJSON desde un archivo
// Cargar y añadir el archivo GeoJSON al mapa
fetch('data/trees_layer.geojson')
.then(response => response.json())
.then(data => {
    L.geoJSON(data, {
        pointToLayer: function (feature, latlng) {
            return L.circleMarker(latlng, {
                //radius: feature.properties.radius / 10, // Ajuste de radio, puedes modificar este valor según la escala que necesites
                color: 'green',
                fillColor: '#00ff00',
                fillOpacity: 0.5

            });
        },
        onEachFeature: function (feature, layer) {
            if (feature.properties && feature.properties.denominacion) {
                var popupContent = '<h4>' + feature.properties.denominacion + '</h4>' +
                               '<p>' + feature.properties.especie + '</p>' +
                               '<img src="' + feature.properties.image + '" style="width:100%;height:auto;">';

            // Asociar el contenido al popup del layer
            layer.bindPopup(popupContent);
            //layer.bindPopup(feature.properties.denominacion);
            }
        }
    }).addTo(map);
})
.catch(error => console.error('Error cargando el archivo GeoJSON:', error));












// Cargar los datos GeoJSON


//Healthy Layer
//loadGeoJSON('data/healthy_layer.geojson', function (data) {
//    window.healthyLayer = L.geoJSON(data).addTo(map);
//});
