from twisted.internet import protocol, reactor

transport = set()
class Chat(protocol.Protocol):
    def connectionMade(self):
        print('connnn')
        transport.add(self.transport)

    def dataReceived(self, data):
        for t in transport:
            if self.transport is not t:
                t.write(data)
        #print(data.decode('utf-8', 'ignore'))  # 인코딩 방식을 'utf-8'로 지정하여 디코드

class ChatFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Chat()

print('Server started!')
reactor.listenTCP(8000, ChatFactory())
reactor.run()