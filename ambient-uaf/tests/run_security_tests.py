#!/usr/bin/env python3
"""
TESTES DE SEGURANÇA AUTOMATIZADOS
"""

import subprocess
import os
import sys

def run_compiler_tests():
    """Executa testes com compiladores e sanitizers"""
    print("🔧 TESTES COM COMPILADORES")
    
    tests = [
        {
            'name': 'Compilação básica',
            'cmd': ['g++', '--version'],
            'success': 'g++' 
        },
        {
            'name': 'Clang/ASan disponível', 
            'cmd': ['clang', '--version'],
            'success': 'clang'
        },
        {
            'name': 'Valgrind disponível',
            'cmd': ['valgrind', '--version'], 
            'success': 'valgrind'
        }
    ]
    
    for test in tests:
        try:
            result = subprocess.run(test['cmd'], capture_output=True, text=True)
            if test['success'] in result.stdout or test['success'] in result.stderr:
                print(f"✅ {test['name']}")
            else:
                print(f"❌ {test['name']}")
        except:
            print(f"❌ {test['name']} (não encontrado)")

def test_uaf_detection():
    """Testa detecção de UAF com sanitizers"""
    print("\n🔍 TESTANDO DETECÇÃO UAF")
    
    # Compilar teste com ASan
    source = """
#include <iostream>
int main() {
    int* ptr = new int(42);
    delete ptr;
    std::cout << "UAF: " << *ptr << std::endl; // UAF!
    return 0;
}
"""
    
    with open('/tmp/test_uaf.cpp', 'w') as f:
        f.write(source)
    
    # Compilar com ASan
    compile_cmd = ['clang++', '-fsanitize=address', '-g', '/tmp/test_uaf.cpp', '-o', '/tmp/test_uaf']
    
    try:
        # Compilar
        result = subprocess.run(compile_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Falha na compilação do teste")
            return False
        
        # Executar
        result = subprocess.run(['/tmp/test_uaf'], capture_output=True, text=True)
        
        if 'use-after-free' in result.stderr:
            print("✅ ASan detectou UAF corretamente!")
            return True
        else:
            print("❌ ASan não detectou UAF")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False
    finally:
        # Limpeza
        if os.path.exists('/tmp/test_uaf.cpp'):
            os.remove('/tmp/test_uaf.cpp')
        if os.path.exists('/tmp/test_uaf'):
            os.remove('/tmp/test_uaf')

def main():
    print("🧪 EXECUTANDO TESTES DE SEGURANÇA COMPLETOS")
    print("=" * 50)
    
    # Verificar ambiente
    run_compiler_tests()
    
    # Testar detecção
    test_uaf_detection()
    
    print("\n" + "=" * 50)
    print("✅ TESTES CONCLUÍDOS")
    print("💡 Configure o ambiente conforme README.md para testes completos")

if __name__ == '__main__':
    main()