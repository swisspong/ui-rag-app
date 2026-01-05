import uuid
from ...domain.services.id_generator import IDGenerator


class UUIDIDGenerator(IDGenerator):
    def new_id(self) -> str:

        return str(uuid.uuid4())
