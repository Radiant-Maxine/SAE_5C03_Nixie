# 🛡️ SIEM Wazuh

Configuration de [Wazuh](https://wazuh.com/) pour la détection d'intrusion et la conformité.

## 🎯 Objectif

- Détection d'intrusion (HIDS)
- Analyse des logs Windows/Linux
- Vérification d'intégrité (FIM)
- Détection de vulnérabilités

## 📦 Architecture

```
┌─────────────────┐     ┌─────────────────┐
│  Wazuh Manager  │◄────│  Wazuh Agents   │
│   (server)      │     │  (endpoints)    │
└────────┬────────┘     └─────────────────┘
         │
         ▼
┌─────────────────┐
│  Wazuh Indexer  │ (OpenSearch)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Wazuh Dashboard │ (Web UI)
└─────────────────┘
```

## 🔌 Ports

| Port | Service | Description |
|------|---------|-------------|
| 1514 | TCP/UDP | Agent communication |
| 1515 | TCP | Agent enrollment |
| 55000 | TCP | Wazuh API |
| 443 | TCP | Dashboard HTTPS |

## 🚀 Déploiement

```bash
# Via Docker (all-in-one)
docker-compose up -d

# Accès dashboard
https://localhost:443
# User: admin / Password: SecretPassword (à changer!)
```

## 📋 Règles de détection

Wazuh inclut des règles pour :
- MITRE ATT&CK mapping
- Détection Mimikatz, PsExec, etc.
- Bruteforce authentication
- Suspicious PowerShell

## 🔗 Ressources

- [Wazuh Documentation](https://documentation.wazuh.com/)
- [Wazuh Ruleset](https://github.com/wazuh/wazuh-ruleset)
