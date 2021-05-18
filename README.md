# GrandPy Bot (Chatbot)


[![Generic badge](https://img.shields.io/badge/<Pur_Beurre>-<0.1>-<065535>.svg)]()
[![version-python](https://img.shields.io/static/v1?label=Python&message=3.7&color=065535)]()
[![made-with-python](https://img.shields.io/badge/Made%20with-Django-1f425f.svg)]()
[![GitHub release](https://img.shields.io/github/release/Naereen/StrapDown.js.svg)](https://GitHub.com/Naereen/StrapDown.js/releases/)


--------------
# Détail du projet

La startup Pur Beurre, avec laquelle vous avez déjà travaillé, souhaite développer une plateforme web à destination de ses clients.  
Ce site permettra à quiconque de trouver un substitut sain à un aliment considéré comme "Trop gras, trop sucré, trop salé" (même si nous savons tous que le gras c’est la vie).

--------------
# Fonctionnalités

- Affichage du champ de recherche dès la page d’accueil
- La recherche ne doit pas s’effectuer en AJAX
- Interface responsive
- Authentification de l’utilisateur : création de compte en entrant un mail et un mot de passe, sans possibilité de changer son mot de passe pour le moment.

--------------
# Installation

Installation des dépendances

```
pip install -r requirements.txt
```

Création des variables d'environnment:
```

ENV = if product, ENV = PRODUCTION
DB_PWSD= password ur database (dev only)
SECRET_KEY = SECRET_KEY for Django App (only prod)
LIST_CATEGORIES = pizzas, fromages

```


--------------
# Manage command

manage.py insert_data_api -> recover data in api and insert into table 
manage.py delete_all_data_in_table -> Delete all data in table database

--------------
# Author

Développeur: Eddy Hubert

Contact: contact@eddy-hubert.fr
