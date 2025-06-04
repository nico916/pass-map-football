# 📊 Pass Map – Football (Streamlit)

Application interactive pour visualiser les échanges de passes d’une équipe de football, à partir des données ouvertes de **StatsBomb**.

---

## 🛠️ Stack technique

- **Python**
- **pandas**, **numpy** : manipulation des données, calculs statistiques
- **matplotlib**, **mplsoccer** : tracé du terrain, flèches, visualisation
- **Streamlit** : interface web interactive

---

## 🚀 Lancer le projet

### 1. Cloner le dépôt
```bash
git clone https://github.com/nico916/pass-map-football.git
```

### 2. (Optionnel mais recommandé) Créer un environnement virtuel
```bash
python -m venv env
env\Scripts\activate       # Sous Windows
# source env/bin/activate  # Sous macOS / Linux
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Lancer l’application
```bash
streamlit run app.py
```

🧠 L’interface se lancera automatiquement dans le navigateur.  
🔁 Redémarrage rapide grâce au cache Streamlit.

---

## 📂 Données utilisées

Les données proviennent du dépôt open-source **StatsBomb Open Data** :  
📎 [https://github.com/statsbomb/open-data](https://github.com/statsbomb/open-data)

Le fichier `events.json` correspond ici au match **FC Barcelone vs Alavés** – saison **2017-2018**.  
⚠️ Utilisation **non commerciale uniquement**, conformément aux conditions d’usage.

---

## 💡 Fonctionnalités principales

✅ **Carte interactive** des échanges de passes (avec flèches directionnelles)  
✅ **Position moyenne** de chaque joueur (calculée à partir des passes)  
✅ **Filtrage dynamique** (ex: « ≥ 10 passes » pour plus de lisibilité)  
✅ **Analyse individuelle** par joueur :
- Partenaires préférés
- Nombre total de passes
- Distance moyenne de transmission

---

## 📌 Pistes d’amélioration

- 🔁 Analyse **multi-matchs** ou comparaison inter-joueurs
- ⚔️ Affichage de **l’adversaire** pour une vision des deux équipes
- ⏱️ Filtrage **temporel** (ex: par période de jeu)
- 🧠 Indicateurs tactiques avancés :
  - Centralité du réseau de passes
  - Switches of play (changements d’aile)
  - Progressivité des transmissions
- 🖼️ Export **PDF / PNG** pour intégration dans des rapports
- 🤖 Intégration d’un **assistant IA** pour des requêtes naturelles (ex: "Quel joueur est le plus central ?")

---

## 📄 Licence

Projet personnel à but éducatif.  
Code sous licence **MIT**.  
Données sous conditions de StatsBomb.
