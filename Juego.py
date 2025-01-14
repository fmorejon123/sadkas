from Jugador import *
from Carta import *
import random

class Juego:

    def __init__(self):
        self.cartas = self.cargar_cartas_desde_archivo("Deck.txt")
        self.jugador = Jugador("jugador")
        self.maquina = Jugador("maquina")
        self.turno = 1  # Iniciar el turno
        self.iniciar_juego()



    def cargar_cartas_desde_archivo(self, archivo):
        cartas = []
        # Abrir el archivo y leerlo línea por línea
        with open(archivo, 'r') as file:
            for linea in file.readlines():
                # Limpiar la línea y dividirla por comas
                datos = linea.strip().split(', ')

                # Procesamos la carta dependiendo del número de atributos
                if len(datos) == 7:  # Es una carta de monstruo
                    nombre = datos[0]
                    descripcion = datos[1]
                    ataque = int(datos[3])
                    defensa = int(datos[4])
                    tipo = datos[5]
                    atributo = datos[6]
                    carta = CartaMonstruo(nombre, descripcion, ataque, defensa, tipo, atributo)

                elif len(datos) == 4: # trampa
                    nombre = datos[0]
                    descripcion = datos[1]
                    tipo = datos[3]
                    carta = CartaTrampa(nombre, descripcion, tipo)
                elif len(datos) == 5:
                    #"Poción de Vida", "Restaura 500 puntos de vida a un jugador", "Mágica", "Ninguno", 0
                    nombre =  datos[0]
                    descripcion = datos [1]
                    tipo = datos [3]
                    incremento = datos [4]
                    carta = CartaMagica(nombre,descripcion,incremento,tipo)
                    
                else:
                    # Si no cumple con ninguna de las condiciones, se puede omitir o mostrar un mensaje de advertencia
                    print(f"Advertencia: Línea no válida para una carta: {linea}")
                    continue  # Salta a la siguiente línea

                # Agregar la carta a la lista
                cartas.append(carta)
        return cartas



    def iniciar_juego(self):
        # Asignar 5 cartas aleatorias a la mano del jugador
        self.jugador.set_mano(random.sample(self.cartas, 5))
        
        # Asignar 5 cartas aleatorias a la mano de la máquina
        self.maquina.set_mano(random.sample(self.cartas, 5))
        
        print("--- Cartas Iniciales del Jugador ---")
        for carta in self.jugador.get_mano():
            print(carta.get_nombre())
        
        print("--- Cartas Iniciales de la Máquina ---")
        for carta in self.maquina.get_mano():
            print(carta.get_nombre())

        

    def realizar_ataque(self, carta_atacante, carta_objetivo=None):
        jugador_atacante = None
        jugador_oponente = None

        # Búsqueda más flexible de la carta en los tableros
        for jugador in [self.jugador, self.maquina]:
            for carta in jugador.get_tablero_monstruos():
                if (carta == carta_atacante) or (carta.get_nombre() == carta_atacante.get_nombre()):
                    jugador_atacante = jugador
                    jugador_oponente = self.maquina if jugador == self.jugador else self.jugador
                    carta_atacante = carta  # Usar la carta del tablero
                    break
            if jugador_atacante:
                break

        # Resto del método permanece igual al código anterior
        if not jugador_atacante or not jugador_oponente:
            print("No se pudo identificar al jugador atacante.")
            return

        # Verificar si la carta atacante está en el tablero
        if carta_atacante not in jugador_atacante.get_tablero_monstruos():
            print("La carta atacante debe estar en tu tablero para atacar.")
            return

        # Ataque directo si no hay monstruos en el tablero oponente
        if not jugador_oponente.get_tablero_monstruos():
            print(f"{carta_atacante.get_nombre()} ataca directamente a {jugador_oponente.nombre}.")
            damage = carta_atacante.get_ataque()
            jugador_oponente.vida -= damage
            print(f"{jugador_oponente.nombre} recibe {damage} puntos de daño. Vida restante: {jugador_oponente.vida}.")
            if jugador_oponente.vida <= 0:
                print(f"{jugador_oponente.nombre} ha sido derrotado. ¡{jugador_atacante.nombre} gana el juego!")
            return

        # Ataque a un monstruo específico si se proporciona
        if carta_objetivo:
            if carta_objetivo not in jugador_oponente.get_tablero_monstruos():
                print("La carta objetivo no está en el tablero del oponente.")
                return
            
            print(f"{carta_atacante.get_nombre()} ataca a {carta_objetivo.get_nombre()}.")
            if carta_atacante.get_ataque() > carta_objetivo.get_defensa():
                print(f"{carta_atacante.get_nombre()} destruye a {carta_objetivo.get_nombre()}.")
                jugador_oponente.get_tablero_monstruos().remove(carta_objetivo)
                # Eliminar también de la mano de la máquina (si está allí)
                if carta_objetivo in jugador_oponente.get_mano():
                    jugador_oponente.get_mano().remove(carta_objetivo)
            elif carta_atacante.get_ataque() < carta_objetivo.get_defensa():
                print(f"{carta_atacante.get_nombre()} es destruida por {carta_objetivo.get_nombre()}.")
                jugador_atacante.get_tablero_monstruos().remove(carta_atacante)
                # Eliminar también de la mano del jugador (si está allí)
                if carta_atacante in jugador_atacante.get_mano():
                    jugador_atacante.get_mano().remove(carta_atacante)
            else:
                print(f"{carta_atacante.get_nombre()} y {carta_objetivo.get_nombre()} se destruyen mutuamente.")
                jugador_atacante.get_tablero_monstruos().remove(carta_atacante)
                jugador_oponente.get_tablero_monstruos().remove(carta_objetivo)
                # Eliminar ambas cartas de la mano de los jugadores si están allí
                if carta_atacante in jugador_atacante.get_mano():
                    jugador_atacante.get_mano().remove(carta_atacante)
                if carta_objetivo in jugador_oponente.get_mano():
                    jugador_oponente.get_mano().remove(carta_objetivo)


    


    def mostrar_estado_juego(self):
        # Muestra el estado del juego después de cada turno
        print("\n--- Estado del Juego ---")
        print(f"Vida del Jugador: {self.jugador.get_vida()} - Vida de la máquina: {self.maquina.get_vida()}")

        # Mostrar monstruos en los tableros
        print("\nTablero de Monstruos del Jugador:")
        for i, carta in enumerate(self.jugador.get_tablero_monstruos()):
            if carta:
                print(f"[{i}] {carta.get_nombre()} - Modo: {carta.get_modo()}")
            
        
        print("\nTablero de monstruos de carta y trampa del jugador: ")
        for i, carta in enumerate(self.jugador.get_tablero_magicas_trampa()):
            if carta:
                print(f"[{i}] {carta.get_nombre()}")
            


        print("\nTablero de Monstruos de la Máquina:")
        for i, carta in enumerate(self.maquina.get_tablero_monstruos()):
            if carta:
                print(f"[{i}] {carta.get_nombre()} - Modo: {carta.get_modo()}")

        print("\nTablero de monstruos de carta y trampa del jugador: ")
        for i, carta in enumerate(self.maquina.get_tablero_magicas_trampa()):
            if carta:
                print(f"[] {carta.get_nombre()}")
        

    def robar_carta(self, jugador):
        # Robar una carta aleatoria de la lista de cartas
        carta_robada = random.choice(self.cartas)
        print(f"{jugador.get_nombre()} ha robado una carta: {carta_robada.get_nombre()}\n")
        return carta_robada

    def jugar_turno_jugador(self):
        print("-------------------")

        print("Turno del Jugador")

        print("-------------------")


        print("\n [Fase: tomar carta]")

        # El jugador roba una carta si tiene menos de 5 cartas en mano
        self.jugador.agregar_carta_a_mano(self.robar_carta(self.jugador))

        # Mostrar las cartas de la jugador
        print("Cartas en la mano de la Jugador:")
        for idx, carta in enumerate(self.jugador.get_mano()):
            tipo = type(carta).__name__
            print(f"[{idx}] {carta.get_nombre()} - {tipo}")
        # El jugador elige una carta de su mano
        # El jugador elige una carta para jugar
        eleccion = -1
        while eleccion < 0 or eleccion >= len(self.jugador.get_mano()):
            try:
                eleccion = int(input("Elige una carta para jugar (0-{}) : ".format(len(self.jugador.get_mano()) - 1)))
            except ValueError:
                print("Por favor, ingresa un número válido.")

        carta = self.jugador.get_mano()[eleccion]  # Se selecciona la carta elegida

        # Verifica si la carta ya fue usada
        while carta.get_usado():
            print(f"La carta '{carta.get_nombre()}' ya ha sido utilizada. Elige otra carta.")
            eleccion = -1
            while eleccion < 0 or eleccion >= len(self.jugador.get_mano()):
                try:
                    eleccion = int(input("Elige otra carta para jugar (0-{}) : ".format(len(self.jugador.get_mano()) - 1)))
                except ValueError:
                    print("Por favor, ingresa un número válido.")
            carta = self.jugador.get_mano()[eleccion]

        print(f"El jugador ha elegido {carta.get_nombre()}.")



        if isinstance(carta, CartaMonstruo) and carta.get_usado()==False:  # Si la carta es un monstruo
            # El jugador decide si jugarla en modo ataque o defensa
            modo = ""
            while modo not in ["A", "D"]:  # Validamos que la entrada sea correcta
                modo = input("¿Quieres jugarlo en modo ataque o defensa? (A/D): ").upper()
                if modo not in ["A", "D"]:
                    print("Opción no válida. Por favor, ingresa 'A' para ataque o 'D' para defensa.")
            if modo == "A":
                print(f"El jugador coloca {carta.get_nombre()} en modo ATAQUE.")
                carta.set_modo("ATAQUE")
                carta.set_boca_arriba(True)
                self.jugador.get_tablero_monstruos().append(carta)
            elif modo == "D":
                print(f"El jugador coloca {carta.get_nombre()} en modo DEFENSA.")
                carta.set_modo("DEFENSA")
                carta.set_boca_arriba(False)
                self.jugador.get_tablero_monstruos().append(carta)
            
            # Ahora, el jugador puede decidir atacar
            if  carta.get_modo() == "ATAQUE":
                # Si la máquina tiene monstruos, el jugador elige uno para atacar
                self.realizar_ataque(carta)
            

        elif isinstance(carta, CartaTrampa):  # Si la carta es una trampa
            print(f"El jugador coloca {carta.get_nombre()} en el campo de trampas.")
            self.jugador.get_tablero_magicas_trampa().append(carta)
            self.jugador.get_mano().remove(carta)
            

        elif isinstance(carta, CartaMagica):  # Si la carta es una carta mágica
            print(f"El jugador activa {carta.get_nombre()}.")
            # Aquí deberías manejar la activación de cartas mágicas
            self.jugador.aplicar_efecto(carta) 
             # Método para manejar cartas mágicas
            self.jugador.get_mano().remove(carta)
        else:
            print("La carta seleccionada no se puede jugar.")

    
    def jugar_turno_maquina(self):
        print("-------------------")
        print("Turno de la Máquina")
        print("-------------------")



        print("Fase tomar carta")


        # La máquina roba una carta si tiene menos de 5 cartas en mano
        carta_robada = self.robar_carta(self.maquina)
        self.maquina.agregar_carta_a_mano(carta_robada)
        print(f"La máquina robó: {carta_robada.get_nombre()}")

        # Mostrar las cartas de la máquina
        print("Cartas en la mano de la máquina:")
        for idx, carta in enumerate(self.maquina.get_mano()):
            tipo = type(carta).__name__
            print(f"[{idx}] {carta.get_nombre()} - {tipo}")

        # La máquina debe decidir qué hacer con la carta
        if self.maquina.get_mano():
            carta = random.choice(self.maquina.get_mano())  # Elegir una carta aleatoria
            print(f"La máquina decide jugar {carta.get_nombre()}.")

            if isinstance(carta, CartaMonstruo):  # Si es una carta de monstruo
                print(f"La máquina coloca {carta.get_nombre()} en el tablero de monstruos.")
                modo = "A" if carta.get_ataque() > carta.get_defensa() else "D"
                if modo == "A":
                    print(f"El monstruo {carta.get_nombre()} se coloca en modo ATAQUE.")
                    carta.set_modo("ATAQUE")
                    carta.set_boca_arriba(True)
                else:
                    print(f"El monstruo {carta.get_nombre()} se coloca en modo DEFENSA.")
                    carta.set_modo("DEFENSA")
                    carta.set_boca_arriba(False)
                self.maquina.get_tablero_monstruos().append(carta)  # Colocar en el tablero de monstruos

            elif isinstance(carta, CartaTrampa):  # Si es una carta trampa
                print(f"La máquina coloca {carta.get_nombre()} en el campo de trampas.")
                self.maquina.get_tablero_magicas_trampa().append(carta)  # Colocar en el campo de trampas

            elif isinstance(carta, CartaMagica):  # Si es una carta mágica
                print(f"La máquina activa {carta.get_nombre()}.")
                self.maquina.aplicar_efecto(carta)  # Activar la carta mágica
                # Si se requiere agregarla al tablero de mágicas:
                self.maquina.get_tablero_magicas_trampa().append(carta)

            # Después de jugar una carta, la máquina decide si atacar
            if self.jugador.get_tablero_monstruos():
                # Si el jugador tiene monstruos, la máquina elige uno para atacar
                ataque_a_realizar = random.randint(0, len(self.jugador.get_tablero_monstruos()) - 1)
                monstruo_objetivo = self.jugador.get_tablero_monstruos()[ataque_a_realizar]
                self.realizar_ataque(carta, monstruo_objetivo)
                print(f"La máquina ataca con {carta.get_nombre()} a {monstruo_objetivo.get_nombre()}.")
            else:
                # Si no hay monstruos, la máquina ataca directamente
                self.realizar_ataque(carta)
                print(f"La máquina ataca directamente con {carta.get_nombre()}.")
        else:
            print("La máquina no tiene cartas para jugar.")




    def ciclo_principal(self):
        print("\n--- ¡Comienza el duelo! ---")
        while self.jugador.get_vida() > 0 and self.maquina.get_vida() > 0:
            # Mostrar el turno actual
            print(f"\n--- Turno {self.turno} ---")
            
            # Turno del jugador
            self.jugar_turno_jugador()
            self.mostrar_estado_juego()
            
            # Verificar si el juego terminó
            if self.maquina.get_vida() <= 0:
                print("¡Felicidades! Has ganado el duelo.")
                break
            
            # Turno de la máquina
            self.jugar_turno_maquina()
            self.mostrar_estado_juego()

            # Verificar si el juego terminó
            if self.jugador.get_vida() <= 0:
                print("¡La máquina ha ganado el duelo!")
                break

            # Incrementar el turno
            self.turno += 1

        print("\n--- Fin del juego ---")


