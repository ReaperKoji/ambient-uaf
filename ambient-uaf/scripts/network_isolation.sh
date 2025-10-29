#!/bin/bash
echo "🔒 CONFIGURANDO ISOLAMENTO DE REDE"

# Desativar rede se possível
read -p "Desativar todas as interfaces de rede? (s/N): " -n 1 -r
if [[ $REPLY =~ ^[Ss]$ ]]; then
    sudo systemctl stop networking
    echo "🌐 Rede desativada"
fi

# Configurar firewall restritivo
echo "🛡️  Configurando firewall restritivo..."
sudo iptables -F
sudo iptables -P INPUT DROP
sudo iptables -P FORWARD DROP
sudo iptables -P OUTPUT DROP
# Permitir apenas loopback
sudo iptables -A INPUT -i lo -j ACCEPT
sudo iptables -A OUTPUT -o lo -j ACCEPT

echo "✅ Rede isolada. Testes serão executados apenas localmente."