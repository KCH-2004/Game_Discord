from __future__ import annotations
from enum import Enum
from dataclasses import dataclass
import copy


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

    def trahison(self):
        return NiveauConfiance.NULLE

@dataclass
class Personnalite:
    trait: str
    multiplicateur_trahison: float

@dataclass
class Ressource:
    vie:int
    mana:int

    def __iadd__(self, ressource:Ressource):
        self.vie += ressource.vie
        self.mana += ressource.mana
        return self

@dataclass
class Stats:
    attaque: int
    magie: int
    defense: int
    mdefense: int
    vitesse: int

    def __iadd__(self, otherstats:Stats):
        self.attaque += otherstats.attaque
        self.magie += otherstats.magie
        self.defense += otherstats.defense
        self.mdefense += otherstats.mdefense
        self.vitesse += otherstats.vitesse
        return self

@dataclass
class Classe:
    stats: Stats
    ressourcesmax: Ressource
    nom: str

@dataclass
class NobleFantasm:
    nom:str
    proprietaire:Servant


@dataclass
class Participants:
    nom: str
    stats: Stats
    ressourcesmax: Ressource
    ressourcesactuel: Ressource
    encombat: bool
    statut:str
    def mourir(self):
        self.ressourcesactuel.vie = 0
        self.statut = "Mort"
        self.encombat = False

    def consommermana(self,montant:int):
        if self.ressourcesactuel.mana >= montant:
            self.ressourcesactuel.mana -= montant
        else:
            raise ArithmeticError("Le mana actuel est insuffisant")

    def initressources(self):
        self.ressourcesactuel = copy.copy(self.ressourcesmax)

@dataclass
class Master(Participants):
    sceauxrestant: int
    servant:Servant = None

    def mourir(self):
        super().mourir()
        self.servant.master = None
        self.servant.statut = "En train de disparaitre"
        if self.servant.classe.nom == "Archer":
            self.servant.touravantdisparition = 4
        else:
            self.servant.touravantdisparition = 2

    def lierservant(self,servant:Servant):
        servant.master = self
        self.servant = servant
        self.sceauxrestant = 3
        self.servant.confiance = NiveauConfiance.MOYENNE
        self.servant.statut = "Vie"


@dataclass
class Servant(Participants):
    classe:Classe
    personnalite:Personnalite
    confiance:NiveauConfiance
    noblefantasm:NobleFantasm
    sexe:str
    master: Master = None
    touravantdisparition:int = None

    def initfinalstats(self):
        self.stats += self.classe.stats
        self.ressourcesmax += self.classe.ressourcesmax
        self.initressources()

    def mourir(self):
        super().mourir()
        self.master.servant = None

    def consommermana(self,montant:int):
        if self.master is not None and self.master.ressourcesactuel.mana >= montant:
            self.master.ressourcesactuel.mana -= montant
            return "Le mana du master a été consommé"
        elif self.master is not None and self.master.ressourcesactuel.mana < montant:
            return "impossible d'attaquer: le mana du master est insuffisant"
        elif self.ressourcesactuel.mana >= montant:
            self.ressourcesactuel.mana -= montant
            return "Le mana du servant a été consommé"
        else:
            return "Le mana actuel est insuffisant"

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
        super().__init__(initiateur)
        self.cible = cible


class AttaquePhysique(Attaque):
    pass

class AttaqueMagique(Attaque):
    pass

class AttaqueNobleFantasm(Attaque):
    pass

class Scout(Action):
    def __init__(self,initiateur:Participants):
        pass

class Sacrifice(Action):
    def __init__(self,initiateur:Participants):
        pass

class Retraite(Action):
    def __init__(self,initiateur:Participants):
        pass

class Suicide(Action):
    def __init__(self,initiateur:Master,cible:Servant):
        super().__init__(initiateur)
        self.cible = cible

    def executer(self,carte:Carte):
        if self.initiateur.sceauxrestant <= 0:
            self.cible.confiance = self.cible.confiance.trahison()
            return ("L'ordre a échoué, vous n'avez plus de sceaux.\n"
                    "Ayant trahi votre servant ce dernier ne vous fait plus confiance")
        else:
            self.initiateur.sceauxrestant -= 1
            self.cible.mourir()
            if self.cible.sexe == "H":
                return f"Par la puissance absolue du sceau:{self.cible.nom} s'est suicidé"
            else:
                return f"Par la puissance absolue du sceau:{self.cible.nom} s'est suicidée"