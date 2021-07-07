In this program you can manage a chess tournament where u are able to :
1) Add player.
2) Create a new tournament.
3) Start a tournament.
4) Resume a tournament.
5) Generating reports.

How to run this program :

- copy the repository in https://github.com/isw120/P4
- if you need to create a virtual env use : Python -m venv env 
- to activate the virtual env use : .\env\Scripts\activate 

Install the requirements.txt needed :

- flake8==3.9.2
- flake8-html==0.4.1
- importlib-metadata==4.6.0
- Jinja2==3.0.1
- MarkupSafe==2.0.1
- mccabe==0.6.1
- pycodestyle==2.7.0
- pyflakes==2.3.1
- Pygments==2.9.0
- tinydb==4.4.0
- zipp==3.5.0

To generate flak8 report you use :
flake8 --format=html --htmldir=flake8_rapport --exclude=.\venv\