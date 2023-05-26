## **Santiago Aguilar Cardenas**

**Este código es un programa de juego de memoria (*Memorama*) desarrollado en Python utilizando la biblioteca Pygame. 
Básicamente, lo que hace cada parte del código es lo siguiente:**

1. **Importaciones:** El código importa varios módulos necesarios para el juego, como math para operaciones matemáticas, pygame para la manipulación de gráficos y sonidos, sys para salir del juego, time para controlar el tiempo, y random para generar números aleatorios.

2. **Inicialización:** Se inicializa la biblioteca Pygame y se configuran algunos componentes, como la fuente de texto, el mezclador de sonido y se carga una imagen oculta que se utilizará para cubrir las tarjetas del juego.

3. **Clase Cuadro:** Esta clase representa una tarjeta del juego de memoria. Cada tarjeta tiene una imagen, un estado de mostrar o descubierto, y una fuente de imagen que se utiliza para comparar las tarjetas.

4. **Arreglo de objetos cuadros:** Se crea una matriz de objetos Cuadro que representan las tarjetas del juego. Cada tarjeta se carga con una imagen correspondiente.

5. **Variables y configuración:** Se definen variables y constantes que se utilizan en el juego, como el tamaño de los botones, el tamaño de las imágenes, los colores, los sonidos, etc.

6. **Funciones auxiliares:** Se definen varias funciones auxiliares que se utilizan en el juego, como ocultar todas las tarjetas, aleatorizar las tarjetas, verificar si se ha ganado el juego, reiniciar el juego, etc.

7. **Decoradores:** Se definen dos decoradores: medir_tiempo_de_ejecucion y reproducir_sonido_al_ejecutar. Estos decoradores se utilizan para medir el tiempo de ejecución de un método y reproducir un sonido al ejecutar una función, respectivamente.

8. **Función iniciar_juego:** Esta función se ejecuta al hacer clic en el botón de inicio. Aleatoriza las tarjetas, oculta todas las tarjetas y marca el inicio del juego.

9. **Ciclo principal del juego:** El programa entra en un ciclo infinito donde se escuchan los eventos del usuario y se actualiza la pantalla del juego. El ciclo principal se ejecuta hasta que el juego se cierre.

10. **Eventos del usuario:** Dentro del ciclo principal, se escuchan los eventos del usuario, como clics del mouse. Dependiendo del evento, se realizan diferentes acciones, como iniciar el juego, descubrir una tarjeta, comprobar si se ha ganado, etc.

11. **Actualización de la pantalla:** En cada iteración del ciclo principal, se actualiza la pantalla del juego. Se dibujan las tarjetas según su estado (descubierto o oculto) y se dibuja el botón de inicio.