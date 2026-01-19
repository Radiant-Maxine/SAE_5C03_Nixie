#!/usr/bin/env bash
set -euo pipefail

# init_sae5_repo.sh
# - Crée l'architecture de dossiers (idempotent)
# - Ajoute un README.md descriptif (avec emoji) dans chaque dossier (sans écraser si déjà présent)
# - Configure Git LFS pour EVTX/PCAP/archives (et optionnellement Vagrant .box)
# - Prépare un .gitignore safe (sans ignorer LOGS/, puisque tu veux versionner les preuves via LFS)

REPO_DIR="${1:-.}"

# --- Helpers ---
die() { echo "[ERREUR] $*" >&2; exit 1; }

ensure_repo() {
  cd "$REPO_DIR" 2>/dev/null || die "Impossible d'accéder à: $REPO_DIR"
  git rev-parse --is-inside-work-tree >/dev/null 2>&1 || die "Pas un repo Git (pas de .git). Lance depuis la racine du repo cloné."
}

mkd() { mkdir -p "$1"; }

write_file_if_missing() {
  local path="$1"
  shift
  if [[ -f "$path" ]]; then
    return 0
  fi
  cat > "$path" <<'EOF'
'"$*"'
EOF
}

write_readme_if_missing() {
  local dir="$1"
  local title="$2"
  local body="$3"
  local path="$dir/README.md"
  if [[ -f "$path" ]]; then
    return 0
  fi
  cat > "$path" <<EOF
# $title

$body
EOF
}

append_if_missing() {
  local file="$1"
  local marker="$2"
  local block="$3"
  touch "$file"
  if ! grep -qF "$marker" "$file"; then
    printf "\n%s\n" "$block" >> "$file"
  fi
}

setup_lfs() {
  if ! command -v git >/dev/null 2>&1; then
    die "git n'est pas installé."
  fi

  if ! git lfs version >/dev/null 2>&1; then
    echo "[INFO] Git LFS n'est pas installé. Skip LFS."
    echo "       Installe Git LFS puis relance ce script."
    return 0
  fi

  echo "[OK] Git LFS détecté."
  git lfs install >/dev/null

  # Fichiers demandés / utiles (preuves)
  git lfs track "*.evtx" >/dev/null
  git lfs track "*.evt"  >/dev/null
  git lfs track "*.pcap" >/dev/null
  git lfs track "*.pcapng" >/dev/null
  git lfs track "*.cap" >/dev/null

  # Archives (si EVTX trop gros -> compresser)
  git lfs track "*.zip" >/dev/null
  git lfs track "*.7z" >/dev/null
  git lfs track "*.rar" >/dev/null
  git lfs track "*.tar" >/dev/null
  git lfs track "*.tar.gz" >/dev/null
  git lfs track "*.tgz" >/dev/null
  git lfs track "*.gz" >/dev/null
  git lfs track "*.xz" >/dev/null

  # Autres “gros fichiers” typiques en cyber
  git lfs track "*.dmp" >/dev/null
  git lfs track "*.core" >/dev/null

  # Vagrant : en général on NE versionne PAS les boxes/VMs.
  # Si vous exportez vraiment des .box, vous pouvez activer:
  ENABLE_VAGRANT_BOX_LFS="${ENABLE_VAGRANT_BOX_LFS:-0}"
  if [[ "$ENABLE_VAGRANT_BOX_LFS" == "1" ]]; then
    git lfs track "*.box" >/dev/null
    echo "[INFO] LFS activé pour *.box (Vagrant box)."
  else
    echo "[INFO] LFS pour *.box désactivé (ENABLE_VAGRANT_BOX_LFS=1 pour l'activer)."
  fi

  echo "[OK] LFS patterns configurés. Pense à committer .gitattributes."
}

# --- Main ---
ensure_repo
echo "[INFO] Repo: $(pwd)"

# 1) Dossiers principaux
mkd "DOCS"
mkd "CONFIGS"
mkd "AUTOMATION"
mkd "LOGS"
mkd "REPORTS"
mkd "TESTS"
mkd "STANDUPS"
mkd "PROJECT_MANAGEMENT"

# 2) Sous-dossiers
mkd "DOCS/01_architecture"
mkd "DOCS/02_installation"
mkd "DOCS/03_procedures"
mkd "DOCS/04_troubleshooting"
mkd "DOCS/05_learning"

mkd "CONFIGS/goad"
mkd "CONFIGS/openwec"
mkd "CONFIGS/siem_elasticsearch"
mkd "CONFIGS/siem_splunk"
mkd "CONFIGS/suricata"
mkd "CONFIGS/sysmon"

