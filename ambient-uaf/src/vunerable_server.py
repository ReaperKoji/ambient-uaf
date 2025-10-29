#!/usr/bin/env python3
"""
SERVIDOR VULNERÁVEL CONTROLADO - APENAS PARA TESTES SEGUROS
"""

import socket
import struct
import threading
import time
import sys

class SecureTestServer:
    def __init__(self, host='127.0.0.1', port=9000):
        self.host = host
        self.port = port
        self.running = False
        self.clients = []
        
        # Estado do heap simulado
        self.heap_chunks = []
        self.freed_chunks = set()
        
        print(f"🧪 SERVIDOR DE TESTE SEGURO - {host}:{port}")
        print("⚠️  APENAS PARA AMBIENTE ISOLADO")
        
    def handle_client(self, conn, addr):
        """Manipula cliente em thread isolada"""
        client_id = f"{addr[0]}:{addr[1]}"
        print(f"📡 Cliente conectado: {client_id}")
        
        try:
            while self.running:
                data = conn.recv(1024)
                if not data:
                    break
                    
                response = self.process_command(data, client_id)
                conn.send(response)
                
        except Exception as e:
            print(f"❌ Erro com {client_id}: {e}")
        finally:
            conn.close()
            print(f"🔌 Cliente desconectado: {client_id}")

    def process_command(self, data, client_id):
        """Processa comandos de teste"""
        try:
            if b":" in data:
                cmd, payload = data.split(b":", 1)
                cmd = cmd.decode('ascii', errors='ignore').strip()
            else:
                cmd = data.decode('ascii', errors='ignore').strip()
                payload = b""
            
            print(f"🎯 Comando de {client_id}: {cmd}")
            
            # Comandos de teste controlados
            if cmd == "CREATE":
                return self.cmd_create(payload)
            elif cmd == "DELETE":
                return self.cmd_delete(payload) 
            elif cmd == "USE":
                return self.cmd_use(payload)
            elif cmd == "ALLOC":
                return self.cmd_alloc(payload)
            elif cmd == "FREE":
                return self.cmd_free(payload)
            elif cmd == "READ":
                return self.cmd_read(payload)
            elif cmd == "HEAPINFO":
                return self.cmd_heapinfo()
            elif cmd == "SHUTDOWN":
                self.running = False
                return b"SERVER_SHUTDOWN"
            else:
                return b"UNKNOWN_COMMAND"
                
        except Exception as e:
            return f"ERROR: {str(e)}".encode()

    def cmd_create(self, payload):
        """Cria objeto 'vulnerável'"""
        obj_id = payload[:32].decode('ascii', errors='ignore')
        
        chunk = {
            'id': obj_id,
            'data': b"initial_data_" + os.urandom(8),
            'size': 64,
            'freed': False
        }
        
        self.heap_chunks.append(chunk)
        return f"CREATED:{obj_id}".encode()

    def cmd_delete(self, payload):
        """Libera objeto (simula free)"""
        obj_id = payload[:32].decode('ascii', errors='ignore')
        
        for chunk in self.heap_chunks:
            if chunk['id'] == obj_id:
                chunk['freed'] = True
                self.freed_chunks.add(obj_id)
                return b"DELETED"
        
        return b"NOT_FOUND"

    def cmd_use(self, payload):
        """Uso após free - comportamento controlado"""
        obj_id = payload[:32].decode('ascii', errors='ignore')
        
        for chunk in self.heap_chunks:
            if chunk['id'] == obj_id:
                if chunk['freed']:
                    # Comportamento de UAF simulado
                    response = b"UAF_DETECTED:"
                    # Dados "vazados" controlados
                    response += struct.pack("<Q", 0x7f001337deadbeef)
                    response += chunk['data'][:8]
                    return response
                return chunk['data']
        
        return b"OBJECT_NOT_FOUND"

    def cmd_alloc(self, payload):
        """Alocação controlada de memória"""
        if len(payload) >= 4:
            size = struct.unpack("<I", payload[:4])[0]
            chunk_id = f"chunk_{len(self.heap_chunks)}"
            
            chunk = {
                'id': chunk_id,
                'data': payload[4:4+min(size, 256)],
                'size': size,
                'freed': False
            }
            
            self.heap_chunks.append(chunk)
            return f"ALLOCATED:{chunk_id}".encode()
        
        return b"ALLOC_FAILED"

    def cmd_free(self, payload):
        """Liberação controlada"""
        chunk_id = payload[:32].decode('ascii', errors='ignore')
        
        for chunk in self.heap_chunks:
            if chunk['id'] == chunk_id:
                if chunk['freed']:
                    return b"DOUBLE_FREE_DETECTED"
                chunk['freed'] = True
                return b"FREED"
        
        return b"CHUNK_NOT_FOUND"

    def cmd_read(self, payload):
        """Leitura controlada"""
        chunk_id = payload[:32].decode('ascii', errors='ignore')
        
        for chunk in self.heap_chunks:
            if chunk['id'] == chunk_id:
                if chunk['freed']:
                    return b"READ_AFTER_FREE:" + chunk['data'][:16]
                return chunk['data']
        
        return b"CHUNK_NOT_FOUND"

    def cmd_heapinfo(self):
        """Informações do heap simulado (para debug)"""
        info = f"Chunks: {len(self.heap_chunks)}, Freed: {len(self.freed_chunks)}"
        return info.encode()

    def start(self):
        """Inicia servidor de teste"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = True
        
        print(f"🚀 Servidor iniciado em {self.host}:{self.port}")
        print("💡 Comandos disponíveis: CREATE, DELETE, USE, ALLOC, FREE, READ, HEAPINFO")
        
        try:
            while self.running:
                conn, addr = self.server_socket.accept()
                client_thread = threading.Thread(
                    target=self.handle_client, 
                    args=(conn, addr)
                )
                client_thread.daemon = True
                client_thread.start()
                
        except KeyboardInterrupt:
            print("\n🛑 Servidor parado pelo usuário")
        except Exception as e:
            print(f"❌ Erro no servidor: {e}")
        finally:
            self.server_socket.close()
            print("✅ Servidor finalizado")

if __name__ == "__main__":
    import os
    server = SecureTestServer()
    server.start()