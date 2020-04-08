class WSSession:
    def __init__(self, distributor, ws):
        self.distributor = distributor
        self.ws = ws

    def receive(self, data):
        print(data)