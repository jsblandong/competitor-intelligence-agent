# Competitor Intelligence Agent

## 🎯 Objetivo

**Chief Market Analyst Automatizado** para el mercado hotel-tech. Una herramienta estratégica autónoma capaz de operar como un analista de mercados completo, extrayendo, estructurando y analizando información de competidores.

## 🏗️ Arquitectura

Arquitectura monolítica escalable con separación clara de responsabilidades:

```
competitor_intelligence_agent/
├── domain/              # Modelos y Reglas de Negocio
│   ├── models.py        # Entidades de dominio
│   └── validators.py    # Validadores de reglas de negocio
├── services/            # Lógica de Negocio
│   ├── extraction_service.py
│   ├── scoring_service.py
│   └── insights_service.py
├── agents/              # Orquestación
│   ├── scraper_agent.py
│   ├── scoring_agent.py
│   ├── insights_agent.py
│   └── db_writer_agent.py
├── infrastructure/      # Infraestructura
│   └── logging_config.py
└── database/            # Esquema y Migraciones
```

Ver [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) para detalles completos.

## ✨ Características Principales

### 1. Extracción Inteligente
- ✅ Extracción de datos estructurados desde sitios web
- ✅ Búsqueda automática de páginas de pricing
- ✅ Renderizado JavaScript con Playwright
- ✅ Trazabilidad completa de fuentes

### 2. Scoring Profesional
- ✅ 10 atributos de evaluación
- ✅ Validación de evidencia obligatoria
- ✅ NULL si no hay evidencia suficiente (no valores por defecto)
- ✅ Cálculo de scores estratégicos (X, Y)

### 3. Insights Estratégicos
- ✅ Fortalezas clave
- ✅ Oportunidades del mercado
- ✅ Riesgos y debilidades
- ✅ Formato JSON validado

### 4. Persistencia Robusta
- ✅ Un competidor = un registro único por dominio
- ✅ Trazabilidad completa (URLs y timestamps)
- ✅ Idempotencia (evita duplicados)

## 📋 Reglas de Negocio

### Fuentes Permitidas
- Sitios web públicos de competidores
- Redes sociales (Instagram) - *Pendiente*
- Documentación oficial o blogs
- Reseñas de usuarios públicas

### Restricciones
- ❌ No información privada o restringida
- ❌ No inferir precios sin evidencia explícita
- ❌ No mezclar competidores en análisis

### Validación
- ✅ Cada dato debe tener URL válida asociada
- ✅ Trazabilidad a fuente original obligatoria
- ✅ Sin información especulativa sin evidencia

## 🚀 Uso Rápido

### Instalación

```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales
```

### Ejecución

```bash
# Análisis básico
python main.py https://competitor.com

# Dry-run (sin guardar en BD)
python main.py https://competitor.com --dry-run

# Con logging a archivo
python main.py https://competitor.com --log-file logs/analysis.log
```

### Verificar Configuración

```bash
# Verificar credenciales
python tests/test_credentials.py

# Seed de base de datos
python seed_db.py
```

## 🔧 Configuración

### Variables de Entorno

```env
# Base de datos (requerido)
SUPABASE_DB_URL=postgresql://user:pass@host:port/db

# LLM Provider (opcional, default: openai)
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...

# Ollama (alternativa local)
OLLAMA_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=llama3.1:8b
```

### Base de Datos

1. Ejecutar esquema base:
```sql
-- Ejecutar en Supabase SQL Editor
\i database/schema.sql
```

2. Seed de datos iniciales:
```bash
python seed_db.py
```

3. Aplicar migraciones:
```sql
-- Migración 002: Productos y Pricing
\i migrations/002_add_product_pricing.sql

-- Migración 003: Dominio y Trazabilidad
\i migrations/003_add_domain_and_traceability.sql
```

## 📊 Estructura de Datos Extraídos

Cada competidor incluye:

- **Identificación**: dominio, nombre, slug (únicos)
- **Servicios**: Lista de servicios ofrecidos
- **Modelo de Negocio**: SaaS, Marketplace, etc.
- **Segmento**: Segmento de mercado objetivo
- **Capacidad Analítica**: Nivel de capacidades
- **Nivel Operativo**: Operativo vs Estratégico
- **Propuesta de Valor**: Propuesta principal
- **Innovaciones**: Innovaciones tecnológicas
- **Integraciones**: Integraciones disponibles
- **Pricing**: Solo si hay evidencia explícita
- **Diferenciadores**: Puntos diferenciadores
- **Casos de Uso**: Casos de uso identificados

