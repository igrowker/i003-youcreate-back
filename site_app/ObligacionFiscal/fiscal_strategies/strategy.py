from abc import (
    ABC,
    abstractmethod,
)  # Importa herramientas para definir clases abstractas


class ObligacionesFiscalesStrategy(ABC):
    """
    Interfaz abstracta que define la estrategia fiscal para cada país.
    Cada país que implemente esta interfaz debe proporcionar su propia lógica fiscal.
    """

    @abstractmethod
    def calcular_obligaciones(self):
        """
        Método abstracto que debe ser implementado por cada estrategia fiscal de país.
        Debe contener la lógica para calcular las obligaciones fiscales.
        """
        pass  # La implementación específica de este método será proporcionada en las clases hijas
