#Estudiante: José Albeiro García
#Grupo: 213023_347
#Universidad Nacional Abierta y a Distancia - UNAD


from abc import ABC, abstractmethod
import logging


# Configuración del archivo de logs

logging.basicConfig(
    filename="logs.txt",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# Excepciones personalizadas

class ClienteInvalidoError(Exception):
    pass


class ReservaInvalidaError(Exception):
    pass


class ServicioNoDisponibleError(Exception):
    pass


# Clase abstracta principal

class Entidad(ABC):

    def __init__(self, id):
        self.id = id

    @abstractmethod
    def mostrar_info(self):
        pass


# Clase cliente

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


# Clase abstracta servicio

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


# Servicios disponibles

class ReservaSala(Servicio):

    def calcular_costo(self, horas):

        return self.tarifa * horas

    def descripcion(self):

        return "Servicio de reserva de salas"


class AlquilerEquipo(Servicio):

    def calcular_costo(self, horas):

        seguro = 15000

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


# Clase reserva

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

    # Método con parámetros opcionales
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

            print(f"Costo: ${total:,.0f}".replace(",", "."))

        except Exception as e:

            logging.error(
                f"Error mostrando reserva: {e}"
            )


# Listas principales

clientes = []
reservas = []


print("========== SOFTWARE FJ ==========\n")


# Registro de clientes

try:

    print("Registrando cliente Juan...")

    cliente1 = Cliente(
        1,
        "Juan",
        "juan@gmail.com"
    )

    clientes.append(cliente1)

    cliente1.mostrar_info()

except Exception as e:

    logging.error(e)


try:

    print("\nRegistrando cliente inválido...")

    cliente2 = Cliente(
        2,
        "",
        "correo_malo"
    )

except ClienteInvalidoError as e:

    print("Error cliente:", e)

    logging.error(e)


try:

    print("\nRegistrando cliente María...")

    cliente3 = Cliente(
        3,
        "Maria",
        "maria@gmail.com"
    )

    clientes.append(cliente3)

    cliente3.mostrar_info()

except Exception as e:

    logging.error(e)


try:

    print("\nRegistrando cliente Carlos...")

    cliente4 = Cliente(
        4,
        "Carlos",
        "carlos@gmail.com"
    )

    clientes.append(cliente4)

    cliente4.mostrar_info()

except Exception as e:

    logging.error(e)


# Creación de servicios

try:

    print("\nCreando servicio de sala...")

    servicio1 = ReservaSala(
        "Sala VIP",
        150000
    )

    print(servicio1.descripcion())

except Exception as e:

    logging.error(e)


try:

    print("\nCreando servicio inválido...")

    servicio2 = AlquilerEquipo(
        "Computador Gamer",
        -20000
    )

except ValueError as e:

    print("Error servicio:", e)

    logging.error(e)


try:

    print("\nCreando servicio de alquiler...")

    servicio3 = AlquilerEquipo(
        "Portatil Empresarial",
        80000
    )

    print(servicio3.descripcion())

except Exception as e:

    logging.error(e)


try:

    print("\nCreando servicio de asesoría...")

    servicio4 = AsesoriaEspecializada(
        "Asesoría Python",
        120000
    )

    print(servicio4.descripcion())

except Exception as e:

    logging.error(e)


# Gestión y procesamiento de reservas

try:

    print("\nProcesando reserva de Juan...")

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


try:

    print("\nProcesando reserva inválida...")

    reserva2 = Reserva(
        cliente1,
        servicio1,
        -5
    )

except ReservaInvalidaError as e:

    print("Error reserva:", e)

    logging.error(e)


try:

    print("\nProcesando reserva de María...")

    reserva3 = Reserva(
        cliente3,
        servicio3,
        2
    )

    reserva3.confirmar()

    reservas.append(reserva3)

    reserva3.mostrar_reserva()

except Exception as e:

    logging.error(e)


try:

    print("\nProcesando asesoría de Carlos...")

    reserva4 = Reserva(
        cliente4,
        servicio4,
        2
    )

    reserva4.confirmar()

    reservas.append(reserva4)

    reserva4.mostrar_reserva()

except Exception as e:

    logging.error(e)


# Cancelación de reserva

try:

    print("\nCancelando reserva de Juan...")

    reserva1.cancelar()

    print("Reserva cancelada")

    reserva1.mostrar_reserva()

except Exception as e:

    logging.error(e)


# Uso de try except else finally

try:

    print("\nRealizando conversión...")

    numero = int("100")

except ValueError as e:

    logging.error(e)

else:

    print("Conversión correcta")

finally:

    print("Proceso terminado")


# Encadenamiento de excepciones

try:

    print("\nProbando excepción encadenada...")

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


print("\nProceso finalizado correctamente")


# Evita que la ventana se cierre automáticamente

input("\nPresione Enter para salir...")