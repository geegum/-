from twisted.internet import protocol, reactor

transport = set()
class Chat(protocol.Protocol):
    def connectionMade(self):
        print('connnn222')
        transport.add(self.transport)

    def dataReceived(self, data):
        for t in transport:
            if self.transport is not t:
                t.write(data)
        #print(data.decode('utf-8', 'ignore'))  # 인코딩 방식을 'utf-8'로 지정하여 디코드

class ChatFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Chat()

print('Server22 started!')
reactor.listenTCP(8005, ChatFactory())
reactor.run()