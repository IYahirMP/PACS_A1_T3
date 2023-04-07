import socket
import Pyro5
import Pyro5.api
import Pyro5.server

# Configura el software de serialización para que se use serpent
Pyro5.config.SERIALIZER = "serpent"

# Se crea la clase ServidorChat
# Su propósito es proveer al usuario remoto una interfaz
# Para enviar mensajes a otros usuarios remotos


class ServidorChat:
    # Inicializa un diccionario de usuarios
    # Este diccionario contendrá pares
    # De la forma (nombre del host, URI del host)
    def __init__(self):
        self.usuarios = {}

    # Se crea el metodo registrar_usuario
    # Sirve para añadir un usuario y la URI de su programa cliente
    # al diccionario usuarios.
    # Se expone al exterior usando el decorador expose
    @Pyro5.api.expose
    def registrar_usuario(self, nombre_usuario, uri):
        self.usuarios[nombre_usuario] = uri
        print(nombre_usuario, "ha entrado al chat.")
        self.enviar_mensaje(nombre_usuario, nombre_usuario +
                            " ha entrado al chat.", True)

    # Se crea el metodo enviar_mensaje
    # Este metodo se llama desde el cliente para
    # que el servidor a su vez solicite a cada usuario registrado
    # diferente del solicitante que reciba un mensaje
    @Pyro5.api.expose
    def enviar_mensaje(self, nombre_usuario, message, esReg=False):
        if (esReg != True):
            print(nombre_usuario, ": ", message)
        # Por cada usuario en el diccionario
        for usuario in self.usuarios:
            # Si el usuario actual es distinto al solicitante
            if usuario != nombre_usuario:
                # Se crea un enlace de comunicacion con el usuario
                proxy_usuario = Pyro5.api.Proxy(self.usuarios[usuario])
                # Se solicita que reciba el mensaje del solicitante
                if (esReg == False):
                    proxy_usuario.recibir_mensaje(
                        nombre_usuario, message)
                else:
                    proxy_usuario.recibir_mensaje("Servidor", message)


# Rutina principal
servidor = ServidorChat()
daemon = Pyro5.server.Daemon(host=socket.gethostname(), port=65530)
print("Demonio creado: ", daemon)
uri = daemon.register(servidor, "ChatSV")
print("URI del objeto creado: ", uri)
print("Iniciando bucle de solicitudes...")
daemon.requestLoop()
