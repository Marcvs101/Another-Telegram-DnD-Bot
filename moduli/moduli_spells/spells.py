import requests
import json
from os import path, getcwd
from bs4 import BeautifulSoup

class SpellFinder():
    def __init__(self, path_spells, path_classes):
        self.filename_spells = path_spells
        self.filename_classes = path_classes
        self.site = "https://dd-5e-italiano.fandom.com"
        if (path.exists(self.filename_spells) and path.exists(self.filename_classes)):
            self.spells = self.__loadSpells__()
            self.classes_spells = self.__loadSpellsByClass__()
            return None
        self.spells = []
        self.classes_spells = {"Bardo": [], "Chierico": [], "Druido": [],
                          "Mago": [], "Paladino": [], "Ranger": [],
                          "Stregone": [], "Warlock": []}
        classes = list(self.classes_spells.keys())
        visited_spells = set()
        for class_name in classes:
            result = requests.get(self.site+"/it/wiki/Incantesimi_da_"+class_name)
            content = result.content
            soup = BeautifulSoup(content, "html.parser")
            samples = soup.find("table").find_all("tr")
            for i in range(1, len(samples)):
                elements = samples[i].find_all("td")
                temp_link = elements[0].find("a", href=True)
                if (temp_link == None):
                    continue
                link = temp_link["href"].strip()
                name = elements[0].text.strip()
                school = elements[1].text.strip()
                level = elements[2].text.strip()
                casting_time = elements[3].text.strip()
                saving_throw = elements[4].text.strip()
                ritual = elements[5].text.strip()
                if (len(elements) > 6):
                    concentration = elements[6].text.strip()
                else:
                    concentration = ""
                spell = {"name": name, "link": link, "school": school,
                         "level": level, "casting_time": casting_time, "saving_throw": saving_throw,
                         "ritual": ritual != "", "concentration": concentration != ""}
                if (name not in visited_spells):      
                    self.spells.append(spell)
                    visited_spells.add(name)
                self.classes_spells[class_name].append(spell)
        f_spells = open(self.filename_spells, "w", encoding="utf-8")
        f_classes = open(self.filename_classes, "w", encoding="utf-8")
        f_spells.write(json.dumps(self.spells))
        f_classes.write(json.dumps(self.classes_spells))
        f_spells.close()
        f_classes.close()

    def __loadSpellsByClass__(self):
        f = open(self.filename_classes, "r")
        spells = json.loads(f.read())
        f.close()
        return spells

    def __loadSpells__(self):
        f = open(self.filename_spells, "r")
        spells = json.loads(f.read())
        f.close()
        return spells

    def getSpellsList(self, project=["name", "link", "school", "level", "casting_time", "saving_throw", "ritual", "concentration"], sortby=None):
        if (sortby not in project):
            raise ValueError("Sorting by an attribute outside the projection is not allowed")
        new_list = []
        for elem in self.spells:
            new_list.append({k:elem[k] for k in project})
        if (sortby != None):
            new_list.sort(key=lambda x: x[sortby])
        return new_list

    def getSpellsByClass(self, class_name=None, project=["name", "link", "school", "level", "casting_time", "saving_throw", "ritual", "concentration"] , sortby=None):
        if (sortby not in project):
            raise ValueError("Sorting by an attribute outside the projection is not allowed")
        if (class_name != None and class_name not in self.classes_spells.keys()):
            raise ValueError("Class 'class_name' not found")
        new_dict= {}
        for class_name_key in self.classes_spells:
            if (class_name != None and class_name_key != class_name):
                continue
            new_dict[class_name_key] = []
            for spell in self.classes_spells[class_name_key]:
                new_dict[class_name_key].append({k: spell[k] for k in project})
            if (sortby != None):
                new_dict[class_name_key].sort(key=lambda x: x[sortby])
        return new_dict

    
    def getSpellInformations(self, spell_name):
        spell = next((item for item in self.spells if item["name"].lower() == spell_name.lower()), None)
        if (spell == None):
            raise ValueError("Spell '"+spell_name+"' is not in the dataset")
        return spell

    def getSpellDescription(self, spell_name):
        spell_link = self.getSpellInformations(spell_name)["link"]
        site = "https://dd-5e-italiano.fandom.com"
        result = requests.get(site+spell_link)
        soup = BeautifulSoup(result.content, "html.parser")
        div = soup.find("div", {"id": "mw-content-text"})
        return spell_name.capitalize()+"\n"+div.text.strip()

