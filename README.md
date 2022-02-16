# Clavitor

# Description :

Mini projet perso de logiciel comptabilisant les entrées clavier et souris, dans le but de faire des statistiques.\
Génère un fichier data.txt exploitable avec pyplot pour générer des graphiques.

Interface graphique sommaire (à améliorer) qui renseigne :
- Le nombre de touches clavier+souris tapées au total.
- Un menu déroulant permettant de choisir le graphique de statistique à afficher.

# Dépendances :

- Tkinter
- pynput
- pyplot
- PIL

# Fonctionnalités :

- Comptabilise toutes les entrées clavier + souris et enregistre dans un fichier data.txt
- Graphiques pyplot :
    1. Camembert des 5 entrées les plus utilisée            --->    OK
    2. Diagramme en bâton des 5 entrées les plus utilisée   --->    OK
    3. Diagramme en bâton de toutes les entrées             --->    PAS OK
    4. Fréquence de frappe                                  --->    PAS OK
    6. Temps moyen entre deux touches                       --->    PAS OK

# Exporter en .exe :

Pour générer clavitor.exe adapté à windows :\
pyinstaller --noconfirm --onefile --windowed --hidden-import "pynput.keyboard._win32" --hidden-import "pynput.mouse._win32" --hidden-import="matplotlib.pyplot" clavitor.py