# 📊 Pass Map – Football (Streamlit)

Application interactive pour visualiser les échanges de passes d’une équipe de football, à partir des données ouvertes de **StatsBomb**.

---

## 🛠️ Stack technique

- **Python**
- **pandas**, **numpy** : manipulation et calculs
- **matplotlib**, **mplsoccer** : tracé du terrain et des flèches de passes
- **Streamlit** : interface web interactive

---

## 🚀 Lancer le projet

### 1. Cloner le dépôt
```bash
git clone https://github.com/nico916/pass-map-football.git
cd pass-map-football
```

(Optionnel mais recommandé) Créer un environnement virtuel
python -m venv env
env\Scripts\activate      # Sous Windows
#source env/bin/activate   # Sous macOS/Linux

3. Installer les dépendances

pip install -r requirements.txt

4. Lancer l’application

streamlit run app.py

L’interface s’ouvrira automatiquement dans le navigateur.
📂 Données utilisées

Les données proviennent du dépôt officiel StatsBomb Open Data.
Le fichier events.json utilisé ici correspond à un match FC Barcelone vs Alavés – saison 2017-2018.

⚠️ Utilisation non commerciale uniquement, en accord avec les conditions d’usage de StatsBomb.
💡 Fonctionnalités principales

  ✅ Carte des échanges de passes sur le terrain

  ✅ Position moyenne des titulaires

  ✅ Filtrage dynamique (ex : « ≥ 10 passes »)
  
  ✅ Analyse individuelle (partenaires préférés, distances moyennes…)


📌 À venir / pistes d’amélioration:
  
  Analyse multi-matchs / comparaisons

  Ajout de l’équipe adverse

  Filtrage temporel (0–15’, 15–30’, etc.)
  
  Indicateurs tactiques (centralité, changements d’aile, progressivité)

  Export PDF ou PNG

  Intégration d’un chatbot IA complémentaire
