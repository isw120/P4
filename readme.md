In this program you can manage a chess tournament where u are able to :
1) Add player.
2) Create a new tournament.
3) Start a tournament.
4) Restart a tournament.
5) Generating reports.

How to run this program :

- copy the repository in https://github.com/isw120/P4
- if you need to create a virtual env use : Python -m venv env 
- to activate the virtual env use : .\env\Scripts\activate 
- Install the requirements.txt needed with this command :

$ pip install -r requirements.txt

To generate flak8 report you use :
flake8 --format=html --htmldir=flake8_rapport --exclude=.\venv\ --max-line-length=119