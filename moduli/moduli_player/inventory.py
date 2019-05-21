from strutture.messaggio import Messaggio

## INVENTORY MODULE

def inventory(mittente_username, comando, chat, dati, speech, logfile):
    messaggi = []

    if comando.startswith("/list"):
        messaggi.append(Messaggio("Non implementato",chat["id"],speech))

    elif comando.startswith("/get"):
        messaggi.append(Messaggio("Non implementato",chat["id"],speech))

    elif comando.startswith("/put"):
        messaggi.append(Messaggio("Non implementato",chat["id"],speech))

    elif comando.startswith("/remove"):
        messaggi.append(Messaggio("Non implementato",chat["id"],speech))

    else:
        messaggi.append(Messaggio("Benvenuto nell' inventario, @"+str(mittente_username)+"\n"+
                                  "I comandi disponibili sono i seguenti:\n"+
                                  "/player/inventory/list - Lista di tutti gli oggetti nell'inventario\n"+
                                  "/player/inventory/get - Esamina un oggetto senza rimuoverlo\n"+
                                  "/player/inventory/put - Aggiungi un oggetto all'inventario\n"+
                                  "/player/inventory/remove - Rimuovi un oggetto dall'inventario",
                                  chat["id"],speech))

    return messaggi
