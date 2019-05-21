import telepot          #telegram
from gtts import gTTS   #Google TTS

# System
import json
from tempfile import NamedTemporaryFile
import random
import httplib2
import os
import time
import math
import datetime
import re

#Strutture
from strutture.messaggio import Messaggio

# Moduli
import moduli.tts as tts
import moduli.roll as roll
import moduli.stats as stats
import moduli.player as player

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
dati = {}
dati["canali"] = {}
dati["utenti"] = {}

if parsed:
    dati["canali"] = parsed["canali"]
    dati["utenti"] = parsed["utenti"]
datafile.close()

#Funzioni aux
def invia_voce(dest,txt):
    tts = gTTS(text=txt, lang='it')
    tts.save("audio.mp3")
    f = open("audio.mp3",mode="rb")
    bot.sendVoice(dest,f)
    f.close()
    os.remove("audio.mp3")

def invia_testo(dest,txt):
    bot.sendMessage(dest,txt,parse_mode="HTML")

#Funzione principale
def handler_messaggio(msg):
    logfile = open(logfile_path,mode='a')
    try:
        chat = msg["chat"]
        mittente = msg["from"]
        mittente_username = ""
        comando = msg["text"]+" "
        risposta = None
        speech = False
        messaggi = []

        if ("username" in mittente):
            mittente_username = mittente["username"]
        elif ("first_name" in mittente):
            mittente_username = str(mittente["id"]) + " (" + mittente["first_name"]
            if ("last_name" in mittente):
                mittente_username = mittente_username + " " + mittente["last_name"]
            mittente_username = mittente_username + ")"

        if ( ( (not(str(chat["id"]) in dati["canali"])) or (not(str(mittente["id"]) in dati["utenti"])) ) and ((chat["type"] == "group") or (chat["type"] == "supergroup")) ):
            dati["canali"][str(chat["id"])] = chat["title"]
            dati["utenti"][str(mittente["id"])] = mittente_username
            datafile = open(datafile_path,mode='w')
            json.dump(dati,datafile,sort_keys=True,indent=4)
            datafile.close()

        if "reply_to_message" in msg:
            risposta = msg["reply_to_message"]
            print(str(mittente_username)+" responded to me")
            print(str(time.time())+" : "+str(mittente_username)+" responded to me",file=logfile)
            messaggi.append(Messaggio("Il Male cortese risponde alla richiesta di @"+str(mittente_username)+"\n"+
                                      "Un assistente malvagio sarà presto mandato ad ascoltare la richiesta",
                                      chat["id"],False))

        if "-tts" in comando:
            speech = True

        if comando.startswith("/start"):
            print(str(mittente_username)+" invoked /start")
            print(str(time.time())+" : "+str(mittente_username)+" invoked /start",file=logfile)
            messaggi.append(Messaggio("Il Male è sceso tra voi\n"+
                                      "Dal momento che i miei malefici assistenti sono in sciopero, le mie funzionalità sono limitate\n"+
                                      "Usa il comando /help per una lista delle funzionalità\n\n"+
                                      "Per qualsiasi problema, mandare un messaggio a @Marcvs101",
                                      chat["id"],False))
            
        elif comando.startswith("/help"):
            print(str(mittente_username)+" invoked /help")
            print(str(time.time())+" : "+str(mittente_username)+" invoked /help",file=logfile)
            messaggi.append(Messaggio("Ecco quello che il Male è in grado di fare, @"+str(mittente_username)+"\n"+
                                      "/help - Mostra alcuni comandi a disposizione del bot\n"+
                                      "/roll [NUMERO]d[FACCE] [+-MODIFICATORE] - Tira per [NUMERO] volte un d[FACCE].\n"+
                                      "    Alla somma totale viene applicato [+-MODIFICATORE]\n"+
                                      "/player - Accesso al menù del giocatore\n"+
                                      "/stats - Mostra le statistiche correnti del bot\n"+
                                      "-tts aggiunto a qualsiasi comando genera una sintesi vocale",
                                      chat["id"],speech))

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
            messaggi = stats.stats(mittente_username, comando.replace("/stats","",1), start_time, chat, dati, speech)

        elif comando.startswith("/roll"):
            print(str(mittente_username)+" invoked /roll")
            print(str(time.time())+" : "+str(mittente_username)+" invoked /roll",file=logfile)
            messaggi = roll.roll(mittente_username, comando.replace("/roll","",1), chat, dati, speech)

        elif comando.startswith("/player"):
            print(str(mittente_username)+" invoked /player in "+str(chat["type"])+" chat")
            print(str(time.time())+" : "+str(mittente_username)+" invoked /player in "+str(chat["type"])+" chat",file=logfile)
            messaggi = player.player(mittente_username, comando.replace("/player","",1), chat, dati, speech, logfile)

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
##        elif comando.startswith("/broadcast"):
##            print(str(mittente_username)+" invoked /broadcast")
##            print(str(time.time())+" : "+str(mittente_username)+" invoked /broadcast",file=logfile)
##            stringa = comando.split(" ",1)[1].strip()
##            for k,v in canali.items():
##                if speech: invia_voce(k,stringa)
##                else: invia_testo(k,stringa)
##                print(" - Found channel "+str(v)+" sending "+stringa)
##                print(" - Found channel "+str(v)+" sending "+stringa,file=logfile)

        elif comando.startswith("/tts"):
            print(str(mittente_username)+" invoked /tts")
            print(str(time.time())+" : "+str(mittente_username)+" invoked /tts",file=logfile)
            messaggi = tts.tts(mittente_username, comando.replace("/tts","",1), chat, dati, logfile)

        elif comando.startswith("/debug"):
            print(str(mittente_username)+" invoked /debug\n"+
                    " - Start time: "+str(start_time)+"\n"+
                    " - Elapsed time (seconds): "+str(time.time()-start_time)+"\n"+
                    " - Current chats: "+str(len(dati["canali"]))+"\n"+
                    " - Telegram token: "+Telegram_Token)
            print(str(time.time())+" : "+str(mittente_username)+" invoked /debug\n"+
                    " - Start time: "+str(start_time)+"\n"+
                    " - Elapsed time (seconds): "+str(time.time()-start_time)+"\n"+
                    " - Current chats: "+str(len(dati["canali"]))+"\n"+
                    " - Telegram token: "+Telegram_Token,file=logfile)
            messaggi.append(Messaggio("@"+str(mittente_username)+"\n"+
                                      "Informazioni di debug stampate sul terminale",
                                      chat["id"],False))

        for i in messaggi:
            if i.speech: invia_voce(i.canale,i.testo)
            else: invia_testo(i.canale,i.testo)

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
