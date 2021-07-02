class Joueur:

    def __init__(self, Nom_de_famille, Prenom, Date_de_naissance, Sexe, Classement):
        self.Nom_de_famille = Nom_de_famille
        self.Prenom = Prenom
        self.Date_de_naissance = Date_de_naissance
        self.Sexe = Sexe
        self.Classement = Classement

    def __str__(self):
        return 'Nom_de_famille : ' + self.Nom_de_famille + '\n' + 'Prénom : ' + self.Prenom + '\n' + 'Date_de_naissance : ' + self.Date_de_naissance + '\n' + 'Sexe : ' + self.Sexe + '\n' + 'Classement : ' + str(self.Classement) + '\n'