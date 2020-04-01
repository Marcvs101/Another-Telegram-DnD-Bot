# M101

# Import per funzionalità
import re
import os
import math
import time
import json
import random
import datetime
import importlib
from tempfile import NamedTemporaryFile

# Servizi esterni
import telepot          #telegram
from gtts import gTTS   #Google TTS

#Strutture
from strutture.messaggio import Messaggio

# Path dei file
telegram_path = "../Chiavi/Telegram.txt"
logfile_path = "../Debug/logfile.log"
datafile_path = "../Dati/datafile.json"

# Token telegram
Telegram_Token = ""
telegramfile = open(telegram_path,mode='r')
Telegram_Token = telegramfile.readline().strip()
telegramfile.close()

# Logfile e Datafile
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

# Caricamento Moduli
print("Loading modules")
print(str(time.time())+" : Loading Modules",file=logfile)
moduli_cartella = "moduli"
moduli_caricati = dict()

for file in os.listdir(path=moduli_cartella):
    if ".py" in file:
        try:
            moduli_caricati[file] = importlib.import_module(name=moduli_cartella+"."+file.replace(".py",""))
            print("Loaded "+file)
            print(str(time.time())+" : Loaded "+file,file=logfile)
        except Exception as e:
            moduli_caricati[file] = None
            print("Failed to load "+file+"\n"+e)
            print(str(time.time())+" : Failed to load "+file+"\n########\n"+e+"\n########",file=logfile)
print("")

# Registrazione Moduli
moduli_comandi = dict()
comandi_moduli = dict()

for modulo in moduli_caricati:
    set_comandi = set()
    set_comandi = moduli_caricati[modulo].set_comandi
    for comando in set_comandi:
        if comando in comandi_moduli:
            print("Command "+comando+" already registered by module "+comandi_moduli[comando])
            print(str(time.time())+" : Command "+comando+" already registered by module "+comandi_moduli[comando],file=logfile)
        else:
            comandi_moduli[comando] = modulo
            if modulo not in moduli_comandi: moduli_comandi[modulo] = set()
            moduli_comandi[modulo].add(comando)
            print("Command "+comando+" registered by module "+modulo)
            print(str(time.time())+" : Command "+comando+" registered by module "+modulo,file=logfile)
print("")

# Costruzione della stringa di aiuto
helpstr_moduli = ""
for modulo in moduli_caricati:
    helpstr_moduli = helpstr_moduli + "Modulo '"+modulo.replace(".py","")+"'\n"
    helpstr_moduli = helpstr_moduli + moduli_caricati[modulo].help()+"\n\n"

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
        # Estrazione elementi del messaggio
        chat = msg["chat"]
        mittente = msg["from"]
        comando = msg["text"]+" "
        comando = comando[:comando.find(" ")]
        messaggio = msg["text"]+" "
        risposta = None
        voce = False

        # Coda di messaggi
        messaggi = list()

        # Gestione username misti
        if (not ("username" in mittente)) or (mittente["username"] == None) or (mittente["username"]==""):
            if ("first_name" in mittente):
                mittente["username"] = str(mittente["id"]) + " (" + mittente["first_name"]
                if ("last_name" in mittente):
                    mittente["username"] = mittente["username"] + " " + mittente["last_name"]
                mittente["username"] = mittente["username"] + ")"

        # Logging dei canali/utenti
        if ( ( (not(str(chat["id"]) in dati["canali"])) or (not(str(mittente["id"]) in dati["utenti"])) ) and ((chat["type"] == "group") or (chat["type"] == "supergroup")) ):
            dati["canali"][str(chat["id"])] = chat["title"]
            dati["utenti"][str(mittente["id"])] = mittente["username"]
            datafile = open(datafile_path,mode='w')
            json.dump(dati,datafile,sort_keys=True,indent=4)
            datafile.close()

        # Gestione risposte
        if "reply_to_message" in msg:
            risposta = msg["reply_to_message"]
            print(str(mittente["username"])+" responded to me")
            print(str(time.time())+" : "+str(mittente["username"])+" responded to me",file=logfile)
            messaggi.append(Messaggio("Il Male cortese risponde alla richiesta di @"+str(mittente["username"])+"\n"+
                                      "Un assistente malvagio sarà presto mandato ad ascoltare la richiesta",
                                      chat["id"],False))

        # Flag vocale
        if "-tts" in comando:
            voce = True

        # Comandi di sistema
        if comando == "/start":
            print(str(mittente["username"])+" invoked /start")
            print(str(time.time())+" : "+str(mittente["username"])+" invoked /start",file=logfile)
            messaggi.append(Messaggio("Il Male è sceso tra voi\n"+
                                      "Dal momento che i miei malefici assistenti sono in sciopero, le mie funzionalità sono limitate\n"+
                                      "Usa il comando /help per una lista delle funzionalità\n\n"+
                                      "Per qualsiasi problema, mandare un messaggio a @Marcvs101",
                                      chat["id"],False))
            
        elif comando == "/help":
            print(str(mittente["username"])+" invoked /help")
            print(str(time.time())+" : "+str(mittente["username"])+" invoked /help",file=logfile)
            messaggi.append(Messaggio("Ecco quello che il Male è in grado di fare, @"+str(mittente["username"])+"\n"+
                                      "/help - Mostra alcuni comandi a disposizione del bot\n"+
                                      "\n"+
                                      helpstr_moduli+
                                      "-tts aggiunto a qualsiasi comando genera una sintesi vocale",
                                      chat["id"],voce))

