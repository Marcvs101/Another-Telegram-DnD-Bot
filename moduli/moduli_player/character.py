from strutture.messaggio import Messaggio

## CHARACTER MODULE

def character(mittente, comando, chat, dati, speech, logfile):
    messaggi = []

    if comando.startswith("_lookat"):
        messaggi.append(Messaggio("Non implementato",chat["id"],speech))

    elif comando.startswith("_new"):
        messaggi.append(Messaggio("Non implementato",chat["id"],speech))

    elif comando.startswith("_edit"):
        messaggi.append(Messaggio("Non implementato",chat["id"],speech))

    elif comando.startswith("_remove"):
        messaggi.append(Messaggio("Non implementato",chat["id"],speech))

    else:
        messaggi.append(Messaggio("Benvenuto nell' inventario, @"+str(mittente["username"])+"\n"+
                                  "I comandi disponibili sono i seguenti:\n"+
                                  "/player_character_lookat - Esamina la tua scheda personaggio\n"+
                                  "/player_character_new - Crea una scheda personaggio\n"+
                                  "/player_character_edit - Aggiorna la tua scheda personaggio\n"+
                                  "/player_character_remove - Elimina la tua scheda personaggio",
                                  chat["id"],speech))

    return messaggi
