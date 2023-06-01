import math      # Redondear.
import pygame 
import sys       # Para salir con el click. Exit Game
import time      # Ciclo infinito.
import random    # Randonizar (cambio de posición). 


#Iniciamos con pygame para usar sonido, pantalla...
pygame.init()
pygame.font.init()  # Número de fuente.
pygame.mixer.init() # Sonidos.


#Variables y configuración a utilizar.
altura_boton = 30    # Botón para iniciar el juego.
medida_cuadro = 200  # Medida de la imágen en píxeles.


#Para la parte trasera de cada imágen.
nombre_imagen_oculta = "Tapar.png"
imagen_oculta = pygame.image.load(nombre_imagen_oculta)
segundos_mostrar_pieza = 2 #Ocultar pieza si no es la correcta


"""
Una clase que representa el cuadro. El mismo tiene una imagen y puede estar
descubierto (cuando ya lo han descubierto anteriormente y no es la tarjeta buscada actualmente)
o puede estar mostrado (cuando se voltea la imagen)
También tiene una fuente o nombre de imagen que servirá para compararlo más tarde
"""

#Punto donde utilizamos *arg, **Kwargs y un decorador
#*args y **kwargs son utilizados en el decorador medir_tiempo_de_ejecucion para permitir que el decorador acepte cualquier número de 
# argumentos posicionales y de palabras clave, y luego los pasa a la función func cuando se llama a func(*args, **kwargs). 
# Esto asegura que el decorador sea compatible con cualquier función que se decore con él, independientemente de la cantidad y tipo de 
# argumentos que la función pueda aceptar.
# Decorador para medir el tiempo de ejecución de un método y se utilizan *arg 
def medir_tiempo_de_ejecucion(func):
    def wrapper(*args, **kwargs):   # Retornar la funcion decorada
        import time
        inicio = time.time()
        resultado = func(*args, **kwargs)
        fin = time.time()
        tiempo_total = fin - inicio
        print(f"Tiempo de ejecución de {func.__name__}: {tiempo_total} segundos")
        return resultado
    return wrapper



class Ejemplo:  #Usamos el decorador
    @medir_tiempo_de_ejecucion
    def metodo_ejemplo(self):
        # Simulación de un proceso que toma tiempo
        time.sleep(2)             # se utiliza para pausar la ejecución de un programa durante un determinado período de tiempo
        print("Método ejecutado")

# Crear una instancia de la clase y llamar al método decorado
ejemplo = Ejemplo()
ejemplo.metodo_ejemplo()



class Cuadro:                        #Constructor
    def __init__(self, fuente_imagen):     #Si se muestra, no se descubre
        self.mostrar = True
        self.descubierto = False
        """
        Una cosa es la fuente de la imagen (es decir, el nombre del archivo) y otra
        la imagen lista para ser pintada por PyGame
        La fuente la necesitamos para más tarde, comparar las tarjetas
        """
        self.fuente_imagen = fuente_imagen
        self.imagen_real = pygame.image.load(fuente_imagen)



# Arreglo de objetos.
cuadros = [
    [Cuadro("Astronauta.png"), Cuadro("Astronauta.png"),
     Cuadro("Blackhole.png"), Cuadro("Blackhole.png")],
    [Cuadro("Brillo.png"), Cuadro("Brillo.png"),
     Cuadro("cometa.png"), Cuadro("cometa.png")],
    [Cuadro("espacio.png"), Cuadro("espacio.png"),
     Cuadro("galaxia.png"), Cuadro("galaxia.png")],
    [Cuadro("planetas.png"), Cuadro("planetas.png"),
     Cuadro("universo.png"), Cuadro("universo.png")],
]


#Colores.
color_blanco = (255, 255, 255)
color_negro = (0, 0, 0)
color_gris = (206, 206, 206)
color_azul = (30, 136, 229)


#Sonidos.
sonido_fondo = pygame.mixer.Sound("Fondo.wav.ogg")
sonido_clic = pygame.mixer.Sound("click.wav.wav")
sonido_exito = pygame.mixer.Sound("ganar.wav.wav")
sonido_fracaso = pygame.mixer.Sound("equivocado.wav.wav")
sonido_voltear = pygame.mixer.Sound("pasar.wav.wav")


#Calculamos el tamaño de la pantalla en base al tamaño de los cuadros.
anchura_pantalla = len(cuadros[0]) * medida_cuadro
altura_pantalla = (len(cuadros) * medida_cuadro) + altura_boton
anchura_boton = anchura_pantalla


#La fuente que estará sobre el botón.
tamanio_fuente = 20
fuente = pygame.font.SysFont("Arial", tamanio_fuente)
xFuente = int((anchura_boton / 2) - (tamanio_fuente / 2))
yFuente = int(altura_pantalla - altura_boton)


