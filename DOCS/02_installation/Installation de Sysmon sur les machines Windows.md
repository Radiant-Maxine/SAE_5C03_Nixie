Installation de Sysmon sur les machines Windows
---
*Par l'équipe Nixie SAE 5C03*

# 1/ Récupération des assets
Une fois nos VM Windows installées, nous allons pouvoir mettre en place le système de journlisation d'évènements Syslog. Pour cela, nous allons utiliser le Set de Règles très performant [SwiftOnSecurity](https://github.com/SwiftOnSecurity/sysmon-config). 

Ainsi, nous allons commencer par téléchrger Sysmon sur une des machines Windows. Pour cela on se rends à l'adresse https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon.

![](https://hedgedoc.botturi.fr/uploads/b2b3adaf-55c8-45df-beaf-2af1c7c97e8e.png)

On télécharge donc le software. Ensuite, on le Unzip dans un dossier temporaire `C:\Tools\Sysmon` : 
![](https://hedgedoc.botturi.fr/uploads/caa701d6-7e75-4c94-97e6-26ffbac2a104.png)

Après nous allons récupérer la configuration Sysmon de SwiftOnSecurity. Pour cela on se rends à https://github.com/SwiftOnSecurity/sysmon-config/blob/master/sysmonconfig-export.xml et on download la Raw File : 
![](https://hedgedoc.botturi.fr/uploads/b44afc7f-635e-420d-8024-f5df1d34ad2b.png)

Et on la met dans le même répertoire que Sysmon : 
![](https://hedgedoc.botturi.fr/uploads/e501c9f9-d169-425a-92ab-77d50f7b344d.png)

# 2/ Installation de Sysmon

On commence par ouvrir un CMD PowerShell en tant qu'administrateur : 
![](https://hedgedoc.botturi.fr/uploads/dac01335-d708-4fa2-8b09-e322b3ed76dd.png)

Ensuite on va dans notre répertoire : 
```powershell=
cd C:\Tools\Sysmon
```
![](https://hedgedoc.botturi.fr/uploads/ca9a41d6-0063-4e69-8864-0d495e6d766d.png)

Et ensuite on va taper la commande d'installation : 
```powershell=
.\Sysmon64.exe -accepteula -i sysmonconfig-export.xml
```
![](https://hedgedoc.botturi.fr/uploads/ff2c7c16-5812-423a-bac4-5c5a16a39970.png)

Tout est donc ici bien installé. 

# 3/ Vérification

Pour vérifier que le service est bien installé on tape la commande : 
```powershell=
Get-Service sysmon64
```

![](https://hedgedoc.botturi.fr/uploads/73519f3d-b9d4-46d3-af23-d569bdb0e8ed.png)

L'indication running nous confirme que le service est bien installé et actif.

Ensuite on va vérifier qu'il y a bien des entrées logs par Sysmon avec le CMDlet : 
```powershell=
Get-WinEvent -LogName "Microsoft-Windows-Sysmon/Operational" -MaxEvents 10
```
![](https://hedgedoc.botturi.fr/uploads/9c6f97ad-4987-46e9-90d5-44057d823b54.png)

La présence d'évènements nous confirme bien que le service fonctionne. 

# 4/ Test

Pour tester on va lancer un bloc notes avec : 
```powershell=
notepad.exe
```

Et on va vérifier le journal de log : 
![](https://hedgedoc.botturi.fr/uploads/afde2017-3411-439b-aac6-e5d0a33e82d5.png)


On voit bien le message Process Create qui apparait.