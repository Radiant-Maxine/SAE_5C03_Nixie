# GESTION DE PROJET - SAE 5C03 Cybersécurité

**SAE:** Proof of Concept Blue Team / Red Team - Environnement GOAD  
**Équipe:**  Maxine Botturi et Syrine Benkadhi 
**Durée:** 10 jours (20/01/2026 - 30/01/2026)  


---

## 1. Introduction & Contexte

### Contexte du projet

Dans le cadre de la SAE 5C03 Cybersécurité, ce projet consiste à déployer un environnement de détection d'intrusions combinant approches Blue Team et Red Team. Notre objectif est d'évaluer l'efficacité de plusieurs solutions de détection (SIEM, IDS, collecteurs de logs) face à des scénarios d'attaque sur un Active Directory vulnérable.

### Objectifs et livrables

Notre projet vise à :
- Déployer l'environnement GOAD (5 machines Windows en domaine Active Directory)
- Mettre en œuvre Wazuh, Elastic, Suricata et OpenWEC
- Automatiser le déploiement des agents via Ansible
- Réaliser des tests d'intrusion documentés
- Analyser l'efficacité comparative des solutions de détection

Les livrables attendus comprennent une synthèse technique de 5 à 10 pages, des annexes techniques détaillées, un rapport de gestion de projet, un dépôt GitHub structuré, et une soutenance prévue le 30 janvier 2026 accompagné d'un diaporama de présentation.


### Organisation de l'équipe

Nous avons réparti le travail selon nos domaines de compétence tout en maintenant une collaboration étroite sur l'ensemble des tâches :

**Blue Team (Syrine) :**
- Wazuh (installation, configuration)
- Elastic Stack (installation, configuration)
- Déploiement des agents via Ansible (Wazuh et Elastic)
- Remontée des logs Sysmon sur Wazuh
- Exegol (installation via pipx)
- Analyse des alertes et détections
- Gestion de projet

**Red Team & Infrastructure (Maxine) :**
- Déploiement environnement GOAD
- OpenWEC et Suricata
- Configuration Sysmon
- Dashboard Streamlit avec IA
- Exegol (installation via pip et Docker)
- Tests d'intrusion et collecte de traces
- Analyse comparative des solutions

Cette répartition nous a permis de travailler en parallèle durant la phase d'installation (semaine 1) tout en collaborant pour l'analyse comparative (semaine 2).

---

## 2. Méthodologie appliquée

### Approche agile

Nous avons mené le projet sur 2 phases d'une semaine chacune, adaptée aux contraintes de temps et à la taille de notre équipe.

| Phase | Période | Objectif principal | Durée |
|--------|---------|-------------------|-------|
| **Phase 1** | 20-24 janvier | Infrastructure & Détection | 5 jours |
| **Phase 2** | 27-30 janvier | Tests & Analyse | 4 jours |

### Organisation du travail

**Répartition des rôles :**

| Domaine | Syrine (Blue) | Maxine (Red + Infra) |
|---------|---------------|---------------------|
| **SIEM** | Wazuh, Elastic | - |
| **Collecteur logs** | - | OpenWEC |
| **IDS** | - | Suricata |
| **Monitoring** | Remontée logs Sysmon, Ansible | Configuration Sysmon |
| **Infrastructure** | - | GOAD (5 VMs) |
| **Attaque** | Exegol (pipx) | Exegol (pip/Docker), Tests intrusion |
| **Analyse** | Détections SIEM | Analyse comparative, Dashboard IA |
| **Gestion projet** | Rapport gestion de projet | - |

### Outils de gestion

| Outil | Usage | Avantages |
|-------|-------|-----------|
| **Trello** | Gestion des tâches (À faire → En cours → Terminé) | Visualisation claire de l'avancement |
| **GitHub** | Dépôt central (code, configs, docs, logs) | Traçabilité par commits, organisation structurée |
| **Réunions quotidiennes** | Synchronisation d'équipe et résolution de blocages | Réactivité face aux problèmes techniques |

### Découpage en phases

#### Phase 1 : Infrastructure & Détection (20-24 janvier)