#El botón, que al final es un rectángulo.
boton = pygame.Rect(0, altura_pantalla - altura_boton,
                    anchura_boton, altura_pantalla)


#Banderas:

#Bandera para saber si se debe ocultar la tarjerta durante N segundos.
ultimos_segundos = None

#Bandera para saber si reaccionar a los eventos del usuario.
puede_jugar = True

#Saber si el juego está iniciado; así sabemos si ocultar o mostrar piezas.
juego_iniciado = False

#Bandera de las tarjetas cuando se busca una pareja.
x1 = None   #Sirve para la primera tarjeta.
y1 = None   #Sirve para la primera tarjeta.
x2 = None   #Sirve para la segunda tarjeta.
y2 = None   #Sirve para la segunda tarjeta.



# Ocultar todos los cuadros
def ocultar_todos_los_cuadros():
    for fila in cuadros:
        for cuadro in fila:
            cuadro.mostrar = False
            cuadro.descubierto = False


def aleatorizar_cuadros():
    # Elegir X e Y aleatorios, intercambiar
    cantidad_filas = len(cuadros)
    cantidad_columnas = len(cuadros[0])
    for y in range(cantidad_filas):
        for x in range(cantidad_columnas):
            x_aleatorio = random.randint(0, cantidad_columnas - 1)
            y_aleatorio = random.randint(0, cantidad_filas - 1)
            cuadro_temporal = cuadros[y][x]
            cuadros[y][x] = cuadros[y_aleatorio][x_aleatorio]
            cuadros[y_aleatorio][x_aleatorio] = cuadro_temporal


def comprobar_si_gana():
    if gana():
        pygame.mixer.Sound.play(sonido_exito)
        reiniciar_juego()


# Regresa False si al menos un cuadro NO está descubierto. True en caso de que absolutamente todos estén descubiertos
def gana():
    for fila in cuadros:
        for cuadro in fila:
            if not cuadro.descubierto:
                return False
    return True


def reiniciar_juego():
    global juego_iniciado
    juego_iniciado = False


##########################

def reproducir_sonido_al_ejecutar(func):
    def wrapper(*args, **kwargs):
        pygame.mixer.Sound.play(sonido_clic)
        resultado = func(*args, **kwargs)
        return resultado
    return wrapper



#################

@reproducir_sonido_al_ejecutar
def iniciar_juego():
    pygame.mixer.Sound.play(sonido_clic)
    global juego_iniciado
    # Aleatorizar 3 veces
    for i in range(3):
        aleatorizar_cuadros()
    ocultar_todos_los_cuadros()
    juego_iniciado = True


#Iniciamos la pantalla con las medidas previamente calculadas, colocamos título y reproducimos el sonido de fondo.
pantalla_juego = pygame.display.set_mode((anchura_pantalla, altura_pantalla))
pygame.display.set_caption('Memorama en Python') #Título
pygame.mixer.Sound.play(sonido_fondo, -1) #El -1 indica un loop infinito.




