from enum import Enum
from dataclasses import dataclass


class NiveauConfiance(Enum):
    #Pourcentage de trahison selon la confiance (modifié selon la personnalité du servant)
    ABSOLUE = 0
    HAUTE = 5
    MOYENNE = 30
    BASSE = 75
    NULLE = 100

    def augmenterConfiance(self):
        confiance = list(NiveauConfiance)
        niveau_confiance_servant = confiance.index(self)

        if not niveau_confiance_servant == 0:
            return confiance[niveau_confiance_servant - 1]
        else:
            return NiveauConfiance.ABSOLUE

    def baisserConfiance(self):
        confiance = list(NiveauConfiance)
        niveau_confiance_servant = confiance.index(self)

        if not niveau_confiance_servant == 4:
            return confiance[niveau_confiance_servant + 1]
        else:
            return NiveauConfiance.NULLE

@dataclass
class Personnalite:
    trait: str
    multiplicateur_trahison: float

@dataclass
class Stats:
    attaque: int
    magie: int
    defense: int
    mdefense: int
    vitesse: int
    mana: int
    vie: int

    def __iadd__(self, otherstats):
        if not isinstance(otherstats, Stats):
            raise TypeError("Type de Otherstats invalide\n"
                            "class: Stats")

        self.attaque += otherstats.attaque
        self.magie += otherstats.magie
        self.defense += otherstats.defense
        self.mdefense += otherstats.mdefense
        self.vitesse += otherstats.vitesse
        self.mana += otherstats.mana
        self.vie += otherstats.vie

        return self

@dataclass
class Classe:
    stats: Stats
    nom: str

@dataclass
class Participants:
    nom: str
    stats: Stats
    sceauxrestant: int
    encombat: bool
    statut:str

@dataclass
class Master(Participants):
    nomservant: str

@dataclass
class Servant(Participants):
    classe:Classe
    nommaster:str
    personnalite:Personnalite
    confiance:NiveauConfiance
    noblefantasm:str

    def setfinalstats(self):
        self.stats += self.classe.stats

class Carte:

    def __init__(self, listelocalisation:list,dictlocalisationmaster:dict,dictlocalisationservant:dict):
        if not all(isinstance(l, str) for l in listelocalisation):
            raise TypeError("Erreur de Localisation dans la Carte.")
        else:
            self.listelocalisation = listelocalisation

        if not all(isinstance(m,Master) and isinstance(l,str) for m,l in dictlocalisationmaster.items()):
            raise TypeError("Erreur de Localisation des Master dans la Carte.")
        else:
            self.dictlocalisationmaster = dictlocalisationmaster

        if not all(isinstance(s,Servant) and isinstance(l,str) for s,l in dictlocalisationservant.items()):
            raise TypeError("Erreur de Localisation des Servant dans la Carte.")
        else:
            self.dictlocalisationservant = dictlocalisationservant

    def deplacermaster(self,master,nouvellelocalisation):
        for l in self.listelocalisation:
            if nouvellelocalisation == l:
                self.dictlocalisationmaster[master] = l
                return
        raise TypeError(f"Erreur de deplacement Master {master} sur la Carte")

    def deplacerservant(self,servant,nouvellelocalisation):
        for l in self.listelocalisation:
            if nouvellelocalisation == l:
                self.dictlocalisationservant[servant] = l
                return
        raise TypeError(f"Erreur de deplacement Servant {servant} sur la Carte")


class Action:

    def __init__(self, initiateur:Participants):
        self.initiateur = initiateur
        self.priorite = 0

    def executer(self, carte:Carte):
        raise NotImplementedError("Cette action n'a pas de logique d'exécution")

class Attaque(Action):
    def __init__(self,initiateur:Participants,cible:Participants):
        pass

class Scout(Action):
    def __init__(self,initiateur:Participants):
        pass

class Ultime(Action):
    def __init__(self,initiateur:Participants):
        pass

class Sacrifice(Action):
    def __init__(self,initiateur:Participants):
        pass

class Retraite(Action):
    def __init__(self,initiateur:Participants):
        pass

class OrdreAbsolue(Action):
    def __init__(self,initiateur:Master,cible:Servant,ordre:str):
        super().__init__(initiateur)
        self.cible = cible
        self.ordre = ordre

    def executer(self,carte:Carte):
        if self.initiateur.sceauxrestant <= 0:
            return False

        self.initiateur.sceauxrestant -= 1
        self.cible.confiance = self.cible.confiance.baisserConfiance()
        return True

class Suicide(OrdreAbsolue):
    def __init__(self,initiateur:Master,cible:Servant):
        super().__init__(initiateur,cible)


    def executer(self, carte:Carte):
        pass