# Configure engine to be used in all modules
from .db.main import setup_engine #To setup the DB session
engine = setup_engine()
