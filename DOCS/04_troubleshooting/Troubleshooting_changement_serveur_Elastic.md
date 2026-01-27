# Troubleshooting : Migration Elastic Agent vers un nouveau serveur SIEM

Documentation complète pour la migration de l'Elastic Agent d'un serveur SIEM vers un autre, couvrant Windows et Linux.

---

## 📋 Table des matières

1. [Windows - Procédure manuelle](#windows--procédure-manuelle)
2. [Windows - Déploiement via GPO](#windows--déploiement-via-gpo)
3. [Linux - Procédure](#linux--procédure)
4. [Prérequis et considérations](#prérequis-et-considérations)

---

## Windows - Procédure manuelle

### Étape 1 : Supprimer l'agent Elastic existant

Exécute en PowerShell **en tant qu'administrateur** :

```powershell
& "C:\\Program Files\\Elastic\\Agent\\elastic-agent.exe" uninstall
```

Cette commande désinstalle proprement l'agent Elastic en supprimant le service Windows et les fichiers associés.

---

### Étape 2 : Récupérer l'installeur (v9.1.9)

Avant de télécharger, **active le protocole TLS 1.2** (recommandé pour éviter les erreurs SSL) :

```powershell
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
Invoke-WebRequest -Uri https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-9.1.9-windows-x86_64.zip -OutFile elastic-agent-9.1.9-windows-x86_64.zip
```

| Étape | Description |
|-------|-----------|
| **TLS 1.2** | Active le protocole sécurisé requis par Elastic |
| **Invoke-WebRequest** | Télécharge le .zip (~154 Mo) |
| **OutFile** | Sauvegarde le fichier dans le répertoire courant |

---

### Étape 3 : Extraire l'archive

```powershell
Expand-Archive .\\elastic-agent-9.1.9-windows-x86_64.zip -DestinationPath .
```

Cela crée un dossier `elastic-agent-9.1.9-windows-x86_64` contenant l'exécutable et les binaires nécessaires.

---

### Étape 4 : Inscrire l'agent auprès du nouveau serveur Fleet

Navigue dans le répertoire extrait et exécute l'installation avec les paramètres du nouveau serveur :

```powershell
cd elastic-agent-9.1.9-windows-x86_64
.\\elastic-agent.exe install --url=https://10.203.19.75:8220 --enrollment-token=ZzdjSUFKd0IyZk9NZ3lUOGRlM2E6bWNFRUVhMUVfd1dtNjd2UDFUb3ROQQ== --insecure
```

| Paramètre | Signification |
|-----------|-------------|
| **--url** | Adresse IP et port du Fleet Server (8220 par défaut) |
| **--enrollment-token** | Token d'authentification fourni par Fleet (différent pour chaque serveur) |
| **--insecure** | Désactive la vérification du certificat SSL (adapter selon ta config) |

---

## Windows - Déploiement via GPO

Pour déployer automatiquement cette migration sur tous les clients Windows du domaine, utilise une **Group Policy Object (GPO)** avec un script startup.

### Préparation sur le Domain Controller

#### 1. Préparer les fichiers source

Sur le Domain Controller, télécharge et extrait l'agent Elastic dans la location NETLOGON :

```powershell
# Sur le DC, en PowerShell admin
cd \\\\domain.local\\NETLOGON
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
Invoke-WebRequest -Uri https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-9.1.9-windows-x86_64.zip -OutFile elastic-agent-9.1.9-windows-x86_64.zip
Expand-Archive .\\elastic-agent-9.1.9-windows-x86_64.zip -DestinationPath .
```

#### 2. Créer un script PowerShell d'installation

Crée un fichier `elastic-agent-install.ps1` dans `\\\\domain.local\\NETLOGON\\Scripts\\` :

```powershell
# Elastic Agent Installer Script
# Ce script s'exécute au démarrage de chaque ordinateur

$LogPath = "C:\\Windows\\Temp\\Elastic-Agent-Install.log"
$SourcePath = "\\\\domain.local\\NETLOGON\\elastic-agent-9.1.9-windows-x86_64"
$LocalPath = "C:\\Windows\\Temp\\elastic-agent-install"

# Crée un log pour le dépannage
Function Write-Log {
    param([string]$Message)
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$Timestamp - $Message" | Out-File -FilePath $LogPath -Append
}

Write-Log "Script de déploiement Elastic Agent démarré"

# Étape 1 : Vérifier si l'agent existe déjà
if (Get-Service -Name "Elastic Agent" -ErrorAction SilentlyContinue) {
    Write-Log "Agent Elastic détecté. Désinstallation..."
    & "C:\\Program Files\\Elastic\\Agent\\elastic-agent.exe" uninstall -y
    Write-Log "Agent Elastic désinstallé"
    Start-Sleep -Seconds 5
} else {
    Write-Log "Aucun agent Elastic trouvé. Procédure d'installation"
}

# Étape 2 : Copier les fichiers en local
if (Test-Path $LocalPath) {
    Remove-Item -Path $LocalPath -Recurse -Force
}
Copy-Item -Path $SourcePath -Destination $LocalPath -Recurse -Force
Write-Log "Fichiers copiés vers $LocalPath"

# Étape 3 : Installer le nouvel agent
try {
    $InstallCmd = & "$LocalPath\\elastic-agent.exe" install --url=https://10.203.19.75:8220 --enrollment-token=ZzdjSUFKd0IyZk9NZ3lUOGRlM2E6bWNFRUVhMUVfd1dtNjd2UDFUb3ROQQ== --insecure -y
    Write-Log "Installation réussie : $InstallCmd"
} catch {
    Write-Log "ERREUR lors de l'installation : $_"
    exit 1
}

# Étape 4 : Nettoyage
Start-Sleep -Seconds 2
Remove-Item -Path $LocalPath -Recurse -Force
Write-Log "Fichiers temporaires nettoyés. Installation terminée."
```

### Configuration de la GPO

#### 1. Ouvrir la console de gestion des stratégies de groupe

```
Win + R → gpmc.msc
```

#### 2. Créer une nouvelle GPO

1. Clique droit sur le dossier contenant l'OU cible (ex: `OU=Computers`) → **Create a GPO in this domain, and Link it here**
2. Nomme la GPO (ex: `Elastic-Agent-Deployment`)
3. Clique **OK**

#### 3. Configurer le script startup

1. Clique droit sur la nouvelle GPO → **Edit**
2. Navigue vers : **Computer Configuration > Policies > Windows Settings > Scripts (Startup/Shutdown)**
3. Double-clique sur **Startup** (onglet PowerShell)
4. Clique **Add**
5. Renseigne :
   - **Script Name** : `\\\\domain.local\\NETLOGON\\Scripts\\elastic-agent-install.ps1`
   - **Script Parameters** : Laisse vide (les paramètres sont dans le script)
6. Clique **OK** et ferme l'éditeur

| Champ | Valeur |
|-------|--------|
| **Script Location** | UNC path vers le .ps1 |
| **Execution Policy** | Bypass (si nécessaire) |
| **Timing** | S'exécute avant le login utilisateur |

#### 4. Lier la GPO aux ordinateurs cibles

1. Dans GPMC, clique droit sur l'OU cible → **Link an Existing GPO**
2. Sélectionne `Elastic-Agent-Deployment`
3. Clique **OK**

#### 5. Forcer l'application de la GPO (optionnel pour test)

Sur chaque machine cible, ouvre PowerShell en tant qu'administrateur et exécute :

```powershell
gpupdate /force /boot
```

L'ordinateur redémarrera et exécutera le script au démarrage.

---

### Points importants pour la GPO

- **Execution Policy** : Les scripts startup s'exécutent en contexte SYSTEM (pas soumis à ExecutionPolicy)
- **Timing** : Le script s'exécute au démarrage (avant le login utilisateur) si tu utilises **Startup** et non **Logon**
- **Token d'enrollment** : Chaque machine peut avoir un token différent ; adapter le script ou utiliser un token de groupe
- **Logs** : Ils sont écrits dans `C:\\Windows\\Temp\\Elastic-Agent-Install.log` sur chaque machine

---

## Linux - Procédure

### Étape 1 : Arrêter et désinstaller l'agent existant

```bash
# Arrête le service Elastic Agent
sudo systemctl stop elastic-agent 2>/dev/null || true

# Supprime le package système
sudo apt remove elastic-agent -y
sudo apt purge elastic-agent -y
sudo apt autoremove -y

# Nettoie les résidus de configuration
sudo rm -rf /opt/elastic-agent
sudo rm -rf /etc/elastic-agent
sudo rm -rf /var/lib/elastic-agent
sudo rm -rf /etc/systemd/system/elastic-agent.service

# Recharge les services systemd
sudo systemctl daemon-reload

# Vérifie que tout est supprimé
dpkg -l | grep elastic
```

| Commande | Effet |
|----------|------|
| **systemctl stop** | Arrête le service (tolère l'absence) |
| **apt remove + purge** | Supprime le package et la config |
| **rm -rf** | Nettoie les fichiers résiduels |
| **daemon-reload** | Recharge la cache systemd |

---

### Étape 2 : Télécharger et installer l'agent

```bash
# Télécharge l'archive
cd /tmp
curl -L -O https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-9.1.9-linux-x86_64.tar.gz

# Extrait les fichiers
tar xzvf elastic-agent-9.1.9-linux-x86_64.tar.gz

# Se place dans le répertoire
cd elastic-agent-9.1.9-linux-x86_64
```

| Étape | Description |
|-------|-----------|
| **curl -L** | Suit les redirections HTTP |
| **-O** | Conserve le nom du fichier |
| **tar xzvf** | Extrait avec affichage des fichiers |

---

### Étape 3 : Inscrire l'agent auprès du nouveau serveur Fleet

```bash
sudo ./elastic-agent install \\
  --url=https://10.203.19.75:8220 \\
  --enrollment-token=NGJwckFKd0IyZk9NZ3lUOFB3Y3M6dFh1bnBmazRYaUN3QjdmSldyUHo5QQ== \\
  --insecure
```

| Paramètre | Signification |
|-----------|-------------|
| **--url** | Adresse du Fleet Server |
| **--enrollment-token** | Token Linux (différent du token Windows) |
| **--insecure** | Désactive la vérification SSL si nécessaire |

---

### Étape 4 : Vérifier le statut

```bash
# Affiche le statut de l'agent
sudo elastic-agent status

# Affiche les logs (optionnel)
sudo journalctl -u elastic-agent -f
```

---

## Prérequis et considérations

### Avant de commencer

- ✅ **Accès administrateur** sur les machines Windows (pour désinstaller/installer)
- ✅ **Accès root/sudo** sur les machines Linux
- ✅ **Identifiants d'enrollment** fournis par ton serveur Fleet Elastic
- ✅ **Connectivité réseau** vers le Fleet Server (ports 8220 TLS)
- ✅ **Firewall** : Vérifie que le port 8220 est accessible depuis les clients

### Tokens d'enrollment

- Les tokens sont **spécifiques à chaque serveur Fleet** et souvent à chaque OS
- Les tokens Windows et Linux sont **différents**
- Les tokens expirent après une durée configurable (par défaut : 10 minutes)
- Récupère les nouveaux tokens depuis Kibana → Fleet → Agents

### Considérations de sécurité

- Le paramètre `--insecure` désactive la vérification du certificat SSL (utiliser uniquement en dev/test)
- En production, utilise des certificats valides et supprime le flag `--insecure`
- Les scripts PowerShell GPO s'exécutent en contexte SYSTEM (privilèges élevés)
- Les logs d'installation peuvent contenir des tokens d'enrollment ; sécurise-les

### Dépannage courant

**Windows : "Could not create SSL/TLS secure channel"**
```powershell
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
```

**Windows : "Agent installation failed"**
- Vérifie le token d'enrollment (doit être actualisé toutes les 10 min)
- Vérifie la connectivité vers le Fleet Server : `Test-NetConnection -ComputerName 10.203.19.75 -Port 8220`

**Linux : "Permission denied"**
- Utilise `sudo` pour la désinstallation et l'installation

**Linux : "Cannot reach Fleet Server"**
- Vérifie la résolution DNS
- Teste la connectivité : `curl -k https://10.203.19.75:8220`

