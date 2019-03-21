## STATS MODULE
def stats(mittente_username, comando, chat, canali, speech, invia_testo, invia_voce):
    elapsedtime = time.time()-start_time
    canali_nomi = ""

    for i in canali.values():
        canali_nomi = canali_nomi + "\n- " + i

    stringa = ("@"+str(mittente_username)+"\n"+
                    "Il bot è in funzione da "+
                    str(math.floor(elapsedtime%60))+" secondi, "+
                    str(math.floor((elapsedtime/60)%60))+" minuti, "+
                    str(math.floor((elapsedtime/60/60)%24))+" ore, "+
                    str(math.floor((elapsedtime/60/60/24)))+" giorni\n"+
                    "Inoltre sono presente nei seguenti canali:"+canali_nomi)

    if speech: invia_voce(chat["id"],stringa)
    else: invia_testo(chat["id"],stringa)
