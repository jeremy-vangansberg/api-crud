from sqlalchemy import create_engine
from model import Base


# Créer une base de données SQLite en mémoire
engine = create_engine('sqlite:///database.db')

# Créer toutes les tables
Base.metadata.create_all(engine)