mkd "AUTOMATION/ansible"
mkd "AUTOMATION/bash"
mkd "AUTOMATION/powershell"
mkd "AUTOMATION/python"

mkd "LOGS/evtx"
mkd "LOGS/pcap"
mkd "LOGS/archives"
mkd "LOGS/exports"
mkd "LOGS/notes"

mkd "REPORTS/appendices"
mkd "TESTS/scenarios"
mkd "TESTS/results"

# 3) README.md avec emojis (sans écraser si déjà présents)
write_readme_if_missing "DOCS" "📚 DOCS" "Documentation du projet : architecture, installation, procédures, troubleshooting, apprentissages."
write_readme_if_missing "DOCS/01_architecture" "🗺️ 01_architecture" "Schémas réseau, topologies, IP plan, flux (GOAD → OpenWEC → SIEM), diagrammes."
write_readme_if_missing "DOCS/02_installation" "🛠️ 02_installation" "Guides d’installation : GOAD, OpenWEC, Sysmon, SIEM1/SIEM2, Suricata, BloodHound, etc."
write_readme_if_missing "DOCS/03_procedures" "📒 03_procedures" "Procédures d’exploitation : collecte logs, runbook blue team, runbook red team, exploitation BloodHound."
write_readme_if_missing "DOCS/04_troubleshooting" "🧯 04_troubleshooting" "Problèmes rencontrés + solutions reproductibles (avec commandes)."
write_readme_if_missing "DOCS/05_learning" "🧠 05_learning" "Notes perso/groupe : wins/fails, compétences acquises, liens utiles, retours portfolio."

write_readme_if_missing "CONFIGS" "🔧 CONFIGS" "Fichiers de configuration (à versionner). Pas de secrets (mots de passe) ici."
write_readme_if_missing "CONFIGS/goad" "♟️ goad" "goad.ini (si vous le versionnez), notes réseau, paramètres provider VirtualBox."
write_readme_if_missing "CONFIGS/openwec" "📡 openwec" "Config OpenWEC, subscriptions, paramètres WinRM/collecte."
write_readme_if_missing "CONFIGS/sysmon" "🧾 sysmon" "Sysmon config XML + scripts d’installation, options d’audit."
write_readme_if_missing "CONFIGS/siem_elasticsearch" "📊 siem_elasticsearch" "Dashboards/export, pipelines, configs (sans données)."
write_readme_if_missing "CONFIGS/siem_splunk" "📈 siem_splunk" "Inputs/props/transforms, dashboards export (sans données)."
write_readme_if_missing "CONFIGS/suricata" "🧿 suricata" "suricata.yaml + règles custom + notes placement réseau."

write_readme_if_missing "AUTOMATION" "🤖 AUTOMATION" "Scripts d’automatisation (déploiement agents, config audit, collecte logs)."
write_readme_if_missing "AUTOMATION/ansible" "🧩 ansible" "Playbooks/roles Ansible (inventaire, déploiement)."
write_readme_if_missing "AUTOMATION/bash" "🐚 bash" "Scripts bash : checks, exports logs, packaging archives."
write_readme_if_missing "AUTOMATION/powershell" "🪟 powershell" "Scripts PowerShell : activer audit, installer Sysmon, config WinRM."
write_readme_if_missing "AUTOMATION/python" "🐍 python" "Scripts Python : parsing, métriques projet, génération de rapports."

write_readme_if_missing "LOGS" "📊 LOGS" "Preuves (EVTX/PCAP/archives). Ici, on stocke les exports. (Avec Git LFS pour éviter d’exploser le repo.)"
write_readme_if_missing "LOGS/evtx" "🧾 evtx" "Exports EVTX (Security/System/Sysmon). Exemple: LOGS/evtx/DC01_Sysmon_2026-01-19.evtx"
write_readme_if_missing "LOGS/pcap" "🕸️ pcap" "Captures réseau (pcap/pcapng) liées aux attaques et à Suricata."
write_readme_if_missing "LOGS/archives" "🗜️ archives" "Archives compressées (.zip/.7z/.tar.gz) si EVTX/PCAP sont trop lourds."
write_readme_if_missing "LOGS/exports" "📦 exports" "Exports depuis SIEM (JSON/NDJSON/CSV) ou exports BloodHound (zip/json) si besoin."
write_readme_if_missing "LOGS/notes" "📝 notes" "Notes courtes sur comment les logs ont été générés + quel scénario/attaque."

write_readme_if_missing "REPORTS" "🧾 REPORTS" "Rapports finaux (synthèse + rapports blue/red + annexes)."
write_readme_if_missing "REPORTS/appendices" "📎 appendices" "Annexes détaillées (installation/config). Chaque annexe = auteur + durée."

