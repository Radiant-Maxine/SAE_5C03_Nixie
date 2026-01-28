# 🛸 **Installation Exegol (Procedure Complète)**

**Auteur:** Nixie  
**Date:** 28 Jan 2026  
**Durée:** ~15 min (dépend de la connexion internet)

---

## 📋 **Intro - C'est quoi Exegol?**

Exegol, c'est essentiellement une boîte à outils **Linux pour les pentesters** qu'on lance via Docker. Dedans, on a tous les outils qu'on veut : impacket, crackmapexec, bloodhound-py, etc.

Pour notre SAE 5, on va l'utiliser pour lancer les **4 attaques GOAD** depuis un conteneur isolé.

---

## 🚀 **Étape 1: Mettre à jour le wrapper Exegol**

Le wrapper, c'est juste le **CLI qui gère les conteneurs Exegol**. On le met à jour via pip.

```powershell
pip install --upgrade exegol
```

**Résultat attendu :**
```
Successfully installed ... exegol
```

---

## ✅ **Étape 2: Accepter la EULA**

La première fois, Exegol te demande d'accepter les conditions. C'est obligatoire.

```powershell
exegol version
```

Ça va te poser des questions :

```
[?] I confirm that I've read and accepted the EULA ... [y/N]: y
[?] Do you want to display EULA here? [Y/n]: y
```

→ Tu peux lire ou skip (appuie sur `n` pour skip)

```
[?] Do you want to activate your Exegol subscription now? [y/N]: n
```

→ On reste sur la version **Community gratuite**

```
[!] Community plan is strictly limited to personal, non-commercial, educational, or research purposes.
[?] I confirm that I'm not trying to rip off the developers ... [y/N]: y
```

→ C'est juste une blague, appuie sur `y`

**Résultat final :**
```
[+] You can now use Exegol Community Edition! Enjoy :)
[*] Exegol Community (personal use only)
```

✅ **Parfait, on peut continuer !**

---

## 🎬 **Étape 3: Créer & Lancer le conteneur Exegol**

C'est là qu'on crée notre **conteneur Exegol** qu'on va utiliser pour les attaques.

```powershell
exegol start exegol-pentest
```

**Première étape :** Choisir l'image
```
🛸 Available images                           
┌─────────┬──────────┬───────────────────────┐
│ Image   │ Size     │ Status                │
├─────────┼──────────┼───────────────────────┤
│ free    │ 16.9 GB  │ Up to date (v.3.1.8)  │
│ ad      │ 28.93 GB │ Pro / Enterprise only │
│ ...     │ ...      │ ...                   │
└─────────┴──────────┴───────────────────────┘

[?] Select an image by its name (free): free
```

→ On garde `free` (appuie sur Enter)

**Deuxième étape :** Télécharger les ressources
```
[?] Do you want to download exegol resources? (~1G) [Y/n]: y
[?] Are you ready to start the download? [Y/n]: y
```

→ Ça va télécharger ~1GB de wordlists, exploits, etc. (ça peut prendre quelques minutes)

```
Downloading • 161.58 MiB | 9.91 MiB/s ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ • 68.3% 382/559
[+] The Git repository resources was successfully cloned!
```

✅ **C'est bon !**

---

## 📊 **Résumé du conteneur créé**

Une fois qu'Exegol finit, on voit ce résumé :

```
⭐ Container summary                                        
┌──────────────────┬───────────────────────────────────────┐
│             Name │ pentest                               │
│            Image │ free - v.3.1.8 (Up to date)           │
├──────────────────┼───────────────────────────────────────┤
│      Credentials │ root : Hd7F1CbyLoYHbXzUjlBheTtJOvJu1t │
│   Remote Desktop │ Off 🪓                                │
│      Console GUI │ On ✔ (X11)                            │
│          Network │ Docker                                │
│         Timezone │ On ✔                                  │
│ Exegol resources │ On ✔ (/opt/resources)                 │
│     My resources │ On ✔ (/opt/my-resources)              │
│    Shell logging │ Off 🪓                                │
│       Privileged │ Off ✔                                 │
│        Workspace │ Dedicated (/workspace)                │
└──────────────────┴───────────────────────────────────────┘

[+] Exegol container successfully created!
[*] Location of the exegol workspace on the host : C:\Users\ROB\.exegol\workspaces\pentest
[+] Opening zsh shell in Exegol pentest
[Jan 28, 2026 - 13:46:41 (CET)] exegol-pentest /workspace #
```

