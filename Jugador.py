from Carta import *

class Jugador:
    def __init__(self, nombre):
        self.puntos = 0  # Atributo corregido
        self.nombre = nombre
        self.vida = 4000
        self.deck = []
        self.mano = []
        self.tablero_monstruos = []  # Lista dinámica para monstruos
        self.tablero_magicas_trampa = []  # Lista de cartas trampa activas
        self.limite_monstruos = 3




    
    def perder_vida(self, cantidad):
        self.vida -= cantidad
        if self.vida < 0:
            self.vida = 0
        print(f"Vida restante del jugador: {self.vida}")

    





    
    def aplicar_efecto(self, carta):


            if carta.get_nombre() == "Espada de Arturo":
                    # Aumenta el ataque de todos los guerreros en el tablero
                    for monstruo in self.get_tablero_monstruos():
                        if monstruo.get_tipo() == "Guerrero":
                            monstruo.set_ataque(monstruo.get_ataque() + self.incremento)
                            print(f"{monstruo.get_nombre()} ahora tiene {monstruo.get_ataque()} de ataque.")

            if carta.get_nombre() == "Escudo de Chamelote":
                    # Aumenta la defensa de todos los guerreros en el tablero
                    for monstruo in self.get_tablero_monstruos():
                        if monstruo.get_tipo() == "G":
                            monstruo.set_defensa(monstruo.get_defensa() + self.incremento)
                            print(f"{monstruo.get_nombre()} ahora tiene {monstruo.get_defensa()} de defensa.")

            if carta.get_nombre()=="Pocion de Vida":
                
                # Restaura 500 puntos de vida al jugador
                self.set_vida(self.get_vida() + 500)
                print(f"{self.get_nombre()} ahora tiene {self.get_vida()} puntos de vida.")

            if carta.get_nombre() == "Rayo Concentrado":
                count = 0
                lista = []               
                # Aumenta el ataque de un monstruo tipo Dragón seleccionado
                for mounstruo in self.get_tablero_magicas_trampa():
                        
                    if mounstruo.get_atributo() == "D" and count==0:
                        count+=1
                        mounstruo.set_ataque(mounstruo.get_ataque() + self.incremento )

                if(count == 0):
                    print("No se seleccionó un monstruo de tipo Dragón válido.")

            if carta.get_nombre() == "Barrera de Magia":
                # Presenta la lista de monstruos en el tablero
                print("se ingreso a barrera de magia1")
                if self.get_tablero_monstruos():
                    print("Selecciona el monstruo al que deseas proteger:")

            # Muestra los monstruos en el tablero con sus posiciones
                    for idx, monstruo in enumerate(self.get_tablero_monstruos()):
                        print(f"[{idx}] {monstruo.get_nombre()} - Ataque: {monstruo.get_ataque()}, Defensa: {monstruo.get_defensa()}")

            # Pide al usuario que seleccione un monstruo por su posición
                    while True:
                        try:
                            seleccion = int(input("Ingresa el número de la posición del monstruo: "))

                    # Verifica que la selección sea válida
                            if 0 <= seleccion < len(self.get_tablero_monstruos()):
                                monstruo_seleccionado = self.get_tablero_monstruos()[seleccion]

                                # Marca al monstruo como protegido
                                monstruo_seleccionado.set_protegido(True)
                                print(f"{monstruo_seleccionado.get_nombre()} ahora está protegido contra ataques.")
                                break
                            else:
                                print("Selección no válida. Por favor, ingresa un número dentro del rango.")
                        except ValueError:
                            print("Entrada no válida. Por favor, ingresa un número.")
                    else:
                        print("No hay monstruos en el tablero para proteger.")


    
    
        



    def colocar_trampa(self, carta):
        if not isinstance(carta, CartaTrampa):
            print(f"{carta.get_nombre()} no es una carta trampa y no puede ser colocada en el tablero de trampas.")
            return False
        self.tablero_magicas_trampa.append(carta)
        self.mano.remove(carta)
        print(f"{self.nombre} ha colocado la carta trampa {carta.get_nombre()} boca abajo.")
        return True
    



    def agregar_carta_deck(self, carta):
        """Agrega una carta al deck del jugador."""
        self.deck.append(carta)

    def mostrar_deck(self):
        """Muestra todas las cartas en el deck."""
        for carta in self.deck:
            print(carta.get_nombre(), "-", carta.get_descripcion())

    

    def agregar_carta_a_mano(self, carta):
        self.mano.append(carta)  # Agregar la carta a la mano del jugador


    def mostrar_mano(self):
        print("Mano de " + self.nombre + ":")
        for idx, carta in enumerate(self.mano):
            # Mostrar el nombre y el tipo de carta
            tipo = type(carta).__name__  # Obtener el nombre de la clase de la carta
            print(f"[{idx}] {carta.get_nombre()} - {tipo}")

    def inicializar_mano(self):
        """Inicializa la mano del jugador, robando 5 cartas de su deck."""
        while len(self.mano) < 5 and self.deck:
            self.robar_carta()

    def get_nombre(self):
        return self.nombre

    def get_vida(self):
        return self.vida
    
    def set_vida(self, nueva_vida):
        self.vida = max(0, nueva_vida)

    def get_puntos(self):
        return self.puntos

    def get_deck(self):
        return self.deck
    
    def set_deck(self, new_deck):
        self.deck = new_deck

    def set_mano(self, new_mano):
        self.mano = new_mano

    def get_mano(self):
        return self.mano

    def get_tablero_monstruos(self):
        return self.tablero_monstruos

    def get_tablero_magicas_trampa(self):
        return self.tablero_magicas_trampa
