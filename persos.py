# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

class Stats:
    def __init__(self,attaque,magie,defense,mdefense,vitesse,mana,vie):
        if type(attaque) == int and attaque > 0:
            self.attaque = attaque
        if type(magie) == int and magie> 0:
            self.magie = magie
        if type(mdefense) == int and mdefense > 0:
            self.mdefense = mdefense
        if type(defense) == int and defense > 0:
            self.defense = defense
        if type(vitesse) == int and vitesse > 0:
            self.vitesse = vitesse
        if type(mana) == int and mana > 0:
            self.mana = mana
        if type(vie) == int and vie > 0:
            self.vie = vie
        self.status = "Alive"

class Classe:
    def __init__(self,stats,nom):
        self.stats = stats
        self.nom = nom

class Location:
    def __init__(self, nom,listemasters,listeservants):
        pass

class Master:
    def __init__(self,nom,stats,nomservant):
        pass

class Servant:
    def __init__(self,nom,classe,stats,nommaster,personnalite,confiance):
        pass


