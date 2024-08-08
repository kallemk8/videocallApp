import cv2
import socket
import struct
import pickle

# Socket setup
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 8080))
print('Connected to server')

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break

    data = pickle.dumps(frame)
    message_size = struct.pack("Q", len(data))

    client_socket.sendall(message_size + data)

    cv2.imshow("Sending Video", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
client_socket.close()
cv2.destroyAllWindows()