**Objectif :** Environnement complet avec toutes les solutions opérationnelles

**Étapes importantes :**
- ✅ Jour 1 (20/01) : GOAD déployé + Wazuh installé
- ✅ Jour 2 (21/01) : Wazuh configuré + agents connectés
- ✅ Jour 3 (22/01) : Ansible opérationnel + Elastic en cours
- ✅ Jour 4 (23/01) : Suricata + procédures documentées
- ✅ Jour 5 (24/01) : Validation infrastructure complète

#### Phase 2 : Tests & Analyse (27-30 janvier)

**Objectif :** Tests d'intrusion + analyse comparative + livrables finaux

**Étapes importantes :**
- ✅ Jour 6 (27/01) : OpenWEC + Dashboard IA + Elastic finalisé + Suricata configuré
- ✅ Jour 7 (28/01) : Exegol + premières attaques Kerberos + traces collectées
- 🔄 Jour 8 (29/01) : Analyse comparative en cours + rédaction
- 📋 Jour 9 (30/01) : Finalisation synthèse + soutenance + réinitialisation matériel

---

## 3. Planification initiale



| Période | Nombre de jours | Heures par jour | Total par personne | Total équipe |
|---------|-----------------|-----------------|-------------------|--------------|
| Semaine 1 | 4j + 1j court | 4×7h30 + 1×3h45 | 33h45 | 67h30 |
| Semaine 2 | 4j + 1j court | 4×7h30 + 1×3h45 | 33h45 | 67h30 |
| **TOTAL** | **10 jours** | - | **67h30** | **135h** |

### Découpage des phases et tâches principales

#### Phase 1 : Infrastructure & Détection (Semaine 1)

| Tâche | Responsable | Estimation | Dépendances |
|-------|-------------|-----------|-------------|
| Initialisation repo GitHub + structure | Les deux | 2h | - |
| Schéma architecture réseau | Les deux | 3h | - |
| Déploiement GOAD (5 VMs Windows) | Maxine | 8h | Schéma réseau |
| Installation Wazuh | Syrine | 5h | - |
| Configuration Wazuh | Syrine | 6h | Installation Wazuh |
| Installation Elastic Stack | Syrine | 5h | - |
| Configuration Elastic | Syrine | 5h | Installation Elastic |
| Installation OpenWEC | Maxine | 7h | GOAD opérationnel |
| Configuration Sysmon | Maxine | 4h | GOAD opérationnel |
| Remontée logs Sysmon sur Wazuh | Syrine | 3h | Sysmon configuré |
| Playbooks Ansible agents | Syrine | 6h | Wazuh/Elastic installés |
| Installation Suricata | Maxine | 5h | - |
| Configuration Suricata + Sigma Rules | Maxine | 3h | Installation Suricata |
| Dashboard Streamlit IA | Maxine | 6h | OpenWEC opérationnel |

**Total estimé Phase 1 : ~68h**

#### Phase 2 : Tests & Analyse (Semaine 2)

| Tâche | Responsable | Estimation | Dépendances |
|-------|-------------|-----------|-------------|
| Installation Exegol | Les deux | 3h | - |
| Installation BloodHound/SharpHound | Maxine | 4h | Exegol |
| Cartographie AD | Maxine | 3h | BloodHound |
| Scénarios d'attaque (Kerberos, etc.) | Maxine | 8h | Cartographie AD |
| Collecte traces attaques | Les deux | 4h | Attaques lancées |
| Analyse alertes Wazuh | Syrine | 3h | Traces collectées |
| Analyse alertes Elastic | Maxine | 3h | Traces collectées |
| Analyse alertes Suricata | Maxine | 2h | Traces collectées |
| Analyse comparative solutions | Les deux | 5h | Toutes analyses faites |
| Rédaction synthèse technique | Les deux | 8h | Analyse terminée |
| Rédaction annexes techniques | Les deux | 6h | - |
| Préparation soutenance | Les deux | 3h | Synthèse finalisée |
| Réinitialisation matériel | Les deux | 1h | Après soutenance |

**Total estimé Phase 2 : ~53h**

### Etapes critiques