##        elif comando.startswith("/adminhelp"):
##            print(str(mittente["username"])+" invoked /helpadmin")
##            print(str(time.time())+" : "+str(mittente["username"])+" invoked /helpadmin",file=logfile)
##            stringa = ("Ecco una lista di comandi di amministrazione, @"+str(mittente["username"])+"\n"+
##                            "/sendto [CHAN] [MSG] - Manda un messaggio al canale\n"+
##                            "/broadcast [MSG] - Manda un messaggio a tutti i canali\n"+
##                            "/debug - Dump dello stato sul log")
##            if speech: invia_voce(chat["id"],stringa)
##            else: invia_testo(chat["id"],stringa)

##        elif comando.startswith("/player"):
##            print(str(mittente["username"])+" invoked /player in "+str(chat["type"])+" chat")
##            print(str(time.time())+" : "+str(mittente["username"])+" invoked /player in "+str(chat["type"])+" chat",file=logfile)
##            messaggi = player.player(mittente, comando.replace("/player","",1).strip(), chat, dati, speech, logfile)

##        elif comando.startswith("/spells"):
##            print(str(mittente["username"])+" invoked /spells in "+str(chat["type"])+" chat")
##            print(str(time.time())+" : "+str(mittente["username"])+" invoked /spells in "+str(chat["type"])+" chat",file=logfile)
##            messaggi = spells.spells(mittente, comando.replace("/spells","",1).strip(), chat, dati, speech, logfile)

##        elif comando.startswith("/sendto"):
##            print(str(mittente["username"])+" invoked /sendto")
##            print(str(time.time())+" : "+str(mittente["username"])+" invoked /sendto",file=logfile)
##            parametri = comando.split(" ",1)
##            for k,v in canali.items():
##                if parametri[1].strip().lower().startswith(v.lower()):
##                    stringa = parametri[1][len(v):].strip()
##                    if speech: invia_voce(k,stringa)
##                    else: invia_testo(k,stringa)
##                    print(" - Found channel "+str(v)+" sending "+parametri[1][len(v):].strip())
##                    print(" - Found channel "+str(v)+" sending "+parametri[1][len(v):].strip(),file=logfile)
##                    break

##        elif comando.startswith("/broadcast"):
##            print(str(mittente["username"])+" invoked /broadcast")
##            print(str(time.time())+" : "+str(mittente["username"])+" invoked /broadcast",file=logfile)
##            stringa = comando.split(" ",1)[1].strip()
##            for k,v in canali.items():
##                if speech: invia_voce(k,stringa)
##                else: invia_testo(k,stringa)
##                print(" - Found channel "+str(v)+" sending "+stringa)
##                print(" - Found channel "+str(v)+" sending "+stringa,file=logfile)

##        elif comando.startswith("/tts"):
##            print(str(mittente["username"])+" invoked /tts")
##            print(str(time.time())+" : "+str(mittente["username"])+" invoked /tts",file=logfile)
##            messaggi = tts.tts(mittente, comando.replace("/tts","",1).strip(), chat, dati, logfile)

        elif comando == "/debug":
            print(str(mittente["username"])+" invoked /debug\n"+
                    " - Start time: "+str(start_time)+"\n"+
                    " - Elapsed time (seconds): "+str(time.time()-start_time)+"\n"+
                    " - Current chats: "+str(len(dati["canali"]))+"\n"+
                    " - Telegram token: "+Telegram_Token)
            print(str(time.time())+" : "+str(mittente["username"])+" invoked /debug\n"+
                    " - Start time: "+str(start_time)+"\n"+
                    " - Elapsed time (seconds): "+str(time.time()-start_time)+"\n"+
                    " - Current chats: "+str(len(dati["canali"]))+"\n"+
                    " - Telegram token: "+Telegram_Token,file=logfile)
            messaggi.append(Messaggio("@"+str(mittente["username"])+"\n"+
                                      "Informazioni di debug stampate sul terminale",
                                      chat["id"],False))

        # Comandi dei moduli
        else:
            if (comando in comandi_moduli) and (comandi_moduli[comando] != None):
                try:
                    modulo = comandi_moduli[comando]
                    print("Module "+modulo+" is handling command "+comando)
                    print(str(time.time())+" : Module "+modulo+" is handling command "+comando,file=logfile)
                    messaggi = moduli_caricati[modulo].gestisci_comando(comando,messaggio,mittente,chat,start_time,dati,voce)
                    print("Module "+modulo+" has finished handling command "+comando)
                    print(str(time.time())+" : Module "+modulo+" has finished handling command "+comando,file=logfile)
                except Exception as em:
                    print("Catastrophic failure in module "+modulo+" while trying to handle command"+comando+"\n"+str(em)+"\n")
                    print(str(time.time())+" : Catastrophic failure in module "+modulo+" while trying to handle command"+comando+"\n########\n"+str(em)+"\n########",file=logfile)

        # Invio della coda di messaggi
        for i in messaggi:
            if i.voce: invia_voce(i.canale,i.testo)
            else: invia_testo(i.canale,i.testo)

    except Exception as e:
        print("Catastrophic failure\n"+str(e)+"\n")
        print(str(time.time())+" : Catastrophic failure\n########\n"+str(e)+"\n########",file=logfile)

    logfile.close()
    return

bot = telepot.Bot(Telegram_Token)
bot.message_loop(handler_messaggio)

print("Server started")
print(str(time.time())+" : Server started",file=logfile)
logfile.close()

while True:
    time.sleep(60) #secondi