#Ciclo infinito.
while True:  

    #Escuchar eventos, ciclo infinito que se repite varias veces por segundo.
    for event in pygame.event.get():
        # Si quitan el juego, salimos
        if event.type == pygame.QUIT:
            sys.exit()
        # Si hicieron clic y el usuario puede jugar...
        elif event.type == pygame.MOUSEBUTTONDOWN and puede_jugar:

            """
            xAbsoluto e yAbsoluto son las coordenadas de la pantalla en donde se hizo
            clic. PyGame no ofrece detección de clic en imagen, por ejemplo. Así que
            se deben hacer ciertos trucos
            """
            # Si el click fue sobre el botón y el juego no se ha iniciado, entonces iniciamos el juego
            xAbsoluto, yAbsoluto = event.pos

            #Código que verifica si el botón ha sido presionado dentro de un bloque try
            try:
                if boton.collidepoint(event.pos):
                    if not juego_iniciado:
                        iniciar_juego()
                else:
                    # Si no hay juego iniciado, ignoramos el clic
                    if not juego_iniciado:
                        raise Exception("No hay juego iniciado")
            except Exception as e:
                print(e)
           
        
            if boton.collidepoint(event.pos):
                if not juego_iniciado:
                    iniciar_juego()

            else:
                # Si no hay juego iniciado, ignoramos el clic
                if not juego_iniciado:
                    continue
                """
                Ahora necesitamos a X e Y como índices del arreglo. Los índices no
                son lo mismo que los pixeles, pero sabemos que las imágenes están en un arreglo
                y por lo tanto podemos dividir las coordenadas entre la medida de cada cuadro, redondeando
                hacia abajo, para obtener el índice.
                Por ejemplo, si la medida del cuadro es 100, y el clic es en 140 entonces sabemos que le dieron
                a la segunda imagen porque 140 / 100 es 1.4 y redondeado hacia abajo es 1 (la segunda posición del
                arreglo) lo cual es correcto. Por poner otro ejemplo, si el clic fue en la X 50, al dividir da 0.5 y
                resulta en el índice 0
                """
                x = math.floor(xAbsoluto / medida_cuadro)    #Se obtiene el índice del arreglo.
                y = math.floor(yAbsoluto / medida_cuadro)
                # Primero lo primero. Si  ya está mostrada o descubierta, no hacemos nada
                cuadro = cuadros[y][x]
                if cuadro.mostrar or cuadro.descubierto:
                    # continue ignora lo de abajo y deja que el ciclo siga
                    continue
                
                # Si es la primera vez que tocan la imagen (es decir, no están buscando el par de otra, sino apenas
                # están descubriendo la primera)
                if x1 is None and y1 is None:
                    # Entonces la actual es en la que acaban de dar clic, la mostramos
                    x1 = x
                    y1 = y
                    cuadros[y1][x1].mostrar = True
                    pygame.mixer.Sound.play(sonido_voltear)
                else:
                    # En caso de que ya hubiera una clickeada anteriormente y estemos buscando el par, comparamos...
                    x2 = x
                    y2 = y
                    cuadros[y2][x2].mostrar = True
                    cuadro1 = cuadros[y1][x1]
                    cuadro2 = cuadros[y2][x2]
                    # Si coinciden, entonces a ambas las ponemos en descubiertas:
                    if cuadro1.fuente_imagen == cuadro2.fuente_imagen:
                        cuadros[y1][x1].descubierto = True
                        cuadros[y2][x2].descubierto = True
                        x1 = None
                        x2 = None
                        y1 = None
                        y2 = None
                        pygame.mixer.Sound.play(sonido_clic)
                    else:
                        pygame.mixer.Sound.play(sonido_fracaso)
                        # Si no coinciden, tenemos que ocultarlas en el plazo de [segundos_mostrar_pieza] segundo(s). Así que establecemos
                        # la bandera. Como esto es un ciclo infinito y asíncrono, podemos usar el tiempo para saber
                        # cuándo fue el tiempo en el que se empezó a ocultar
                        ultimos_segundos = int(time.time())
                        # Hasta que el tiempo se cumpla, el usuario no puede jugar
                        puede_jugar = False
                comprobar_si_gana()


    ahora = int(time.time())
    # Y aquí usamos la bandera del tiempo, de nuevo. Si los segundos actuales menos los segundos
    # en los que se empezó el ocultamiento son mayores a los segundos en los que se muestra la pieza, entonces
    # se ocultan las dos tarjetas y se reinician las banderas
    if ultimos_segundos is not None and ahora - ultimos_segundos >= segundos_mostrar_pieza:
        cuadros[y1][x1].mostrar = False
        cuadros[y2][x2].mostrar = False
        x1 = None
        y1 = None
        x2 = None
        y2 = None
        ultimos_segundos = None
        # En este momento el usuario ya puede hacer clic de nuevo pues las imágenes ya estarán ocultas
        puede_jugar = True

    # Hacer toda la pantalla blanca
    pantalla_juego.fill(color_blanco)
    # Banderas para saber en dónde dibujar las imágenes, pues al final
    # la pantalla de PyGame son solo un montón de pixeles
    x = 0
    y = 0
    # Recorrer los cuadros
    for fila in cuadros:
        x = 0
        for cuadro in fila:
            """
            Si está descubierto o se debe mostrar, dibujamos la imagen real. Si no,
            dibujamos la imagen oculta
            """
            if cuadro.descubierto or cuadro.mostrar:
                pantalla_juego.blit(cuadro.imagen_real, (x, y))
            else:
                pantalla_juego.blit(imagen_oculta, (x, y))
            x += medida_cuadro
        y += medida_cuadro

    # También dibujamos el botón
    if juego_iniciado:
        # Si está iniciado, entonces botón blanco con fuente gris para que parezca deshabilitado
        pygame.draw.rect(pantalla_juego, color_blanco, boton)
        pantalla_juego.blit(fuente.render(
            "Iniciar juego", True, color_gris), (xFuente, yFuente))
    else:
        pygame.draw.rect(pantalla_juego, color_azul, boton)
        pantalla_juego.blit(fuente.render(
            "Iniciar juego", True, color_blanco), (xFuente, yFuente))

    # Actualizamos la pantalla
    pygame.display.update()



