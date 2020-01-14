from network import *

def app():
    while True:
        try:
            for peer in P2PNetwork.peers:
                try:
                    client = Client(peer)
                    while True:
                        message = input()
                        if message == 'cmd_show_peers':
                            client.send_message('cmd_show_peers')
                        elif message == 'cmd_quit':
                            client.send_message('cmd_quit')
                            client.send_disconnect_signal()
                        else:
                            client.send_message(message)
                except KeyboardInterrupt:
                    sys.exit(0)
                except Exception as exception:
                    print(exception)

                try:
                    server = Server(byte_size = 1024)
                    server.run()
                except KeyboardInterrupt:
                    sys.exit(0)
                except Exception as exception:
                    print(exception)


        except KeyboardInterrupt:
            sys.exit(0)

if __name__ == '__main__':
    app()