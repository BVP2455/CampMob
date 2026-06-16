# Semana 1 - Día 2

Fecha: 05/05/2026

## Objetivo del día
Entender mejor la estructura básica de NetLogo, empezar a investigar cómo importar mapas reales del campus usando la extensión GIS y empezar a elaborar el primer modelo del simulador en NetLogo con algún dato recibido.

## Datos recibidos para modelar campus en NetLogo
Carpeta gross_data:
- buildings
- roads
- zone
- bâtiment.gpkg

Carpeta net_data:
- busway
- pedestrian
- bicycle
- footway
- motorway

## Tareas
- Revisar estructura básica de modelos NetLogo.
- Investigar la extensión GIS.
- Crear un primer archivo base del simulador, con algún shapefile ya dibujado.
- Elaborar un pequeño informe de errores que he tenido.

## Notas
Hoy dia 5 de mayo, he empezado el día asistiendo a una defensa de tesis de una persona del equipo que finalmente se ha convertido en doctor tras la aprobación del comité. Posteriormente por la tarde, he empezado a trabajar siguiendo los modelos de aprendizaje de NetLogo para saber como funcionan los principales componentes que vamos a necesitar en NetLogo, he reforzado los conceptos de setup y go, básicos en las interacciones con el modelo, ya que setup reincia el modelo y go empieza a correr la simulación. Después, Louis me ha dado un conjunto de datos shapefile que me van a servir para definir el campus para el simulador. Tal y como me los ha dado me he puesto a entender como funcionan este tipo de datos y como se utilizan en NetLogo gracias a los modelos que tienen en sus librerías, me he fijado en los modelos GIS Gradient Example y GIS General Example que son ejemplos de como se utiliza la extensión gis en NetLogo, el primer ejemplo simula como la lluvia sigue la bajada por la superficie terrestre, y el segundo demuestra el funcionamiento de esta extensión creando el mapa del mundo con las distintas ciudades, países, etc.

Antes de ponerme con mi propio modelo he revisado como se crean, para que sirven y que tipo de variables existen. A través de la documentación he encontrado la siguiente información. Existen 4 tipos:
- globals: representa una variable que va a compartir todo el modelo. Se les da/cambia el valor con set.
- turtles: son agentes móviles, y cada una puede tener sus propios datos usando turtle-own.
- patches: son la base del modelo, donde se va a construir la simulación, para patches propios usamos patches-own.
- let: variable temporal que se crea dentro de un bloque de código cuando sea necesaria.

Después tenemos breed que lo utilizamos para que todas las turtle no tengan las mismas variables. Con cada breed, se hace un breed-own si quieres ponerle atributos propios a cada uno.

Una vez visto los tipos de variables me he puesto a crear mi propio modelo y que será el primer prototipo del simulador. He empezado importando los edificios del campus en NetLogo, con los archivos que me habia pasado Louis, he utilizado la extensión GIS para poder importarlo y dibujarlo en la interfaz y he creado el boton de setup donde al pulsarlo salta toda la logica para que salgan los edificios. Tuve problemas para importarlo porque era la primera vez que escribía código en esta aplicación, por ejemplo al principio no utilizaba los primitives correctos y me daba algunos errores, pasé a no tener errores pero no funcionaba cuando le daba al boton que habia creado en la interfaz, debido a que en la pestaña comandos del botón no había puesto nada. Una vez arreglado le daba pero no se ejecutaba del todo porque estaba marcado el Forever dentro de la configuración del botón y también tenía el fondo negro y los edificios se me dibujaban en negro por lo que tampoco lo veía. Errores de novato en general, pero finalmente conseguí ver los edificios en pantalla tras corregir todos estos errores.

![Primer avance en simulador](../images/buildings.png)