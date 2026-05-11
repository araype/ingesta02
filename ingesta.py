import boto3
import mysql.connector
import csv

# --- Configuración MySQL ---
host_db     = "mysql-ingesta.crjrytku2mvw.us-east-1.rds.amazonaws.com"      # ej: endpoint de RDS
usuario_db  = "admin"
password_db = "Ut3c651620_14"
nombre_db   = "cursodb"
nombre_tabla = "personas"

# --- Configuración S3 ---
ficheroCSV   = "output.csv"
nombreBucket = "araype3047"

# 1. Conectar a MySQL y leer todos los registros
conn = mysql.connector.connect(
    host=host_db,
    user=usuario_db,
    password=password_db,
    database=nombre_db
)
cursor = conn.cursor()
cursor.execute(f"SELECT * FROM {nombre_tabla}")
filas = cursor.fetchall()
columnas = [desc[0] for desc in cursor.description]
cursor.close()
conn.close()

# 2. Guardar en CSV
with open(ficheroCSV, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(columnas)
    writer.writerows(filas)

print(f"CSV generado con {len(filas)} registros")

# 3. Subir CSV a S3
s3 = boto3.client("s3")
s3.upload_file(ficheroCSV, nombreBucket, ficheroCSV)

print("Ingesta completada — archivo subido a S3")