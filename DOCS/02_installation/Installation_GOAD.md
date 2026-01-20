Setup des machines GOAD
==
*Maxine Botturi RT3 Cyber*

# 0/ Mise en place de l'hôte ([source](https://orange-cyberdefense.github.io/GOAD/installation/linux/))

Pour commencer, nous allons mettre en place notre machine Linux pour pouvoir installer correctements les différentes machines. On commence par installer Vagrant sur le serveur selon la procédure https://developer.hashicorp.com/vagrant/install#linux : 
```bash=
wget -O - https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(grep -oP '(?<=UBUNTU_CODENAME=).*' /etc/os-release || lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install vagrant
```
![](https://hedgedoc.botturi.fr/uploads/1e9b48a9-74ba-4448-ac5e-10aa9841ce19.png)

Ensuite on installe les plugins Vagrant nécessaires : 

```bash=
vagrant plugin install vagrant-reload vagrant-vbguest winrm winrm-fs winrm-elevated
```
![](https://hedgedoc.botturi.fr/uploads/50554f60-c29c-4a6a-a5cd-91dc8cac7206.png)

Ensuite d'après la doc nous devons vérifier la version actuelle de Python et instller le paquet venv correspondant : 
```bash
python3 --version
sudo apt install python3.11-venv
```
![](https://hedgedoc.botturi.fr/uploads/fbb6ea4a-a62c-4d4d-ba85-3fc49318bf9a.png)

# 1/ Mise en place des VMs GOADyo
Ensuite, on va cloner le repo GOAD et on va s'y déplacer : 
```bash=
git clone https://github.com/Orange-Cyberdefense/GOAD.git
cd GOAD
```

![](https://hedgedoc.botturi.fr/uploads/5a677690-37ed-4812-b934-64aafc93d6fb.png)

Ensuite on va lancer le script `goad.sh` qui permet de vérifier les prérequis, créer le venv python et installer les dep Ansible : 
```bash=
./goad.sh
```
![](https://hedgedoc.botturi.fr/uploads/95eb695b-d6d7-4ebc-8dfd-42c13358b719.png)
![](https://hedgedoc.botturi.fr/uploads/ad2d0c18-8ace-4d0b-830c-ad9a97236b3b.png)

Une fois que tout est bon, on est arrivé dans la console de GOAD, et on peut installer les machines pour Virtualbox : 
```bash
exit
```

Et de retour dans le terminal bash on fait : 
```bash=
# On commence par installer la machine GOAD Ansible 
sudo docker build -t goadansible .
# Et on installe le tout
./goad.sh -t install -l GOAD -p virtualbox -m docker
```
![](https://hedgedoc.botturi.fr/uploads/4f0adf2f-54fb-4f85-a728-fdee66b5185d.png)

Je risque d'avoir une erreur de desync : 
![](https://hedgedoc.botturi.fr/uploads/33ee6c05-6238-41f5-831a-2bb2fe9d86c1.png)
![](https://hedgedoc.botturi.fr/uploads/522990c9-1b62-4137-9e3f-062f784b5d0a.png)

Ainsi je la corrige en faisant : 
```bash=
./goad.sh
load 870f5f-goad-virtualbox
provision_lab_from vulnerabilities.yml
```
A la fin les erreurs ont bien été corrigées et tout semble bon : 
![](https://hedgedoc.botturi.fr/uploads/058a3b79-2235-4f8f-a848-91b5036ea066.png)

On constate bien que les VM sont apparues sur Virtualbox : 
![](https://hedgedoc.botturi.fr/uploads/f8c761a8-6234-42f6-a4fb-28964c90ffc5.png)


En effet quand on se connecte depuis Virtualbox sur la machine en erreur on voit bien que la connection au domaine et le service SQL Tourne : 
![](https://hedgedoc.botturi.fr/uploads/d4acd556-07cd-4b5f-823c-6b340f383f21.png)

# 2/ Rendre les VMs accessibles sur le réseau

Pour chaque VM, nous allons modifier l'interface NAT par une interface pont réseau pour qu'elle soit accessible. Pour cela on se rends dans les paramètres de la VM, dans Réseau, et on passe du type NAT à pont réseau : 
![](https://hedgedoc.botturi.fr/uploads/3b8455fb-646d-490f-8b8d-de086418b4c8.png)

Ensuite on va forcer les IPs en dur pour qu'elles correspondent à notre plan. Pour cela on fait `ncpa.cpl` dans un terminal et on indique les adresses IP dans Ethernet (clic droit > properties > Internet Protocol V4) : 
![](https://hedgedoc.botturi.fr/uploads/b18396f8-1c5d-41e3-9255-ef0903ca6bd6.png)
![](https://hedgedoc.botturi.fr/uploads/9ea9a54c-829c-4eb4-93bc-1dcba81f1597.png)
![](https://hedgedoc.botturi.fr/uploads/d5d98c57-f1b9-4574-a7af-e86676adc14a.png)
Et on renseigne les bons paramètres IPs : 
![](https://hedgedoc.botturi.fr/uploads/e1334420-12fa-465b-98ce-6de9556e0cfd.png)

Ensuite on reboot le serveur : 
![](https://hedgedoc.botturi.fr/uploads/986ea734-30a9-4683-861c-87ea7ec280f4.png)

Les tests nous montrent bien que le réseau fonctionne : 
![](https://hedgedoc.botturi.fr/uploads/4eedfd6c-e6e1-4048-9374-a2ebf38d31be.png)

Les serveurs eux doivent rester leurs propres DNS primaire : 
![](https://hedgedoc.botturi.fr/uploads/7e21c2b1-a294-4ab7-9d3e-bbfe5bf8be80.png)

Nos VMS sont désormais prêtes.