# 🔧 CONFIGS

Fichiers de configuration pour l'ensemble de l'infrastructure Blue Team / Red Team.

> ⚠️ **Important** : Ne jamais commiter de secrets (mots de passe, clés API, certificats privés). Utilisez `.env.example` comme template.

## 📂 Structure

| Dossier | Description | Composant |
|---------|-------------|----------|
| `goad/` | Configuration du lab Active Directory vulnérable | [GOAD](https://github.com/Orange-Cyberdefense/GOAD) |
| `openwec/` | Collecteur de logs Windows (WEF/WEC) | [OpenWEC](https://github.com/cea-sec/openwec) |
| `siem_elasticsearch/` | Stack ELK pour analyse des logs | Elasticsearch + Kibana |
| `siem_wazuh/` | SIEM open-source avec détection d'intrusion | [Wazuh](https://wazuh.com/) |
| `suricata/` | IDS/IPS réseau | [Suricata](https://suricata.io/) |
| `sysmon/` | Monitoring système Windows | [Sysmon](https://docs.microsoft.com/sysinternals/downloads/sysmon) |

## 🔄 Flux de données

```
┌─────────────────────────────────────────────────────────────────┐
│                        GOAD Lab (VirtualBox)                    │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐            │
│  │  DC01   │  │  SRV01  │  │  WKS01  │  │  WKS02  │            │
│  │ Sysmon  │  │ Sysmon  │  │ Sysmon  │  │ Sysmon  │            │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘            │
│       │            │            │            │                  │
│       └────────────┴─────┬──────┴────────────┘                  │
│                          │ WinRM/WEF                            │
└──────────────────────────┼──────────────────────────────────────┘
                           ▼
                    ┌─────────────┐
                    │   OpenWEC   │ ← Collecte centralisée
                    └──────┬──────┘
                           │ JSON/Syslog
              ┌────────────┴────────────┐
              ▼                         ▼
      ┌───────────────┐         ┌───────────────┐
      │ Elasticsearch │         │    Wazuh      │
      │   + Kibana    │         │   Manager     │
      └───────────────┘         └───────────────┘
              ▲                         ▲
              │                         │
              └─────────┬───────────────┘
                        │
                 ┌──────┴──────┐
                 │  Suricata   │ ← IDS réseau
                 │  (mirror)   │
                 └─────────────┘
```

## 🚀 Déploiement rapide

```bash
# 1. Copier le template d'environnement
cp .env.example .env

# 2. Éditer les variables
nano .env

# 3. Lancer le déploiement
./init.sh
```

## 📝 Convention de nommage

- `*.example` : Templates à copier et adapter
- `*.local` : Fichiers locaux (gitignorés)
- `*.bak` : Sauvegardes (gitignorées)
