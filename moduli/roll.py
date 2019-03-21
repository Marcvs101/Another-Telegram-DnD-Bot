## DICE ROLL MODULE
from random import randint

def roll(mittente_username, comando, chat, canali, speech, invia_testo, invia_voce):
##    parametri = comando.lower().strip().split(" ",1)[1].split(" ")
##    somma_dadi = 0
##    somma_costanti = 0
##    stringa = "@"+str(mittente_username)+"\n"
##    for token in parametri:
##        if (token.isdecimal()):
##            somma_costanti += int(token)
##        else:
##            dice = token.split("d")
##            dice_type = int(dice[1])
##            dice_number = 1
##            if (dice[0] != ""):
##                dice_number = int(dice[0])
##            stringa += "Tirando "+str(dice_number)+" volte un D"+str(dice_type)+" ho ottenuto:\n"
##            for _ in range(dice_number):
##                dice_roll = randint(1, dice_type)
##                stringa += "- "+str(dice_roll)+"\n"
##                somma_dadi += dice_roll
##    stringa += "Totale: "+str(somma_dadi)
##    if (somma_costanti > 0):
##        stringa += " + "+str(somma_costanti)+" -> "+str(somma_dadi + somma_costanti)
##    if speech: invia_voce(chat["id"],stringa)
##    else: invia_testo(chat["id"],stringa)

    parametri = comando.lower().strip().split(" ")
    comando.pop(0)
    somma_dadi = 0
    somma_costanti = 0
    stringa = "@"+str(mittente_username)+"\n"
    for token in parametri:
        print("token: ", token)
        if (token.isdecimal()):
            print("identified as constant")
            somma_costanti += int(token)
        else:
            print("identified as dice")
            dice = token.split("d")
            print("dice: ", dice)
            dice_type = int(dice[1])
            dice_number = 1
            print("dice_type: ", dice_type)
            print("dice_number: ", dice_number)
            if (dice[0] != ""):
                dice_number = int(dice[0])
            stringa += "Tirando "+str(dice_number)+" volte un D"+str(dice_type)+" ho ottenuto:\n"
            for _ in range(dice_number):
                dice_roll = randint(1, dice_type)
                stringa += "- "+str(dice_roll)+"\n"
                somma_dadi += dice_roll
    stringa += "Totale: "+str(somma_dadi)
    if (somma_costanti > 0):
        stringa += " + "+str(somma_costanti)+" -> "+str(somma_dadi + somma_costanti)
    if speech: invia_voce(chat["id"],stringa)
    else: invia_testo(chat["id"],stringa)
