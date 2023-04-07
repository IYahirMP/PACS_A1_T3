import Pyro5.api
import time
name = input("Cual es tu nombre: ").strip()
uri = input("Enter the uri that the server printed:").strip()
obj = Pyro5.api.Proxy(uri)
# use name server object lookup uri shortcut

while True:
    print("call...")
    try:
        obj.Metodo_a_Invocar(42)
        print("Sleeping 1 second")
        time.sleep(1)
    except Pyro5.errors.ConnectionClosedError:  # or possibly CommunicationError
        print("Connection lost. REBINDING...")
        print("(restart the server now)")
        obj._pyroReconnect()
