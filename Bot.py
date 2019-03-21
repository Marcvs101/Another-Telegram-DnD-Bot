import telepot          #telegram
from gtts import gTTS   #Google TTS

# System
import json
from tempfile import NamedTemporaryFile
from random import randint
import httplib2
import os
import time
import math
import datetime
import re

telegram_path = "../Chiavi/Telegram.txt"
logfile_path = "../Debug/logfile.log"
datafile_path = "../Dati/datafile.json"

Telegram_Token = ""
telegramfile = open(telegram_path,mode='r')
Telegram_Token = telegramfile.readline().strip()
telegramfile.close()

start_time = time.time()
logfile = open(logfile_path,mode='a')
datafile = open(datafile_path,mode='r')
parsed = json.loads(datafile.read())
canali = {}

if parsed:
    canali = parsed
datafile.close()

def invia_voce(dest,txt):
    tts = gTTS(text=txt, lang='it')
    tts.save("audio.mp3")
    f = open("audio.mp3",mode="rb")
    bot.sendVoice(dest,f)
    f.close()
    os.remove("audio.mp3")

def invia_testo(dest,txt):
    bot.sendMessage(dest,txt,parse_mode="HTML")

def handler_messaggio(msg):
    logfile = open(logfile_path,mode='a')
    try:
        chat = msg["chat"]
        mittente = msg["from"]
        mittente_username = ""
        comando = msg["text"]+" "
        risposta = None
        speech = False

        if ("username" in mittente):
            mittente_username = mittente["username"]
        elif ("first_name" in mittente):
            mittente_username = str(mittente["id"]) + " (" + mittente["first_name"]
            if ("last_name" in mittente):
                mittente_username = mittente_username + " " + mittente["last_name"]
            mittente_username = mittente_username + ")"

        if (not(str(chat["id"]) in canali) and (chat["type"] == "group" or chat["type"] == "supergroup")):
            canali[str(chat["id"])] = chat["title"]
            datafile = open(datafile_path,mode='w')
            json.dump(canali,datafile,sort_keys=True,indent=4)
            datafile.close()
        
        if "reply_to_message" in msg:
            risposta = msg["reply_to_message"]
            print(str(mittente_username)+" responded to me")
            print(str(time.time())+" : "+str(mittente_username)+" responded to me",file=logfile)
            invia_testo(chat["id"],"Il Male cortese risponde alla richiesta di @"+
                        str(mittente_username)+"\n"+
                        "Un assistente malvagio sarà presto mandato ad ascoltare la richiesta")

        if "-tts" in comando:
            speech = True


        if comando.startswith("/start"):
            print(str(mittente_username)+" invoked /start")
            print(str(time.time())+" : "+str(mittente_username)+" invoked /start",file=logfile)
            stringa = ("Il Male è sceso tra voi\n"+
                            "Dal momento che i miei malefici assistenti sono in sciopero, le mie funzionalità sono limitate\n"+
                            "Usa il comando /help per una lista delle funzionalità\n\n"+
                            "Per qualsiasi problema, mandare un messaggio a @Marcvs101")
            invia_testo(chat["id"],stringa)

            
        elif comando.startswith("/help"):
            print(str(mittente_username)+" invoked /help")
            print(str(time.time())+" : "+str(mittente_username)+" invoked /help",file=logfile)
            stringa = ("Ecco quello che il Male è in grado di fare, @"+str(mittente_username)+"\n"+
                            "/help - Mostra alcuni comandi a disposizione del bot\n"+
                            "/roll [NUMERO]d[FACCE] [+-MODIFICATORE] - Tira per [NUMERO] volte un d[FACCE].\n"+
                            "    Alla somma totale viene applicato [+-MODIFICATORE]\n"+
                            "/stats - Mostra le statistiche correnti del bot\n"+
                            "-tts aggiunto a qualsiasi comando genera una sintesi vocale")
            if speech: invia_voce(chat["id"],stringa)
            else: invia_testo(chat["id"],stringa)

            
