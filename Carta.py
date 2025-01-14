class Carta:
    def __init__(self, nombre, descripcion):
        self.nombre = nombre
        self.descripcion = descripcion

    def get_nombre(self):
        return self.nombre

    def get_descripcion(self):
        return self.descripcion

class CartaMonstruo(Carta):
    def __init__(self, nombre, descripcion, ataque, defensa, tipo, atributo):
        super().__init__(nombre, descripcion)
        self.ataque = ataque
        self.defensa = defensa
        self.tipo = tipo
        self.atributo = atributo
        self.boca_arriba = True
        self.modo = "ATAQUE"  # Puede ser "ATAQUE" o "DEFENSA"
        self.protegido = False 
        self.usado = False



    def get_usado(self):
        return self.usado
    
    def usar(self):
        self.usado = True  # Marca la carta como usada
    
    def set_usado(self, bool):
        self.usado = bool
        
    def set_protegido (self, bool):
        self.protegido = bool
    def get_ataque(self):
        return self.ataque

    def set_ataque(self, nuevo_ataque):
        self.ataque = nuevo_ataque

    def get_defensa(self):
        return self.defensa

    def set_defensa(self, nueva_defensa):
        self.defensa = nueva_defensa

    def get_tipo(self):
        return self.tipo

    def get_elemento(self):
        return self.atributo

    def get_boca_arriba(self):
        return self.boca_arriba

    def set_boca_arriba(self, estado):
        self.boca_arriba = estado

    def get_modo(self):
        return self.modo

    def set_modo(self, nuevo_modo):
        self.modo = nuevo_modo

class CartaMagica(Carta):
    def __init__(self, nombre, descripcion, incremento, tipo_monstruo):
        """
        :param nombre: Nombre de la carta.
        :param descripcion: Descripción de la carta.
        :param incremento: El incremento en puntos de ataque o defensa.
        :param tipo_monstruo: Tipo de monstruo al que afecta la carta (o 'Ninguno' para efecto global).
        :param tipo_efecto: Tipo de efecto ('Ataque' o 'Defensa').
        """
        super().__init__(nombre, descripcion)
        self.incremento = incremento
        self.tipo_monstruo = tipo_monstruo
        self.usado = False

    def get_usado(self):
        return self.usado


    def get_incremento(self):
        return self.incremento

    def get_tipo_monstruo(self):
        return self.tipo_monstruo

    def get_tipo_efecto(self):
        return self.tipo_efecto  # Método para obtener el tipo de efecto

    def aplicar_efecto(self, monstruo):
        """Aplica el efecto de la carta mágica sobre un monstruo si el tipo coincide."""
        




            

class CartaTrampa(Carta):
    def __init__(self, nombre, descripcion, atributo):
        super().__init__(nombre, descripcion)
        self.atributo = atributo
        self.usado = False

    def set_usado(self, estado):
        self.usado = estado  # Método para cambiar el estado de uso de la trampa

    def get_usado(self):
        return self.usado

    def get_atributo(self):
        return self.atributo

    def activar(self, monstruo_atacante):
        """Verifica si la trampa se activa dependiendo del monstruo atacante"""
        if self.atributo == monstruo_atacante.get_elemento():
            print(f"La trampa {self.get_nombre()} ha detenido el ataque del monstruo {monstruo_atacante.get_nombre()} ({monstruo_atacante.get_elemento()}).")
            self.set_usado(True)  # Marca la trampa como usada
            return True  # La trampa se activa
        return False