write_readme_if_missing "TESTS" "🧪 TESTS" "Scénarios d’attaque, plans de tests, résultats, mapping attaques ↔ alertes."
write_readme_if_missing "TESTS/scenarios" "🎭 scenarios" "Scénarios d’attaque (étapes, commandes, objectifs, prérequis)."
write_readme_if_missing "TESTS/results" "✅ results" "Résultats d’exécution + détections observées (SIEM1, SIEM2, Suricata, sigma)."

write_readme_if_missing "STANDUPS" "📋 STANDUPS" "Standups (matin/soir) : ce qui est fait / à faire / blocages / métriques."
write_readme_if_missing "PROJECT_MANAGEMENT" "📁 PROJECT_MANAGEMENT" "Rôles, décisions, temps passé, questions à l’ingénieur, suivi agile."

# 4) Fichiers racine : créer seulement si manquants
if [[ ! -f "README.md" ]]; then
  cat > "README.md" <<'EOF'
# SAE 5 - Cyber & DevCloud (GOAD Lab)

## 🎯 Objectif
POC Blue Team / Red Team basé sur GOAD (AD vulnérable) + collecte logs (OpenWEC) + SIEM x2 + IDS Suricata.

## 📂 Structure
- DOCS/ : documentation
- CONFIGS/ : configs (sans secrets)
- AUTOMATION/ : scripts
- LOGS/ : preuves (EVTX/PCAP/archives) — idéalement via Git LFS
- REPORTS/ : rapports finaux
- TESTS/ : scénarios & résultats
- STANDUPS/ : suivi agile
- PROJECT_MANAGEMENT/ : gestion projet
EOF
fi

if [[ ! -f "CONTRIBUTING.md" ]]; then
  cat > "CONTRIBUTING.md" <<'EOF'
# CONTRIBUTING

## Règles simples
- Pas de secrets dans Git (passwords, tokens, clés privées).
- Commit & push régulièrement (au moins 3-4 commits par demi-journée).
- Documenter : un fichier dans STANDUPS/ par demi-journée.

## Git LFS
Les gros fichiers (EVTX/PCAP/archives) sont suivis via Git LFS.
EOF
fi

if [[ ! -f "ARCHITECTURE.md" ]]; then
  cat > "ARCHITECTURE.md" <<'EOF'
# Architecture (brouillon)

## GOAD (VirtualBox)
- Réseau : vboxnet0 192.168.56.0/24
- DC01 : 192.168.56.10
- SRV01 : 192.168.56.11
- SRV02 : 192.168.56.12
- WKS01 : 192.168.56.110
- WKS02 : 192.168.56.111

## Monitoring (LAN)
- OpenWEC : à définir
- SIEM1 : à définir
- SIEM2 : à définir
- Suricata : à définir
EOF
fi

# 5) .gitignore : safe + compatible LFS (ne pas ignorer LOGS/)
GITIGNORE_BLOCK_MARKER="# === SAE5 DEFAULT IGNORE BLOCK ==="
GITIGNORE_BLOCK=$(cat <<'EOF'
# === SAE5 DEFAULT IGNORE BLOCK ===

# 🧨 Secrets / credentials (NEVER COMMIT)
.env
.env.*
credentials.txt
secrets.txt
*password*
*.key
*.pem
id_rsa
id_ed25519

# 🧱 VirtualBox / Vagrant artifacts (NE PAS VERSIONNER)
.vagrant/
VirtualBox VMs/
*.vdi
*.vmdk
*.vbox
*.vbox-prev
*.ova
*.ovf

# 🧹 OS / Editor
.DS_Store
Thumbs.db
*.swp
*.swo
*~

# 🐍 Python cache (si besoin)
__pycache__/
*.pyc
EOF
)
append_if_missing ".gitignore" "$GITIGNORE_BLOCK_MARKER" "$GITIGNORE_BLOCK"

# 6) Git LFS
setup_lfs

echo
echo "✅ Structure prête."
echo "➡️ Next steps (recommandé):"
echo "   1) git status"
echo "   2) git add .gitattributes .gitignore DOCS CONFIGS AUTOMATION LOGS REPORTS TESTS STANDUPS PROJECT_MANAGEMENT README.md ARCHITECTURE.md CONTRIBUTING.md"
echo "   3) git commit -m \"chore(repo): init folder structure + LFS tracking\""
echo "   4) git push"
echo
echo "ℹ️ Si tu veux tracker les Vagrant boxes (*.box) en LFS:"
echo "   ENABLE_VAGRANT_BOX_LFS=1 bash init_sae5_repo.sh"
