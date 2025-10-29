# PROTOCOLO DE SEGURANÇA

## 🚫 NUNCA FAÇA
- Execute em sistemas de produção
- Teste em redes públicas  
- Use em sistemas de terceiros
- Compartilhe exploits sem contexto educativo

## ✅ SEMPRE FAÇA
- Use VMs isoladas
- Tire snapshots antes dos testes
- Desative rede ou use host-only
- Documente todos os testes
- Relate vulnerabilidades responsavelmente

## 🛡️ MEDIDAS DE SEGURANÇA IMPLEMENTADAS

### 1. Isolamento de Rede
- Firewall restritivo
- Apenas localhost permitido
- Verificação de endereços

### 2. Controle de Acesso  
- Verificação de ambiente
- Alertas para alvos não-locais
- Confirmação do usuário

### 3. Detecção Científica
- AddressSanitizer integrado
- Valgrind para análise
- Logs detalhados

## 📞 CONTATO EM CASO DE ACIDENTE
Se algo sair do controle:
1. Desligue a VM imediatamente
2. Restaure do snapshot limpo
3. Reporte o incidente