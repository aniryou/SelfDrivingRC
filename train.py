import os
from AMSpi import AMSpi
import picamera
import time
import uuid
import sys, tty, termios


TRAIN_DATA_DIR = 'traindata'
LBL_FILE = os.path.join(TRAIN_DATA_DIR, 'labels.txt')


class _Getch:
    def __call__(self):
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(3)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch


if __name__ == '__main__':
	getch = _Getch()
	with AMSpi() as amspi, picamera.PiCamera() as camera, open(LBL_FILE, 'a') as lblfile:
		amspi.set_74HC595_pins(21, 20, 16)
		amspi.set_L293D_pins(5, 6, 13, 19)

		camera.resolution = (320, 240)

		while True:
			img_filename = '{0}.jpg'.format(uuid.uuid4().hex)
			img_filepath = os.path.join(TRAIN_DATA_DIR, img_filename)
			print('Command: ')
			cmd = getch()
			if cmd == 'XXX':
				# STOP
				amspi.stop_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4])
				time.sleep(1)
				break
			elif cmd == '\x1b[A':
				# FORWARD
				camera.capture(img_filepath)
				lblfile.write(img_filename + '\t' + 'F' + '\n')
				amspi.run_dc_motor(amspi.DC_Motor_1, clockwise=True)
				amspi.run_dc_motor(amspi.DC_Motor_2, clockwise=True)
				amspi.run_dc_motor(amspi.DC_Motor_3, clockwise=True)
				amspi.run_dc_motor(amspi.DC_Motor_4, clockwise=False)
				time.sleep(.1)
				amspi.stop_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4])
			elif cmd == '\x1b[B':
				# BACKWARD
				camera.capture(img_filepath)
				lblfile.write(img_filename + '\t' + 'B' + '\n')
				amspi.run_dc_motor(amspi.DC_Motor_1, clockwise=False)
				amspi.run_dc_motor(amspi.DC_Motor_2, clockwise=False)
				amspi.run_dc_motor(amspi.DC_Motor_3, clockwise=False)
				amspi.run_dc_motor(amspi.DC_Motor_4, clockwise=True)
				time.sleep(.1)
				amspi.stop_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4])
			elif cmd == '\x1b[D':
				# LEFT
				camera.capture(img_filepath)
				lblfile.write(img_filename + '\t' + 'L' + '\n')
				amspi.run_dc_motor(amspi.DC_Motor_1, clockwise=False)
				amspi.run_dc_motor(amspi.DC_Motor_2, clockwise=False)
				amspi.run_dc_motor(amspi.DC_Motor_3, clockwise=True)
				amspi.run_dc_motor(amspi.DC_Motor_4, clockwise=False)
				time.sleep(.1)
				amspi.stop_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4])
			elif cmd == '\x1b[C':
				# RIGHT
				lblfile.write(img_filename + '\t' + 'R' + '\n')
				camera.capture(img_filepath)
				amspi.run_dc_motor(amspi.DC_Motor_1, clockwise=True)
				amspi.run_dc_motor(amspi.DC_Motor_2, clockwise=True)
				amspi.run_dc_motor(amspi.DC_Motor_3, clockwise=False)
				amspi.run_dc_motor(amspi.DC_Motor_4, clockwise=True)
				time.sleep(.1)
				amspi.stop_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4])
				pass
			else:
				print("Invalid input")
				continue