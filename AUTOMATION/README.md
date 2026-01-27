# 🤖 AUTOMATION

Scripts d'automatisation pour le déploiement et la gestion du lab.

## 📂 Structure

```
AUTOMATION/
├── ansible/      # Playbooks Ansible
├── bash/         # Scripts shell Linux
├── powershell/   # Scripts PowerShell Windows
└── python/       # Scripts Python
```

## 🎯 Objectifs

- Déploiement automatisé des agents (Sysmon, Wazuh)
- Configuration des GPO (audit policy, WEF)
- Collecte de logs et preuves
- Tests de validation

## 🚀 Scripts disponibles

### Ansible

```bash
# Déployer Sysmon sur toutes les machines Windows
ansible-playbook -i inventory.yml deploy-sysmon.yml

# Configurer WEF (Windows Event Forwarding)
ansible-playbook -i inventory.yml configure-wef.yml
```

### Bash

```bash
# Initialisation complète du lab
./init.sh

# Collecte des logs
./collect-logs.sh
```

### PowerShell

```powershell
# Installation Sysmon
.\Install-Sysmon.ps1 -ConfigPath .\sysmonconfig.xml

# Vérification de la config audit
.\Check-AuditPolicy.ps1
```

## 📝 Conventions

- Les scripts doivent être idempotents (relançables sans effet de bord)
- Documenter les prérequis en en-tête
- Utiliser des variables pour les chemins/IPs
- Logguer les actions importantes
