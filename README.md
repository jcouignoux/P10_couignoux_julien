# P10_couignoux_julien

![](docs/logo.png)

# SoftDesk-API: API permettant le suivi des problèmes techniques.

SoftDesk, une société d'édition de logiciels de développement et de collaboration, a décidé de publier une application permettant de remonter et suivre des problèmes techniques (issue tracking system). Cette solution s’adresse à des entreprises clientes, en B2B.

## Installation

Cette API exécutable localement peut être installée en suivant les étapes décrites ci-dessous. L'usage de pipenv est recommandé, mais des instuctions utilisant venv et pip sont également fournies plus bas. Si pipenv n'est pas encore installé sur votre ordinateur, vous trouverez des instuctions d'installation détaillées [sur cette page](docs/pipenv/installation-fr.md).

### Installation et exécution de l'application avec pipenv

1. Cloner ce dépôt de code à l'aide de la commande `$ git clone clone https://github.com/OpenClassrooms-Student-Center/OCMovies-API-EN-FR.git` (vous pouvez également télécharger le code [en temps qu'archive zip](https://github.com/OpenClassrooms-Student-Center/OCMovies-API-EN-FR/archive/refs/heads/master.zip))
2. Rendez-vous depuis un terminal à la racine du répertoire ocmovies-api-fr avec la commande `$ cd ocmovies-api-fr`
3. Installez les dépendances du projet à l'aide de la commande `pipenv install` 
4. Créer et alimenter la base de données à l'aide de la commande `pipenv run python manage.py create_db`
5. Démarrer le serveur avec `pipenv run python manage.py runserver`

Lorsque le serveur fonctionne, après l'étape 5 de la procédure, l'API OCMovies peut être interrogée à partir des points d'entrée commençant par l'url de base [http://localhost:8000/api/v1/](http://localhost:8000/api/v1/). Le point d'entrée principal permettant de consulter les films est [http://localhost:8000/api/v1/titles](http://localhost:8000/api/v1/titles/). Si vous accédez à cette url depuis un navigateur,ce dernier vous présentera une interface naviguable servant de documentation et de laboratoire d'expériementation. Vous trouvez également une documentation plus formelle en bas de ce README.

Les étapes 1 à 4 ne sont requises que pout l'installation initiale. Pour les lancements ultérieurs du serveur de l'API, il suffit d'exécuter l'étape 5 à partir du répertoire racine du projet.

### Installation et exécution de l'application sans pipenv (avec venv et pip)

1. Cloner ce dépôt de code à l'aide de la commande `$ git clone clone https://github.com/OpenClassrooms-Student-Center/OCMovies-API-EN-FR.git` (vous pouvez également télécharger le code [en temps qu'archive zip](https://github.com/OpenClassrooms-Student-Center/OCMovies-API-EN-FR/archive/refs/heads/master.zip))
2. Rendez-vous depuis un terminal à la racine du répertoire ocmovies-api-fr avec la commande `$ cd ocmovies-api-fr`
3. Créer un environnement virtuel pour le projet avec `$ python -m venv env` sous windows ou `$ python3 -m venv env` sous macos ou linux.
4. Activez l'environnement virtuel avec `$ env\Scripts\activate` sous windows ou `$ source env/bin/activate` sous macos ou linux.
5. Installez les dépendances du projet avec la commande `$ pip install -r requirements.txt`
6. Créer et alimenter la base de données avec la commande `$ python manage.py create_db`
7. Démarrer le serveur avec `$ python manage.py runserver`

Lorsque le serveur fonctionne, après l'étape 7 de la procédure, l'API OCMovies peut être interrogée à partir des points d'entrée commençant par l'url de base [http://localhost:8000/api/v1/](http://localhost:8000/api/v1/). Le point d'entrée principal permettant de consulter les films est [http://localhost:8000/api/v1/titles](http://localhost:8000/api/v1/titles/). Si vous accédez à cette url depuis un navigateur,ce dernier vous présentera une interface naviguable servant de documentation et de laboratoire d'expériementation. Vous trouvez également une documentation plus formelle en bas de ce README.

Les étapes 1 à 6 ne sont requises que pout l'installation initiale. Pour les lancements ultérieurs du serveur de l'API, il suffit d'exécuter les étapes 4 et 7 à partir du répertoire racine du projet.

## Utilisation et documentation des points d'entrée

Une fois que vous avez lancé le serveur, vous pouvez lire la documentation depuis un navigateur web par le biais de l'interface navigable disponible ici [http://localhost:8000/api/v1/titles/](http://localhost:8000/api/v1/titles/). Cette interface naviguable vous sert à la fois de source de documentation et de laboratoire d'expérimentation. L'API actuelle ne fournit que les points d'entrées suivants. Tous ces points d'entrée sont en lecture seule et supportent exclusivement les requêtes HTTP utilisant la **méthode GET**: 

- Rechercher et filtrer des films: [http://localhost:8000/api/v1/titles/](http://localhost:8000/api/v1/titles/). Vous pouvez tester directement chaque filtre en accédant à l'URL ci-dessus depuis un navigateur web. Les filtres disponibles sont:

   - `year=<year>`, `min_year=<year>` ou `max_year=<year>` pour obtenir des films filtrés par années. Le premier de ces filtres réalise une correspondance exacte lors de la recherche.
   - `imdb_score_min=<score>` et `imdb_score_max<score>` pour obtenir des films avec un score imdb inférieurs ou supérieur à une note donnée.
   - `title=<title>` ou `title_contains=<string>` pour obtenir des films dont le titre correspond à la chaine de caractères recherchée. Le premier effectue une recherche avec une correspondance extacte tandis que le second recherche les titres contenant le terme recherché. La recherche est indédendante de la casse.
   - `director=<director-name>` ou `director_contains=<string>` pour obtenir des films dont un réalisateur correspond à la chaine de caractères recherchée. Le premier effectue une recherche avec une correspondance extacte tandis que le second filtre en fonction des réalisateurs contenant le terme recherché. La recherche est indédendante de la casse.
   - `writer=<name>` ou `writer_contains=<string>` pour obtenir des films dont un auteur correspond à la chaine de caractères recherchée. Le premier effectue une recherche avec une correspondance extacte tandis que le second filtre en fonction des auteurs contenant le terme recherché. La recherche est indédendante de la casse.
   - `actor=<name>` ou `actor_contains=<string>` pour obtenir des films dont un des acteurs correspond à la chaine de caractères recherchée. Le premier effectue une recherche avec une correspondance extacte tandis que le second recherche filtre en fonction des acteurs contenant le terme recherché. La recherche est indédendante de la casse.
   - `genre=<name>` ou `genre_contains=<string>` pour obtenir des films dont un genre correspond à la chaine de caractères recherchée. Le premier effectue une recherche avec une correspondance extacte tandis que le second filtre en fonction des genres contenant le terme recherché. La recherche est indédendante de la casse.
   - `country=<name>` ou `country_contains=<string>` pour obtenir des films dont un pays correspond à la chaine de caractères recherchée. Le premier effectue une recherche avec une correspondance extacte tandis que le second filtre en fonction des pays contenant le terme recherché. La recherche est indédendante de la casse.
   - `lang=<name>` ou `lang_contains=<string>` pour obtenir des films dont la langue correspond la chaine de caractères recherchée. Le premier effectue une recherche avec une correspondance extacte tandis que le second filtre en fonction des langues contenant le terme recherché. La recherche est indédendante de la casse.
   - `company=<name>` ou `company_contains=<string>` pour obtenir des films dont la compagnie de production correspond à la chaine de caractères recherchée. Le premier effectue une recherche avec une correspondance extacte tandis que le second filtre en fonction des compagnies contenant le terme recherché. La recherche est indédendante de la casse.
   - `rating=<name>` ou `rating_contains=<string>` pour obtenir des films dont le politique de restriction correspond à la chaine de caractères recherchée. Le premier effectue une recherche avec une correspondance extacte tandis que le second filtre en fonction des restrictions contenant le terme recherché. La recherche est indédendante de la casse.
   - `sort_by=<field>` pour obtenir des films triés selon un ordre particulier. Par exemple, utiliser `sort_by=title` pour trier les films selon l'ordre alphabétique de teur titre et `sort_by=-title` pour trier les films dans le sens inverse. Il est également possible de trier par critères multiples en séparant les critères par des virgules comme dans `sort_by=-year,title` qui affiche d'abord les films les plus récents, puis trie les films de la même années par ordre alphabétique.

- Demander des informations détaillées sur un film dont on connait l'identifiant: [http://localhost:8000/api/v1/titles/499549](http://localhost:8000/api/v1/titles/499549) où 499549 est l'identifiant (`id`) du film "Avatar".
- Rechercher les genres disponibles: [http://localhost:8000/api/v1/genres/](http://localhost:8000/api/v1/genres/). Les filtres disponibles sont:
   - `name_contains=<search string>` pour n'afficher que les genres dont la nom contient la chaine de caractère recherchée.
   - `movie_title_contains=<search string>` pour rechercher les genres associés à film dont le titre contient la chaine de caractère recherchée.
   a particular movie searched by title.
