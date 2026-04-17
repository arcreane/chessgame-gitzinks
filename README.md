# Projet Échecs - Équipe Gitzinks

Jeu d'échecs développé en Python. 

## But du jeu

L'objectif est de recréer les règles officielles des échecs :
- **Déplacements :** Chaque pièce calcule elle-même si son mouvement est mathématiquement valide (diagonales, lignes droites, etc.).
- **Plateau :** Un dictionnaire gère en temps réel quelles cases sont occupées.
- **Victoire :** (En cours de dev) Mettre le Roi adverse échec et mat via le moteur de jeu principal.

## Commandes

- **Lancer le jeu principal :** `python chess.py` (en cours d'intégration)
- **Jouer :** Taper les coordonnées dans le terminal (ex: "e2 e4")
- **Tester une pièce isolée :** Lancer directement son fichier (ex: `python bishop.py` pour tester les règles du Fou)

## Règles d'équipe

- **Main Stable :** Interdiction de push directement sur `main` sans vérifier que tout marche.
- **Une Tâche = une pièce ou une fonctionnalité.**
- **Commits Clairs :** Messages simples pour dire ce qu'on a ajouté (ex: "feat: ajout du Fou").
- **Pull avant Push :** Toujours récupérer le travail des autres (`git pull`) avant d'envoyer (`git push`) pour éviter de tout casser.

## Architecture du projet

Le projet est structuré avec des classes pour séparer la logique :
- `piece.py` et `position.py` : Les fondations (coordonnées et classe mère abstraite).
- `board.py` : Gestionnaire du plateau (dictionnaire des cases occupées/libres).
- `bishop.py`, `rook.py`... : Implémentation spécifique de la logique et des mathématiques de chaque pièce.
- `chess.py` : Script principal gérant la boucle de jeu, les tours des joueurs et l'IA.
