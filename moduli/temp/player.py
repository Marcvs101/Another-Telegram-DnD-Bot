import moduli.moduli_player.character as character
import moduli.moduli_player.inventory as inventory
from strutture.messaggio import Messaggio

## PLAYER MODULE

def player(mittente, comando, chat, dati, speech, logfile):
    messaggi = []

    if (chat["type"]!="private"):
        messaggi.append(Messaggio("@"+str(mittente["username"])+", il menù del giocatore può essere acceduto solo nelle conversazioni private",chat["id"],speech))
        messaggi.append(Messaggio("@"+str(mittente["username"])+", i comandi possono essere inviati qui",mittente["id"],speech))

    elif comando.startswith("_character"):
        print(" - navigated to /player_character")
        print(" - navigated to /player_character",file=logfile)
        messaggi = character.character(mittente, comando.replace("_character","",1), chat, dati, speech, logfile)

    elif comando.startswith("_inventory"):
        print(" - navigated to /player_inventory")
        print(" - navigated to /player_inventory",file=logfile)
        messaggi = inventory.inventory(mittente, comando.replace("_inventory","",1), chat, dati, speech, logfile)
        
    else:
        messaggi.append(Messaggio("Benvenuto nel menù del giocatore, @"+str(mittente["username"])+"\n"+
                                  "I comandi disponibili sono i seguenti:\n"+
                                  "/player_character - Accedi al personaggio\n"+
                                  "/player_inventory - Accedi all'inventario",
                                  chat["id"],speech))
    return messaggi
