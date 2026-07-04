import sqlite3
import pandas as pd

DB_NAME = "saas_metrics.db"

def init_mock_db():
    """Initializes a local database containing high-risk vs healthy customer metrics."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customer_health (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT,
        contact_email TEXT,
        monthly_spend_usd REAL,
        days_since_last_login INTEGER,
        support_tickets_opened INTEGER,
        feature_adoption_rate REAL
    )
    """)
    
    # Pre-populate only if completely empty to preserve data consistency
    cursor.execute("SELECT COUNT(*) FROM customer_health")
    if cursor.fetchone()[0] == 0:
        mock_data = [
            ("AlphaCorp", "tech@alphacorp.com", 4500.00, 18, 5, 0.22),
            ("BetaIndustries", "ops@betaindustries.com", 6200.00, 2, 1, 0.85),
            ("GammaLogistics", "contact@gammalogix.com", 1200.00, 25, 4, 0.10),
            ("DeltaMedia", "billing@deltamedia.io", 5500.00, 14, 7, 0.35),
            ("ZetaLabs", "admin@zetalabs.co", 800.00, 1, 0, 0.90)
        ]
        cursor.executemany("""
        INSERT INTO customer_health (company_name, contact_email, monthly_spend_usd, days_since_last_login, support_tickets_opened, feature_adoption_rate)
        VALUES (?, ?, ?, ?, ?, ?)
        """, mock_data)
        conn.commit()
    conn.close()

def execute_query(sql_query: str) -> pd.DataFrame:
    """Executes compiled SQLite commands and outputs tabular metrics data frames."""
    conn = sqlite3.connect(DB_NAME)
    try:
        df = pd.read_sql_query(sql_query, conn)
        return df
    except Exception as e:
        raise Exception(f"Database Runtime Exception: {str(e)}")
    finally:
        conn.close()

if __name__ == "__main__":
    init_mock_db()
    print("📦 Data warehouse layer successfully deployed locally.")