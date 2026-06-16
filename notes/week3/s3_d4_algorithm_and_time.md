# Semana 3 - Día 4

Fecha: 21/05/2026

## Objetivo del día
Reunión diaria con el grupo y comentar con Bruno el problema de las intersecciones y como es que interactua el coche con el grafo. Implementar el algoritmo de camino mínimo entre dos puntos añadiendo pesos a las aristas, con la distancia entre los puntos. Además, en la última reunión Bruno me dijo que tenía que desarrollarse el proceso con un timing que fuese realista, voy a intentar implementarlo hoy también.

## Tareas
- Reunión diaria para definir tareas del día.
- Solucionar direcciones con las intersecciones y revisar el funcionamiento del grafo.
- Implementar el algoritmo de shortest path entre dos puntos del campus, donde hay que poner peso en los edges que debe ser la distancia entre punto y punto.
- Implementar el timing dentro del simulador con ciclos y un contador que vaya contando esos ciclos.

## Notas
Hoy día 21 de mayo, hemos tenido la reunión diaria del día a las 10 a.m., he estado hablando con Bruno sobre el problema de las intersecciones que encontraba, y hemos estado discutiendo de si debería ser así o que no fuese posible. Me aclaro bastante como debían ser las distintas intersecciones y que sentido debían llevar los agentes. Tuve que corregir una pequeña cosa de como lo tenia ya que le faltaba a cada intersección el punto/nodo que unía los distintos caminos, sin él no se podrían conectar correctamente siempre llevarían el mismo camino. Tras todo esto me puse a elaborar el algoritmo de camino mínimo para unir dos puntos del grafo por el camino más corto. Para ello, utilicé Dijkstra. Creé dos botones para poder elegir el origen y el destino del camino, y un tercer botón que ejecute este algoritmo una vez que están definidos ambos puntos, si no hay camino posible te lo indica con un alert el sistema.