| Date | Etape | Critère de validation |
|------|-------|----------------------|
| **24/01** | Fin Phase 1 - Infrastructure complète | Tous les SIEM/IDS/collecteurs opérationnels avec agents déployés |
| **28/01** | Attaques réalisées + traces collectées | Au moins 3 scénarios d'attaque documentés avec logs |
| **29/01** | Analyse comparative terminée | Tableau comparatif d'efficacité finalisé |
| **30/01 matin** | Synthèse finale + annexes prêtes | Documents complets pour le rendu |
| **30/01 après-midi** | Soutenance + réinitialisation | Présentation effectuée + matériel nettoyé |

### Risques identifiés en amont

| Risque | Impact | Probabilité | Plan d'atténuation |
|--------|--------|-------------|-------------------|
| GOAD ne se déploie pas correctement | ⚠️ Critique | Moyenne | Snapshots réguliers, documentation Orange Cyberdefense |
| Problèmes de communication agents SIEM | ⚠️ Élevé | Élevée | Tests firewall Windows, config réseau validée en amont |
| Manque de temps pour analyse comparative | ⚠️ Moyen | Élevée | Prioriser 2-3 scénarios d'attaque représentatifs |
| Retard sur déploiement Suricata | ⚠️ Moyen | Moyenne | Documentation en parallèle, support communauté |
| Oubli réinitialisation matériel | ⚠️ Élevé | Faible | Checklist finale obligatoire, alarme rappel |

---

## 4. Bilan chiffré & Suivi du temps

### Temps de travail par personne

| Période | Syrine | Maxine | Total équipe |
|---------|--------|--------|---------------|
| **Semaine 1** (20-24 janvier) | 32h | 36h | 68h |
| **Semaine 2** (27-30 janvier) | 35h30 | 36h30 | 72h |
| **TOTAL PROJET** | **67h30** | **72h30** | **140h** |

### Répartition du temps par catégorie de tâches

| Catégorie | Syrine | Maxine | Total | % du projet |
|-----------|--------|--------|-------|-------------|
| **Infrastructure & GOAD** | 3h | 17h | 20h | 14% |
| **SIEM (Wazuh + Elastic)** | 26h | 0h | 26h | 19% |
| **Collecteur logs (OpenWEC)** | 0h | 13h | 13h | 9% |
| **IDS & Détection (Suricata, Sysmon)** | 4h | 12h | 16h | 11% |
| **Automatisation (Ansible)** | 6h | 0h | 6h | 4% |
| **Dashboard IA** | 0h | 7h | 7h | 5% |
| **Red Team (Exegol, attaques)** | 3h | 13h | 16h | 11% |
| **Analyse & Tests** | 8h | 7h | 15h | 11% |
| **Documentation** | 10h | 6h | 16h | 11% |
| **Gestion de projet** | 4h30 | 0h30 | 5h | 4% |
| **TOTAL** | **67h30** | **72h30** | **140h** | **100%** |

### Graphiques à créer pour le rendu

#### Graphique 1 : Répartition du temps par personne (Diagramme en barres)

```
[À générer avec Excel/Python/autre outil]

Axes :
- X : Catégories de tâches (Infrastructure, SIEM, IDS, Red Team, etc.)
- Y : Heures de travail
- Deux barres par catégorie : Syrine (bleu) vs Maxine (rouge)
```

#### Graphique 2 : Répartition globale par type de tâche (Camembert)

```
[À générer avec Excel/Python/autre outil]

Parts du camembert :
- SIEM : 19%
- Infrastructure : 14%
- Documentation : 11%
- IDS & Détection : 11%
- Red Team : 11%
- Analyse & Tests : 11%
- Collecteur logs : 9%
- Dashboard : 5%
- Automatisation : 4%
- Gestion projet : 4%
```

#### Graphique 3 : Timeline de progression hebdomadaire (Gantt simplifié ou timeline)