##        elif comando.startswith("/adminhelp"):
##            print(str(mittente_username)+" invoked /helpadmin")
##            print(str(time.time())+" : "+str(mittente_username)+" invoked /helpadmin",file=logfile)
##            stringa = ("Ecco una lista di comandi di amministrazione, @"+str(mittente_username)+"\n"+
##                            "/sendto [CHAN] [MSG] - Manda un messaggio al canale\n"+
##                            "/broadcast [MSG] - Manda un messaggio a tutti i canali\n"+
##                            "/debug - Dump dello stato sul log")
##            if speech: invia_voce(chat["id"],stringa)
##            else: invia_testo(chat["id"],stringa)


        elif comando.startswith("/stats"):
            print(str(mittente_username)+" invoked /stats")
            print(str(time.time())+" : "+str(mittente_username)+" invoked /stats",file=logfile)
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


        elif comando.startswith("/roll"):
            print(str(mittente_username)+" invoked /roll")
            print(str(time.time())+" : "+str(mittente_username)+" invoked /roll",file=logfile)
            parametri = comando.split(" ")
            paramDado = parametri[1].strip().lower().split("d",1)

            paramModificatore = 0
            if (len(parametri) >= 3):
                if (parametri[2].strip().replace("-","").replace("+","").isdigit()):
                    paramModificatore = int(parametri[2])

            if (len(paramDado) >= 2):
                if (paramDado[1].replace("d","").strip().isdigit()):
                    num = 1
                    if paramDado[0].strip().isdigit():
                        num = int(paramDado[0].strip())
                    dado = int(paramDado[1].replace("d","").strip())

            stringa = ("@"+str(mittente_username)+"\n"+
                           "Tirando "+str(num)+" volte un D"+
                           str(dado)+" ho ottenuto:\n")

            somma = 0
            for i in range(num):
                tiro = randint(1,dado)
                somma = somma + tiro
                stringa = stringa+" "+str(i+1)+"- "+str(tiro)+"\n"
            stringa = stringa + "Totale: "+str(somma)
    
            if paramModificatore > 0:
                stringa = stringa + "+" + str(paramModificatore) + " -> " + str(somma+paramModificatore)
            if paramModificatore < 0:
                stringa = stringa + str(paramModificatore) + " -> " + str(somma+paramModificatore)

            if speech: invia_voce(chat["id"],stringa)
            else: invia_testo(chat["id"],stringa)


##        elif comando.startswith("/sendto"):
##            print(str(mittente_username)+" invoked /sendto")
##            print(str(time.time())+" : "+str(mittente_username)+" invoked /sendto",file=logfile)
##            parametri = comando.split(" ",1)
##            for k,v in canali.items():
##                if parametri[1].strip().lower().startswith(v.lower()):
##                    stringa = parametri[1][len(v):].strip()
##                    if speech: invia_voce(k,stringa)
##                    else: invia_testo(k,stringa)
##                    print(" - Found channel "+str(v)+" sending "+parametri[1][len(v):].strip())
##                    print(" - Found channel "+str(v)+" sending "+parametri[1][len(v):].strip(),file=logfile)
##                    break
##
##
##        elif comando.startswith("/broadcast"):
##            print(str(mittente_username)+" invoked /broadcast")
##            print(str(time.time())+" : "+str(mittente_username)+" invoked /broadcast",file=logfile)
##            stringa = comando.split(" ",1)[1].strip()
##            for k,v in canali.items():
##                if speech: invia_voce(k,stringa)
##                else: invia_testo(k,stringa)
##                print(" - Found channel "+str(v)+" sending "+stringa)
##                print(" - Found channel "+str(v)+" sending "+stringa,file=logfile)
##
##
##        elif comando.startswith("/tts"):
##            print(str(mittente_username)+" invoked /tts")
##            print(str(time.time())+" : "+str(mittente_username)+" invoked /tts",file=logfile)
##            parametri = comando.split(" ",1)
            
##            if parametri[1].strip().startswith("/broadcast"):
##                parametri = parametri[1].split(" ",1)
##                for k,v in canali.items():
##                    invia_voce(k,parametri[1].strip())
##                    print(" - Found channel "+str(v)+" sending "+parametri[1][len(v):].strip())
##                    print(" - Found channel "+str(v)+" sending "+parametri[1][len(v):].strip(),file=logfile)
            
##            elif parametri[1].strip().startswith("/sendto"):
##                parametri = parametri[1].split(" ",1)
##                for k,v in canali.items():
##                    if parametri[1].strip().lower().startswith(v.lower()):
##                        invia_voce(k,parametri[1][len(v):].strip())
##                        print(" - Found channel "+str(v)+" sending "+parametri[1][len(v):].strip())
##                        print(" - Found channel "+str(v)+" sending "+parametri[1][len(v):].strip(),file=logfile)
##                        break
            
##            else:
##                invia_voce(chat["id"],parametri[1].strip())


        elif comando.startswith("/debug"):
            print(str(mittente_username)+" invoked /debug\n"+
                    " - Start time: "+str(start_time)+"\n"+
                    " - Elapsed time (seconds): "+str(time.time()-start_time)+"\n"+
                    " - Current chats: "+str(len(canali))+"\n"+
                    " - Telegram token: "+Telegram_Token)
            print(str(time.time())+" : "+str(mittente_username)+" invoked /debug\n"+
                    " - Start time: "+str(start_time)+"\n"+
                    " - Elapsed time (seconds): "+str(time.time()-start_time)+"\n"+
                    " - Current chats: "+str(len(canali))+"\n"+
                    " - Telegram token: "+Telegram_Token,file=logfile)
            invia_testo(chat["id"],"@"+str(mittente_username)+"\n"+
                            "Informazioni di debug stampate sul terminale")


    except Exception as e:
        print("Catastrophic failure\n"+str(e)+"\n")
        print(str(time.time())+" : "+"Catastrophic failure\n"+str(e)+"\n",file=logfile)
    logfile.close()
    return

bot = telepot.Bot(Telegram_Token)
bot.message_loop(handler_messaggio)

print(str(time.time())+" : Server start",file=logfile)
logfile.close()

while 1:
    time.sleep(60) #secondi
