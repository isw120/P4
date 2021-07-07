import sys
from controller import menu_controller


class Menu:
    controller = menu_controller.MenuController()

    def showMenu(self):
        print("Menu :")
        print("1) Ajouter un joueur")
        print("2) Créer un nouveau tournoi")
        print("3) Lancer un tournoi")
        print("4) Reprendre un tournoi")
        print("5) Générer des rapports")
        print("6) exit")
        self.chooseOption()

    def chooseOption(self):
        while True:
            option = input("Enter an option : " + "\n")
            if option == "1":
                self.controller.addingANewPlayer()
                self.showMenu()
            if option == "2":
                self.controller.createANewTournement()
                self.showMenu()
            if option == "3":
                self.controller.startingTournemant()
                self.showMenu()
            if option == "4":
                self.controller.continueTournement()
                self.showMenu()
            if option == "5":
                self.controller.creatReports()
                self.showMenu()
            if option == "6":
                print("You choosed to exit" + "\n")
                sys.exit()
            else:
                print("Wrong option" + "\n")
                self.showMenu()
