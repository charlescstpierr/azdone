# Gabarit du skill repo-local `verifier-<app>`

`verifier-application-azd generer` écrit ce fichier dans le dossier de skills de l'hôte (`.claude/skills/verifier-<app>/SKILL.md`, `.cursor/skills/verifier-<app>/SKILL.md` ou `.agents/skills/verifier-<app>/SKILL.md`), avec `<app>` = nom court du dépôt en minuscules. Le fichier appartient au projet : un humain peut le corriger, et `maintenir` le met à jour sans écraser une ligne éditée à la main sans le dire. Remplacer chaque `<...>` par une valeur observée dans le dépôt, jamais devinée ; une inconnue reste `unknown` et devient un gap.

```markdown
---
name: verifier-<app>
description: "Lancer et exercer <app> en isolation pour prouver ses fonctionnalités sur la surface réelle. Utiliser depuis prouver-resultat-azd ou verifier-application-azd executer, jamais contre la production."
---

# Vérifier <app>

Généré par `verifier-application-azd` le <date> sur le commit <sha>. Surfaces : <web | api | cli | ...>.

## Démarrer en isolation

- Commande : `<npm run dev -- --port 4173 | python -m app --port 8081 | ./bin/app>`
- Port ou chemin : `<http://localhost:4173 | ./dist/app>`
- Environnement non secret : `<APP_ENV=test DATABASE_URL=sqlite:///tmp/azd-test.db>`
- Données de test : `<commande de fixture ou chemin>`
- Santé : `<curl -sf http://localhost:4173/health | ligne de log "listening" | prompt affiché>`
- Arrêt : `<kill du PID | docker compose down | Ctrl-C>`

## Observer

- Web : `<navigateur piloté (Playwright) ; viewports 1280x800 et 390x844 ; clavier ; capture .png>`
- API : `<curl ou client HTTP ; schéma attendu ; codes d'erreur>`
- CLI ou TUI : `<commande ; stdout et stderr séparés ; exit code ; 80x24 et 120x40 ; SIGINT>`
- Mobile ou desktop : `<simulateur ou appareil ; permissions ; capture>`
- Chat : `<transcript rejoué ; continuité ; récupération>`
- Données : `<requête ; invariant ; volume attendu>`

## Fonctionnalités

| Fonctionnalité | Comment observer | Attendu | États non nominaux |
| --- | --- | --- | --- |
| <export CSV> | <ouvrir /exports, cliquer Exporter, lire le fichier> | <n lignes, en-têtes exacts> | <liste vide, date invalide> |

## Feature map

`<chemin repo-local de la feature map, format de feature-map-template.md>`

## Interdits

- Jamais la production, un compte réel, des credentials ou des données client.
- Aucune modification du code pendant une vérification.
- Une observation impossible rend `blocked`, jamais `verified`.
```

## Ce que `generer` doit observer avant d'écrire

1. La commande de démarrage réelle (scripts déclarés, Makefile, Procfile, compose), et non une commande plausible.
2. Un port ou un chemin libre, distinct de celui du développeur.
3. Les variables d'environnement exigées par le code (`process.env`, `os.environ`, fichiers `.env.example`) ; les secrets deviennent des gaps, jamais des valeurs.
4. Le signal de santé le plus simple et vérifiable.
5. Les fonctionnalités du System Success Map et du contrat public, une ligne chacune.
