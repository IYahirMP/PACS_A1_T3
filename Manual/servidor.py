# Con un servidor de nombres
# Si bien el ejemplo anterior funciona, podría volverse tedioso trabajar con objetos uri como ese. Ya hay un gran problema, ¿ cómo se supone que el cliente obtenga el uri, si no lo estamos copiando y pegando? Afortunadamente, Pyro proporciona un servidor de nombres que funciona como una guía telefónica automática. Puede nombrar sus objetos usando nombres lógicos y usar el servidor de nombres para buscar el uri correspondiente.
import Pyro5.api
import socket
import Pyro5.socketutil

hostname = socket.gethostname()  # nombredelapc
my_ip = Pyro5.socketutil.get_ip_address(None, workaround127=True, version=4)


@Pyro5.api.expose
class Clase_que_se_expone(object):
    def Metodo_a_Invocar(self, name):
        return "Hola, {0}. Aqui esta tu mensaje:\n" \
               "El metodo u objeto fue invocado correctamente.".format(name)


daemon = Pyro5.api.Daemon(host=hostname)         # make a Pyro daemon
print("HOST: ", hostname)
print("NOMBRE del Deamon: ", daemon)
print("IP DEL EQUIPO: ", my_ip)  # verificar como asignar IP de la maquina
uri = daemon.register(Clase_que_se_expone, objectId="metodo")
print("Server started, uri: %s" % uri)
print("NOMBRE del demonio: ", daemon)

print("Ready.")
# start the event loop of the server to wait for calls
daemon.requestLoop()