# Inicializamos el juego
juego = Juego()
juego.ciclo_principal()






#La solucion seria crear una forma de juego de maquina que sea igual a la de juego, pero que esta se pueda controlar por si sola,
#El error radica en que la IA no sabe como usar x poder, y depende siempre que una carta aleatoria sea de tipo monstruo y que este en ataques
#Si buscamos la manera en la que la maquina pueda interactuar por si misma, ya seria increible, eso seria lo unico que nos falta
#El juego de por si ya es completo, solo hay que ver una forma en la que la maquina pueda usar aleatoriamente una carta y usarla como se debe
#La maquina por si sola debera escojer una carta de sus 5 que tiene en su mazo:
#Si la carta es de clase Monstruo, que decida si le es conveniente atacar o defenderse con ella, y ya se sabe que hace si esta en modo ataque o defensa
#Si la carta es de clase Trampa, deberia usarla si es que un oponente quiere atacar con una carta, si este ataca, la carta de clase trampa aparece y bloquea el ataque

#se considera esto para la maquina
#Lógica de la Máquina	
#La máquina debe jugar todas las opciones que tenga en su mano. 
#La máquina siempre debe declara batalla, si es posible.
#La máquina solo debe jugar cartas en defensa si no es posible jugar en ataque.



#La solucion seria crear una forma de juego de maquina que sea igual a la de juego, pero que esta se pueda controlar por si sola,
#El error radica en que la IA no sabe como usar x poder, y depende siempre que una carta aleatoria sea de tipo monstruo y que este en ataques
#Si buscamos la manera en la que la maquina pueda interactuar por si misma, ya seria increible, eso seria lo unico que nos falta
#El juego de por si ya es completo, solo hay que ver una forma en la que la maquina pueda usar aleatoriamente una carta y usarla como se debe
#La maquina por si sola debera escojer una carta de sus 5 que tiene en su mazo:
#Si la carta es de clase Monstruo, que decida si le es conveniente atacar o defenderse con ella, y ya se sabe que hace si esta en modo ataque o defensa
#Si la carta es de clase Trampa, deberia usarla si es que un oponente quiere atacar con una carta, si este ataca, la carta de clase trampa aparece y bloquea el ataque

#se considera esto para la maquina
#Lógica de la Máquina	
#La máquina debe jugar todas las opciones que tenga en su mano. 
#La máquina siempre debe declara batalla, si es posible.
#La máquina solo debe jugar cartas en defensa si no es posible jugar en ataque.