# LAB SEGURO PARA TESTE UAF (Use-After-Free)

## ⚠️ AVISOS DE SEGURANÇA
- Execute apenas em VM ISOLADA
- Rede: host-only ou offline
- Snapshots antes de cada teste
- Não use em sistemas de produção

## 🚀 COMO USAR

### 1. Configurar ambiente
````
chmod +x scripts/setup_environment.sh
./scripts/setup_environment.sh
````

2. Isolar rede
````
./scripts/network_isolation.sh
````

3. Executar testes seguros
````
cd tests
python3 run_security_tests.py
````


💾 PARA CRIAR O ZIP:

# Na pasta raiz do projeto
mkdir UAF_Test_Lab_Seguro
# Copie todos os arquivos acima para suas respectivas pastas
zip -r UAF_Test_Lab_Seguro.zip UAF_Test_Lab_Seguro/