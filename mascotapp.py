from datetime import datetime

class Mascota:
    def __init__(self, id_mascota, nombre, especie, edad_meses, historia=""):
        self.id_mascota = id_mascota
        self.nombre = nombre
        self.especie = especie.lower()
        self.edad_meses = edad_meses
        self.historia = historia
        self.estado = "Disponible"  # Disponible, En Proceso, Adoptado

    def __repr__(self):
        return f"[{self.id_mascota}] {self.nombre} ({self.especie.capitalize()}) - Estado: {self.estado}"


class Adoptante:
    def __init__(self, id_adoptante, nombre, contacto):
        self.id_adoptante = id_adoptante
        self.nombre = nombre
        self.contacto = contacto
        self.solicitudes = []

    def __repr__(self):
        return f"Adoptante: {self.nombre} | Contacto: {self.contacto}"


class Mascotapp:
    def __init__(self):
        self.mascotas = {}
        self.adoptantes = {}
        self._contador_mascotas = 1
        self._contador_adoptantes = 1

    def registrar_mascota(self, nombre, especie, edad_meses, historia=""):
        pet = Mascota(self._contador_mascotas, nombre, especie, edad_meses, historia)
        self.mascotas[pet.id_mascota] = pet
        self._contador_mascotas += 1
        return pet

    def listar_disponibles(self, especie=None):
        disponibles = [m for m in self.mascotas.values() if m.estado == "Disponible"]
        if especie:
            disponibles = [m for m in disponibles if m.especie == especie.lower()]
        return disponibles

    def procesar_adopcion(self, id_mascota, id_adoptante):
        mascota = self.mascotas.get(id_mascota)
        if not mascota:
            return "Mascota no encontrada."
        if mascota.estado != "Disponible":
            return f"{mascota.nombre} no está disponible para adopción."

        mascota.estado = "Adoptado"
        return f"¡Felicidades! {mascota.nombre} ha sido adoptado/a con éxito."