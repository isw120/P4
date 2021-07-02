class Tournoi:
    def __init__(self, Nom, Lieu, Date, Nombre_de_tours, Tournees, Joueurs, Controle_du_temps, Description, status, secondRoundPlayers, thirdRoundPlayers):
        self.Nom = Nom
        self.Lieu = Lieu
        self.Date = Date
        self.Nombre_de_tours = Nombre_de_tours
        self.Tournees = Tournees
        self.Joueurs = Joueurs
        self.Controle_du_temps = Controle_du_temps
        self.Description = Description
        self.status = status
        self.secondRoundPlayers = secondRoundPlayers
        self.thirdRoundPlayers = thirdRoundPlayers


    def __str__(self):
        return 'Nom : ' + self.Nom + '\n' + 'Lieu : ' + self.Lieu + '\n' + 'Date : ' + self.Date + '\n'+ 'Nombre_de_tours : ' + str(self.Nombre_de_tours) + '\n' + 'Tournées : ' + str(self.Tournees) + '\n' + 'Joueurs : ' + str(self.Joueurs) + '\n' + 'Contrôle_du_temps : ' + self.Controle_du_temps + '\n' + 'Description : ' + self.Description + '\n'