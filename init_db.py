

from database.database import Base, engine

# Importar entidades para registrar tablas y relaciones en metadata
from entities.jugador import Jugador  # noqa: F401
from entities.juego import Juego  # noqa: F401
from entities.sorteo import Sorteo  # noqa: F401
from entities.boleto import Boleto  # noqa: F401
from entities.premio import Premio  # noqa: F401
from entities.pago import Pago  # noqa: F401


def main() -> None:
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas correctamente.")


if __name__ == "__main__":
    main()
