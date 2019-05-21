from strutture.messaggio import Messaggio

## INVENTORY MODULE

def inventory(mittente, comando, chat, dati, speech, logfile):
    messaggi = []

    if comando.startswith("_list"):
        messaggi.append(Messaggio("Non implementato",chat["id"],speech))

    elif comando.startswith("_get"):
        messaggi.append(Messaggio("Non implementato",chat["id"],speech))

    elif comando.startswith("_put"):
        messaggi.append(Messaggio("Non implementato",chat["id"],speech))

    elif comando.startswith("_remove"):
        messaggi.append(Messaggio("Non implementato",chat["id"],speech))

    else:
        messaggi.append(Messaggio("Benvenuto nell' inventario, @"+str(mittente["username"])+"\n"+
                                  "I comandi disponibili sono i seguenti:\n"+
                                  "/player_inventory_list - Lista di tutti gli oggetti nell'inventario\n"+
                                  "/player_inventory_get - Esamina un oggetto senza rimuoverlo\n"+
                                  "/player_inventory_put - Aggiungi un oggetto all'inventario\n"+
                                  "/player_inventory_remove - Rimuovi un oggetto dall'inventario",
                                  chat["id"],speech))

    return messaggi
