# 🪟 powershell

Scripts PowerShell : activer audit, installer Sysmon, config WinRM.

# PowerShell – scripts Windows (GOAD / préparation hôtes)

Ce dossier regroupe des scripts PowerShell utilisés pour **préparer les hôtes Windows** de l’environnement GOAD.
Ils servent principalement à automatiser la mise en place des prérequis nécessaires à nos déploiements (WinRM pour Ansible, configuration système, etc.) avant la collecte des logs (ex : Sysmon / Event Logs).

> ⚠️ Ces scripts sont destinés à un **lab pédagogique** (GOAD). Ils ne sont pas pensés pour un environnement de production.

---

## Contenu

### `goad_vagrant_scripts/`
Scripts exécutés lors du provisioning Vagrant (création/initialisation des VMs).

- `ConfigureRemotingForAnsible.ps1`  
  Configure **WinRM** et les paramètres nécessaires pour permettre l’administration distante via **Ansible**.

- `enable-winrm.ps1` / `disable-winrm.ps1`  
  Active/désactive WinRM (utile pour sécuriser ou pour des tests).

- `fixnetwork.ps1` / `fix_ip.ps1`  
  Ajuste la configuration réseau (résolution de soucis IP/DNS possibles lors du provisioning).

- `set-powerplan.ps1`  
  Met un plan d’alimentation “performance” pour éviter des comportements imprévisibles (mise en veille, etc.).

- `disable-screensaver.ps1`  
  Désactive l’économiseur d’écran pour éviter les interruptions pendant les démos/tests.

- `win-updates.ps1`  
  Gère les updates Windows durant la phase de build/provisioning.

- `unattend.xml` / `Autounattend.xml`  
  Fichiers de réponse Windows utilisés pour l’installation automatique (langue, paramètres initiaux, etc.).

---

### `goad_packer_scripts/`
Scripts utilisés pendant la **construction d’images** Windows (Packer).  
Objectif : produire des VMs prêtes à être utilisées dans le lab GOAD.

On retrouve généralement les mêmes actions que côté Vagrant (WinRM, réseau, power plan, updates, etc.), mais appliquées au moment de la génération de l’image.

---

## Lien avec notre SAE (pipeline logs Windows)
Ces scripts permettent d’obtenir des machines Windows :
- administrables à distance (WinRM/Ansible),
- correctement configurées (réseau, paramètres système),
- prêtes à recevoir nos outils de collecte (ex : **Sysmon**, agents, forwarding Event Logs).

La configuration Sysmon utilisée pour la collecte est versionnée dans :
- `CONFIGS/sysmon/sysmonconfig-export.xml`
- `CONFIGS/sysmon/bin/Sysmon.zip`

---

## Notes
- Les scripts GOAD peuvent contenir des valeurs “lab” (ex : comptes/services).  
  Avant tout partage public, vérifier l’absence de secrets.
