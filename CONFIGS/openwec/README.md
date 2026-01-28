# 📡 OpenWEC - Windows Event Collector

Configuration d'[OpenWEC](https://github.com/cea-sec/openwec) pour la collecte centralisée des logs Windows.

## 🎯 Objectif

Collecter les événements Windows (Security, Sysmon, PowerShell) depuis les machines GOAD vers les SIEMs.

## 📂 Structure

```
openwec/
├── Docker/                      # Déploiement conteneurisé
├── Openwec ESSOS_LOCAL/         # Config pour domaine essos.local
├── Openwec Seventhkingdom.local/ # Config pour domaine sevenkingdoms.local
└── README.md
```

## ⚙️ Configuration

### Subscriptions (événements collectés)

| Subscription | Event IDs | Description |
|--------------|-----------|-------------|
| Security | 4624, 4625, 4648, 4672... | Authentification, privilèges |
| Sysmon | 1, 3, 7, 8, 10, 11... | Process, réseau, fichiers |
| PowerShell | 4103, 4104 | Script block logging |

### Ports

| Port | Protocole | Usage |
|------|-----------|-------|
| 5985 | HTTP | WinRM (non chiffré) |
| 5986 | HTTPS | WinRM (TLS) |

## 🚀 Déploiement

```bash
# Via Docker
cd Docker/
docker-compose up -d

# Vérifier le statut
docker logs openwec
```

## 🔧 Configuration Windows (GPO)

Sur les machines Windows du lab :

```powershell
# Activer WinRM
winrm quickconfig -q

# Configurer le collecteur
wecutil qc /q
```

## 🔗 Ressources

- [OpenWEC GitHub](https://github.com/cea-sec/openwec)
- [Windows Event Forwarding](https://docs.microsoft.com/en-us/windows/security/threat-protection/use-windows-event-forwarding-to-assist-in-intrusion-detection)
