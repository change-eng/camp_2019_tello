import threading
import socket
import time

class drone:
    DRONE_COMMAND_PORT = 8889

    def __init__(self, drone_address, local_address, local_receive_port) :
        # 初期化しておくべき変数の対応
        self.is_accept_command = False
        # 受け取った値で変数を初期化
        self.drone_address_port = (drone_address, self.DRONE_COMMAND_PORT)
        self.drone_address = drone_address
        self.local_address = local_address
        self.local_receive_port = local_receive_port


    def connect(self) :
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # UDP通信、コマンドresponse受け取りを行うsocketでアドレスをbind
        local_address_port = (self.local_address, self.local_receive_port)
        self.sock.bind(local_address_port)

        # コマンドresponse受け取りのスレッドを起動
        receive_thread = threading.Thread(target=self.receive_command_thread)
        receive_thread.start()


    def disconnect(self) :
        self.sock.close()


    def receive_command_thread(self) :
        while True:
            try:
                # ソケットからメッセージを受け取る
                data, server = self.sock.recvfrom(1518)

                # 受信したメッセージをデバグ出力
                receive_message = data.decode(encoding="utf-8")
                timestamp = str(int(time.time()))
                debug_message = self.drone_address + ':'  + timestamp  + ':' + receive_message
                print(debug_message)

                # メッセージを受信したタイミングでコマンドの受信を受け入れる
                self.is_accept_command = True
            except Exception:
                # 終了時のメッセージを出力して終了
                timestamp = str(int(time.time()))
                debug_message = self.drone_address + ':'  + timestamp  + ':Exit...'
                print (debug_message)
                break


    def send_command(self, command) :
        # コマンドをソケットに流す
        command_message = command.encode(encoding="utf-8")
        self.sock.sendto(command_message, self.drone_address_port)
        timestamp = str(int(time.time()))
        debug_message = self.drone_address + ':'  + timestamp  +':' + command
        print(debug_message)

