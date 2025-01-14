import Jugador 
import Carta
import random

class Juego:
    def __init__(self):
        self.cartas = self.cargar_cartas_desde_archivo("Deck.txt")
        self.jugador = Jugador("jugador")
        self.maquina = Jugador("maquina")
        self.turno = 1
        self.iniciar_juego()

    def cargar_cartas_desde_archivo(self, archivo):
        cartas = []
        with open(archivo, 'r') as file:
            for linea in file.readlines():
                datos = linea.strip().split(', ')
                if len(datos) == 7:
                    carta = CartaMonstruo(datos[0], datos[1], int(datos[3]), int(datos[4]), datos[5], datos[6])
                elif len(datos) == 4:
                    carta = CartaTrampa(datos[0], datos[1], datos[3])
                elif len(datos) == 5:
                    carta = CartaMagica(datos[0], datos[1], datos[4], datos[3])
                else:
                    print(f"Advertencia: Línea no válida para una carta: {linea}")
                    continue
                cartas.append(carta)
        return cartas

    def iniciar_juego(self):
        self.jugador.set_mano(random.sample(self.cartas, 5))
        self.maquina.set_mano(random.sample(self.cartas, 5))
        
        print("--- Cartas Iniciales del Jugador ---")
        for carta in self.jugador.get_mano():
            print(carta.get_nombre())
        
        print("--- Cartas Iniciales de la Máquina ---")
        for carta in self.maquina.get_mano():
            print(carta.get_nombre())

    def realizar_ataque(self, carta_atacante, carta_objetivo=None):
        def obtener_atacante_y_oponente():
            for jugador in [self.jugador, self.maquina]:
                for carta in jugador.get_tablero_monstruos():
                    if carta == carta_atacante or carta.get_nombre() == carta_atacante.get_nombre():
                        oponente = self.maquina if jugador == self.jugador else self.jugador
                        return jugador, oponente, carta
            return None, None, None

        atacante, oponente, carta_atacante = obtener_atacante_y_oponente()
        if not atacante or not oponente:
            print("No se pudo identificar al jugador atacante.")
            return

        if carta_atacante not in atacante.get_tablero_monstruos():
            print("La carta atacante debe estar en tu tablero para atacar.")
            return

        if not oponente.get_tablero_monstruos():
            print(f"{carta_atacante.get_nombre()} ataca directamente a {oponente.nombre}.")
            oponente.recibir_daño(carta_atacante.get_ataque())
            return

        if carta_objetivo and carta_objetivo not in oponente.get_tablero_monstruos():
            print("La carta objetivo no está en el tablero del oponente.")
            return

        self.evaluar_ataque(carta_atacante, carta_objetivo, atacante, oponente)

    def evaluar_ataque(self, carta_atacante, carta_objetivo, atacante, oponente):
        if carta_objetivo:
            print(f"{carta_atacante.get_nombre()} ataca a {carta_objetivo.get_nombre()}.")
            if carta_atacante.get_ataque() > carta_objetivo.get_defensa():
                print(f"{carta_atacante.get_nombre()} destruye a {carta_objetivo.get_nombre()}.")
                oponente.eliminar_carta(carta_objetivo)
            elif carta_atacante.get_ataque() < carta_objetivo.get_defensa():
                print(f"{carta_atacante.get_nombre()} es destruida por {carta_objetivo.get_nombre()}.")
                atacante.eliminar_carta(carta_atacante)
            else:
                print(f"{carta_atacante.get_nombre()} y {carta_objetivo.get_nombre()} se destruyen mutuamente.")
                atacante.eliminar_carta(carta_atacante)
                oponente.eliminar_carta(carta_objetivo)

    def jugar_turno_jugador(self):
        print("-------------------\nTurno del Jugador\n-------------------")
        self.jugador.robar_carta(self.cartas)
        print("Cartas en la mano del Jugador:")
        for idx, carta in enumerate(self.jugador.get_mano()):
            print(f"[{idx}] {carta.get_nombre()} - {type(carta).__name__}")

        carta_elegida = self.jugador.seleccionar_carta()
        self.jugador.jugar_carta(carta_elegida, self.maquina)

    def jugar_turno_maquina(self):
        print("-------------------\nTurno de la Máquina\n-------------------")
        self.maquina.robar_carta(self.cartas)
        carta_a_jugar = random.choice(self.maquina.get_mano())
        self.maquina.jugar_carta(carta_a_jugar, self.jugador)

    def ciclo_principal(self):
        print("\n--- ¡Comienza el duelo! ---")
        while self.jugador.get_vida() > 0 and self.maquina.get_vida() > 0:
            print(f"\n--- Turno {self.turno} ---")
            self.jugar_turno_jugador()
            self.mostrar_estado_juego()
            if self.maquina.get_vida() <= 0:
                print("¡Felicidades! Has ganado el duelo.")
                break

            self.jugar_turno_maquina()
            self.mostrar_estado_juego()
            if self.jugador.get_vida() <= 0:
                print("¡La máquina ha ganado el duelo!")
                break

            self.turno += 1
        print("\n--- Fin del juego ---")

juego = Juego()
juego.ciclo_principal()


