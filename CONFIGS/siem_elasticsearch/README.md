# 🔍 SIEM Elasticsearch

Stack ELK (Elasticsearch, Logstash, Kibana) pour l'analyse des logs.

## 🎯 Objectif

- Indexation des événements Windows/Sysmon
- Visualisation via Kibana
- Corrélation et alerting

## 📦 Composants

| Service | Port | Description |
|---------|------|-------------|
| Elasticsearch | 9200 | Moteur de recherche/indexation |
| Kibana | 5601 | Interface web de visualisation |
| Logstash | 5044 | Pipeline d'ingestion |

## 🚀 Déploiement

```bash
# Démarrer la stack
docker-compose up -d

# Accéder à Kibana
open http://localhost:5601
```

## 📊 Dashboards recommandés

- **Sysmon Overview** : Vue d'ensemble des événements Sysmon
- **Authentication** : Tentatives de connexion (succès/échecs)
- **Process Creation** : Exécution de processus suspects
- **Network Connections** : Connexions réseau sortantes

## ⚙️ Index patterns

```
winlogbeat-*     # Logs Windows natifs
sysmon-*         # Événements Sysmon
suricata-*       # Alertes IDS
```

## 🔗 Ressources

- [Elastic SIEM](https://www.elastic.co/security)
- [Sigma Rules](https://github.com/SigmaHQ/sigma) - Règles de détection
