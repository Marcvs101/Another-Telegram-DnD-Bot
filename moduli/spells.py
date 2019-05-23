from strutture.messaggio import Messaggio
from os import path, getcwd
from moduli.moduli_spells.spells import SpellFinder

def spells(mittente, comando, chat, dati, speech, logfile):
    messaggi = []
    if (chat["type"]!="private"):
        messaggi.append(Messaggio("@"+str(mittente["username"])+", il menù del giocatore può essere acceduto solo nelle conversazioni private",chat["id"],speech))
        messaggi.append(Messaggio("@"+str(mittente["username"])+", i comandi possono essere inviati qui",mittente["id"],speech))
    else:
        token = comando.split()
        help_required = False
        if (len(token) == 0):
            help_required = True
        else:
            f_spells = path.join(getcwd(), "moduli", "moduli_spells", "spells.txt")
            f_classes = path.join(getcwd(), "moduli", "moduli_spells", "classes.txt")
            finder = SpellFinder(f_spells, f_classes)
            if (token[0].strip() == "find"):
                spell_name = " ".join(token[1:])
                info = finder.getSpellDescription(spell_name)
                messaggi.append(Messaggio(info,chat["id"],speech))
            elif (token[0].strip() == "list"):
                option = token[1].strip().lower()
                if (option == "all"):
                    response = finder.getSpellsByClass(project=["name", "level"], sortby="level")
                    s = ""
                    for class_name in response:
                        s+=class_name+":\n"
                        for spell in response[class_name]:
                            s += spell["name"]+" ("+spell["level"]+")\n"
                    messaggi.append(Messaggio(s,chat["id"],speech))
                else:
                    response = finder.getSpellsByClass(class_name=option.capitalize(), project=["name", "level"], sortby="level")
                    s = ""
                    for spell in response[option.capitalize()]:
                        s += spell["name"]+" ("+spell["level"]+")\n"
                    messaggi.append(Messaggio(s,chat["id"],speech))
            else:
                help_required = True
        if (help_required):
            s = "/spells find spell_name: Guarda la descrizione della spell"
            messaggi.append(Messaggio(s,chat["id"],speech))
    return messaggi