```
[À créer sous forme de timeline visuelle]

Semaine 1 : Infrastructure & Détection (49% du temps)
|████████████████████████████████████|
Jour 1-2 : GOAD + Wazuh + Elastic
Jour 3-4 : Ansible + Sysmon + OpenWEC
Jour 5 : Suricata + Dashboard + Validation

Semaine 2 : Tests & Analyse (51% du temps)
|████████████████████████████████████|
Jour 6-7 : Exegol + Attaques + Collecte traces
Jour 8-9 : Analyse comparative + Rédaction
Jour 10 : Finalisation + Soutenance
```

### Comparaison estimé vs réel

| Phase | Temps estimé | Temps réel | Écart | Commentaire |
|-------|--------------|-----------|-------|-------------|
| **Phase 1 : Infrastructure** | 68h | ~68h | 0h | Estimation correcte malgré problèmes réseau |
| **Phase 2 : Tests & Analyse** | 53h | ~72h | +19h | Complexité analyse + rédaction sous-estimée |
| **TOTAL** | **121h** | **140h** | **+19h** | Budget temps respecté grâce aux 2 personnes |



---

## 5. Risques & Gestion

### Risques identifiés et gestion

| # | Risque | Impact | Probabilité | Statut | Actions menées |
|---|--------|--------|-------------|--------|----------------|
| **R1** | GOAD ne se déploie pas correctement | Critique | Moyenne | ✅ Géré | Suivi strict documentation Orange Cyberdefense, snapshots VMs réguliers, +2h de débogage |
| **R2** | Agents SIEM ne communiquent pas avec serveurs | Élevé | Élevée | ✅ Géré | Tests firewall Windows, validation config réseau, déploiement Ansible progressif |
| **R3** | Problèmes réseau entre GOAD et infrastructure salle | Élevé | Moyenne | ⚠️ Survenu | Reconfiguration réseau VirtualBox, tests connectivité, +3h perdues |
| **R4** | Retard déploiement Suricata | Moyen | Moyenne | ✅ Géré | Documentation en parallèle, tests de placement réseau optimisés |
| **R5** | Manque de temps pour analyse comparative | Moyen | Élevée | ⚠️ Partiellement | Priorisation 2-3 scénarios d'attaque clés (Kerberos principalement) |
| **R6** | Installation Elastic complexe | Moyen | Élevée | ⚠️ Survenu | Troubleshooting documenté (Windows/Debian), +3h supplémentaires |
| **R7** | Synthèse finale bâclée (deadline 30/01) | Critique | Élevée | 🔄 En cours | Début rédaction dès 29/01, template préparé, répartition sections |
| **R8** | Oubli réinitialisation matériel | Élevé | Faible | 📋 Planifié | Checklist finale créée, alarme rappel 30/01 après-midi |

### Problèmes rencontrés et solutions

**Problème 1 : Connectivité réseau GOAD ↔ Infrastructure**
- **Description :** Les VMs GOAD ne communiquaient pas correctement avec nos serveurs SIEM/IDS
- **Impact :** Retard de 3h sur déploiement agents
- **Solution appliquée :** Nous avons reconfiguré le mode réseau VirtualBox (bridge + NAT), validation ping/telnet systématique
- **Leçon apprise :** Valider l'architecture réseau complète avant de déployer les agents

**Problème 2 : Installation Elastic sous-estimée**
- **Description :** Configuration Elasticsearch + Kibana + Fleet plus complexe que prévu
- **Impact :** +3h par rapport à notre estimation initiale
- **Solution appliquée :** Nous avons créé une documentation troubleshooting, tests sur Debian puis Windows
- **Leçon apprise :** Prévoir du temps de débogage pour des outils non maîtrisés

**Problème 3 : Compression du temps d'analyse**
- **Description :** Phase 1 plus longue que prévu, réduisant le temps disponible pour l'analyse comparative
- **Impact :** Limitation à 2-3 scénarios d'attaque au lieu de 5-6 prévus
- **Solution appliquée :** Nous avons focalisé sur les attaques Kerberos (très représentatives), collecte traces précise
- **Leçon apprise :** Prévoir une marge de sécurité de 20% sur les estimations

### Décisions d'ajustement prises

