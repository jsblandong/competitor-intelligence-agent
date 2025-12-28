import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def seed_database():
    db_url = os.getenv("SUPABASE_DB_URL")
    if db_url:
        db_url = db_url.strip()
        
    try:
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        
        print("--- Seeding dim_source ---")
        sources = [
            {
                "name": "AI Agent Scraper",
                "url": "https://github.com/your-org/competitor-intelligence-agent",
                "description": "Automated web scraping agent that extracts competitor data using AI-powered analysis. Provides scoring on 10 attributes and generates strategic insights.",
                "source_type": "automated",
                "reliability_score": 0.85
            },
            {
                "name": "Manual Entry",
                "url": None,
                "description": "Manual data entry by research team. Used for verified information and corrections to automated data.",
                "source_type": "manual",
                "reliability_score": 1.0
            },
            {
                "name": "API Import",
                "url": None,
                "description": "Direct API integration with third-party data providers for competitor intelligence.",
                "source_type": "api",
                "reliability_score": 0.90
            }
        ]
        
        for source in sources:
            cursor.execute("SELECT 1 FROM dim_source WHERE name = %s", (source['name'],))
            if not cursor.fetchone():
                cursor.execute(
                    """INSERT INTO dim_source (name, url, description, source_type, reliability_score, is_active) 
                       VALUES (%s, %s, %s, %s, %s, %s)""",
                    (source['name'], source['url'], source['description'], 
                     source['source_type'], source['reliability_score'], True)
                )
                print(f"Inserted source: {source['name']}")
            else:
                # Update existing sources with new fields
                cursor.execute(
                    """UPDATE dim_source 
                       SET url = %s, description = %s, source_type = %s, 
                           reliability_score = %s, is_active = %s
                       WHERE name = %s""",
                    (source['url'], source['description'], source['source_type'], 
                     source['reliability_score'], True, source['name'])
                )
                print(f"Updated source: {source['name']}")

        print("\n--- Seeding dim_attribute ---")
        # Attributes with their dimension (Strategy/Complexity)
        attributes = [
            ("price_competitiveness", "Price Competitiveness", "Higher is better/cheaper", "Strategy"),
            ("feature_set_completeness", "Feature Set Completeness", "Completeness of features", "Complexity"),
            ("brand_sentiment", "Brand Sentiment", "Public perception", "Strategy"),
            ("market_reach", "Market Reach", "Market presence", "Strategy"),
            ("innovation_score", "Innovation Score", "Level of innovation", "Strategy"),
            ("customer_satisfaction", "Customer Satisfaction", "User happiness", "Strategy"),
            ("ease_of_use", "Ease of Use", "Usability", "Complexity"),
            ("integration_capabilities", "Integration Capabilities", "Ability to integrate", "Complexity"),
            ("support_quality", "Support Quality", "Quality of support", "Complexity"),
            ("security_compliance", "Security/Compliance", "Security standards", "Complexity")
        ]
        
        for code, name, desc, dimension in attributes:
            cursor.execute("SELECT 1 FROM dim_attribute WHERE code = %s", (code,))
            if not cursor.fetchone():
                # Trying X and Y as they correspond to the axes in scoring_agent.py
                dim_val = 'X' if dimension == 'Strategy' else 'Y'
                
                cursor.execute(
                    "INSERT INTO dim_attribute (code, name, description, dimension) VALUES (%s, %s, %s, %s)", 
                    (code, name, desc, dim_val)
                )
                print(f"Inserted attribute: {code}")
            else:
                print(f"Attribute already exists: {code}")
        
        conn.commit()
        conn.close()
        print("\n[SUCCESS] Database seeding complete.")
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"[ERROR] Seeding failed: {repr(e)}")

if __name__ == "__main__":
    seed_database()
