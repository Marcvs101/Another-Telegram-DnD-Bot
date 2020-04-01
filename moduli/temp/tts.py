from strutture.messaggio import Messaggio

## TEXT TO SPEECH MODULE

def tts(mittente, comando, chat, dati, logfile):
    messaggi = []

    if comando.strip().startswith("/broadcast"):
        parametri = comando.split(" ",2)
        for k,v in dati["canali"].items():
            print(" - Found channel "+str(v)+" sending "+parametri[2].strip())
            print(" - Found channel "+str(v)+" sending "+parametri[2].strip(),file=logfile)
            messaggi.append(Messaggio(parametri[2].strip(),k,True))
    
    elif comando.strip().startswith("/sendto"):
        parametri = comando.split(" ",2)
        for k,v in dati["canali"].items():
            if parametri[1].strip().lower().startswith(v.lower()):
                print(" - Found channel "+str(v)+" sending "+parametri[2].strip())
                print(" - Found channel "+str(v)+" sending "+parametri[2].strip(),file=logfile)
                messaggi.append(Messaggio(parametri[2].strip(),k,True))
                break
    
    else:
        messaggi.append(Messaggio(comando.strip(),chat["id"],True))

    return messaggi
