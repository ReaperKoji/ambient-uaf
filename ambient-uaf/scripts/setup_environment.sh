#!/bin/bash
echo "🔧 CONFIGURANDO AMBIENTE SEGURO UAF"

# Verificar se está em VM
if [[ $(systemd-detect-virt) == "none" ]]; then
    echo "⚠️  AVISO: Não parece ser uma VM. Recomendado executar em VM isolada!"
    read -p "Continuar mesmo assim? (s/N): " -n 1 -r
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        exit 1
    fi
fi

# Instalar dependências
sudo apt update
sudo apt install -y \
    python3 python3-pip \
    clang gcc g++ \
    valgrind \
    gdb \
    net-tools \
    tcpdump

# Instalar ferramentas Python
pip3 install -r ../requirements.txt

# Configurar aliases úteis
echo "alias asan-test='clang -fsanitize=address -g -O1'" >> ~/.bashrc
echo "alias valgrind-test='valgrind --leak-check=full --track-origins=yes'" >> ~/.bashrc

echo "✅ Ambiente configurado. RECOMENDADO: Criar snapshot da VM agora!"