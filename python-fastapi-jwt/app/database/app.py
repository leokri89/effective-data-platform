import psycopg2

conn = psycopg2.connect(
    dbname='postgres',
    user='postgres',
    password='postgres',
    host='127.0.0.1',
    port=5432
)

cursor = conn.cursor()

cursor.execute("""
SELECT pg_get_functiondef('dax.sp_uma_proc'::regproc);
""")

result = cursor.fetchall()
print(result)

