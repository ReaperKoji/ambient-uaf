#include <iostream>
#include <cstdlib>
#include <cstring>

// Teste de UAF com AddressSanitizer
class UAFTest {
public:
    char* buffer;
    
    UAFTest() {
        buffer = new char[64];
        strcpy(buffer, "UAF Test Data");
        std::cout << "✅ Objeto criado em: " << (void*)buffer << std::endl;
    }
    
    ~UAFTest() {
        std::cout << "🗑️  Objeto destruído: " << (void*)buffer << std::endl;
        delete[] buffer;
    }
    
    void use() {
        std::cout << "📖 Lendo: " << buffer << std::endl;
    }
};

void test_uaf_asan() {
    std::cout << "\n🧪 TESTE UAF COM ASAN\n";
    
    UAFTest* obj = new UAFTest();
    delete obj;  // Liberar objeto
    
    // UAF INTENCIONAL - deve ser detectado pelo ASan
    obj->use();  // Use After Free!
}

void test_double_free() {
    std::cout << "\n🧪 TESTE DOUBLE FREE\n";
    
    char* data = new char[32];
    delete[] data;  // Primeiro free
    
    // Double free intencional
    delete[] data;  // Segundo free - deve ser detectado
}

void test_heap_overflow() {
    std::cout << "\n🧪 TESTE HEAP OVERFLOW\n";
    
    char* small = new char[8];
    strcpy(small, "Very long string that overflows");  // Overflow
    delete[] small;
}

int main() {
    std::cout << "🔍 INICIANDO TESTES DE DETECÇÃO UAF\n";
    std::cout << "⚠️  Compile com: clang++ -fsanitize=address -g este_arquivo.cpp\n\n";
    
    // test_uaf_asan();      // Descomente para testar UAF
    // test_double_free();   // Descomente para testar double free  
    // test_heap_overflow(); // Descomente para testar overflow
    
    std::cout << "\n✅ Testes concluídos (comentados por segurança)\n";
    std::cout << "💡 Descomente os testes no código para executar\n";
    
    return 0;
}