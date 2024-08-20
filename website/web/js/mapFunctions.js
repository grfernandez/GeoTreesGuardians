// Función para manejar el popup y eventos de clic
function setupMapInteractions() {
    if (window.treeLayer) {
        window.treeLayer.eachLayer(function (layer) {
            var properties = layer.feature.properties;
            console.log('Punto clickeado:', properties.denominacion); 
            // Crear el contenido del popup con una imagen
            var popupContent = '<h4>' + properties.denominacion + '</h4>' +
                               '<p>' + properties.especie + '</p>' +
                               '<img src="' + properties.image + '" alt="' + properties.denominacion + '" style="width:100%;height:auto;">';

            // Asociar el contenido al popup del layer
            layer.bindPopup(popupContent);

            // Evento de clic para actualizar el frame a la izquierda
            layer.on('click', function () {
                console.log('Punto clickeado:', properties.denominacion); 
                var info = document.getElementById('info');
                info.innerHTML = popupContent;
            });
            layer.on('mouseover', function (e) {
                console.log('Mouse sobre:', layer.feature.properties.denominacion);
            });
        });
    }
/*
    if (window.healthyLayer) {
        window.healthyLayer.eachLayer(function (layer) {
            var properties = layer.feature.properties;
            console.log('Punto clickeado:', properties.denominacion); 
            // Crear el contenido del popup con una imagen
            var popupContent = '<h4>' + properties.denominacion + '</h4>' +
                               '<p>' + properties.especie + '</p>' +
                               '<img src="' + properties.image + '" alt="' + properties.denominacion + '" style="width:100%;height:auto;">';

            // Asociar el contenido al popup del layer
            layer.bindPopup(popupContent);

            // Evento de clic para actualizar el frame a la izquierda
            layer.on('click', function () {
                var info = document.getElementById('info');
                info.innerHTML = popupContent;
            });
        });
    }*/
}

// Configurar las interacciones del mapa después de cargar los GeoJSON
window.onload = setupMapInteractions;
