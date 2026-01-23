# Mise en place d'un serveur OpenWec via GPO 
---
*Maxine Botturi RT3 Cyber*

# 0/ Setup initial 

On pars d'une VM Debian 12 avec 2 VCPU, 4Go de RAM & 20Go de stockage disque.
![](https://hedgedoc.botturi.fr/uploads/934ca5d5-2b21-44fd-b1cc-9447f771988a.png)

Ensuite je vais installer les paquets essentiels : 
```bash=
apt update && apt upgrade && apt install wget curl nano unzip -y
```

# 1/ Installation de Docker 

 Set up le répertoire `apt` de Docker.

```bash
# Add Docker's official GPG key:
apt install sudo -y
sudo apt-get update
sudo apt-get install ca-certificates curl -y
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/debian
Suites: $(. /etc/os-release && echo "$VERSION_CODENAME")
Components: stable
Signed-By: /etc/apt/keyrings/docker.asc
EOF

sudo apt-get update
```

Installation des packages Docker.

```bash

 sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
```

# 2/ Création de l'image Docker pour OpenWec

Pour cela on va d'abord cloner le répertoire du projet principal d'OpenWec : 
```bash=
apt install git -y
git clone https://github.com/cea-sec/openwec.git
cd openwec
```
![](https://hedgedoc.botturi.fr/uploads/5db7971b-26d9-4821-a801-fe714fe1c062.png)

Comme on peut le voir, le répertoire docker contient déjà des Dockerfile. On va ici choisir l'image "normale" (non-alpine) car nous n'avons pas de problèmes de performances. Ainsi on build localement l'image : 
```bash
docker build -f docker/openwec.Dockerfile -t openwec .
```


Une fois le build terminé : 
![](https://hedgedoc.botturi.fr/uploads/70f64469-4661-496b-8649-922c0f55b4ff.png)

On va créer un répertoire dédié dans /opt/ au service conteneurisé : 
```bash=
# Création du dossier
sudo mkdir -p /opt/openwec
cd /opt/openwec
```

Ensuite on va créer ce fichier de configuration : 
```bash=
nano config.toml
```

```ini=
[server]
node_name = "openwec-server"
keytab = "/opt/openwec/openwec.essos.local.keytab"

[database]
type = "SQLite"
path = "/var/lib/openwec/db/openwec.sqlite"

[logging]
verbosity = "info"
server_logs = "stderr"

[[collectors]]
listen_address = "0.0.0.0"
listen_port = 5985
hostname = "openwec.essos.local"

[collectors.authentication]
type = "Kerberos"
service_principal_name = "http/openwec.essos.local@ESSOS.LOCAL"

[outputs]
garbage_collect_interval = 600
```
On va ensuite build ce docker compose : 
```bash=
nano docker-compose.yml
```

```yaml=
services:
  openwec:
    container_name: openwec
    image: openwec
    pull_policy: never
    restart: unless-stopped
    ports:
      - "5985:5985"
    volumes:
      - ./config.toml:/etc/openwec.conf.toml:ro
      - ./openwec.essos.local.keytab:/opt/openwec/openwec.essos.local.keytab:ro
      - ./subscriptions:/etc/openwec/subscriptions:ro
      - ./data_openwec:/var/lib/openwec/db/:rw
      - /etc/localtime:/etc/localtime:ro           # Pour la sync temporelle
      - /etc/timezone:/etc/timezone:ro             # De même
    healthcheck:
      test: ["CMD", "nc", "-zv", "127.0.0.1", "5985"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s
```

Avant de up le docker on va récupérer la keytab Kerberos depuis le DC. 

# 3/ Mise en place de l'auth Kerberos

## 3.1/ Création du compte
Pour utiliser Kerberos pour l'authentification et le chiffrement OpenWec, nous allons créer sur les DCs un utilisateur service OpenWec. Pour cela nous automatisons via un script : 
```powershell=
# Crée un compte de service pour OpenWec
# PowerShell Admin sur le DC

$spn = "http/openwec.essos.local"
$realm = "ESSOS.LOCAL"  # Pour le DC5
$username = "openwec_svc"

# Créer un user account dans AD
New-ADUser -Name $username -SamAccountName $username `
    -UserPrincipalName "$spn@$realm" `
    -PasswordNeverExpires $true `
    -CannotChangePassword $true

# Définir un mot de passe
Set-ADAccountPassword -Identity $username -NewPassword (ConvertTo-SecureString -AsPlainText "DràcùLàùra782/" -Force) -Reset

# Activer le compte
Set-ADUser -Identity openwec_svc -Enabled $true

# Enregistrer le SPN
setspn -A $spn $username

# Vérifier
setspn -L $username
```
![](https://hedgedoc.botturi.fr/uploads/4f5ebe85-10b9-4e19-a625-4514f9f75610.png)

## 3.2/ Générer le fichier keytab sur le DC

```powershell=
# Génère le fichier keytab
ktpass -out openwec.essos.local.keytab `
    -princ http/openwec.essos.local@ESSOS.LOCAL `
    -mapuser ESSOS\openwec_svc `
    -pass "DràcùLàùra782/" `
    -ptype KRB5_NT_SRV_HST `
    -crypto AES256-SHA1
```

![](https://hedgedoc.botturi.fr/uploads/75b7bbc3-68e6-4605-bdad-9c8532a3696e.png)

## 3.3/ Importer la keytab

Pour importer la keytab on va l'afficher en base 64 sur le serveur : 
```powershell=
$path = "C:\Temp\openwec.essos.local.keytab"
[Convert]::ToBase64String([IO.File]::ReadAllBytes($path))
```
![](https://hedgedoc.botturi.fr/uploads/9ef94c3b-288a-4d86-b30b-026f8bd453e7.png)

Et on l'importe sur le serveur : 
```bash=
echo "BQIAAABXAAIAC0VTU09TLkxPQ0FMAARodHRwABNvcGVud2VjLmVzc29zLmxvY2FsAAAAAwAAAAADABIAIO++h7c5Nn9Km7XcW+ujuXkWuXOBf/OPF5GYSNIlkTSx" | base64 -d > /opt/openwec/openwec.essos.local.keytab
```
![](https://hedgedoc.botturi.fr/uploads/9416b294-b466-4321-9b9c-a8151f42243f.png)

Ensuite on va donner les bonnes permissions sur la keytab : 
```bash=
chmod 600 openwec.essos.local.keytab
chown 1000:1000 openwec.essos.local.keytab
```

## 3.4/ Donner les bons droits au compte openwec_svc
Ensuite on se rends dans le soft **Active Directory Users and Computers** et on modifie les propritétés du compte : 
![](https://hedgedoc.botturi.fr/uploads/694244d3-80f6-48c5-8ded-efba384fbe6b.png)


Dans l'onglet **Delegation**, on choisit "Trust this user for delegation to any service (Kerberos only)" : 
![](https://hedgedoc.botturi.fr/uploads/a98ffaa1-3bc9-4543-95b7-d69707a76282.png)

On apply

# 4/ Lancer le conteneur

Avant de lancer on va créer le répertoire contenant la base de données : 
```bash=
mkdir -p /opt/openwec/data_openwec
chown 1000:1000 /opt/openwec/data_openwec
```
Ensuite on va lancer le conteneur : 
```bash=
cd /opt/openwec/ && docker compose up -d
```

En regardant les docker logs, on voit bien que tout tourne bien : 
![](https://hedgedoc.botturi.fr/uploads/f3d95615-7209-43dd-9a43-3839b243ce43.png)


# 5/ Connecter une machine Windows

## 5.1/ Configuration Réseau et DNS
On commence par définir sur le PDC dans l'App DNS une entrée pour le serveur correspondant à l'IP du serveur du domaine : 

![](https://hedgedoc.botturi.fr/uploads/43cb8d1e-2d6e-4260-92f6-ee3101856ff5.png)

Ensuite, nous allons devoir configurer WinRM pour que le forwarding d'évènements vers OpenWec se fasse automatiquement. 

## 5.2/ GPO pour la connexion

On ouvre le soft de GPO : 
![](https://hedgedoc.botturi.fr/uploads/d9552dcb-ffd9-4208-9099-f7926a337faf.png)

Ensuite on créé une new GPO sur le domaine : 
![](https://hedgedoc.botturi.fr/uploads/2403c889-9049-4c98-9813-ae4c93fe6438.png)

On l'appelle OpenwecConf
![](https://hedgedoc.botturi.fr/uploads/3d710c7a-3b1f-4efe-8727-dd9d7abf8519.png)
La première policy qu'on apply est dans **Computer Configuration > Policies > Windows Settings > Security Settings > System Services** 
![](https://hedgedoc.botturi.fr/uploads/10b11409-5c39-4373-ba7c-8b95561d8976.png)

On passe le Windows Remote Management en automatique : 
![](https://hedgedoc.botturi.fr/uploads/a96b61ed-8a8f-4b7d-b29b-a1e0c6149371.png)

Ensuite on modifie le paramètre **Computer Configuration > Policies > Administrative Templates > Windows Components > Windows Remote Management (WinRM) > WinRM Service** : 
![](https://hedgedoc.botturi.fr/uploads/91bfcc6b-99f5-49fb-896e-6c7ca060afb7.png)
On passe le paramètres **Allow remote server management through WinRM**
![](https://hedgedoc.botturi.fr/uploads/2b46d906-aec1-4c50-9176-f2780893848c.png)
 
à Enabled sans filtre : 
![](https://hedgedoc.botturi.fr/uploads/2de1e908-b0b3-4518-b08c-e62320aa59e9.png)

Ensuite on va modifier la subscription à **Computer Configuration > Policies > Administrative Templates > Windows Components > Event Forwarding**. On modifie le setting *Configure target Subscription Manager* : 
![](https://hedgedoc.botturi.fr/uploads/6ede93d8-6672-4dab-b5ec-661885189fe4.png)

On l'enable et on passe la valeur a `Server=http://openwec.essos.local:5985/wsman/SubscriptionManager/WEC,Refresh=30` : 
![](https://hedgedoc.botturi.fr/uploads/d60367e0-c989-45be-b470-d6f3cad92397.png)

Ensuite on continue en modifiant **Computer Configuration > Policies > Administrative Templates > Windows Components > Event Log Service > Security** le paramètre *Configure log access* avec l'action Enables et l'option `O:BAG:SYD:(A;;0xf0005;;;SY)(A;;0x5;;;BA)(A;;0x1;;;S-1-5-32-573)(A;;0x1;;;NS)`: 
![](https://hedgedoc.botturi.fr/uploads/114c23e1-43ef-443b-8398-fb33606e9844.png)

On fait de même avec le log access Legacy : 
![](https://hedgedoc.botturi.fr/uploads/0545d1ea-5858-411c-8ce7-d59d4587738f.png)

Enfin il faut aussi automatiser le fait que le compte Network ait accès aux logs sysmon. C'est pas une GPO proposée par défaut, donc on va devoir faire le script manuel utilisé dans la doc sans GPO. Ainsi on crée le script `\\Essos.local\sysvol\essos.local\scripts\Set-SysmonPermissions.ps1` (via un notepad admin): 
```powershell=
# Script: Set-SysmonPermissions.ps1
# But: Donner les droits de lecture au compte "Network Service" pour OpenWec

# SDDL qui inclut (A;;0x1;;;NS) à la fin
$sddl = "O:BAG:SYD:(A;;0xf0005;;;SY)(A;;0x5;;;BA)(A;;0x1;;;S-1-5-32-573)(A;;0x1;;;NS)"

# Appliquer la permission au journal Sysmon
wevtutil sl Microsoft-Windows-Sysmon/Operational "/ca:$sddl"
```
![](https://hedgedoc.botturi.fr/uploads/10aedc7e-9fa8-4008-898e-b8d3ee938f83.png)
![](https://hedgedoc.botturi.fr/uploads/8d7380af-eceb-4d2e-aaae-3f2a75a3cc98.png)
Ensuite on créé une GPO dans **Computer Configuration > Policies > Windows Settings > Scripts > Startup** en sélectionnant notre script : 
![](https://hedgedoc.botturi.fr/uploads/252363f0-0f8b-479c-81c8-c3a11d2aee97.png)

Enfin on update les GPO : 
```powershell=
gpupdate /force
```

## 5.3/ Créations des souscriptions sur le serveur Docker

Pour cela, on se rends sur le serveur Debian et on va créer un répertoire : 

```bash=
mkdir -p /opt/openwec/subscriptions
nano /opt/openwec/subscriptions/sysmon.toml
```

On va créer ce fichier de subscription avec ces paramètres: 
```toml=
uuid = "e5a422e8-5420-4e4f-a7b2-35623b371e7d"
name = "Sysmon-Security-Collection"
uri = "/wsman/SubscriptionManager/WEC"

# La requête XML reste identique
query = """
<QueryList>
  <Query Id="0" Path="Microsoft-Windows-Sysmon/Operational">
    <Select Path="Microsoft-Windows-Sysmon/Operational">*</Select>
  </Query>
  <Query Id="1" Path="Security">
    <Select Path="Security">*[System[(Level=1 or Level=2 or Level=3)]]</Select>
  </Query>
</QueryList>
"""

# Les options de lecture se mettent dans une section dédiée
[options]
read_existing_events = true

[[outputs]]
driver = "Files"
format = "Json"

# Configuration spécifique au driver Files (chemin dans le conteneur)
config = { path = "/var/lib/openwec/db/sysmon_events.json" }
```

Ensuite, on rajoute ce volume et cette commande au docker-compose.yml : 
```yaml=
- ./subscriptions:/etc/openwec/subscriptions:ro
```

Et enfin on donne les bons droits au répertoire des subscriptions et on relance le conteneur : 
```bash=
chown -R 1000:1000 /opt/openwec/subscriptions
docker compose down && docker compose up -d
```