**Qu'est-ce que ça veut dire ?**
- `Name: pentest` → Le conteneur s'appelle "pentest"
- `Credentials: root:...` → On peut accéder avec ces creds si besoin
- `Network: Docker` → Il est connecté au réseau Docker (pas le host network de Windows)
- `/workspace #` → **On est rentré DEDANS ! On a un shell Linux !** 🎉

---

## 🔧 **Étape 4: Vérifier que tout marche**

On teste si les outils d'attaque sont présents.

```bash
which impacket
which crackmapexec
which python3
```

**Résultat attendu :**
```
/usr/local/bin/impacket
/usr/local/bin/crackmapexec
/usr/bin/python3
```

✅ **Tout est là !**

---

## 📡 **Étape 5: Tester la connectivité vers GOAD**

On vérifie qu'on peut atteindre nos VMs GOAD depuis Exegol.

```bash
ping -c 2 192.168.56.10
```

**Résultat attendu :**
```
PING 192.168.56.10 (192.168.56.10): 56 data bytes
64 bytes from 192.168.56.10: icmp_seq=0 ttl=63 time=5.234 ms
64 bytes from 192.168.56.10: icmp_seq=1 ttl=63 time=4.891 ms
```

✅ **Connectivité OK !**

---

## 🚪 **Étape 6 (Plus tard): Sortir & Rentrer d'Exegol**

**Pour SORTIR du conteneur :**
```bash
exit
```

Ça t'amène back sur Windows PowerShell.

**Pour RENTRER dans le conteneur :**
```powershell
exegol exec exegol-pentest
```

Et boum, tu es de retour dans le shell Linux d'Exegol.

---

## 🎯 **Résumé rapide**

| Étape | Commande | Résultat |
|-------|----------|----------|
| **1** | `pip install --upgrade exegol` | Wrapper à jour ✅ |
| **2** | `exegol version` | Accept EULA + Community ✅ |
| **3** | `exegol start exegol-pentest` | Conteneur créé + shell dedans ✅ |
| **4** | `which impacket` | Outils là ✅ |
| **5** | `ping 192.168.56.10` | Connectivité OK ✅ |

---

## 💡 **Notes importantes**

- **Host network mode pas dispo sur Docker Desktop Windows** → C'est normal, on utilise le mode "Docker" (bridged)
- **Workspace Exegol** → Les fichiers qu'on crée dedans se retrouvent sur l'hôte à `C:\Users\ROB\.exegol\workspaces\pentest`
- **Ressources téléchargées** → Wordlists, outils, exploits sont dans `/opt/resources` (dedans le conteneur)

---

## 🔴 **Erreurs courantes & solutions**

### **Erreur : "Host network mode not available"**
```
[!] Host network mode for Docker Desktop is not available
```
→ **Normal sur Windows**, on utilise Docker bridged, ça marche pareil

### **Erreur : "Cannot connect to GOAD"**
```bash
ping 192.168.56.10
PING 192.168.56.10 (192.168.56.10): 56 data bytes
100% packet loss
```
→ Vérifier que VirtualBox est en bridged mode + que les VMs tournent

### **Erreur : "Impacket not found"**
```bash
which impacket
```
→ L'image `free` contient impacket, sinon l'installer manuellement dedans le conteneur

---

## 📝 **Prochaines étapes**

Maintenant qu'Exegol est setup, on peut lancer les **4 attaques GOAD** :

```bash
# À l'intérieur d'Exegol
python3 -m impacket.GetUserSPN -dc-ip 192.168.56.10 GOADDOMAIN.LOCAL/guest:password
```

Voir le fichier "4_Attaques_GOAD.md" pour les procédures complètes.

---

**Installation terminée ! 🚀 On est prêt pour les attaques !**