from strutture.messaggio import Messaggio

## CHARACTER MODULE

def character(mittente_username, comando, chat, dati, speech, logfile):
    messaggi = []

    if comando.startswith("/get"):
        messaggi.append(Messaggio("Non implementato",chat["id"],speech))

    elif comando.startswith("/new"):
        messaggi.append(Messaggio("Non implementato",chat["id"],speech))

    elif comando.startswith("/edit"):
        messaggi.append(Messaggio("Non implementato",chat["id"],speech))

    elif comando.startswith("/remove"):
        messaggi.append(Messaggio("Non implementato",chat["id"],speech))

    else:
        messaggi.append(Messaggio("Benvenuto nell' inventario, @"+str(mittente_username)+"\n"+
                                  "I comandi disponibili sono i seguenti:\n"+
                                  "/player/character/lookat - Esamina la tua scheda personaggio\n"+
                                  "/player/inventory/new - Crea una scheda personaggio\n"+
                                  "/player/inventory/edit - Aggiorna la tua scheda personaggio\n"+
                                  "/player/inventory/remove - Elimina la tua scheda personaggio",
                                  chat["id"],speech))

    return messaggi
