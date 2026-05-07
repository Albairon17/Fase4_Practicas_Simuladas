from abc import ABC, abstractmethod
import logging


# ---------------- LOGS ----------------

logging.basicConfig(
    filename="logs.txt",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# ---------------- EXCEPCIONES ----------------

class ClienteInvalidoError(Exception):
    pass


class ReservaInvalidaError(Exception):
    pass


class ServicioNoDisponibleError(Exception):
    pass


# ---------------- CLASE ABSTRACTA ----------------

class Entidad(ABC):

    def __init__(self, id):
        self.id = id

    @abstractmethod
    def mostrar_info(self):
        pass


# ---------------- CLIENTE ----------------

class Cliente(Entidad):

    def __init__(self, id, nombre, correo):

        super().__init__(id)

        if nombre == "":
            raise ClienteInvalidoError(
                "El nombre no puede estar vacío"
            )

        if "@" not in correo:
            raise ClienteInvalidoError(
                "Correo inválido"
            )

        self.__nombre = nombre
        self.__correo = correo

    def get_nombre(self):
        return self.__nombre

    def get_correo(self):
        return self.__correo

    def mostrar_info(self):

        print(
            f"Cliente: {self.__nombre} - {self.__correo}"
        )


# ---------------- SERVICIO ABSTRACTO ----------------

class Servicio(ABC):

    def __init__(self, nombre, tarifa):

        self.nombre = nombre

        if tarifa <= 0:
            raise ValueError(
                "La tarifa debe ser mayor a 0"
            )

        self.tarifa = tarifa

    @abstractmethod
    def calcular_costo(self, horas):
        pass

    @abstractmethod
    def descripcion(self):
        pass


# ---------------- SERVICIOS ----------------

class ReservaSala(Servicio):

    def calcular_costo(self, horas):

        return self.tarifa * horas

    def descripcion(self):

        return "Servicio de reserva de salas"


class AlquilerEquipo(Servicio):

    def calcular_costo(self, horas):

        seguro = 15

        return (self.tarifa * horas) + seguro

    def descripcion(self):

        return "Servicio de alquiler de equipos"


class AsesoriaEspecializada(Servicio):

    def calcular_costo(self, horas):

        subtotal = self.tarifa * horas

        iva = subtotal * 0.19

        return subtotal + iva

    def descripcion(self):

        return "Servicio de asesoría especializada"


# ---------------- RESERVA ----------------

class Reserva:

    def __init__(self, cliente, servicio, horas):

        if horas <= 0:
            raise ReservaInvalidaError(
                "Las horas deben ser mayores a 0"
            )

        self.cliente = cliente
        self.servicio = servicio
        self.horas = horas
        self.estado = "Pendiente"

    def confirmar(self):

        self.estado = "Confirmada"

    def cancelar(self):

        self.estado = "Cancelada"

    # método tipo sobrecarga
    def calcular_total(
        self,
        descuento=0,
        impuesto=0
    ):

        total = self.servicio.calcular_costo(
            self.horas
        )

        total = total - (total * descuento)

        total = total + (total * impuesto)

        return total

    def mostrar_reserva(self):

        print("------ RESERVA ------")

        print(
            "Cliente:",
            self.cliente.get_nombre()
        )

        print(
            "Servicio:",
            self.servicio.nombre
        )

        print(
            "Estado:",
            self.estado
        )

        try:

            total = self.calcular_total()

            print("Costo:", total)

        except Exception as e:

            logging.error(
                f"Error mostrando reserva: {e}"
            )


# ---------------- LISTAS ----------------

clientes = []
reservas = []


# ---------------- OPERACIONES ----------------

print("========== SOFTWARE FJ ==========\n")


# 1 CLIENTE CORRECTO

try:

    cliente1 = Cliente(
        1,
        "Juan",
        "juan@gmail.com"
    )

    clientes.append(cliente1)

    cliente1.mostrar_info()

except Exception as e:

    logging.error(e)


# 2 CLIENTE INCORRECTO

try:

    cliente2 = Cliente(
        2,
        "",
        "correo_malo"
    )

except ClienteInvalidoError as e:

    print("Error cliente:", e)

    logging.error(e)


# 3 SERVICIO CORRECTO

try:

    servicio1 = ReservaSala(
        "Sala VIP",
        50
    )

    print(servicio1.descripcion())

except Exception as e:

    logging.error(e)


# 4 SERVICIO INCORRECTO

try:

    servicio2 = AlquilerEquipo(
        "Computador Gamer",
        -20
    )

except ValueError as e:

    print("Error servicio:", e)

    logging.error(e)


# 5 RESERVA CORRECTA

try:

    reserva1 = Reserva(
        cliente1,
        servicio1,
        3
    )

    reserva1.confirmar()

    reservas.append(reserva1)

    reserva1.mostrar_reserva()

except Exception as e:

    logging.error(e)


# 6 RESERVA INCORRECTA

try:

    reserva2 = Reserva(
        cliente1,
        servicio1,
        -5
    )

except ReservaInvalidaError as e:

    print("Error reserva:", e)

    logging.error(e)


# 7 ASESORIA

try:

    servicio3 = AsesoriaEspecializada(
        "Asesoría Python",
        100
    )

    reserva3 = Reserva(
        cliente1,
        servicio3,
        2
    )

    reserva3.confirmar()

    reserva3.mostrar_reserva()

except Exception as e:

    logging.error(e)


# 8 CANCELACION

try:

    reserva1.cancelar()

    print("Reserva cancelada")

    reserva1.mostrar_reserva()

except Exception as e:

    logging.error(e)


# 9 TRY EXCEPT ELSE FINALLY

try:

    numero = int("100")

except ValueError as e:

    logging.error(e)

else:

    print("Conversión correcta")

finally:

    print("Proceso terminado")


# 10 ENCADENAMIENTO DE EXCEPCIONES

try:

    try:

        int("abc")

    except ValueError as e:

        raise ReservaInvalidaError(
            "Error procesando la reserva"
        ) from e

except ReservaInvalidaError as e:

    print(
        "Excepción encadenada:",
        e
    )

    logging.error(e)


print("\nSistema finalizado sin detenerse")


# PARA QUE LA VENTANA NO SE CIERRE

input("\nPresione Enter para salir...")
