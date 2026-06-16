# Semana 4 - Día 1

Fecha: 26/05/2026

## Objetivo del día
Empezamos el día con una reunión con Adrien y Guillaume donde cada uno exponemos lo que llevamos hecho. En el día de hoy tengo pensado corregir el tema de la velocidad ya que es raro que entre nodos la velocidad sea la que aparece en el slider, pero después cuando llega a una zona donde hay muchos nodos juntos se ralentiza el agente incluso va con cortes. Por lo que, tengo que solucionar este problema.

## Tareas
- Reunión con Adrien y Guillaume. Exponerles el trabajo realizado.
- Corregir la velocidad del agente en el grafo.
- Preguntar por como puedo implementar mejor el tiempo, porque ahora mismo hay un reloj donde cada tick es 1 segundo pero no sé si debe ser así.

## Notas
Hoy día 26 de mayo, hemos tenido la reunión con Adrien y Guillaume. Les he estado explicando como funciona mi grafo y funcionalidades. En general, me han dicho que funciona bastante bien, yo les he estado preguntando por el tema de la velocidad y como puedo abordarlo, y me ha comentado que él en su modelo tiene de distinta forma la velocidad. Utiliza la primitiva de NetLogo para moverse "fd" a la cual le da un valor y esta sigue el camino hasta recibir otra instrucción. Una vez que se encuentra con el siguiente nodo le dice al agente que cambie su orientación mirando al siguiente nodo con la función "face". Y que con eso podía seguir un camino con la misma velocidad todo el tiempo sin interrupciones ni nada. Así que por la tarde me puse a implementarlo y a ver algún cambio.