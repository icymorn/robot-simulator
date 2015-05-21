import cv2

def main():
	cap = cv2.VideoCapture(0)
	num = 0
	while True:
		_, frame = cap.read()
		cv2.imshow('frame',frame)
		k = cv2.waitKey(300) & 0xff
		if k == 27:
			break
		elif k == 13:
			cv2.imwrite(str(num) + '.jpg', frame)
			print('save image to:', str(num) + '.jpg')
			num += 1
if __name__ == '__main__':
	main()