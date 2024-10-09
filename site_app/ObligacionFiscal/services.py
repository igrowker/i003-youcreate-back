from .fiscal_strategies.argentina_strategy import ArgentinaFiscalStrategy


class ObligacionesFiscalesService:
    """Servicio para manejar las obligaciones fiscales según el país del usuario."""

    def __init__(self, usuario):
        self.usuario = usuario
        self.pais = usuario.pais_residencia.lower()
        self.strategy = self._elegir_estrategia_fiscal()

    def _elegir_estrategia_fiscal(self):
        """Selecciona la estrategia fiscal según el país del usuario."""
        if self.pais == "argentina":
            return ArgentinaFiscalStrategy(self.usuario)
        # Aquí podrías agregar otras estrategias para otros países, ejemplo:
        # elif self.pais == "mexico":
        #     return MexicoFiscalStrategy(self.usuario)
        else:
            raise ValueError(
                f"No hay estrategia fiscal disponible para el país: {self.pais}"
            )

    def manejar_obligaciones(self):
        """Maneja el cálculo y almacenamiento de las obligaciones fiscales."""
        if not self.strategy:
            print(f"No hay estrategia fiscal para el país: {self.pais}")
            return
        self.strategy.calcular_obligaciones()
