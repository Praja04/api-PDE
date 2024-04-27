import tkinter
import tkinter.messagebox
import requests
import socketio

class SampleWindow(tkinter.Frame):

    TIMEOUT_DEFAULT = 1

    sio = socketio.Client()

    @sio.on('buttonStateChange')
    def on_button_state_change(self, button_state):  # Tambahkan self di sini
        print('Button state changed:', button_state)
        if button_state == 'pressed':
            self.click_button_3()  # Ubah click_button_3() menjadi self.click_button_3()

    def __init__(self, window):
        super().__init__(window)
        window.title("Sample")
        window.geometry("497x309")
        self.__TextBox1 = None
        self.__TextBox2 = None
        self.__TextBox3 = None
        self.__TextBox4 = None
        self.__TextBox5 = None
        self.__Communication = None
        self.__CreateWidgets()
        
        # Memeriksa status tombol dari server
        response = requests.get('http://34.101.184.127:3000/api/button')

        if response.status_code == 200:
            button_state = response.json().get('buttonState')
            if button_state == 'pressed':
                self.click_button_3()

        # Mengatur polling untuk memeriksa status tombol setiap 1 detik
        self.after(1000, self.poll_button_state)

    def __CreateWidgets(self):
        # Kode pembuatan widget di sini
        self.__Label1 = tkinter.Label(text="IP address")
        self.__Label1.place(anchor=tkinter.NE, x=84, y=18)
        self.__TextBox1 = tkinter.Entry()
        self.__TextBox1.place(x=87, y=18, width=102, height=19)
        self.__Label2 = tkinter.Label(text="Port")
        self.__Label2.place(anchor=tkinter.NE, x=241, y=18)
        self.__TextBox2 = tkinter.Entry(justify=tkinter.RIGHT)
        self.__TextBox2.place(x=244, y=18, width=51, height=19)
        self.__Label4 = tkinter.Label(text="Commands")
        self.__Label4.place(anchor=tkinter.NE, x=84, y=58)
        self.__TextBox3 = tkinter.Entry()
        self.__TextBox3.place(x=87, y=58, width=229, height=19)
        self.__Label5 = tkinter.Label(text="Timeout")
        self.__Label5.place(anchor=tkinter.NE, x=84, y=83)
        self.__TextBox4 = tkinter.Entry(justify=tkinter.RIGHT)
        self.__TextBox4.place(x=87, y=83, width=51, height=19)
        self.__Label6 = tkinter.Label(text="sec")
        self.__Label6.place(x=141, y=83)
        self.__TextBox5 = tkinter.Text(wrap=tkinter.NONE)
        self.__TextBox5.place(x=11, y=119, width=298, height=168)
        self.__Scrollbar1 = tkinter.Scrollbar(orient=tkinter.VERTICAL, command=self.__TextBox5.yview)
        self.__Scrollbar1.place(x=310, y=119, width=16, height=160)
        self.__TextBox5["yscrollcommand"] = self.__Scrollbar1.set
        self.__Scrollbar2 = tkinter.Scrollbar(orient=tkinter.HORIZONTAL, command=self.__TextBox5.xview)
        self.__Scrollbar2.place(x=11, y=280, width=298, height=16)
        self.__TextBox5["xscrollcommand"] = self.__Scrollbar2.set
        self.__Button1 = tkinter.Button(text="Connect", command=self.__Button1_Click)
        self.__Button1.place(x=331, y=12, width=73, height=30)
        self.__Button2 = tkinter.Button(text="Disconnect", command=self.__Button2_Click)
        self.__Button2.place(x=410, y=12, width=73, height=30)
        self.__Button3 = tkinter.Button(text="Transmit and Receive", command=self.__Button3_Click)
        self.__Button3.place(x=331, y=52, width=152, height=50)

    def __Button1_Click(self):
        # Kode untuk tombol Connect
        ip = self.__TextBox1.get()
        port = int(self.__TextBox2.get())
        self.__Communication = Lan(self.TIMEOUT_DEFAULT)
        if self.__Communication.open(ip, port):
            self.__Button1.configure(state=tkinter.DISABLED)
            self.__Button2.configure(state=tkinter.NORMAL)
            self.__Button3.configure(state=tkinter.NORMAL)
            self.__TextBox1.configure(state=tkinter.DISABLED)
            self.__TextBox2.configure(state=tkinter.DISABLED)
            self.__TextBox3.configure(state=tkinter.NORMAL)
            self.__TextBox4.configure(state=tkinter.NORMAL)

    def __Button2_Click(self):
        # Kode untuk tombol Disconnect
        if self.__Communication:
            self.__Communication.close()
            self.__Button1.configure(state=tkinter.NORMAL)
            self.__Button2.configure(state=tkinter.DISABLED)
            self.__Button3.configure(state=tkinter.DISABLED)
            self.__TextBox1.configure(state=tkinter.NORMAL)
            self.__TextBox2.configure(state=tkinter.NORMAL)
            self.__TextBox3.configure(state=tkinter.DISABLED)
            self.__TextBox4.configure(state=tkinter.DISABLED)

    def __Button3_Click(self):
        self.__Button3.configure(state=tkinter.DISABLED)
        command = self.__TextBox3.get()
        timeout = int(self.__TextBox4.get())
        self.__TextBox5.configure(state=tkinter.NORMAL)
        self.__TextBox5.insert(tkinter.END, "<< " + command + "\n")
        self.__TextBox5.see(tkinter.END)
        self.__TextBox5.configure(state=tkinter.DISABLED)
        if "?" in command:
            msgBuf = self.__Communication.SendQueryMsg(command, timeout)
            self.__TextBox5.configure(state=tkinter.NORMAL)
            self.__TextBox5.insert(tkinter.END, ">> " + msgBuf + "\n")
            self.__TextBox5.see(tkinter.END)
            self.__TextBox5.configure(state=tkinter.DISABLED)
        else:
            self.__Communication.sendMsg(command)
        self.__Button3.configure(state=tkinter.NORMAL)
        # Kode untuk tombol Transmit and Receive

    def click_button_3(self):  # Tambahkan self di sini
        # Kode untuk mengeklik tombol 3 di aplikasi tkinter
        pass


if __name__ == "__main__":
    root = tkinter.Tk()
    window = SampleWindow(root)
    window.mainloop()

# Menghubungkan ke server Node.js
window.sio.connect('http://localhost:3000')  # Ganti sio.connect menjadi window.sio.connect
