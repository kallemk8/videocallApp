import cv2
import socket
import struct
import pickle

# Socket setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8080))
server_socket.listen(5)
print('Server listening on port 8080')

conn, addr = server_socket.accept()
print(f'Connection from: {addr}')
data = b""
payload_size = struct.calcsize("Q")

while True:
    while len(data) < payload_size:
        packet = conn.recv(4*1024)  # 4K
        if not packet: break
        data += packet
    
    if len(data) < payload_size:
        break
    
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]
    
    while len(data) < msg_size:
        data += conn.recv(4*1024)
    
    frame_data = data[:msg_size]
    data = data[msg_size:]
    
    frame = pickle.loads(frame_data)
    cv2.imshow("Receiving Video", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

conn.close()
cv2.destroyAllWindows()
