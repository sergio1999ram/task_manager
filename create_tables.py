from app_config import db

db.create_all()
db.session.commit()
