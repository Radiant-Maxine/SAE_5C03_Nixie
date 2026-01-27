# 1/ Installation des dépendances python pour le dashboard streamlit

On commence par installer pip : 
```bash=
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv
```
Ensuite nous allons créer un environnement virtuel pour télécharger nos librairies : 
```bash=
python3 -m venv ollama-openwec-streamlit
source ollama-openwec-streamlit/bin/activate
```
![](https://hedgedoc.botturi.fr/uploads/a60bfe9a-fe74-48ab-9324-eb9679d9f853.png)

Ensuite on installe les librairies nécessaires : 
```bash=
pip install ollama streamlit pandas requests plotly
```

Pour run le serveur on fait la commande : 
```bash
streamlit run dashboard.py
```
