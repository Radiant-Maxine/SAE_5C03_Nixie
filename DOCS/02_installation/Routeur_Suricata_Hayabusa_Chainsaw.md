Création du routeur Suricata
---

# 1/ Setup réseau

On va commencer par mettre en dur sur notre machines ces paramètres réseaux : 
```bash=
# This file describes the network interfaces available on your system
# and how to activate them. For more information, see interfaces(5).

source /etc/network/interfaces.d/*

# The loopback network interface
auto lo
iface lo inet loopback

# The primary network interface
allow-hotplug enp0s3
iface enp0s3 inet static
        address 10.203.19.254
        netmask 255.255.0.0
        gateway 10.203.255.254
        dns-nameservers 10.255.255.200
```
![](https://hedgedoc.botturi.fr/uploads/fd9258f9-03f5-4994-ace2-303f337ed9b9.png)

Afin de donner à la machine l'adresse `10.203.19.254` et la Gateway de la salle.

# 2/ Mise en place du Forwarding IP & du NAT 

Pour activer l'IPv4 Forwarding on fait les commandes : 
```bash=
echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf
sysctl -p
```

Ensuite on utilise NFTables pour le NAT : 
```bash=
nft add table ip nat
nft add chain ip nat postrouting { type nat hook postrouting priority 100 \; }
nft add rule ip nat postrouting oifname "enp0s3" counter masquerade
# Pour rendre persistant :
nft list ruleset > /etc/nftables.conf
systemctl enable nftables
```
![](https://hedgedoc.botturi.fr/uploads/9b33bcf3-ab95-4ad0-9a40-aa91a5ca20ee.png)

# 3/ Installation et Configuration de Suricata

## 3.1/ Installation
Ensuite on installe Suricata depuis les dépôts : 
```bash=
apt update && apt install suricata -y
```

Ensuite, nous allons changer la configuration de Suricata pour que seuls les paquets à destination de 10.203.19.0/24 soient traités. Ainsi on modifie le fichier de configuration : 
```bash=
nano /etc/suricata/suricata.yaml
```

## 3.2/ Configuration des réseaux internes et externes
Ensuite, on va définir le HOME NET à notre réseau interne : 
```yaml=

vars:
  # more specific is better for alert accuracy and performance
  address-groups:
    HOME_NET: "[10.203.19.0/24]"
```
![](https://hedgedoc.botturi.fr/uploads/44a2f021-b0ed-4213-bd7d-1e6219c39453.png)

On laisse le EXTERNAL NET comme "!\$HOME_NET" pour que toute machine en dehors de ce réseau soit considérée comme potentiellement attaquante. 
```yaml=
    EXTERNAL_NET: "!$HOME_NET"
```

![](https://hedgedoc.botturi.fr/uploads/3837452c-1436-4944-b1bc-ffe09c9af122.png)

## 3.3/ Mise en place du filtre : 

Ensuite nous allons mettre un filtre réseau pour que seul les paquets concernant le réseau `10.203.19.0/24` soit analysés : 


On va référencer ce filtre dans la conf de Suricata. Dans la partie *af-packet*, on rajoute le paramètre : `    bpf-filter: "10.203.19.0/24"` dans le fichier de conf : 
```bash=
nano /etc/suricata/suricata.yaml
```
: 
![](https://hedgedoc.botturi.fr/uploads/758663c0-7f65-4220-85fe-08522e5f6b55.png)

# 4/ Mise en place de Hayabusa

# 4.1/ Installation
On commence par installer le soft sur le serveur : 
```bash=
cd /opt
# On télécharge le binaire Linux 64 bits (version musl pour avoir la version de glibc embarquée)
wget https://github.com/Yamato-Security/hayabusa/releases/download/v3.7.0/hayabusa-3.7.0-lin-x64-musl.zip
```
![](https://hedgedoc.botturi.fr/uploads/43f9b9c2-7acf-4e69-bafe-4d03420a2fde.png)

Ensuite, on unzip le fichier : 
```bash=
apt install unzip -y
unzip hayabusa-3.7.0-lin-x64-musl.zip -d hayabusa
cd hayabusa
chmod +x hayabusa-3.7.0-lin-x64-musl
mv hayabusa-3.7.0-lin-x64-musl hayabusa
```
![](https://hedgedoc.botturi.fr/uploads/756b137b-6775-4050-8888-01d70ec13789.png)

## 4.2/ Configuration des règles
Après, on va charger les règles hayabusa : 
```bash=
./hayabusa update-rules
```
![](https://hedgedoc.botturi.fr/uploads/4877e8c3-df13-40e8-868c-b77bff52cf37.png)
![](https://hedgedoc.botturi.fr/uploads/60c191af-f529-4d0b-acac-90463322e59e.png)

# 5/ Chainsaw

De même, on va installer Chainsaw depuis les releases Git. On choisit la version `chainsaw_all_platforms+rules.zip` : 
```bash=
cd /opt/
wget https://github.com/WithSecureLabs/chainsaw/releases/download/v2.13.1/chainsaw_all_platforms+rules.zip
```

Ensuite on dezip le fichier : 
```bash=
unzip chainsaw_all_platforms+rules.zip -d chainsaw
cd chainsaw/chainsaw
chmod +x chmod +x chainsaw_x86_64-unknown-linux-gnu
mv chainsaw_x86_64-unknown-linux-gnu chainsaw
```
![](https://hedgedoc.botturi.fr/uploads/6c9a810a-8be5-4b99-98ac-3c4559791602.png)

# 6/ Ajouter les outils au path

Pour rajouter les outils au PATH, nous allons créer des liens symboliques dans `/usr/local/bin` : 
```bash=
ln -s /opt/chainsaw/chainsaw/chainsaw /usr/local/bin/chainsaw
ln -s /opt/hayabusa/hayabusa /usr/local/bin/hayabusa
```
![](https://hedgedoc.botturi.fr/uploads/721ce285-94ad-4622-886f-eed93f71c05b.png)
