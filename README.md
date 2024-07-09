
# Lancer le Spider de votre Projet

Pour lancer le spider de votre projet, suivez les étapes ci-dessous. Assurez-vous d'avoir installé Scrapy et configuré votre environnement Python correctement.

## Prérequis

- Python 3.6 ou plus récent.
- Scrapy. Vous pouvez l'installer via pip avec la commande `pip install scrapy`.

## Lancement du Spider

1. Ouvrez un terminal ou une invite de commande.
2. Naviguez jusqu'au répertoire racine de votre projet.
3. Pour lancer le spider `formations`, exécutez la commande suivante :
   ```bash
   scrapy crawl formations

Ce spider parcourt les formations disponibles sur le site de Simplon, extrait les informations pertinentes et les traite selon les pipelines configurés dans custom_settings.

## Configuration
Le spider formations est configuré pour démarrer à partir de l'URL https://simplon.co/notre-offre-de-formation.html#nos-formations0 et accepte les domaines simplon.co et francecompetences.fr comme indiqué dans les allowed_domains.

Les items extraits sont traités par les pipelines spécifiés dans custom_settings, qui sont Cleaning et FormationSaving, pour le nettoyage et la sauvegarde des données.
