## DICE ROLL MODULE
def roll(mittente_username, comando, chat, canali, speech, invia_testo, invia_voce):
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
