# 📋 GESTION DE PROJET - SAE 5C03 Cybersécurité

**Projet:** Proof of Concept Blue Team / Red Team - Environnement GOAD  
**Équipe:** Syrine Belkadhi et Maxine Botturi 
**Durée:** 2 semaines (19/01/2026 - 30/01/2026)  
**Soutenance:** 30/01/2026

---

## 🎯 1. VUE D'ENSEMBLE

### Objectifs du projet
- Déployer un environnement Active Directory vulnérable (GOAD) sur VirtualBox
- Mettre en œuvre des outils de détection : 2 SIEM (Wazuh + Elastic), IDS (Suricata), collecteur de logs (OpenWEC)
- Automatiser le déploiement des agents avec Ansible
- Cartographier l'AD avec BloodHound/SharpHound
- Réaliser des tests d'intrusion et analyser les détections
- Comparer l'efficacité des différentes méthodes de détection

### Stack technique
- **Infrastructure:** VirtualBox, GOAD (5 VMs Windows AD)
- **SIEM:** Wazuh, Elastic Stack
- **Collecteur logs:** OpenWEC (+ dashboard IA)
- **IDS:** Suricata + Sigma Rules
- **Outils portables:** Chainsaw, Hayabusa
- **Monitoring Windows:** Sysmon, Audit natif
- **Red Team:** Exegol, BloodHound, SharpHound, Neo4J
- **Automatisation:** Ansible playbooks

