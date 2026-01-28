# 🦊 Suricata IDS/IPS

Configuration de [Suricata](https://suricata.io/) pour la détection d'intrusion réseau.

## 🎯 Objectif

- Analyse du trafic réseau (NIDS)
- Détection d'attaques connues (signatures)
- Extraction de métadonnées réseau
- Intégration avec les SIEMs

## 📂 Structure

```
suricata/
├── Agent Wazuh/              # Config agent Wazuh sur la VM Suricata
├── suricata/                 # Fichiers de config Suricata
│   └── suricata.yaml         # Configuration principale
├── var_lib_suricata_rules/   # Règles de détection
│   └── suricata.rules        # Règles actives
└── README.md
```

## ⚙️ Configuration réseau

```yaml
# Dans suricata.yaml
vars:
  address-groups:
    HOME_NET: "[192.168.56.0/24]"      # Réseau GOAD
    EXTERNAL_NET: "!$HOME_NET"
```

## 📡 Mode de capture

Suricata écoute sur l'interface miroir du trafic GOAD :

```bash
# Lancer Suricata
suricata -c /etc/suricata/suricata.yaml -i eth1
```

## 📋 Règles incluses

| Ruleset | Description |
|---------|-------------|
| ET Open | Emerging Threats - règles communautaires |
| Custom | Règles spécifiques au lab |

## 📊 Logs générés

| Fichier | Format | Contenu |
|---------|--------|--------|
| `eve.json` | JSON | Alertes, flux, DNS, HTTP... |
| `fast.log` | Text | Alertes format court |
| `stats.log` | Text | Statistiques de performance |

## 🔗 Ressources

- [Suricata Documentation](https://docs.suricata.io/)
- [ET Open Rules](https://rules.emergingthreats.net/)
