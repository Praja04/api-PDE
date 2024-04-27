import socket
import time

class Lan:

    def __init__(self, timeout):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
        self.sock.settimeout(timeout)  # Timeout

    def open(self, IP, port):
        try:
            self.sock.connect((IP, port))
            return True
        except Exception as e:
            print("Open error:", e)
            return False

    def close(self):
        try:
            self.sock.close()
            return True
        except Exception as e:
            print("Close error:", e)
            return False

    def sendMsg(self, strMsg):
        try:
            strMsg = strMsg + '\r\n'
            self.sock.sendall(bytes(strMsg, 'utf-8'))
            return True
        except Exception as e:
            print("Send Error:", e)
            return False

    def receiveMsg(self, timeout):
        msgBuf = bytes()
        try:
            start = time.time()
            while True:
                rcv = self.sock.recv(4096)
                rcv = rcv.strip(b"\r")
                if b"\n" in rcv:
                    rcv = rcv.strip(b"\n")
                    msgBuf += rcv
                    msgBuf = msgBuf.decode('utf-8')
                    break
                else:
                    msgBuf += rcv
                if time.time() - start > timeout:
                    msgBuf = "Timeout Error"
                    break
        except Exception as e:
            print("Receive Error:", e)
            msgBuf = "Error"
        return msgBuf

    def SendQueryMsg(self, strMsg, timeout):
        if self.sendMsg(strMsg):
            msgBuf_str = self.receiveMsg(timeout)
        else:
            msgBuf_str = "Error"
        return msgBuf_str
