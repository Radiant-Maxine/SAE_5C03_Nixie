Intégration AI a OpenWec
---

*Note : pour que l'IA passe bien on met la RAM à 12Go sur la VM*

# 1/ Installation d'Ollama

Pour installer Ollama sur la VM on run : 
```bash=
curl https://ollama.ai/install.sh | sh
```
![](https://hedgedoc.botturi.fr/uploads/414c0905-4a54-45ee-9289-4b8ade101e9c.png)
![](https://hedgedoc.botturi.fr/uploads/8a1f9ba1-d037-43ed-8b51-8a69fa9b0841.png)

Ensuite on va démarrer et enable le système : 
```bash=
# Lance Ollama en tant que service
sudo systemctl start ollama
sudo systemctl enable ollama

# Vérifie que c'est lancé
sudo systemctl status ollama
```
![](https://hedgedoc.botturi.fr/uploads/e5f26104-9545-4cab-a61c-7cda803968fc.png)

Enfin, on installe le modèle léger Qwen2 7B

```bash
ollama pull qwen2:7b-instruct-q4_K_M
```
![](https://hedgedoc.botturi.fr/uploads/a1dd70ba-5f1d-4182-944e-4d4619690677.png)

# 2/ Installation des dépendances python

On commence par installer pip : 
```bash=
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv
```
Ensuite nous allons créer un environnement virtuel pour télécharger nos librairies : 
```bash=
python3 -m venv ollama-env
source ollama-env/bin/activate
```

Puis on dl la lib ollama : 
```bash=
pip3 install ollama
```
![](https://hedgedoc.botturi.fr/uploads/321dab2f-0c2d-4ecc-98a9-318fb4a1cbbb.png)

Ensuite on va installer les librairies pour les sms : 
```bash=
pip3 install huawei-lte-api schedule
```

# 3/ Création de l'app

Pour cela on va créer un répertoire personnalisé dans : 
```bash=
mkdir -p /opt/ollama_sms_openwec/
cd /opt/ollama_sms_openwec/
```
![](https://hedgedoc.botturi.fr/uploads/1ef257a0-9205-4e9d-9519-52881b1bef84.png)

Ensuite dans le répertoire on va créer cette app : 

```bash=
nano app.py
```
```python=
import time
import json
import os
import schedule
import ollama
from huawei_lte_api.Client import Client
from huawei_lte_api.Connection import Connection

# --- CONFIGURATION ---
LOG_FILE = "/opt/openwec/data_openwec/sysmon_events.json"
STATE_FILE = "watcher_state.txt"  # Pour se souvenir de la position de lecture
PHONE_NUMBER = "+33772337418"
ROUTER_URL = 'http://admin:admin@192.168.8.1/' # Changez le mdp si besoin
MODEL_NAME = "qwen2:7b-instruct-q4_K_M"

def send_sms_alert(message_content):
    """Envoie le SMS via le routeur Huawei"""
    print(f"📡 Envoi SMS : {message_content}")
    try:
        with Connection(ROUTER_URL) as connection:
            client = Client(connection)
            # On coupe le message si trop long pour éviter les erreurs, bien que les SMS concaténés existent
            client.sms.send_sms(phone_numbers=PHONE_NUMBER, message=message_content[:160])
            print("✅ SMS envoyé avec succès.")
    except Exception as e:
        print(f"❌ Erreur envoi SMS : {e}")

def analyze_chunk(logs_lines):
    """Demande à Ollama si c'est grave (Mode Streaming)"""
    if not logs_lines:
        return None

    print("\n🤔 L'IA commence l'analyse... (les mots vont s'afficher en direct)\n" + "-"*50)

    prompt = f"""
    Tu es un système d'alerte de sécurité (SOC). Analyse ces logs Sysmon récents.

    Logs:
    {logs_lines}

    Règles :
    1. Si c'est bénin, réponds juste "NON". Rien d'autre.
    2. Si c'est GRAVE (attaque, mimikatz, rdp suspect), réponds "OUI" suivi d'une phrase courte explicative (machine et incident). Rien d'autre.
    """

    full_response = ""
    try:
        # On active le stream=True
        stream = ollama.chat(model=MODEL_NAME, messages=[{'role': 'user', 'content': prompt}], stream=True)

        for chunk in stream:
            content = chunk['message']['content']
            print(content, end='', flush=True) # Affiche chaque mot sans retour à la ligne
            full_response += content

        print("\n" + "-"*50 + "\n✅ Analyse terminée.")

        # Logique de détection pour le SMS
        if full_response.strip().upper().startswith("OUI"):
            msg = full_response.replace("OUI", "").replace("|", "").strip()
            return f"🚨 ALERTE OPENWEC: {msg}"
        return None

    except Exception as e:
        print(f"\n❌ Erreur Ollama: {e}")
        return None
def job():
    """Tâche principale exécutée toutes les 5 minutes"""
    print("🔍 Vérification des logs...")

    # 1. Gestion de la position dans le fichier (pour ne lire que les nouveaux logs)
    start_pos = 0
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            try:
                start_pos = int(f.read())
            except:
                start_pos = 0

    new_logs = []
    current_pos = start_pos

    try:
        # Vérification si log rotation (fichier plus petit qu'avant)
        file_size = os.path.getsize(LOG_FILE)
        if file_size < start_pos:
            start_pos = 0 # Le fichier a été vidé, on recommence du début

        with open(LOG_FILE, 'r') as f:
            f.seek(start_pos)
            lines = f.readlines()
            current_pos = f.tell()

            # Parsing rapide pour alléger ce qu'on envoie à l'IA
            for line in lines:
                if line.strip():
                    try:
                        data = json.loads(line)
                        # On extrait juste l'essentiel pour l'IA
                        simplified = {
                            "Computer": data.get("System", {}).get("Computer"),
                            "User": data.get("EventData", {}).get("User"),
                            "Command": data.get("EventData", {}).get("CommandLine"),
                            "Image": data.get("EventData", {}).get("Image")
                        }
                        new_logs.append(json.dumps(simplified))
                    except:
                        continue

        # Sauvegarde de la nouvelle position
        with open(STATE_FILE, 'w') as f:
            f.write(str(current_pos))

        # 2. Analyse
        if new_logs:
            count = len(new_logs)
            print(f"📊 {count} nouveaux logs trouvés.")

            # --- MODIFICATION DE SECURITE ---
            # Si on a trop de logs (ex: premier lancement), on ne garde que les 50 derniers
            # pour éviter de faire exploser Ollama et d'attendre 3 heures.
            if count > 50:
                print(f"⚠️ Trop de logs d'un coup ! On ignore les {count - 50} plus vieux et on analyse les 5 derniers.")
                logs_to_analyze = new_logs[-5:] # On garde la fin de la liste
            else:
                logs_to_analyze = new_logs
            # On envoie par paquets si trop gros, ici on prend tout le batch des 5 min
            alert_msg = analyze_chunk("\n".join(logs_to_analyze))

            if alert_msg:
                send_sms_alert(alert_msg)
            else:
                print("RAS (Pas de menace détectée par l'IA)")
                send_sms_alert("désolée pour le message ; rep moi demain matin si ça a marcher")
        else:
            print("Pas de nouveaux logs.")

    except FileNotFoundError:
        print("Fichier de log non trouvé (pas encore créé ?)")

# --- LANCEMENT ---
print("🛡️ Sentinel OpenWEC Démarrée (Scan toutes les 5min)")
# Exécuter une première fois au lancement
job()

# Programmer toutes les 5 minutes
schedule.every(5).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
```

Ensuite on va run le programme pour tester : 
```bash=
python3 app.py
```

Après quelques minutes d'attente nous avons un résultat concluant : 
![](https://hedgedoc.botturi.fr/uploads/5776c05d-1a39-4eb8-9426-638a08c73016.png)
