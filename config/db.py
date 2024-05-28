from pymongo import MongoClient

# Conectarse al servidor MongoDB
conn = MongoClient("mongodb://localhost:27017/")

# Acceder a la base de datos llamada 'apiBasesAvanzadas'
db = conn.apiBasesAvanzadas

# Acceder a la colección llamada 'nomina'
nomina_collection = db.nomina