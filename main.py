import threading
import socket
import sys
import time

from drone import drone

# このプログラムを実行するPCのアドレス
host = '192.168.11.2'

# droneA との通信でのPC側のアドレス
portA = int(9000)
locaddrA = (host,portA)

# droneB との通信でのPC側のアドレス
portB = int(9001)
locaddrB = (host,portB)

# droneA/droneB のアドレス
addressA = '192.168.11.65'
addressB = '192.168.11.64'

# droneを制御するためのオブジェクトを作成
droneA = drone(addressA, host, portA)
droneB = drone(addressB, host, portB)

# コマンドの送信先としてdroneを配列に格納
drones = {droneA, droneB}

# droneに送信するコマンドの配列※順番に実行
command_dict = [
  'takeoff',
  'forward 50',
  'right 50',
  'back 70',
  'left 50',
  'land',
]


print ('formation flight start\n')

# コマンド配列の中の実行対象を特定するindex
command_index = 0

# command コマンドを全droneに送信、コマンドを受け付ける状態にする
for drone in drones:
    drone.connect()
    drone.send_command('command')

while True:
    try:
        #次に実行するコマンド
        step_command = command_dict[command_index]

        accepted = 0
        #全機がコマンド送信可能状態になるまで待つ
        for drone in drones:
            if drone.is_accept_command:
                accepted += 1
            if accepted == len(drones):
                break

        if accepted == len(drones):
            for drone in drones:
                #全機にコマンド送信
                drone.send_command(step_command)
            #コマンド位置を進め次のコマンドに
            command_index += 1
            # コマンド送信後に固定の待ち時間を追加
            time.sleep(2)
            # 離陸コマンドを実行したあとは長めのインターバル
            if step_command == 'takeoff':
                time.sleep(6)
            # 着陸コマンドを実行したあとは抜ける
            if step_command == 'land':
                break

        # accept検査のインターバル
        time.sleep(0.1)

    except Exception as e:
        tb = sys.exc_info()[2]
        print (e.with_traceback(tb))

# droneとの通信を終了
for drone in drones:
    drone.disconnect()

print ('\nformation flight end')
