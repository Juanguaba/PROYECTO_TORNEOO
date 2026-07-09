class EquipoForm:

    def __init__(self, form):

        self.nombre = form.get("nombre", "").strip()
        self.ciudad = form.get("ciudad", "").strip()
        self.entrenador = form.get("entrenador", "").strip()
        self.fundacion = form.get("fundacion", "").strip()
        self.estado = form.get("estado") == "1"

    def valido(self):

        return all([
            self.nombre,
            self.ciudad,
            self.entrenador,
            self.fundacion
        ])
