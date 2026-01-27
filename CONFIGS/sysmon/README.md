# 🔬 Sysmon - System Monitor

Configuration de [Sysmon](https://docs.microsoft.com/sysinternals/downloads/sysmon) pour le monitoring avancé Windows.

## 🎯 Objectif

Sysmon enrichit les logs Windows avec :
- Création de processus (ligne de commande complète)
- Connexions réseau par processus
- Chargement de DLL
- Modifications du registre
- Accès fichiers

## 📂 Fichiers

| Fichier | Description |
|---------|-------------|
| `sysmonconfig-export.xml` | Configuration Sysmon exportée |

## 🚀 Installation

```powershell
# Télécharger Sysmon
Invoke-WebRequest -Uri "https://download.sysinternals.com/files/Sysmon.zip" -OutFile Sysmon.zip
Expand-Archive Sysmon.zip

# Installer avec la config
.\Sysmon64.exe -accepteula -i sysmonconfig-export.xml

# Mettre à jour la config
.\Sysmon64.exe -c sysmonconfig-export.xml
```

## 📋 Event IDs principaux

| Event ID | Description | Criticité |
|----------|-------------|----------|
| 1 | Process Create | 🔴 Haute |
| 3 | Network Connection | 🟡 Moyenne |
| 7 | Image Loaded (DLL) | 🟡 Moyenne |
| 8 | CreateRemoteThread | 🔴 Haute |
| 10 | Process Access | 🔴 Haute |
| 11 | File Create | 🟢 Basse |
| 12/13/14 | Registry | 🟡 Moyenne |
| 22 | DNS Query | 🟢 Basse |

## ⚙️ Configuration utilisée

La config inclut des filtres pour :
- ✅ Capturer les processus suspects (mimikatz, powershell encoded, etc.)
- ✅ Tracer les connexions réseau sortantes
- ✅ Détecter les injections de code
- ❌ Exclure le bruit (Windows Update, télémétrie...)

## 🔗 Ressources

- [Sysmon Documentation](https://docs.microsoft.com/sysinternals/downloads/sysmon)
- [SwiftOnSecurity Config](https://github.com/SwiftOnSecurity/sysmon-config) - Config de référence
- [Olaf Hartong Config](https://github.com/olafhartong/sysmon-modular) - Config modulaire
