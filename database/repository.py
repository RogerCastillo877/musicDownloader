from database.engine import SessionLocal


class Repository:

    def __init__(self):
        self.session = SessionLocal()

    def close(self):
        self.session.close()