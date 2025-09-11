#!/usr/bin/env bash

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

TOOLS=(
  "DockerSlim|https://github.com/slimtoolkit/slim"
  "Dive|https://github.com/wagoodman/dive"
  "Hadolint|https://github.com/hadolint/hadolint"
  "Trivy|https://github.com/aquasecurity/trivy"
)

function install_with_apt() {
  echo -e "${GREEN}Installing with APT...${NC}"
  
  # DockerSlim
  echo -e "${GREEN}Dockerslim...${NC}"
  curl -sL https://raw.githubusercontent.com/slimtoolkit/slim/master/scripts/install-slim.sh | sudo -E bash -

  # Dive
  echo -e "${GREEN}Dive...${NC}"
  curl -s https://api.github.com/repos/wagoodman/dive/releases/latest \
    | grep "browser_download_url.*linux_amd64.deb" \
    | cut -d '"' -f 4 \
    | wget -i - && sudo dpkg -i dive_*.deb

  # Hadolint
  echo -e "${GREEN}Hadolint...${NC}"
  wget -O hadolint https://github.com/hadolint/hadolint/releases/latest/download/hadolint-Linux-x86_64
  chmod +x hadolint
  sudo mv hadolint /usr/local/bin/

  # Trivy
  # sudo apt install wget apt-transport-https gnupg lsb-release -y
  # wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
  # echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee -a /etc/apt/sources.list.d/trivy.list
  # sudo apt update
  # sudo apt install trivy -y
  echo -e "${GREEN}Trivy...${NC}"
  curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sudo sh -s -- -b /usr/local/bin
}

function install_with_brew() {
  echo -e "${GREEN}Installing with Homebrew...${NC}"
  brew install slimtoolkit/tap/slim
  brew install dive
  brew install hadolint
  brew install aquasecurity/trivy/trivy
}

function print_manual_instructions() {
  echo -e "${RED}No supported package manager found. Please install the tools manually:${NC}"
  for tool in "${TOOLS[@]}"; do
    IFS='|' read -r name url <<< "$tool"
    echo -e "${GREEN}$name:${NC} $url"
  done
  exit 1
}

# Parse argument
if [[ $1 == "--use=apt" ]]; then
  echo "running apt installer ..."
  sleep 5
  install_with_apt
elif [[ $1 == "--use=brew" ]]; then
  install_with_brew
else
  if command -v apt &> /dev/null; then
    install_with_apt
  elif command -v brew &> /dev/null; then
    install_with_brew
  else
    print_manual_instructions
  fi
fi
