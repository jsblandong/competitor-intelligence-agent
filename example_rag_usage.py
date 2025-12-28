"""
Ejemplo de Uso de RAG para Evitar Alucinaciones
Muestra cómo usar MongoDB para recuperar contexto relevante
"""
import os
import sys
from dotenv import load_dotenv

# Configurar encoding para Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

load_dotenv()

def example_rag_usage():
    """Ejemplo de uso de RAG"""
    
    print("=" * 80)
    print("EJEMPLO DE USO DE RAG")
    print("=" * 80)
    
    try:
        from infrastructure.mongodb_client import MongoDBClient
        from services.embedding_service import EmbeddingService
        from services.rag_service import RAGService
        
        # Inicializar servicios
        mongodb = MongoDBClient()
        embedding_service = EmbeddingService()
        rag_service = RAGService(mongodb, embedding_service)
        
        print("\n1. Buscar contexto relevante...")
        query = "competitor with AI features and hotel management"
        context = rag_service.get_relevant_context(query, context_type="extraction", limit=3)
        
        print(f"   Consulta: {query}")
        print(f"   Contextos encontrados: {len(context)}")
        
        for i, ctx in enumerate(context, 1):
            print(f"\n   Contexto {i}:")
            print(f"   - Dominio: {ctx.get('domain')}")
            print(f"   - Similitud: {ctx.get('similarity', 0):.2f}")
            print(f"   - Datos: {str(ctx.get('extracted_data', {}))[:200]}...")
        
        print("\n2. Construir prompt con RAG...")
        base_prompt = "Analiza este texto y extrae información del competidor."
        enhanced_prompt = rag_service.build_rag_prompt(
            base_prompt,
            query,
            context_type="extraction",
            context_limit=2
        )
        
        print("   Prompt mejorado (primeras 500 caracteres):")
        print(f"   {enhanced_prompt[:500]}...")
        
        print("\n3. Validar datos contra historial...")
        new_data = {
            "name": "Test Competitor",
            "servicios": ["AI", "Analytics"],
            "segmento": "Enterprise"
        }
        
        validation = rag_service.validate_against_history(
            new_data,
            domain="test.com",
            similarity_threshold=0.85
        )
        
        print(f"   Es consistente: {validation['is_consistent']}")
        print(f"   Dominios similares: {validation['similar_domains']}")
        if validation['warnings']:
            print(f"   Advertencias: {validation['warnings']}")
        
        print("\n" + "=" * 80)
        print("✅ EJEMPLO COMPLETADO")
        print("=" * 80)
        
        mongodb.close()
        
    except Exception as e:
        import traceback
        print(f"\n❌ Error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    example_rag_usage()


