import uuid
from datetime import datetime

class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Actualizar la marca de tiempo updated_at cada vez que se modifique el objeto"""
        self.updated_at = datetime.now()

    def update(self, data):
        """Actualizar los atributos del objeto según el diccionario proporcionado"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Actualizar la marca de tiempo updated_at
