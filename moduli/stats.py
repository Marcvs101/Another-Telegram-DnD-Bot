import time
import math
from strutture.messaggio import Messaggio

## STATS MODULE
def stats(mittente, comando, start_time, chat, dati, speech):
    messaggi = []
    
    elapsedtime = time.time()-start_time
    canali_nomi = ""

    for i in dati["canali"].values():
        canali_nomi = canali_nomi + "\n- " + i

    stringa = ("@"+str(mittente["username"])+"\n"+
                    "Il bot è in funzione da "+
                    str(math.floor(elapsedtime%60))+" secondi, "+
                    str(math.floor((elapsedtime/60)%60))+" minuti, "+
                    str(math.floor((elapsedtime/60/60)%24))+" ore, "+
                    str(math.floor((elapsedtime/60/60/24)))+" giorni\n"+
                    "Inoltre sono presente nei seguenti canali:"+canali_nomi)

    messaggi.append(Messaggio(stringa,chat["id"],speech))
    return messaggi
