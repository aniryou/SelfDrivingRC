import io
import struct
import socket
import time
import traceback
import picamera
from AMSpi import AMSpi

SERVER_IP = '192.168.1.6'
SERVER_PORT = 8000

if __name__ == '__main__':
    with AMSpi() as amspi, picamera.PiCamera() as camera:
        client_socket = socket.socket()
        client_socket.connect((SERVER_IP, SERVER_PORT))
        connection = client_socket.makefile('wb')
        stream = io.BytesIO()

        amspi.set_74HC595_pins(21, 20, 16)
        amspi.set_L293D_pins(5, 6, 13, 19)

        camera.resolution = (640, 480)
        camera.framerate = 10
        camera.start_preview()
        time.sleep(2)

        for foo in camera.capture_continuous(stream, 'jpeg'):
            try:
                connection.write(struct.pack('<L', stream.tell()))
                connection.flush()
                stream.seek(0)
                connection.write(stream.read())
                cmd = client_socket.recv(4096)
                print(cmd)
                
                if cmd == 'F':
                    # FORWARD
                    amspi.run_dc_motor(amspi.DC_Motor_1, clockwise=True,)
                    amspi.run_dc_motor(amspi.DC_Motor_2, clockwise=True)
                    amspi.run_dc_motor(amspi.DC_Motor_3, clockwise=True)
                    amspi.run_dc_motor(amspi.DC_Motor_4, clockwise=False)
                    time.sleep(.1)
                    amspi.stop_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4])
                elif cmd == 'B':
                    # BACKWARD
                    amspi.run_dc_motor(amspi.DC_Motor_1, clockwise=False)
                    amspi.run_dc_motor(amspi.DC_Motor_2, clockwise=False)
                    amspi.run_dc_motor(amspi.DC_Motor_3, clockwise=False)
                    amspi.run_dc_motor(amspi.DC_Motor_4, clockwise=True)
                    time.sleep(.1)
                    amspi.stop_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4])
                elif cmd == 'L':
                    # LEFT
                    amspi.run_dc_motor(amspi.DC_Motor_1, clockwise=False)
                    amspi.run_dc_motor(amspi.DC_Motor_2, clockwise=False)
                    amspi.run_dc_motor(amspi.DC_Motor_3, clockwise=True)
                    amspi.run_dc_motor(amspi.DC_Motor_4, clockwise=False)
                    time.sleep(.1)
                    amspi.stop_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4])
                elif cmd == 'R':
                    # RIGHT
                    amspi.run_dc_motor(amspi.DC_Motor_1, clockwise=True)
                    amspi.run_dc_motor(amspi.DC_Motor_2, clockwise=True)
                    amspi.run_dc_motor(amspi.DC_Motor_3, clockwise=False)
                    amspi.run_dc_motor(amspi.DC_Motor_4, clockwise=True)
                    time.sleep(.1)
                    amspi.stop_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4])
                stream.seek(0)
                stream.truncate()
            except:
                amspi.stop_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4])
                connection.close()
                client_socket.close()
                print(traceback.format_exc())
                break