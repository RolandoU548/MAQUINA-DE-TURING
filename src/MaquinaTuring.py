class MaquinaTuring:
    def __init__(self, maquina_codificada: str):
        self.ESTADO_FINAL = "s2"
        self.estado_actual = "s1"
        self.apuntador_de_cinta = 0
        self.codificacion = self.decodificar_maquina(maquina_codificada)
        self.transiciones = self.decodificar_transiciones(self.codificacion[0])
        self.cinta = self.decodificar_cinta(self.codificacion[1])

    def decodificar_maquina(self, maquina_codificada: str) -> list:
        return maquina_codificada.split("000")

    def decodificar_transiciones(self, transiciones_codificadas: str) -> list:
        transiciones_codificadas = transiciones_codificadas.split("00")
        transiciones_por_estado = {}

        for transicion_codificada in transiciones_codificadas:
            transicion = Transicion(transicion_codificada)
            if transicion.estado not in transiciones_por_estado:
                transiciones_por_estado[transicion.estado] = []
            if transicion.estado_siguiente not in transiciones_por_estado:
                transiciones_por_estado[transicion.estado_siguiente] = []
            transiciones_por_estado[transicion.estado].append(transicion)

        return transiciones_por_estado

    def decodificar_cinta(self, cinta_codificada: str) -> list:
        return [str(len(simbolo)) for simbolo in cinta_codificada.split("0") if simbolo]

    def evaluar_cadena(self) -> bool:
        self.estado_actual = "s1"
        self.apuntador_de_cinta = 0
        while True:
            if not self.hay_transicion(
                self.estado_actual, self.cinta[self.apuntador_de_cinta]
            ):
                break
            for transicion_actual in self.transiciones[self.estado_actual]:
                if transicion_actual.simbolo == self.cinta[self.apuntador_de_cinta]:
                    self.estado_actual = transicion_actual.estado_siguiente
                    self.cinta[self.apuntador_de_cinta] = (
                        transicion_actual.simbolo_siguiente
                    )
                    if transicion_actual.desplazamiento == "->":
                        if self.apuntador_de_cinta == len(self.cinta) - 1:
                            self.cinta.append("1")
                        self.apuntador_de_cinta += 1
                    elif transicion_actual.desplazamiento == "<-":
                        if self.apuntador_de_cinta == 0:
                            self.cinta.insert(0, "1")
                        else:
                            self.apuntador_de_cinta -= 1
                    break

        if self.estado_actual == self.ESTADO_FINAL:
            return True
        return False

    def hay_transicion(self, estado: str, simbolo: str) -> bool:
        if len(self.transiciones[estado]) == 0:
            return False
        for transicion in self.transiciones[estado]:
            if transicion.simbolo == simbolo:
                return True
        return False

    def __str__(self):
        transiciones_str = ""
        for transiciones in self.transiciones.values():
            for transicion in transiciones:
                transiciones_str += f"{str(transicion)}\n"
        return transiciones_str + str(self.cinta)


class Transicion:
    def __init__(self, transicion_codificada: str):
        self.codificacion = self.decodificar_transicion(transicion_codificada)
        self.estado = self.decodificar_estado(self.codificacion[0])
        self.simbolo = self.decodificar_simbolo(self.codificacion[1])
        self.estado_siguiente = self.decodificar_estado(self.codificacion[2])
        self.simbolo_siguiente = self.decodificar_simbolo(self.codificacion[3])
        self.desplazamiento = self.decodificar_desplazamiento(self.codificacion[4])

    def decodificar_transicion(self, transicion_codificada: str) -> list:
        return [simbolo for simbolo in transicion_codificada.split("0") if simbolo]

    def decodificar_estado(self, estado: str) -> str:
        return f"s{len(estado)}"

    def decodificar_simbolo(self, simbolo: str) -> str:
        return str(len(simbolo))

    def decodificar_desplazamiento(self, desplazamiento: str) -> str:
        return {"1": "->", "11": "<-", "111": "-"}[desplazamiento]

    def __str__(self):
        return f"f({self.estado}, {self.simbolo}) = ({self.estado_siguiente}, {self.simbolo_siguiente}, {self.desplazamiento})"
