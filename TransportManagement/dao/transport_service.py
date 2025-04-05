from dao.transport_dao import TransportDAO
from entity.transport import Transport

class TransportService:
    def __init__(self):
        self.transport_dao = TransportDAO()

    def add_transport(self, transport: Transport):
        self.transport_dao.insert_transport(transport)

    def view_all_transports(self):
        return self.transport_dao.get_all_transports()
