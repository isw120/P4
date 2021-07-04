from tinydb import TinyDB, Query, where


class DatabaseController:

    def insertPlayer(self, joueur):
        serialized_player = {
            'Nom_de_famille': joueur.Nom_de_famille,
            'Prenom': joueur.Prenom,
            'Date_de_naissance': joueur.Date_de_naissance,
            'Sexe': joueur.Sexe,
            'Classement': joueur.Classement
        }

        db = TinyDB('db.json')

        players = db.table('players')
        players.insert(serialized_player)

    def getAllPlayers(self):
        db = TinyDB('db.json')
        players = db.table('players')
        serialized_players = players.all()
        return serialized_players

    def insertTournement(self, tournoi):
        serialized_tournement = {
            'Nom': tournoi.Nom,
            'Lieu': tournoi.Lieu,
            'Date': tournoi.Date,
            'Nombre_de_tours': tournoi.Nombre_de_tours,
            'Tournees': tournoi.Tournees,
            'Joueurs': tournoi.Joueurs,
            'Controle_du_temps': tournoi.Controle_du_temps,
            'Description': tournoi.Description,
            'status': tournoi.status,
            'secondRoundPlayers': tournoi.secondRoundPlayers,
            'thirdRoundPlayers': tournoi.thirdRoundPlayers
        }

        db = TinyDB('db.json')

        tournements = db.table('tournements')
        tournements.insert(serialized_tournement)

    def getAPlayer(self, family_name, name):
        db = TinyDB('db.json')
        players = db.table('players')
        serialized_player = players.get(Query()['Nom_de_famille'] == family_name and Query()['Prenom'] == name)
        return serialized_player

    def getTournementByName(self, tournement_name):
        db = TinyDB('db.json')
        tournement = db.table('tournements')
        serialized_tournement = tournement.get(Query()['Nom'] == tournement_name)
        return serialized_tournement

    def updateTournementByName(self, tournoi):
        db = TinyDB('db.json')
        tournement = db.table('tournements')
        tournement.update({'Joueurs': tournoi.Joueurs, 'Tournees': tournoi.Tournees, 'status': tournoi.status,
                           'secondRoundPlayers': tournoi.secondRoundPlayers,
                           'thirdRoundPlayers': tournoi.thirdRoundPlayers}, where('Nom') == tournoi.Nom)

    def getAllTournements(self):
        db = TinyDB('db.json')
        tournement = db.table('tournements')
        serialized_tournement = tournement.all()
        return serialized_tournement
