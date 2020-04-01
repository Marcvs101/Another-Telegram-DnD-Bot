# M101
# Modulo per statistiche

# Import necessario al bot
from strutture.messaggio import Messaggio

# Import di funzionalità
import time
import math

# Comandi gestiti
# Questa variabile è usata dal main per capire quale modulo gestisce cosa
set_comandi = {"/stats"}

# Funzione principale
# Questa funzione è chiamata dal main per permettere al modulo di gestire
# ogni suo comando
def gestisci_comando(comando,messaggio,mittente,chat,start_time,dati,voce):
    messaggi = list()

    if comando == "/stats":
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

        messaggi.append(Messaggio(stringa,chat["id"],voce))

    return messaggi

# Funzione per popolare il comando help
def help():
    helpstr = "/stats - Mostra le statistiche correnti del bot"
    return helpstr
