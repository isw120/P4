import sys
from controller import menu_controller

class Menu:

    controller = menu_controller.MenuController()

    def showMenu(self):
        print("Menu :")
        print("1) Créer un nouveau tournoi")
        print("2) Lancer un tournoi")
        print("3) Ajouter un joueur")
        print("4) Générer des rapports")
        print("5) exit")
        self.chooseOption()

    def chooseOption(self):
        while (True):
            option = input("Enter an option:")
            if (option == "1"):
                print("You choosed option 01")
                self.controller.createANewTournement()
                self.showMenu()
            if (option == "3"):
                print("you choosed option 03")
                self.controller.addingNewPlayers()
                self.showMenu()
            if (option == "2"):
                print("you choosed option 02")
                self.controller.startingTournemant()
                self.showMenu()
            if (option == "4"):
                print("you choosed option 04")
                self.controller.creatReports()
                self.showMenu()

            else:
                print("You choosed to exit")
                sys.exit()