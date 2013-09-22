from twisted.internet import protocol, reactor
from twisted.protocols.basic import LineReceiver

class Echo(LineReceiver):

    #second parameter is used to share state that exists beyong the lifetime of each connection
    def __init__(self, users):
    	self.users = users
    	self.name = None
    	self.state = "GETNAME"

	# dataReceived - data is received to be processed
    def dataReceived(self, data):
        self.transport.write("data is received: " + data)

    def connectionMade(self):
    	#self.transport.write("there are now %d open connections\n" % (self.factory.numProtocols))
    	self.sendLine("What's your name?")

    def connectionLost(self, reason):
    	#terminate connection only when all data has been written to buffer
    	#self.transport.loseConnection()
    	#abort connection closes it immediately (available 11.1+)
        if self.users.has_key(self.name):
            del self.users[self.name]

    def lineReceived(self, line):
        if self.state == "GETNAME":
            self.handle_GETNAME(line)
        else:
            self.handle_CHAT(line)

    #called when setRawMode is executed
    def rawDataReceived(self, line):
    	pass


    def handle_GETNAME(self, name):
        if self.users.has_key(name):
            self.sendLine("Name taken, please choose another.")
            return
        self.sendLine("Welcome, %s!" % (name,))
        self.name = name
        self.users[name] = self
        self.state = "CHAT"

    def handle_CHAT(self, message):
        message = "<%s> %s" % (self.name, message)
        for name, protocol in self.users.iteritems():
            if protocol != self:
                protocol.sendLine(message)


class EchoFactory(protocol.Factory):
    def __init__(self):
        self.users = {} # maps user names to Chat instances

    def buildProtocol(self, addr):
        return Echo(self.users)

reactor.listenTCP(1234, EchoFactory())
reactor.run()