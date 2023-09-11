# Mode d'emploi : Template Dash 

# 1. Edition du portail 

## 1.1 Ajout d'une application 

Si l'on souhaite ajouter une nouvelle application au template, il suffit de : 
1. Créer un nouveau dossier « appN » à la racine de votre projet (N représentant le numéro de l’application) : à l'intérieur créer 2 fichiers : **layout.py** et **callbacks_appN.py**
2.	Remplir le fichier **list_app.csv** : celui-ci permet d'accéder aux informations relatives aux différentes applications. Ajouter une ligne à la suite des précédentes, et indiquer le titre de l'application, son url et l'icone qui la représentera sur la page d'accueil.
3.	Dans le fichier **layout.py** du dossier **appN**:
    1. Recopier cette section (et affecter à *n_app* le numéro associé à la nouvelle appli) : 
    ```python   
    ##Chargement fichier csv : pour gérer infos principales des différentes applis
    list_app = pd.read_csv("assets/list_app.csv", header=0, sep=';')
    n_app =  3 # numéro de l'appli
    ```

    2. Ajouter l'en-tête template : 
    ```python 
    dbc.Row([
        dbc.Col([   
            dbc.Navbar([
                    dbc.Col([dcc.Link(dbc.Button(html.Img(src=app.get_asset_url("accueil.png"),style={"height":"30px"}), id="bouton_accueil", style={'border':'2px solid white','margin-left':'-1vw'},color='white'), href = '/'),
                        html.Img(src=app.get_asset_url("logo_seenovate.png"), height="30px",style={'margin-left':'1vw'})],xs=2,sm=2,md=2,lg=2,xl=2),
                    dbc.Col([html.Div(dbc.NavbarBrand(list_app["name"].loc[list_app["ind"]==n_app].iloc[0], id="titre",className="text-white"),style={"textAlign":"center"})
                    ],xs=9,sm=9,md=9,lg=9,xl=9,align="center"),
                    dbc.Col([html.Div(html.Img(src=app.get_asset_url("user.png"), height="30px"))])
            ],color="dark")
        ],xs=12,sm=12,md=12,lg=12,xl=12)
    ]),  
    ```

    NB : l'ajout de ces lignes permet par ailleurs d'ajouter un bouton "accueil", qui redirige l'utilisateur à la page d'accueil. 

    Remplacer les images par les logos clients.

    
4.	Dans le fichier **layout.py** à la racine du projet :
    Si besoin, réajuster les *width* et *margin-left* entre les différentes *cards* (dans la partie *children*), afin que la liste des boutons renvoyant vers les applis sur la page d'accueil soit la plus agréable possible. Voir le fichier *BP_Python_Dash.docx* pour consulter les bonnes pratiques liées au caractère responsive d'une application Dash.

5.	Dans le **callbacks.py** à la racine du projet  : 
    1. Importer les éléments *layout_appN* : 
    ```python
    from app3.layout import layout_appN
    ```
    2.	dans la fonction *display_page*, ajouter les 2 lignes correspondant à la nouvelle application : 
    ```python
    elif pathname == '/appN':
	        content = layout_appN
    
    ``` 
    Cette fonction gère la redirection vers une des applications selon le choix de l'utilisateur sur le portail d'accueil.

6. Dans le fichier **index.py**, ajouter les lignes d'imports vers les nouveaux fichiers *layout* et *callbacks* :
```python
from app3 import layout, callbacks_app3
```

## 1.2. Pour supprimer une application

1. Dans le fichier *list_app.csv*, supprimer la ligne correspondante.

2. Supprimer tous les fichiers compris dans le dossier *appN*, ainsi que le dossier associé. 

3. Supprimer tous les imports des fichiers *layout* et *callbacks* à la racine. 
 


## 1.3. Pour changer l'apparence du favicon 

Pour changer le favicon (icône représentant l'application sur la barre d'onglets du navigateur web), il faut se rendre dans le fichier **app.py** :

```python
app.title = "Seenovate Dash App"
app._favicon = "logo_favicon.ico"
```
On peut alors modifier le titre ainsi que le logo de l'application, stocké dans le dossier *assets*.


## 1.4. Pour ajouter une authentification par mot de passe 

Si l'on souhaite restreindre l'accès à l'application à un certain nombre d'invididus, il suffit d'ajouter les lignes suivantes (et ajouter les couples ID/MDP correspondant) dans le fichier *index.py* : 

```python
VALID_USERNAME_PASSWORD_PAIRS = {
    'template': 'Seenovate1234' ,
 
}
 
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
```

Autre alternative adoptée dans certains projets : **keycloack** (permet d'affecter à un utilisateur un groupe, et de lui proposer un contenu associé).


# 2. Les applications du Template :

1. Application 1 : Sidebar par onglet

Une application composée de plusieurs onglets, dans laquelle on retrouve divers graphiques *Plotly* usuels. A gauche, une sidebar pour chaque onglet qui permet de filtrer / sélectionner les données à afficher.

2. Application 2 : Sidebar commune à tous les onglets

Assez similaire à la première application, celle-ci propose néanmoins une sidebar commune, qui permet à l'utilisateur de filtrer les données une fois pour tous les onglets.

3. Application 3 : Formulaire de saisie 

Cette application est dédiée à la création de formulaires de saisies "statiques" : on renseigne une liste de champs et on l'enregistre dans une base de données.
Dans cette application, nous avons ajouté un *dbc.Modal* permettant de faire afficher le formulaire à l'intérieur d'une pop-up. Ceci est régulièrement utilisé pour les applications Dash Plotly. On retrouvera alors le callbacks permettant de gérer l'ouverture du Modal dans le fichier *callbacks_app3.py*. Enfin, on écrit les formulaires de saisie dans des objets *dc.Form*, qui sont dédiés à ce besoin, et permettent de gérer divers aspects (contrôle des champs obligatoires, bouton de validation du formulaire, design, ...).


## Autres fichiers du Template

1. Le fichier **colors.py** : dans ce fichier, on stocke les couleurs que l'on va utiliser dans le Template, en renseignant leur code couleur hexadécimal associé. Ceci a l'avantage d'éviter de rappeler le code couleur à l'intérieur de chaque fichier, et de créer des dictionnaires de couleurs "Corporate".

2. Le fichier **sheet.css** (dans le dossier *assets*) : celui-ci permet de gérer la partie CSS de l'application. Par exemple, on peut créer des classes d'objets (par exemple une classe "label_dropdowns" pour gérer le style de tous les noms de listes déroulantes).  

3. Le fichier **sql_utils.py** (dans le dossier *src*) : nous avons recensé des fonctions fréquemment utilisées pour travailler avec une base de données SQL (type PostgreSQL ici).

4. Le fichier **fonctions.py** (dans le dossier *src*) : Lorsqu’un bout de code est répété plusieurs fois faire une fonction. Cela permet de diminuer la longueur du code et de le rendre plus lisible. Mais surtout cela rend l’application plus maintenable et homogène.


## Conseils de développement 

Si vous travaillez avec plusieurs objets voués à effectuer la même action (ex : des Dropdowns que l'on souhaite tous afficher selon une même condition, ou un indicateur rouge ou vert à faire afficher pour chaque input), il est utile d'utiliser les composantes MATCH et ALL de Dash. Celles-ci permettent d'affecter un type d'id à chacun de nos objets (ex : dbc.Dropdown,dbc.Input, etc) et de contrôler l'affichage de tous les objets d'un même type dans le même callbacks.
Ces aspects sont détaillés sur le lien suivant : https://dash.plotly.com/pattern-matching-callbacks
