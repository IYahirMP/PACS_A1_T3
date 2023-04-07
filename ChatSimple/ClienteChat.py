import Pyro5.api
import Pyro5
import Pyro5.server
import socket
import threading

# Se configura un serializador.
# Por defecto es serpent,
# solo existen 4 permitidos en Pyro5 según los docs
Pyro5.config.SERIALIZER = "serpent"

# Definición de la clase ClienteChat, para conectarse al servidor


class ClienteChat:
    # Constructor, solo se conecta al servidor
    def __init__(self):
        self.server = Pyro5.api.Proxy(
            "PYRO:ChatSV@"+socket.gethostname()+":65530")

    # Este método está pensado para invocarse de forma remota
    # Por tanto, se expone usando el decorator expose
    # Imprime un mensaje enviado desde otro cliente remoto
    @Pyro5.api.expose
    def recibir_mensaje(self, nombre_usuario, mensaje):
        print(f"{nombre_usuario}: {mensaje}")

    # Este método se comunica con el servidor para enviar un mensaje
    def enviar_mensaje(self, mensaje):
        self.server.enviar_mensaje(self.nombre_usuario, mensaje)

    # Este método es un setter para la URI del objeto ClienteChat
    # La URI se almacena y envia usando registrar_usuario
    # Para que el servidor pueda reenviar mensajes de otros usuarios
    def set_uri(self, uri):
        self.uri = uri

    # Setter para el nombre de usuario
    def set_nombre_usuario(self, nombre_usuario):
        self.nombre_usuario = nombre_usuario

    # Se comunica con el servidor para enviar su nombre de usuario
    # y su URI
    def registrar_usuario(self):
        self.server.registrar_usuario(self.nombre_usuario, self.uri)


# Se ingresa el nombre de usuario
nombre_usuario = input("Ingresa tu nombre de usuario: ")
# Se crea un objeto ClienteChat para establecer comunicación con el servidor
cliente = ClienteChat()
# Se crea un demonio Pyro en el host actual.
# Esto significa que no se podrá comunicar a través de la red, solo de forma local
daemon = Pyro5.server.Daemon(host=socket.gethostname())
# Se registra el objeto Cliente en el demonio con nombre de usuario como nombre de objeto
# El URI retornado se almacena
uri = daemon.register(cliente, nombre_usuario)
# Se establecen el nombre de usuario y URI en el objeto.
cliente.set_nombre_usuario(nombre_usuario)
cliente.set_uri(uri)
# Se envían los datos del usuario (nombre de usuario y URI) al servidor
cliente.registrar_usuario()

# Se crea un hilo secundario para escuchar las solicitudes del servidor
# Esto es para que se puedan enviar mensajes y recibirlos a la vez.
daemon_thread = threading.Thread(target=daemon.requestLoop, args=())
daemon_thread.start()

# Este bucle permite mandar mensajes hasta que el mensaje sea EXIT.
# Cuando el mensaje sea EXIT, el bucle se rompe y el hilo secundario se termina
while True:
    mensaje = input("> ")
    if mensaje == "EXIT":
        break
    cliente.enviar_mensaje(mensaje)

# Saliendo del bucle, habiendo escrito EXIT:
# Se apaga el daemon de Pyro
daemon.shutdown()
# Se espera a que el hilo termine su trabajo y terminar el proceso
daemon_thread.join()
