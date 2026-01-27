# Installation de Elastic
---
*Maxine Botturi RT3*

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

# 2/ Installation des autres dépendances 

```bash
sudo apt update && sudo apt install -y \
  git \
  make \
  curl \
  jq
```

# 3/ Récupération du dépot git siem : 

```bash=
cd /opt
git clone https://github.com/pushou/siem.git
cd siem

# Vérifie la structure
ls -la
```
![](https://hedgedoc.botturi.fr/uploads/195be6be-22b0-4ad3-87d8-85dc98a3d8c7.png)

# 4/ Lancement des docker

Pour cela on commence par faire : 
```bash=
make es
```

Pour récupérer les images docker, mettre en place les certificats et préparer le terrain en général : 
![](https://hedgedoc.botturi.fr/uploads/bfaf8d49-91fe-43f7-be95-28df5dc17062.png)

Ensuite on va déployer le SIEM (notamment pour l'interface graphique Kibana) avec : 
```bash=
make siem
```

![](https://hedgedoc.botturi.fr/uploads/8158524b-f05f-404e-bd63-6b902faf0cfe.png)
![](https://hedgedoc.botturi.fr/uploads/2eb63be6-3485-4424-8c62-bbee968190a5.png)

Enfin on fais un `make pass` pour afficher les mots de passe : 
```bash=
make pass
```

![](https://hedgedoc.botturi.fr/uploads/1fce8216-5dcf-4257-a7c6-bd05c6054cc6.png)

Enfin, on va lancer la commande pour créer le serveur fleet : 
```bash=
make fleet
```
![](https://hedgedoc.botturi.fr/uploads/d828ffcb-1a4a-46f7-8320-02f87c824833.png)

# 5/ Première connexion graphique & Fleet Server

Ensuite on se rends à https://10.203.19.75:5601/ et on se connecte avec le mot de passe elastic `ZeX59FpQZODHb7fm8fBj` : 

On va ensuite se rendre dans **Management** > **Fleet** : 
![](https://hedgedoc.botturi.fr/uploads/1e65c907-a34c-4872-8638-a557b351c182.png)

On clique sur **Add Fleet Server** : 
![](https://hedgedoc.botturi.fr/uploads/37923b97-ee28-45e2-9044-bd4354d2c79e.png)

Ensuite, on rentre le nom `fleet` et l'adrese `https://10.203.19.75:8220`
![](https://hedgedoc.botturi.fr/uploads/e70cf3f2-0ac9-4877-90ec-1d4026482b1d.png)

On appuie sur **Generate Fleet Server policy**, et après un peu d'attente on voit bien notre serveur fleet : 
![](https://hedgedoc.botturi.fr/uploads/a86a6256-06e4-4368-96b6-19a8e1478dd7.png)
De même Dans l'onglet Settings : 
![](https://hedgedoc.botturi.fr/uploads/9968c53f-2012-4074-9d86-2c017147e2ae.png)

Ensuite, nous allons faire la commande `make fgprint`et la commande `make prca` : 
![](https://hedgedoc.botturi.fr/uploads/af308c75-6032-4a1c-b6ab-40fb9b8b2952.png)

Sur l'interface web, toujours dans l'onglet settings, on va ensuite rajouter un output : 
![](https://hedgedoc.botturi.fr/uploads/af9e49fc-8bf1-42fa-956c-0addad95345e.png)

On définit le nom à `aerith_output`, le host à `https://10.203.19.75:9200`, le trusted fingerprint à `B32DFF3EBBD336ECA0E0C2250761412E508C3C6F97C6C96B111EA3197CAD786A`. 
![](https://hedgedoc.botturi.fr/uploads/92c9db5f-9157-4572-84b0-e5e939c85c2f.png)
Ensuite, on met ces paramètres yaml : 
```yaml=
ssl:
  certificate_authorities:
    - |
      -----BEGIN CERTIFICATE-----
      MIIDWTCCAkGgAwIBAgIUTvaM62awHwkPF+zN/9/VhZehGrwwDQYJKoZIhvcNAQEL
      BQAwNDEyMDAGA1UEAxMpRWxhc3RpYyBDZXJ0aWZpY2F0ZSBUb29sIEF1dG9nZW5l
      cmF0ZWQgQ0EwHhcNMjYwMTI3MTQzODAxWhcNMjkwMTI2MTQzODAxWjA0MTIwMAYD
      VQQDEylFbGFzdGljIENlcnRpZmljYXRlIFRvb2wgQXV0b2dlbmVyYXRlZCBDQTCC
      ASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALZ+x6TZV2/hGkKk8UpOWD6c
      YR3KBD7Wnh6245SCDp11ZxprVEBN6WqkBoSIjJzHRGZk0o6eCEdouz1PR/br8qkU
      qT1YqV4p/9XnC1toM+UityKSZO0rfqFZ8zRzixUHJ+8y7thZjAq3ngtlW2qN32z5
      ETlUcrHIga+6iWb/aVWIEwH7R/xigOFK0EalHjPTB1FgqGd4BgZ9DooqWnZBOqZm
      NZCLkYIsigcWLrDg1rbw6SfsRtnj9F2I/Z5nBmO0Ks6BY5MikiXMsMwjU9uClo7m
      w5ubc3s9k0pvHfJZEErheM7zUputiF2H8NCUIVI3MeE0wDSttok4UliAo60Q5bMC
      AwEAAaNjMGEwHQYDVR0OBBYEFEXKMWuAo5nU7AUwsxWP1u6c8gFkMB8GA1UdIwQY
      MBaAFEXKMWuAo5nU7AUwsxWP1u6c8gFkMA8GA1UdEwEB/wQFMAMBAf8wDgYDVR0P
      AQH/BAQDAgEGMA0GCSqGSIb3DQEBCwUAA4IBAQAEbeYKCSItPyvwEjYkv8OSPRo/
      rilz6o9LIxOn9Mrvlg0mKs/xFkusbu1+V/9/n44mzMA1nvK4orj91AJfxnGDYutO
      CMtFRg920Z9RcSpARTLDLgVr86oTz86cFK1YHa05KS7rhB+SUFGLTHZ0LAuAt0kf
      J9JfFATGSr0liy3lGbmy+GoI34/hvVvlm1/X3vA68edzSMwy10hWHUfdciss0QdG
      XtU9mApo9JNWdyHK5J81b3R2XBsc/qY1jQZiXJiMGlTde/op4NBv+iHkavAF9sUs
      zkxmcqTCcfSJDmjmLlKfr+FlzHcKqS4CGth79IN0oV1QpthD+JWYJdmBT9Oq
      -----END CERTIFICATE-----
ssl.verification_mode : none
```


![](https://hedgedoc.botturi.fr/uploads/48df5700-2db5-4ccd-a299-f86686082182.png)
On applique ces mêmes paramètres à l'output par défaut pour gagner du temps.
On save et on apply. 

## 6/ Intégration Windows

Pour que les metrics CPU, RAM etc remontent il faut rajouter à notre policy l'integration windows. On fait cela en allant dans **Management** > **Fleet** et en sélectionnant l'Agent policy 1 : 
![](https://hedgedoc.botturi.fr/uploads/c67e04c2-1d76-4e92-89a6-b21c71f91fcc.png)

Puis en cliquant sur **Add integration** : 
![](https://hedgedoc.botturi.fr/uploads/16afadd5-306c-4e7a-a02a-da8247ad167a.png)

On sélectionne l'integration Windows et on laisse par défaut : 
![](https://hedgedoc.botturi.fr/uploads/f0c32301-38d0-4633-8b37-8121f24f5bb1.png)


## 7/ Monitorer Sysmon

Par défaut, l'intégration Windows de Elastic monitore les logs sysmon. On peut le vérifier en allant dans **Management** > **Fleet** et en sélectionnant l'Agent policy 1 : 
![](https://hedgedoc.botturi.fr/uploads/c67e04c2-1d76-4e92-89a6-b21c71f91fcc.png)

On clique ensuite sur *windows-1* : 
![](https://hedgedoc.botturi.fr/uploads/b01cb5c5-f10b-4bcf-bdb0-f8ee7376f349.png)

Et on scroll jusqu'à **Sysmon Operational** qui est normalement coché par défaut : 
![](https://hedgedoc.botturi.fr/uploads/628aaf1d-9439-49c7-9309-84d5c44e959a.png)

Pour le vérifier on peut se rendre à l'URL `https://10.203.19.75:5601/app/discover#/?_g=(filters:!(),refreshInterval:(pause:!t,value:0),time:(from:now-24h,to:now))&_a=(columns:!(),dataSource:(dataViewId:'logs-*',type:dataView),filters:!(),interval:auto,query:(language:lucene,query:'event.provider:%22Microsoft-Windows-Sysmon%22'),sort:!(!('@timestamp',desc)))` Pour voir les évènements sysmon remontés : 
![](https://hedgedoc.botturi.fr/uploads/f4ab797c-13ff-47aa-88a7-b324d67d21f0.png)
