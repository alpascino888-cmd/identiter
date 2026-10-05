# Groupe Omega et Partenaires

Site vitrine en français construit avec Django. Il comprend une page d’accueil, un carrousel illustré des six domaines d’activité, une page de présentation et un formulaire de contact.

## Exécution en local

Prérequis : Python 3.12 ou plus récent.

```bash
python3 -m venv .venv
source .venv/bin/activate       # Windows : .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # Windows : copy .env.example .env
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copiez la clé générée dans `DJANGO_SECRET_KEY` du fichier `.env`, puis :

```bash
python manage.py migrate
python manage.py runserver
```

Ouvrez <http://127.0.0.1:8000/>.

La base de données locale est `db.sqlite3`. Elle est exclue de Git ; conservez-en une copie de sauvegarde avant toute opération qui pourrait la modifier.

## Déploiement gratuit sur Render

Le fichier [`render.yaml`](./render.yaml) décrit le service web Render : il installe les dépendances, collecte les fichiers statiques, applique les migrations au démarrage et lance Gunicorn. La configuration crée la clé secrète dans Render et désactive le mode debug en production.

1. Placez ce projet dans un dépôt Git accessible par votre compte Render. Ne publiez jamais `.env`, `db.sqlite3`, une sauvegarde de base ou une vraie clé secrète.
2. Dans Render, choisissez **New + → Blueprint**, reliez le dépôt et validez la création du service `groupe-omega-site` à partir de `render.yaml`.
3. Attendez la fin du build et du déploiement, puis ouvrez l’URL `onrender.com` affichée par Render. Le contrôle de santé utilise `/`.
4. Si vous utilisez un domaine personnalisé, ajoutez-le à `ALLOWED_HOSTS` et son origine `https://...` à `CSRF_TRUSTED_ORIGINS` dans les variables d’environnement Render.

Variables configurées automatiquement par le Blueprint :

| Variable | Rôle |
| --- | --- |
| `DJANGO_SECRET_KEY` | Clé secrète générée par Render ; ne pas la publier ni la remplacer par une valeur partagée. |
| `DEBUG` | Doit rester à `False` en production. |
| `RENDER_EXTERNAL_HOSTNAME` | Nom d’hôte Render, utilisé automatiquement pour les hôtes autorisés et CSRF. |

Les requêtes HTTP sont redirigées vers HTTPS. Les cookies de session et CSRF sont réservés à HTTPS ; HSTS est activé pour un an. Render termine TLS sur son proxy et fournit l’en-tête de protocole utilisé par Django.

La typographie Manrope est hébergée dans `static/fonts/` (avec sa licence OFL). Le bandeau d’accueil présente un carrousel plein écran de six photos locales, une par domaine ; il avance automatiquement toutes les 5 secondes, se commande par ses indicateurs et se met en pause au survol, au focus clavier ou lorsque le visiteur préfère réduire les animations. Les six cartes des activités restent affichées en grille sous le bandeau. Les photos proviennent d’Unsplash et sont utilisées conformément à sa [licence](https://unsplash.com/license) ; les illustrations SVG complémentaires sont dans `static/img/services/`.

### Limite importante : SQLite et l’offre gratuite

Render précise que les instances gratuites sont destinées aux tests et projets personnels, pas aux applications de production. Le service se met en veille après 15 minutes sans trafic et son système de fichiers est éphémère. **La base SQLite peut être perdue lors d’une mise en veille, d’un redéploiement, d’un redémarrage ou du remplacement de l’instance.** Elle ne convient donc qu’à une démonstration sans données à conserver. Une variable `DATABASE_PATH` peut déplacer le fichier, mais ne rend pas le stockage persistant ; les disques persistants Render sont réservés aux services payants.

Avant de stocker des données importantes ou de prendre des demandes clients, choisissez un stockage persistant et prévoyez des sauvegardes. SQLite ne doit pas être partagé entre plusieurs instances web. Consultez les [limites des instances gratuites Render](https://render.com/docs/free) et la documentation des [disques persistants Render](https://render.com/docs/disks).

### Formulaire de contact

Le formulaire actuel valide les champs et affiche un message de confirmation, mais le projet ne configure ni envoi d’e-mail ni stockage des demandes. **Les messages ne sont donc pas transmis à l’entreprise.** Configurez un fournisseur d’e-mail ou un mécanisme de stockage avant d’utiliser ce formulaire pour recevoir de vrais contacts.

## Vérifications avant publication

```bash
python manage.py check
python manage.py check --deploy
python manage.py test
```

Pour `check --deploy`, activez les réglages de production (`DEBUG=False`) et définissez une clé secrète ainsi que des hôtes explicites. Le service Render configure ces valeurs à partir du Blueprint et des variables d’environnement.

## Structure du projet

```text
core/                  Pages et vues du site
identity_digitale/     Configuration Django et sécurité
static/                Fichiers statiques sources
static/img/            Emblème, logo complet et favicon du groupe
static/img/services/   Illustrations SVG originales des six activités
static/fonts/          Police Manrope auto-hébergée et licence OFL
templates/             Gabarit commun
render.yaml            Blueprint de déploiement Render
requirements.txt       Dépendances Python épinglées
```
