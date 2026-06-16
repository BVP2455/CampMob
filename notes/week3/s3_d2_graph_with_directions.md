# Semana 3 - Día 2

Fecha: 19/05/2026

## Objetivo del día
Reunión diaria con el grupo y analizar la situación en la que me encuentro para reconocer el siguiente paso que debo realizar si crear nuevos agentes, empezar a realizar algunas restricciones sobre el agente que ya tenemos, definir los trayectos que van a seguir, afinar los caminos y las posibles trayectorias porque no puede ser que un vehículo vaya de un nodo a otro y después pueda volver sobre el mismo camino aunque tenga doble sentido esa carretera, porque en la vida real un coche no puede en la misma carretera cambiar el sentido como el quiera, hay que poner una restricción a eso.

## Tareas
- Reunión diaria para definir tareas del día.
- Implementar restricción o caminos dirigidos para que el agente no pueda ser totalmente aleatorio.
- Preguntar por siguientes pasos a seguir después de la implementación del grafo con el agente del coche.

## Notas
Hoy día 19 de mayo, nos hemos reunido todo el grupo en Manufactures a las 9 de la mañana para realizar la Week Meeting. En esta hemos acordado lo que va a realizar cada uno y lo que ha hecho. Yo expuse los avances que había conseguido tras la implementación del grafo junto a la creación y movimiento de los vehículos, y expuse las distintas dudas que tenía respecto a los siguientes pasos y a algún aspecto lógico como las trayectorias/direcciones que cojen los vehículos en las distintas carreteras. A esto me propuso una solución, la cual es la que voy a tomar. Duplicar los nodos de cada posición en donde las carreteras salientes o entrantes tengan ambas direccionalidades para hacer dos caminos distintos una de una dirección y la otra de la contrasrioa. Para ello tuve que cambiar como se generaba el grafo totalmente, como se hacían las conexiones y las intersecciones. Tras los cambios realizados los caminos son más realistas, pero las intersecciones no funcionan del todo bien, ya que cuando llega a una este toma la decisión un poco al azar y hay decisiones que en la realidad no puede tomar. Mañana preguntaré a Bruno y intentaré mejorar eso.