### Répartition des rôles
- **Syrine:** Blue Team (SIEM, détection, monitoring, gestion de projet)
- **Maxine:** Red Team (attaques, cartographie AD, scénarios d'intrusion, logs, analyse)
- **Les deux:** Documentation, synthèse finale, bilan chiffré

---

## 📅 2. PLANNING & TIMELINE

### Semaine 1 (20/01 - 24/01) - Sprint 1: Infrastructure & Blue Team
**Charge de travail:** 4j × 7h30 + 1j × 3h45 = **33h45/personne**

| Jour | Focus principal |
|------|----------------|
| Lun 20/01 | Déploiement GOAD, installation Wazuh |
| Mar 21/01 | Configuration SIEM, déploiement agents Ansible |
| Mer 22/01 | OpenWEC + Sysmon, connexion logs |
| Jeu 23/01 | Suricata + Sigma Rules, Chainsaw/Hayabusa |
| Ven 24/01 | BloodHound/SharpHound, vérifications infrastructure |

### Semaine 2 (27/01 - 30/01) - Sprint 2: Red Team & Synthèse
**Charge de travail:** 4j × 7h30 + 1j × 3h45 = **33h45/personne**

| Jour | Focus principal |
|------|----------------|
| Lun 27/01 | Scénarios d'attaque, cartographie AD |
| Mar 28/01 | Tests d'intrusion, collecte traces/détections |
| Mer 29/01 | Analyse comparative détection, préventions |
| Jeu 30/01 | **Rédaction synthèse + annexes + soutenance** |
| Jeu 30/01 | **Réinitialisation matériel + rendu final** |

---

## 📝 3. BACKLOG COMPLET

### Légende estimation
- **XS:** 0.5 - 1h
- **S:** 1 - 2h
- **M:** 2 - 4h
- **L:** 4 - 6h
- **XL:** 6h+

---

### 🔵 EPIC 1: Infrastructure de base

| # | Tâche | Responsable | Estimation | Statut | Temps réel |
|---|-------|-------------|-----------|--------|-----------|
| 1.1 | Mettre en place le repo Git & structure | Les deux | S (1.5h) | ✅ Terminé | 1.5h |
| 1.2 | Créer plan d'adressage & schéma réseau | Les deux | M (3h) | ✅ Terminé | 3h |
| 1.3 | Déploiement machines GOAD (5 VMs) | Maxine | XL (8h) | ✅ Terminé | 9h |
| 1.4 | Vérifier installation GOAD | Maxine | S (1.5h) | ✅ Terminé | 2h |
| 1.5 | Connecter machines GOAD au réseau salle | Les deux | M (2h) | ✅ Terminé | 2.5h |
| **TOTAL EPIC 1** | | | **16h** | | **18h** |

---

### 🔵 EPIC 2: Déploiement SIEM & Collecteur

| # | Tâche | Responsable | Estimation | Statut | Temps réel |
|---|-------|-------------|-----------|--------|-----------|
| 2.1 | Installation Wazuh | Syrine | L (5h) | ✅ Terminé | 5h |
| 2.2 | Configuration Wazuh + lien machines domaine | Syrine | L (6h) | ✅ Terminé | 7h |
| 2.3 | Installation Elastic Stack | Syrine | L (5h) | 🔄 En cours | - |
| 2.4 | Configurer Elastic | Syrine | L (5h) | 🔄 En cours | - |
| 2.5 | Installer OpenWEC + connecter logs | Maxine | XL (7h) | ✅ Terminé | 8h |
| 2.6 | Mettre en place Sysmon sur Windows | Syrine | M (4h) | ✅ Terminé | 4.5h |
| 2.7 | Playbooks Ansible déploiement agents | Syrine | XL (6h) | 🔄 En cours | - |
| **TOTAL EPIC 2** | | | **38h** | | **24.5h** |

---

### 🔵 EPIC 3: IDS & Outils de détection

| # | Tâche | Responsable | Estimation | Statut | Temps réel |
|---|-------|-------------|-----------|--------|-----------|
| 3.1 | Installer Suricata + Sigma Rules | Syrine | L (5h) | 🔄 En cours | - |
| 3.2 | Configurer Suricata (placement réseau) | Syrine | M (3h) | 📋 À faire | - |
| 3.3 | Installer Chainsaw + Hayabusa | Syrine | S (2h) | 🔄 En cours | - |
| 3.4 | Tester détection avec outils portables | Syrine | M (3h) | 📋 À faire | - |
| **TOTAL EPIC 3** | | | **13h** | | **0h** |

---

### 🔴 EPIC 4: Red Team - Cartographie & Attaques

| # | Tâche | Responsable | Estimation | Statut | Temps réel |
|---|-------|-------------|-----------|--------|-----------|
| 4.1 | Installation Exegol | Maxine | M (2h) | 🔄 En cours | - |
| 4.2 | Installer BloodHound + SharpHound + Neo4J | Maxine | M (4h) | 📋 À faire | - |
| 4.3 | Cartographier AD avec SharpHound | Maxine | M (3h) | 📋 À faire | - |
| 4.4 | Analyser chemins d'attaque BloodHound | Maxine | M (4h) | 📋 À faire | - |
| 4.5 | Définir scénarios d'attaque | Maxine | M (3h) | 📋 À faire | - |
| 4.6 | Lancer scénarios d'attaques | Maxine | L (6h) | 📋 À faire | - |
| 4.7 | Récupérer traces & détections | Les deux | M (3h) | 📋 À faire | - |
| **TOTAL EPIC 4** | | | **25h** | | **0h** |

---

### 🟢 EPIC 5: Analyse & Prévention

| # | Tâche | Responsable | Estimation | Statut | Temps réel |
|---|-------|-------------|-----------|--------|-----------|
| 5.1 | Analyser alertes Wazuh | Maxine | M (3h) | 📋 À faire | - |
| 5.2 | Analyser alertes Elastic | Maxine | M (3h) | 📋 À faire | - |
| 5.3 | Analyser alertes Suricata | Maxine | M (2h) | 📋 À faire | - |
| 5.4 | Comparer efficacité SIEM/IDS/Outils | Maxine | L (4h) | 📋 À faire | - |
| 5.5 | Mettre en place des préventions | Les deux | M (4h) | 📋 À faire | - |
| **TOTAL EPIC 5** | | | **16h** | | **0h** |

---

### 📄 EPIC 6: Documentation & Livrables

| # | Tâche | Responsable | Estimation | Statut | Temps réel |
|---|-------|-------------|-----------|--------|-----------|
| 6.1 | Documenter chaque process | Les deux | Continu | 🔄 En cours | - |
| 6.2 | Rédiger synthèse finale (5-10 pages) | Les deux | XL (8h) | 📋 À faire | - |
| 6.3 | Créer schémas & graphiques | Syrine | M (3h) | 📋 À faire | - |
| 6.4 | Bilan chiffré & graphique gestion projet | Syrine | M (2h) | 📋 À faire | - |
| 6.5 | Rédiger annexes techniques détaillées | Les deux | L (6h) | 📋 À faire | - |
| 6.6 | Documenter Win/Fail & compétences acquises | Les deux | M (2h) | 📋 À faire | - |
| 6.7 | Bilan questions/réponses expert | Les deux | S (1h) | 📋 À faire | - |
| 6.8 | Réinitialiser matériel LAB | Les deux | S (1h) | 📋 À faire | - |
| 6.9 | Préparer soutenance | Les deux | M (3h) | 📋 À faire | - |
| **TOTAL EPIC 6** | | | **26h** | | **0h** |

---

### 📊 RÉCAPITULATIF GLOBAL

| Epic | Heures estimées | Heures réelles | Delta | Avancement |
|------|-----------------|----------------|-------|-----------|
| EPIC 1: Infrastructure | 16h | 18h | +2h | 100% ✅ |
| EPIC 2: SIEM & Logs | 38h | 24.5h | -13.5h | ~50% 🔄 |
| EPIC 3: IDS & Détection | 13h | 0h | - | ~20% 🔄 |
| EPIC 4: Red Team | 25h | 0h | - | ~10% 🔄 |
| EPIC 5: Analyse | 16h | 0h | - | 0% 📋 |
| EPIC 6: Documentation | 26h | 0h | - | ~15% 🔄 |
| **TOTAL PROJET** | **134h** | **42.5h** | | **~25%** |

**Charge totale disponible:** 67.5h × 2 personnes = **135h** ✅ Budget OK

---

## ⏱️ 4. SUIVI DU TEMPS (Bilan chiffré)

### Heures par personne & par semaine

| Période | Syrine (Blue) | Maxine (Red + Logs + Analyse) | Total équipe |
|---------|---------------|-------------------------------|-------------|
| **Semaine 1** (20-24/01) | 16.5h | 26h | 42.5h |
| **Semaine 2** (27-30/01) | 0h | 0h | 0h |
| **TOTAL** | **16.5h** | **26h** | **42.5h / 135h** |

### Répartition par type de tâche

| Catégorie | Syrine | Maxine | Total | % du projet |
|-----------|--------|--------|-------|-----------|
| Infrastructure | 6h | 12h | 18h | 42% |
| SIEM | 16.5h | 0h | 16.5h | 39% |
| Logs | 0h | 8h | 8h | 19% |
| IDS/Détection | 0h | 0h | 0h | 0% |
| Red Team | 0h | 0h | 0h | 0% |
| Analyse | 0h | 0h | 0h | 0% |
| Documentation | 0h | 0h | 0h | 0% |
| **TOTAL** | **22.5h** | **20h** | **42.5h** | **31%** |

### Graphique à créer pour le rendu
```
[À générer en fin de projet]
- Diagramme en barres : heures par personne
- Camembert : répartition par type de tâche
- Timeline : progression hebdomadaire
```

---

## ⚠️ 5. RISQUES & SOLUTIONS

| # | Risque | Probabilité | Impact | Mitigation | Statut |
|---|--------|-------------|--------|-----------|--------|
| R1 | GOAD ne démarre pas correctement | Moyenne | Critique | Documentation Orange Cyberdefense, backup snapshots VMs | ✅ Résolu |
| R2 | Agents SIEM ne communiquent pas | Élevée | Élevé | Tester config réseau, firewall Windows, playbooks Ansible robustes | 🔄 En cours |
| R3 | Manque de temps pour analyse comparative | Élevée | Moyen | Prioriser 2-3 scénarios d'attaque clés, automatiser collecte logs | ⚠️ À surveiller |
| R4 | Suricata placement réseau incorrect | Moyenne | Moyen | Valider architecture réseau en amont, mode promiscuous | 📋 À traiter |
| R5 | Synthèse finale bâclée (deadline 30/01) | Élevée | Critique | **Commencer rédaction dès 28/01**, template prêt, sections pré-remplies | ⚠️ Critique |
| R6 | Oubli réinitialisation matériel | Faible | Élevé | Checklist finale, alarme rappel 30/01 | 📋 Planifié |
| R7 | Disponibilité expert senior limitée | Moyenne | Moyen | Préparer questions précises en amont, sessions groupées | 🔄 Géré |

---

## 📄 6. TEMPLATE SYNTHÈSE FINALE

### Structure attendue (5-10 pages max)

#### A. Page de garde
- Titre du projet
- Noms : Syrine Belkadhi, Maxine Botturi
- Date : 30/01/2026
- Logo établissement

---

#### B. Synthèse technique (3-4 pages)

**1. Descriptif de l'environnement déployé**
- Schéma d'architecture réseau (1 page)
- Liste des VMs et leurs rôles
- Stack technique complète (tableau)
- Choix techniques justifiés (SIEM, IDS, placement Suricata)

**2. Résultats des tests d'intrusion**
- Scénarios d'attaque réalisés (tableau)
- Détections obtenues par SIEM/IDS (tableau comparatif)
- Traces collectées (exemples logs clés)
- Taux de détection par outil (%)

**3. Analyse comparative de détection**
- Wazuh : points forts / limites / cas d'usage
- Elastic : points forts / limites / cas d'usage
- Suricata : points forts / limites / cas d'usage
- Chainsaw/Hayabusa : utilité en forensics
- **Recommandations** : quel outil pour quel contexte

---

#### C. Gestion de projet (2-3 pages)

**4. Bilan chiffré & graphique**
- Tableau heures par personne (cf. section 4)
- Graphique en barres : Syrine vs Maxine
- Camembert : répartition par type de tâche
- Timeline : progression hebdomadaire
- Respect du budget temps : 42.5h / 135h utilisées

**5. Méthodologie agile appliquée**
- Découpage en 2 sprints
- Gestion Trello : backlog → en cours → terminé
- Stand-ups (si réalisés)
- Rétrospective : ce qui a marché / ce qui n'a pas marché

---

#### D. Retour d'expérience (1-2 pages)

**6. Compétences acquises**

*Techniques :*
- Déploiement Active Directory vulnérable (GOAD)
- Configuration SIEM en environnement Windows
- Automatisation Ansible
- Analyse logs EVTX avec Sigma Rules
- Cartographie AD avec BloodHound
- Tests d'intrusion et méthodologie Red Team

*Gestion de projet :*
- Méthode agile appliquée
- Estimation de charge
- Gestion des risques
- Travail en binôme Blue/Red Team

**7. Win / Fail**

*🎉 Wins :*
- GOAD déployé fonctionnel en 1 journée
- Wazuh opérationnel avec agents connectés
- Automatisation Ansible réussie
- Organisation Git/Trello claire

*❌ Fails :*
- Sous-estimation temps configuration Elastic
- Problèmes réseau entre GOAD et salle
- Retard sur déploiement Suricata
- Manque de temps pour tests d'intrusion variés

**8. Questions/Réponses avec l'expert**
- Liste des questions posées
- Réponses apportées
- Impact sur le projet

---

#### E. Conclusion (0.5 page)
- Objectifs atteints / partiellement atteints
- Apports pédagogiques principaux
- Axes d'amélioration pour un déploiement réel

---

### Annexes (documents séparés)

**Annexe A : Documentation d'installation**
- Procédure déploiement GOAD (auteur, durée)
- Procédure installation Wazuh (auteur, durée)
- Procédure installation Elastic (auteur, durée)
- Procédure installation OpenWEC (auteur, durée)
- Procédure installation Suricata (auteur, durée)
- Procédure configuration Sysmon (auteur, durée)
- Procédure BloodHound/SharpHound (auteur, durée)

**Annexe B : Configurations**
- Fichiers config Wazuh (ossec.conf)
- Fichiers config Elastic (elasticsearch.yml, kibana.yml)
- Config Sysmon (XML)
- Sigma rules utilisées
- Playbooks Ansible

**Annexe C : Traces & Logs**
- Exemples logs EVTX significatifs
- Alertes SIEM (screenshots)
- Graphes BloodHound (chemins d'attaque)
- Résultats Chainsaw/Hayabusa

**Annexe D : Dépôt Git**
- Lien GitHub : https://github.com/Radiant-Maxine/SAE_5C03_Nixie
- Structure du repo
- Commits principaux avec messages explicatifs

---

## 📝 7. NOTES & DÉCISIONS IMPORTANTES

### Décisions d'architecture
- **Date:** 20/01/2026
- **Décision:** Déploiement Suricata en mode bridge entre VirtualBox et réseau physique
- **Justification:** Maximiser la visibilité du trafic AD
- **Impact:** Configuration VirtualBox avancée nécessaire

---

- **Date:** 21/01/2026
- **Décision:** Utilisation OpenWEC avec dashboard IA (non SIEM classique)
- **Justification:** Innovation, collecteur spécialisé Windows plus léger
- **Impact:** Nécessite formation supplémentaire sur l'outil

---

- **Date:** 22/01/2026
- **Décision:** Automatisation déploiement agents via Ansible (pas GPO)
- **Justification:** Reproductibilité, versionning, skills DevOps
- **Impact:** Temps dev playbooks mais gain long terme

---

### Questions pour l'expert senior

**Session 1 - Date: __/__/2026**
- Q1: [À compléter]
- R1: [À compléter]

**Session 2 - Date: __/__/2026**
- Q2: [À compléter]
- R2: [À compléter]

---

### Changelog du projet

| Date | Événement | Impact |
|------|-----------|--------|
| 19/01 | Kick-off projet, création repo | - |
| 20/01 | GOAD déployé | +2h vs estimation |
| 21/01 | Wazuh connecté aux machines | ✅ Milestone atteint |
| 22/01 | OpenWEC opérationnel | ✅ Milestone atteint |
| 23/01 | Sysmon déployé sur toutes VMs | ✅ |
| 28/01 | [En cours] | - |

---

## ✅ 8. CHECKLIST FINALE (30/01/2026)

### Avant soutenance
- [ ] Synthèse finale rédigée (5-10 pages)
- [ ] Tous les graphiques créés (bilan chiffré)
- [ ] Annexes complètes avec auteurs & durées
- [ ] Dépôt Git à jour avec commits explicites
- [ ] Screenshots/traces d'attaques collectés
- [ ] Comparatif efficacité SIEM finalisé
- [ ] Win/Fail documentés
- [ ] Questions/Réponses expert compilées
- [ ] Support de présentation prêt

### Après soutenance
- [ ] ⚠️ **CRITIQUE:** Réinitialiser tout le matériel (VMs, snapshots, configs)
- [ ] Vérifier que rien ne reste sur les machines physiques
- [ ] Confirmer auprès de l'enseignant la réinitialisation

---

## 🎯 OBJECTIFS RESTANTS (Priorisation)

### 🔴 Priorité CRITIQUE (avant 29/01)
1. Finaliser configuration Elastic + agents
2. Déployer Suricata fonctionnel
3. Installer Chainsaw/Hayabusa
4. Installer BloodHound + cartographier AD
5. Lancer **au moins 2-3 scénarios d'attaque** représentatifs

### 🟠 Priorité HAUTE (29/01)
1. Collecter toutes les traces/détections
2. Analyser alertes SIEM/IDS
3. Créer tableau comparatif efficacité
4. Commencer rédaction synthèse (structure + intro)

### 🟡 Priorité MOYENNE (30/01 matin)
1. Finaliser synthèse + graphiques
2. Rédiger annexes techniques
3. Compiler Win/Fail
4. Préparer support soutenance

### 🟢 Priorité BASSE (30/01 après-midi)
1. Soutenance
2. Réinitialisation matériel
3. Rendu final

---

**Dernière mise à jour:** 28/01/2026  
**Statut global:** 🟡 En bonne voie, vigilance sur deadline 30/01  
**Next steps:** Finir config SIEM, lancer Red Team, anticiper rédaction synthèse
