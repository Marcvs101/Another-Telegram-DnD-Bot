import moduli.moduli_player.character as character
import moduli.moduli_player.inventory as inventory
from strutture.messaggio import Messaggio

## PLAYER MODULE

def player(mittente_username, comando, chat, dati, speech, logfile):
    messaggi = []

    if (chat["type"]!="private"):
        messaggi.append(Messaggio("@"+str(mittente_username)+", il menù del giocatore può essere acceduto solo nelle conversazioni private",chat["id"],speech))

    elif comando.startswith("/character"):
        print(" - navigated to /player/character")
        print(" - navigated to /player/character",file=logfile)
        messaggi = character.character(mittente_username, comando.replace("/character","",1), chat, dati, speech, logfile)

    elif comando.startswith("/inventory"):
        print(" - navigated to /player/inventory")
        print(" - navigated to /player/inventory",file=logfile)
        messaggi = inventory.inventory(mittente_username, comando.replace("/inventory","",1), chat, dati, speech, logfile)
        
    else:
        messaggi.append(Messaggio("Benvenuto nel menù del giocatore, @"+str(mittente_username)+"\n"+
                                  "I comandi disponibili sono i seguenti:\n"+
                                  "/player/character - Accedi al personaggio\n"+
                                  "/player/inventory - Accedi all'inventario",
                                  chat["id"],speech))
    return messaggi
