# Connecter Suricata à Wazuh et à Elastic
---

# 1/ Connecter Suricata à Wazuh : 
Sur Wazuh on se rends dans la partie `Agents Management` de l'interface web : 
![](https://hedgedoc.botturi.fr/uploads/c6260751-309d-431a-acf9-5a98c1f0793c.png)

Et on déploie un nouvel agent. ![](https://hedgedoc.botturi.fr/uploads/4160414a-e5cb-42ee-8caf-1003e4bd0793.png)

On sélectionne ensuite l'architecture Debx64 et l'adresse IP du serveur Wazuh `10.203.19.50` : 
![](https://hedgedoc.botturi.fr/uploads/39f9259d-b392-4b29-8315-90ab61d649c6.png)

On met Suricata en nom dans les optionnals settings : 
![](https://hedgedoc.botturi.fr/uploads/3ad72874-281c-4410-a3dd-2f40688768e6.png)

Puis on va run la commande sur le routeur :
```bash
wget https://packages.wazuh.com/4.x/apt/pool/main/w/wazuh-agent/wazuh-agent_4.14.2-1_amd64.deb && sudo WAZUH_MANAGER='10.203.19.50' WAZUH_AGENT_NAME='Suricata' dpkg -i ./wazuh-agent_4.14.2-1_amd64.deb
```
![](https://hedgedoc.botturi.fr/uploads/ff364f5c-899b-42e0-b151-c5c91d684dd2.png)

Ensuite on démarre l'agent sur le serveur : 
```bash=
sudo systemctl daemon-reload
sudo systemctl enable wazuh-agent
sudo systemctl start wazuh-agent
```

![](https://hedgedoc.botturi.fr/uploads/3d7c7bd3-5a95-4b18-ae6f-9b36edcec581.png)

## 1.1/ Edition de la conf de Suricata : 
Pour commencer on va modifier la conf de l'agent Wazuh sur le routeur Suricata : 
```bash=
nano /var/ossec/etc/ossec.conf
```
Et on rajoute ce bloc dans le bloc `<ossec_config>` : 
```xml=
<localfile>
  <log_format>json</log_format>
  <location>/var/log/suricata/eve.json</location>
</localfile>
```
![](https://hedgedoc.botturi.fr/uploads/33c67375-13e7-4b8b-99cf-a16a4a0308e7.png)

Ensuite on donne à l'agent wazuh l'accès aux logs suricata en créant un groupe suricata avec les droits de lecture sur les logs suricata : 
```bash=
groupadd suricata

usermod -aG suricata wazuh

chgrp -R suricata /var/log/suricata

chmod -R g+r /var/log/suricata
chmod g+x /var/log/suricata

systemctl restart wazuh-agent
```

## 1.2/ Vérifier la connection

Ensuite, sur le routeur Suricata, nous allons créer une alerte pour vérifier que Wazuh la lit bien. Pour cela on fait : 
```bash=
curl http://testmyids.com
```

Ensuite, en regardant le dashboard Wazuh et en filtrant par IP de notre routeur, on voit bien la location des logs Suricata apparaitre : 
![](https://hedgedoc.botturi.fr/uploads/65897495-50c7-4039-b527-1d114207f9b8.png)

# 2/ Connecter Suricata à Elastic

## 2.1/ Installation et configuration de l'Elastic Agent sur Suricata

On se rends, sur l'Interface web de Elastic, dans **Management** > **Fleet**, et on sélectionne **Add Agent** : 
![](https://hedgedoc.botturi.fr/uploads/a7912e12-ab14-45cc-9e21-a8b08c610616.png)

On laisse ici les paramètres **Agent policy 1** & **Enroll in Fleet** : 
![](https://hedgedoc.botturi.fr/uploads/02e2ab6b-56e1-4de4-9cba-0a65d6ea7cd5.png)

Ensuite, on sélectionne la procédure pour **DEB x86_64** : 
```bash=
curl -L -O https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-9.1.9-amd64.deb 
sudo dpkg -i elastic-agent-9.1.9-amd64.deb
sudo systemctl enable elastic-agent 
sudo systemctl start elastic-agent 
sudo elastic-agent enroll --url=https://10.203.19.70:8220 --enrollment-token=Rzc0eS1ac0J5czJ1MkVCSlJkOUU6UVd0YmJCVzV1QXgtSnZKcGNOOUtZdw== --insecure
```
Une fois le message de succès arrivé : 
![](https://hedgedoc.botturi.fr/uploads/6a6581c1-18a4-4a38-b00d-dfd0dad79910.png)

On voit sur Elastic aussi le succès: 
![](https://hedgedoc.botturi.fr/uploads/e95673c4-aa86-4564-a4c7-ef3ee29732f9.png)

## 2.2/ Configurer Elastic pour lire les logs de Suricata

Ensuite, nous allons ajouter l'intégration Suricata à Elastic : 
![](https://hedgedoc.botturi.fr/uploads/1bb97556-a85f-44f1-8da6-38f2c46c5c6f.png)

On choisit l'intégration Suricata pour Elastic : 
![](https://hedgedoc.botturi.fr/uploads/4b2e7432-f4e3-455e-87c8-74740d70e6de.png)
On l'installe : 
![](https://hedgedoc.botturi.fr/uploads/02dab269-52d8-467f-bed9-35960490f86b.png)

On laise ces paramètres par défauts : 
![](https://hedgedoc.botturi.fr/uploads/80e42368-a26e-4cfc-8476-4fd5d6db2bc3.png)
Et on créé l'intégration Suricata for Avalanche : 
![](https://hedgedoc.botturi.fr/uploads/dc041131-1fa7-40d7-8dc5-f1f385c7857a.png)


Ici on voit bien que le module est bien installé : 
![](https://hedgedoc.botturi.fr/uploads/97dc0154-99fd-48d9-bb48-1451376c54b2.png)
Ensuite on retourne sur Fleet et on va `Assogn to new policy` notre agent créé : 
![](https://hedgedoc.botturi.fr/uploads/b7483ab9-45dc-474c-99d6-2d0a59ab9190.png)

Et on sélectionne l'agent policy créée avec l'intégration suricata : 
![](https://hedgedoc.botturi.fr/uploads/6cbb3a65-7a60-4a78-a57b-8cf01d6e8c70.png)

## 2.3/ Voir les logs : 

![](https://hedgedoc.botturi.fr/uploads/3300a719-08f0-494f-8cc9-61647a53d529.png)
