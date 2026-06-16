# Semana 2 - Día 2

Fecha: 12/05/2026

## Objetivo del día
Tras la reunión con Adrien y Guillaume de ayer y el grafo realizado a mano sobre el modelo, hoy Bruno me dijo que se pondría a trabajar conmigo por la mañana para aclarar ciertos temas del grafo y el modelo. Por la tarde seguiré avanzando en lo trabajado por la mañana para dejarlo bien definido y que sea el grafo final.

## Tareas
- Reunión diaria con el grupo para comentar que hemos hecho y que vamos a hacer cada uno.
- Trabajar con Bruno sobre el grafo del modelo sobre el que circularán los agentes.
- Afinar el grafo para que sea el definitivo.

## Notas
Hoy día 12 de mayo, tuvimos una reunión diaria todo el grupo para establecer el plan de trabajo de cada uno y hacer un breve repaso de lo que habíamos hecho hasta ahora, estuvo bien para repasar y plantear dudas de lo que teniamos que hacer cada uno. Posteriormente, he trabajado con Bruno tal y como me dijo para afinar el grafo. Coincidimos en que el grafo no podía ser manual ya que ir dibujando uno a uno los nodos e ir conectandolos no es eficiente. Para solucionar esta situación, primero realicé dos csv, uno con los nodos y otro con los edges del modelo, estos extraidos con un script de Python de los shapefiles que me habia pasado Louis. La solución no era mala, de hecho pienso que era la mejor, pero Bruno intentó hacerlo directamente sobre el código de NetLogo cogiendo el shapefile y extrayendo de él los datos necesarios para hacer el grafo. De esa forma funcionaba y era bastante más rápido y efectivo, por lo que nos quedamos con esa opción. 

Por la tarde ya sin Bruno, pero con la idea definida seguí implementando el grafo para quedarnos con el definitivo. Al principio tuve algún error con las conexiones entre distintos nodos porque se conectaban directamente sin pasar por todos los puntos que había en la carretera, porque no recorría bien las aristas. Finalmente, deje el grafo bien armado, con todas las aristas pasando por los distintos nodos y waypoints, y cubriendo a la perfección el campus.