| Date | Décision | Justification | Impact |
|------|----------|---------------|--------|
| **22/01** | Ajout dashboard Streamlit IA pour OpenWEC | Valoriser le collecteur, faciliter analyse logs | +6h de dev mais gain en analyse |
| **24/01** | Report finalisation Elastic à semaine 2 | Prioriser infrastructure GOAD fonctionnelle | Réorganisation planning semaine 2 |
| **27/01** | Priorisation attaques Kerberos uniquement | Manque de temps pour scénarios multiples | Focus qualité > quantité |
| **28/01** | Répartition rédaction synthèse 50/50 | Deadline serrée 30/01 | Parallélisation rédaction |

### Gestion des imprévus

**Stratégies que nous avons appliquées :**
- **Communication quotidienne** : Point rapide chaque matin pour identifier blocages
- **Priorisation dynamique** : Ajustement Trello en temps réel selon contraintes
- **Documentation continue** : Rédaction procédures au fur et à mesure pour gagner du temps semaine 2
- **Entraide technique** : Nous nous sommes dépannées mutuellement sur les blocages

**Outils de mitigation :**
- Snapshots des VMs 
- Scripts de déploiement versionnés sur Git
- Documentation troubleshooting centralisée dans DOCS/04_troubleshooting/

---

## 6. Rétrospective : Win/Fail & Leçons apprises

### Ce qui a bien fonctionné (Wins) 🎉

| Aspect | Description | Impact positif |
|--------|-------------|----------------|
| **Organisation GitHub** | Structure de dossiers claire dès le départ (DOCS, CONFIGS, AUTOMATION, LOGS) | Gain de temps énorme, pas de perte de fichiers, collaboration fluide |
| **Répartition Blue/Red Team** | Séparation des rôles claire : Syrine (détection) / Maxine (infra + attaque) | Travail en parallèle efficace semaine 1, expertise ciblée |
| **Automatisation Ansible** | Déploiement agents Wazuh et Elastic automatisé sur toutes les VMs | Reproductibilité, gain de temps, moins d'erreurs manuelles |
| **GOAD déployé rapidement** | Environnement AD vulnérable opérationnel en 1 jour | Respect du planning, base solide pour la suite |
| **Documentation continue** | Procédures rédigées au fur et à mesure des installations | Pas de stress en fin de projet, annexes prêtes |
| **Dashboard Streamlit IA** | Innovation non prévue initialement pour valoriser OpenWEC | Différenciation du projet, démo visuelle impressionnante |
| **Gestion Trello efficace** | Kanban simple et clair, mis à jour régulièrement | Vision d'avancement partagée, pas de tâches oubliées |
| **Communication quotidienne** | Points rapides chaque matin au labo | Résolution rapide des blocages, entraide technique |
| **Collaboration étroite** | Travail réellement ensemble sur l'ensemble du projet | Complémentarité des compétences, entraide constante |

### Ce qui n'a pas fonctionné (Fails) ❌

| Aspect | Description | Impact négatif | Amélioration possible |
|--------|-------------|----------------|----------------------|
| *[À compléter en fin de projet]* | | | |
| | | | |
| | | | |
| | | | |


---

## 7. Conclusion

Notre projet de 10 jours nous a permis de déployer avec succès un environnement de détection complet (GOAD + Wazuh + Elastic + OpenWEC + Suricata) et d'analyser son efficacité face à des attaques réelles. 

La méthodologie agile que nous avons appliquée, combinée à une répartition claire des rôles, une collaboration étroite et à l'automatisation via Ansible, nous a permis de respecter la deadline du 30 janvier malgré un planning serré et des imprévus techniques.

Au-delà des compétences techniques en cybersécurité (SIEM, IDS, Red Team) que nous avons développées, ce projet a renforcé nos capacités en gestion de projet, priorisation et adaptation face aux contraintes. La principale leçon que nous retenons est l'importance de prévoir des marges sur les estimations et de documenter en continu plutôt qu'à posteriori.

Les livrables attendus (synthèse technique, annexes, dépôt GitHub structuré) sont prêts pour la soutenance, démontrant notre capacité à mener un projet technique complexe en autonomie.

---

**Dernière mise à jour :** 29/01/2026  
**Statut :** Document finalisé, prêt pour le rendu
