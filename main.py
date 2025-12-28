"""
Main Entry Point - Refactorizado
Orquesta el flujo completo según reglas de negocio.
"""
import argparse
import os
from dotenv import load_dotenv
from agents.scraper_agent import ScraperAgent
from agents.scoring_agent import ScoringAgent
from agents.db_writer_agent import DBWriterAgent
from agents.insights_agent import InsightsAgent
from infrastructure.logging_config import get_logger

# Load environment variables
load_dotenv()

def main():
    """Función principal del agente de inteligencia competitiva"""
    parser = argparse.ArgumentParser(
        description="Competitor Intelligence Agent - Chief Market Analyst Automatizado"
    )
    parser.add_argument("url", nargs="?", help="URL del competidor a analizar")
    parser.add_argument("--dry-run", action="store_true", help="Ejecutar sin guardar en base de datos")
    parser.add_argument("--log-file", help="Archivo de log (opcional)")
    args = parser.parse_args()
    
    # Configurar logger
    logger = get_logger("Main", args.log_file)
    
    logger.info("=" * 80)
    logger.info("🚀 INICIANDO ANÁLISIS DE COMPETIDOR")
    logger.info("=" * 80)
    
    # Obtener URL
    if not args.url:
        args.url = input("Por favor ingresa la URL del competidor: ").strip()
        if not args.url:
            logger.error("❌ URL es requerida")
            return
    
    logger.info(f"📋 URL objetivo: {args.url}")
    
    try:
        # 1. Extracción de datos
        logger.info("\n" + "=" * 80)
        logger.info("FASE 1: EXTRACCIÓN DE DATOS")
        logger.info("=" * 80)
        
        scraper = ScraperAgent()
        competitor_data = scraper.scrape(args.url)
        
        if not competitor_data:
            logger.error("❌ No se pudieron extraer datos del competidor")
            return
        
        logger.info(f"✓ Datos extraídos para: {competitor_data.name} ({competitor_data.domain})")
        logger.info(f"  - Fuentes: {len(competitor_data.sources)}")
        logger.info(f"  - Servicios: {len(competitor_data.servicios) if competitor_data.servicios else 0}")
        logger.info(f"  - Integraciones: {len(competitor_data.integraciones) if competitor_data.integraciones else 0}")
        logger.info(f"  - Pricing explícito: {'Sí' if competitor_data.has_explicit_pricing else 'No'}")
        
        # 2. Scoring
        logger.info("\n" + "=" * 80)
        logger.info("FASE 2: SCORING Y EVALUACIÓN")
        logger.info("=" * 80)
        
        scorer = ScoringAgent()
        scores = scorer.calculate_scores(competitor_data)
        
        if not scores:
            logger.error("❌ No se pudieron calcular scores")
            return
        
        logger.info(f"✓ Scores calculados:")
        logger.info(f"  - Strategy Score (X): {scores.x_score:.2f}" if scores.x_score else "  - Strategy Score (X): NULL")
        logger.info(f"  - Complexity Score (Y): {scores.y_score:.2f}" if scores.y_score else "  - Complexity Score (Y): NULL")
        
        # Mostrar scores con evidencia
        scores_with_evidence = sum(1 for attr in scores.attributes.values() if attr.raw_score is not None)
        logger.info(f"  - Atributos con score: {scores_with_evidence}/{len(scores.attributes)}")
        
        # 3. Insights estratégicos
        logger.info("\n" + "=" * 80)
        logger.info("FASE 3: INSIGHTS ESTRATÉGICOS")
        logger.info("=" * 80)
        
        insights_agent = InsightsAgent()
        insights = insights_agent.generate_insights(competitor_data, scores)
        
        if not insights:
            logger.error("❌ No se pudieron generar insights")
            return
        
        logger.info(f"✓ Insights generados:")
        logger.info(f"  - Fortalezas clave: {len(insights.fortalezas_clave)}")
        logger.info(f"  - Oportunidades: {len(insights.oportunidades_mercado)}")
        logger.info(f"  - Riesgos/Debilidades: {len(insights.riesgos_debilidades)}")
        
        # Mostrar insights resumidos
        if insights.fortalezas_clave:
            logger.info("\n  Fortalezas clave:")
            for i, fortaleza in enumerate(insights.fortalezas_clave[:3], 1):
                logger.info(f"    {i}. {fortaleza}")
        
        # 4. Guardar en base de datos (a menos que sea dry-run)
        if not args.dry_run:
            logger.info("\n" + "=" * 80)
            logger.info("FASE 4: PERSISTENCIA EN BASE DE DATOS")
            logger.info("=" * 80)
            
            db_writer = DBWriterAgent()
            try:
                competitor_id = db_writer.save_competitor(competitor_data, scores, insights)
                
                if competitor_id:
                    logger.log_db_save(competitor_data.domain, competitor_id, True)
                    logger.info(f"✓ Competidor guardado con ID: {competitor_id}")
                    
                    # Guardar productos si hay
                    if competitor_data.pricing and competitor_data.pricing.get('products'):
                        logger.info("  Guardando productos y pricing...")
                        # El DBWriter maneja productos internamente
                        logger.info("  ✓ Productos guardados")
                else:
                    logger.log_db_save(competitor_data.domain, None, False)
                    logger.warning("⚠ No se pudo guardar competidor")
                    
            except Exception as e:
                logger.log_db_save(competitor_data.domain, None, False)
                logger.error(f"❌ Error al guardar en BD: {e}", exc_info=True)
        else:
            logger.info("\n" + "=" * 80)
            logger.info("MODO DRY-RUN: Saltando guardado en base de datos")
            logger.info("=" * 80)
        
        # Resumen final
        logger.info("\n" + "=" * 80)
        logger.info("✅ ANÁLISIS COMPLETADO")
        logger.info("=" * 80)
        logger.info(f"Competidor: {competitor_data.name}")
        logger.info(f"Dominio: {competitor_data.domain}")
        if scores.x_score and scores.y_score:
            logger.info(f"Posición estratégica: X={scores.x_score:.2f}, Y={scores.y_score:.2f}")
        logger.info("=" * 80)
        
    except KeyboardInterrupt:
        logger.warning("\n⚠ Análisis interrumpido por el usuario")
    except Exception as e:
        logger.error(f"❌ Error fatal: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
