# 🏰 GOAD - Game of Active Directory

Configuration du lab Active Directory vulnérable basé sur [GOAD](https://github.com/Orange-Cyberdefense/GOAD).

## 🎯 Objectif

Fournir un environnement réaliste pour :
- Tests d'intrusion Active Directory
- Détection d'attaques (Blue Team)
- Collecte et analyse de logs

## 🖥️ Machines virtuelles

| VM | IP | Rôle | OS |
|----|-----|------|----|
| DC01 | 192.168.56.10 | Domain Controller (севенки́нгдом.local) | Windows Server 2019 |
| DC02 | 192.168.56.11 | Domain Controller (essos.local) | Windows Server 2019 |
| SRV02 | 192.168.56.22 | File Server | Windows Server 2019 |
| WKS01 | 192.168.56.110 | Workstation | Windows 10 |
| WKS02 | 192.168.56.111 | Workstation | Windows 10 |

## 🌐 Réseau

- **Interface** : vboxnet0
- **Subnet** : 192.168.56.0/24
- **Gateway** : 192.168.56.1 (host)

## 📦 Prérequis

- VirtualBox 7.x
- Vagrant 2.3+
- 32 Go RAM minimum
- 100 Go espace disque

## 🚀 Installation

```bash
# Cloner GOAD
git clone https://github.com/Orange-Cyberdefense/GOAD.git
cd GOAD

# Lancer le lab
./goad.sh -t install -l GOAD -p virtualbox
```

## 🔗 Ressources

- [Documentation GOAD](https://github.com/Orange-Cyberdefense/GOAD)
- [Attaques AD communes](https://adsecurity.org/)
