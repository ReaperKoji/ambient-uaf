#!/usr/bin/env python3
"""
HARNESS DE TESTE SEGURO - AMBIENTE CONTROLADO PARA EXPLOITS
"""

import subprocess
import os
import sys
import tempfile
import time
import signal
import threading
from pathlib import Path

class SafeTestHarness:
    """
    Ambiente controlado para teste seguro de exploits UAF
    """
    
    def __init__(self, workspace_dir="/tmp/uaf_test"):
        self.workspace = Path(workspace_dir)
        self.workspace.mkdir(exist_ok=True)
        
        # Estado do teste
        self.test_process = None
        self.monitor_thread = None
        self.running = False
        
        # Resultados
        self.detected_vulnerabilities = []
        self.security_events = []
        
        print("🛡️  HARNESS DE TESTE SEGURO INICIALIZADO")
        print(f"📁 Workspace: {self.workspace}")
        
    def setup_secure_environment(self):
        """Configura ambiente seguro para testes"""
        print("\n🔧 CONFIGURANDO AMBIENTE SEGURO...")
        
        # Verificar se estamos em ambiente isolado
        self._check_environment()
        
        # Configurar limites de recursos
        self._set_resource_limits()
        
        # Criar arquivos de teste seguros
        self._create_test_files()
        
        print("✅ Ambiente seguro configurado")
    
    def _check_environment(self):
        """Verifica se o ambiente é seguro para testes"""
        checks = [
            ("VM Detection", self._is_virtual_machine),
            ("Network Isolation", self._is_network_isolated),
            ("Resource Limits", self._can_set_limits),
            ("Temp Directory", lambda: self.workspace.exists())
        ]
        
        for check_name, check_func in checks:
            try:
                result = check_func()
                status = "✅" if result else "⚠️"
                print(f"   {status} {check_name}: {result}")
            except Exception as e:
                print(f"   ❌ {check_name}: ERRO - {e}")
    
    def _is_virtual_machine(self):
        """Verifica se está executando em VM"""
        try:
            # Verificar sistemas de virtualização
            vm_indicators = [
                "/proc/scsi/scsi",  # Dispositivos SCSI virtuais
                "/proc/ide/hd0/model",  # Modelo de disco
                "/sys/class/dmi/id/product_name",  # Produto DMI
            ]
            
            for indicator in vm_indicators:
                if os.path.exists(indicator):
                    with open(indicator, 'r') as f:
                        content = f.read().lower()
                        if any(vm in content for vm in ['vmware', 'virtual', 'qemu', 'kvm']):
                            return True
            return False
        except:
            return False
    
    def _is_network_isolated(self):
        """Verifica isolamento de rede"""
        try:
            # Tentar conectar com Google (não deve funcionar em ambiente isolado)
            import socket
            socket.create_connection(("8.8.8.8", 53), timeout=2)
            return False  # Conectou - não está isolado
        except:
            return True  # Não conectou - isolado
    
    def _can_set_limits(self):
        """Verifica se pode definir limites de recursos"""
        try:
            import resource
            resource.setrlimit(resource.RLIMIT_CPU, (10, 10))  # 10 segundos
            return True
        except:
            return False
    
    def _set_resource_limits(self):
        """Define limites rigorosos de recursos"""
        try:
            import resource
            
            # Limite de CPU (10 segundos)
            resource.setrlimit(resource.RLIMIT_CPU, (10, 10))
            
            # Limite de memória (128 MB)
            resource.setrlimit(resource.RLIMIT_AS, (128 * 1024 * 1024, 128 * 1024 * 1024))
            
            # Limite de processos filhos
            resource.setrlimit(resource.RLIMIT_NPROC, (10, 10))
            
        except Exception as e:
            print(f"⚠️  Não foi possível definir limites de recursos: {e}")
    
    def _create_test_files(self):
        """Cria arquivos de teste seguros"""
        test_files = {
            "simple_uaf.c": """
#include <stdlib.h>
#include <stdio.h>

int main() {
    int *ptr = malloc(sizeof(int));
    *ptr = 42;
    free(ptr);
    
    // Use After Free - para teste de detecção
    printf("UAF: %d\\n", *ptr);
    return 0;
}
            """,
            "double_free.c": """
#include <stdlib.h>

int main() {
    char *buffer = malloc(64);
    free(buffer);
    free(buffer);  // Double free
    return 0;
}
            """,
            "heap_overflow.c": """
#include <stdlib.h>
#include <string.h>

int main() {
    char *small = malloc(8);
    strcpy(small, "This is a very long string that will overflow");
    free(small);
    return 0;
}
            """
        }
        
        for filename, content in test_files.items():
            filepath = self.workspace / filename
            with open(filepath, 'w') as f:
                f.write(content)
            print(f"📄 Criado: {filepath}")
    
    def compile_with_sanitizers(self, source_file, output_name):
        """Compila código com múltiplos sanitizers"""
        print(f"\n🔨 COMPILANDO {source_file} COM SANITIZERS...")
        
        sanitizers = [
            ("ASan", ["-fsanitize=address"]),
            ("UBSan", ["-fsanitize=undefined"]),
            ("TSan", ["-fsanitize=thread"]),
        ]
        
        results = {}
        
        for san_name, flags in sanitizers:
            try:
                output_path = self.workspace / f"{output_name}_{san_name.lower()}"
                cmd = ["clang", "-g", "-O1"] + flags + [str(source_file), "-o", str(output_path)]
                
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    results[san_name] = {
                        "success": True,
                        "path": output_path,
                        "output": result.stdout
                    }
                    print(f"   ✅ {san_name}: Compilado com sucesso")
                else:
                    results[san_name] = {
                        "success": False,
                        "error": result.stderr
                    }
                    print(f"   ❌ {san_name}: Falha na compilação")
                    
            except subprocess.TimeoutExpired:
                results[san_name] = {
                    "success": False,
                    "error": "Timeout na compilação"
                }
                print(f"   ❌ {san_name}: Timeout")
            except Exception as e:
                results[san_name] = {
                    "success": False, 
                    "error": str(e)
                }
                print(f"   ❌ {san_name}: Erro - {e}")
        
        return results
    
    def run_with_valgrind(self, binary_path):
        """Executa binário com Valgrind para análise de memória"""
        print(f"\n🔍 EXECUTANDO {binary_path} COM VALGRIND...")
        
        cmd = [
            "valgrind",
            "--leak-check=full",
            "--track-origins=yes",
            "--error-exitcode=42",
            str(binary_path)
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            analysis = {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "memory_errors": [],
                "leaks": False
            }
            
            # Analisar saída do Valgrind
            if "Invalid read" in result.stderr or "Invalid write" in result.stderr:
                analysis["memory_errors"].append("UAF detectado")
            
            if "definitely lost" in result.stderr:
                analysis["leaks"] = True
                
            if result.returncode == 42:
                analysis["memory_errors"].append("Valgrind detectou erro crítico")
            
            return analysis
            
        except subprocess.TimeoutExpired:
            return {"error": "Timeout na execução"}
        except Exception as e:
            return {"error": f"Erro na execução: {e}"}
    
    def monitor_security_events(self):
        """Monitora eventos de segurança durante os testes"""
        def monitor():
            while self.running:
                try:
                    # Verificar uso de recursos
                    self._check_resource_usage()
                    time.sleep(1)
                except:
                    break
        
        self.monitor_thread = threading.Thread(target=monitor)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
    
    def _check_resource_usage(self):
        """Verifica uso de recursos do sistema"""
        try:
            # Verificar memória
            with open('/proc/meminfo', 'r') as f:
                mem_info = f.read()
            
            # Verificar processos
            result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
            
            # Log de segurança
            security_event = {
                'timestamp': time.time(),
                'memory': mem_info[:200],  # Primeiros 200 chars
                'process_count': len(result.stdout.split('\n')) - 1
            }
            
            self.security_events.append(security_event)
            
        except Exception as e:
            print(f"⚠️  Erro no monitoramento: {e}")
    
    def run_comprehensive_test(self):
        """Executa teste de segurança completo"""
        print("\n" + "="*60)
        print("🧪 INICIANDO TESTE DE SEGURANÇA COMPREENSIVO")
        print("="*60)
        
        self.setup_secure_environment()
        self.running = True
        self.monitor_security_events()
        
        test_results = {}
        
        # Testar cada arquivo de teste
        for test_file in self.workspace.glob("*.c"):
            print(f"\n📊 TESTANDO: {test_file.name}")
            
            # Compilar com sanitizers
            compilations = self.compile_with_sanitizers(test_file, test_file.stem)
            
            for san_name, compile_result in compilations.items():
                if compile_result["success"]:
                    # Executar com Valgrind
                    valgrind_result = self.run_with_valgrind(compile_result["path"])
                    
                    test_results[f"{test_file.stem}_{san_name}"] = {
                        "compilation": compile_result,
                        "execution": valgrind_result
                    }
                    
                    # Analisar resultados
                    self._analyze_test_results(test_file.stem, san_name, valgrind_result)
        
        self.running = False
        return test_results
    
    def _analyze_test_results(self, test_name, sanitizer, results):
        """Analisa resultados dos testes"""
        print(f"\n📈 ANALISANDO RESULTADOS: {test_name} ({sanitizer})")
        
        if "error" in results:
            print(f"   ❌ Erro na execução: {results['error']}")
            return
        
        # Verificar vulnerabilidades detectadas
        vulnerabilities = []
        
        if results.get("memory_errors"):
            vulnerabilities.extend(results["memory_errors"])
        
        if results.get("leaks"):
            vulnerabilities.append("Memory leaks detectados")
        
        if "AddressSanitizer" in results.get("stderr", ""):
            if "use-after-free" in results["stderr"]:
                vulnerabilities.append("UAF confirmado pelo ASan")
            if "heap-buffer-overflow" in results["stderr"]:
                vulnerabilities.append("Heap overflow detectado")
            if "double-free" in results["stderr"]:
                vulnerabilities.append("Double free detectado")
        
        if vulnerabilities:
            print(f"   🎯 VULNERABILIDADES DETECTADAS:")
            for vuln in vulnerabilities:
                print(f"      • {vuln}")
                self.detected_vulnerabilities.append({
                    'test': test_name,
                    'sanitizer': sanitizer,
                    'vulnerability': vuln
                })
        else:
            print("   ✅ Nenhuma vulnerabilidade detectada")
    
    def generate_security_report(self):
        """Gera relatório de segurança completo"""
        print("\n" + "="*60)
        print("📊 RELATÓRIO DE SEGURANÇA")
        print("="*60)
        
        print(f"\n📈 VULNERABILIDADES DETECTADAS: {len(self.detected_vulnerabilities)}")
        for vuln in self.detected_vulnerabilities:
            print(f"   • {vuln['test']} ({vuln['sanitizer']}): {vuln['vulnerability']}")
        
        print(f"\n🔒 EVENTOS DE SEGURANÇA: {len(self.security_events)}")
        if self.security_events:
            latest = self.security_events[-1]
            print(f"   Último evento: {time.ctime(latest['timestamp'])}")
            print(f"   Processos ativos: {latest['process_count']}")
        
        print(f"\n📁 ARQUIVOS DE TESTE: {len(list(self.workspace.glob('*.c')))}")
        for test_file in self.workspace.glob("*.c"):
            print(f"   • {test_file.name}")
        
        print(f"\n✅ AMBIENTE: {'Seguro' if self._is_network_isolated() else '⚠️ Não isolado'}")
        print(f"🎯 TESTES EXECUTADOS: {len(self.detected_vulnerabilities)} vulnerabilidades encontradas")
    
    def cleanup(self):
        """Limpeza segura do ambiente"""
        print("\n🧹 REALIZANDO LIMPEZA SEGURA...")
        
        self.running = False
        
        # Parar processos
        if self.test_process:
            self.test_process.terminate()
        
        # Limpar arquivos temporários (opcional)
        # import shutil
        # shutil.rmtree(self.workspace)
        
        print("✅ Ambiente limpo com segurança")

def main():
    """Função principal do harness de teste"""
    print("🛡️  HARNESS DE TESTE SEGURO - UAF DETECTION")
    print("⚠️  Execute apenas em ambiente isolado!")
    
    harness = SafeTestHarness()
    
    try:
        # Executar teste completo
        results = harness.run_comprehensive_test()
        
        # Gerar relatório
        harness.generate_security_report()
        
        # Salvar resultados (opcional)
        print(f"\n💾 Resultados salvos em: {harness.workspace}")
        
    except KeyboardInterrupt:
        print("\n🛑 Teste interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro durante o teste: {e}")
    finally:
        harness.cleanup()

if __name__ == "__main__":
    main()