## 🎯 Scoring

### Atributos Evaluados

**Estrategia (X Score):**
- Price Competitiveness
- Brand Sentiment
- Market Reach
- Innovation Score
- Customer Satisfaction

**Complejidad (Y Score):**
- Feature Set Completeness
- Ease of Use
- Integration Capabilities
- Support Quality
- Security/Compliance

### Reglas de Scoring

- ✅ Solo scores con evidencia explícita
- ✅ NULL si no hay evidencia suficiente
- ✅ Cada score tiene URLs de evidencia asociadas
- ✅ Prohibido inferir sin prueba

## 💡 Insights Estratégicos

Cada análisis genera:

1. **Fortalezas Clave** (3-5 items)
   - Propuesta de valor única
   - Características diferenciadoras
   - Posicionamiento en mercado

2. **Oportunidades del Mercado** (3-5 items)
   - Gaps en el mercado
   - Tendencias emergentes
   - Segmentos no atendidos

3. **Riesgos/Debilidades** (3-5 items)
   - Vulnerabilidades competitivas
   - Limitaciones técnicas
   - Riesgos de mercado

## 📈 Plano Cartesiano Estratégico

Los competidores se ubican en un plano X-Y:
- **X (Strategy Score)**: Posicionamiento estratégico
- **Y (Complexity Score)**: Nivel de sofisticación

Permite identificar:
- Market Leaders (X alto, Y alto)
- Magic Quadrant Candidates (X alto, Y bajo)
- Niche Players (X bajo, Y bajo)
- Enterprise Players (X alto, Y alto)

## 🔍 Logging y Auditoría

Sistema de logging estructurado:
- Timestamps precisos
- Niveles: DEBUG, INFO, WARNING, ERROR
- Trazabilidad de operaciones
- Logs a archivo opcional

Ejemplo de log:
```
2025-01-XX 10:30:15 | INFO     | ScraperAgent | 🔍 INICIO EXTRACCIÓN | URL: https://competitor.com
2025-01-XX 10:30:18 | INFO     | ScraperAgent | 🔍 FIN EXTRACCIÓN | ✓ ÉXITO | Dominio: competitor.com
2025-01-XX 10:30:20 | INFO     | ScoringAgent | 📊 INICIO SCORING | Dominio: competitor.com
2025-01-XX 10:30:25 | INFO     | ScoringAgent | 📊 FIN SCORING | X: 0.75 | Y: 0.68
```

## 🛠️ Desarrollo

### Estructura del Código

- **Domain Layer**: Modelos y validadores (sin dependencias externas)
- **Services Layer**: Lógica de negocio reutilizable
- **Agents Layer**: Orquestación de servicios
- **Infrastructure Layer**: Utilidades compartidas

### Testing

```bash
# Verificar credenciales
python tests/test_credentials.py

# Inspeccionar fuente de datos
python tests/inspect_source.py

# Verificar proveedor LLM
python tests/check_llm_provider.py

# Validar agentes
python tests/validate_agents.py

# Validar extracción de segmentos
python tests/validate_segment_extraction.py

# Analizar calidad de datos
python tests/analyze_data_quality.py
```

### Migraciones

Las migraciones están numeradas y deben ejecutarse en orden:
1. `002_add_product_pricing.sql`
2. `003_add_domain_and_traceability.sql`

## 📝 Mejoras Implementadas

1. ✅ Arquitectura monolítica escalable
2. ✅ Sistema de validación robusto
3. ✅ Eliminación de datos mock (solo datos reales)
4. ✅ Estructura de datos según reglas de negocio
5. ✅ Scoring con validación de evidencia
6. ✅ Insights estratégicos estructurados
7. ✅ Persistencia única por dominio
8. ✅ Trazabilidad completa
9. ✅ Sistema de logging estructurado
10. ✅ Esquema de BD actualizado

## 🚧 Próximos Pasos

- [ ] Implementar scraping de Instagram
- [ ] Mejorar extracción de pricing con más patrones
- [ ] Visualización de plano cartesiano estratégico
- [ ] Análisis comparativo entre competidores
- [ ] Dashboard web para visualización
- [ ] API REST para integración externa

## 📄 Licencia

[Especificar licencia]

## 🤝 Contribuciones

[Instrucciones para contribuir]

---

**Nota**: Este proyecto está diseñado para ser el desarrollo inicial de un producto estratégico. La arquitectura es monolítica pero escalable, preparada para crecer según necesidades del negocio.

