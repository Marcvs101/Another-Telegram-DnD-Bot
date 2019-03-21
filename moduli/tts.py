## TEXT TO SPEECH MODULE
def tts(mittente_username, comando, chat, canali, logfile, invia_voce, time):
    print(str(mittente_username)+" invoked /tts")
    print(str(time.time())+" : "+str(mittente_username)+" invoked /tts",file=logfile)
    parametri = comando.split(" ",1)
	
    if parametri[1].strip().startswith("/broadcast"):
        parametri = parametri[1].split(" ",1)
        for k,v in canali.items():
            invia_voce(k,parametri[1].strip())
            print(" - Found channel "+str(v)+" sending "+parametri[1][len(v):].strip())
            print(" - Found channel "+str(v)+" sending "+parametri[1][len(v):].strip(),file=logfile)
    
    elif parametri[1].strip().startswith("/sendto"):
        parametri = parametri[1].split(" ",1)
        for k,v in canali.items():
            if parametri[1].strip().lower().startswith(v.lower()):
                invia_voce(k,parametri[1][len(v):].strip())
                print(" - Found channel "+str(v)+" sending "+parametri[1][len(v):].strip())
                print(" - Found channel "+str(v)+" sending "+parametri[1][len(v):].strip(),file=logfile)
                break
    
    else:
        invia_voce(chat["id"],parametri[1].strip())
