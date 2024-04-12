from uuid import UUID, uuid4
from applications.models import Operation

operations: dict[UUID, Operation] = {}


class OperationsService:
    def create_operation(self) -> UUID:
        id = uuid4()
        operations[id] = Operation(id)
        return id
    
    
    def finish_operation(self, id: UUID, result):
        if not id in operations:
            raise KeyError
        operations[id].result = result
        operations[id].done = True
    
    
    def get_operation(self, id: UUID) -> Operation:
        if not id in operations:
            raise KeyError
        return operations[id]