# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

class Stats:

    def __init__(self, attaque, magie, defense, mdefense, vitesse, mana, vie):
        stats = {
            "attaque": attaque,
            "magie": magie,
            "defense": defense,
            "mdefense": mdefense,
            "vitesse": vitesse,
            "mana": mana,
            "vie": vie
        }

        for name, value in stats.items():
            if type(value) == int and value > 0:
                setattr(self, name, value)
            else:
                raise ValueError(f"Type ou valeur de {name} incorrecte")

        self.status = "Alive"

    def getAtq(self):
        return self.attaque

    def getmag(self):
        return self.magie

    def getdef(self):
        return self.defense

    def getmdef(self):
        return self.mdefense

    def getvit(self):
        return self.vitesse

    def getmana(self):
        return self.mana

    def getvie(self):
        return self.vie

class Classe:
    def __init__(self,stats,nom):
        self.stats = stats
        self.nom = nom

    def getstats(self):
        return self.stats

class Localisation:
    def __init__(self, nom,listemasters,listeservants):
        pass

class Master:
    def __init__(self,nom,stats,nomservant):
        pass

class Servant:
    def __init__(self,nom,classe,stats,nommaster,personnalite,confiance):
        strings = {"nom": nom,
                   "nommaster": nommaster,
                   "personnalite": personnalite,
                   "confiance": confiance}
        if not isinstance(classe,Classe):
            raise TypeError("Type classe invalide")
        else:
            self.classe = classe

        if not isinstance(stats,Stats):
            raise TypeError("Type de stats invalide")
        else:
            self.stats = stats

        for nameArg,arg in strings.items():
            if isinstance(arg,str):
                setattr(self, nameArg, arg)
            else:
                raise TypeError(f"Type de {arg} invalide")

    def setFinalStats(self):
        for args in self.stats:
            newstat = args + self.classe.getstats()
