import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import *
from tkinter import ttk
import tkinter.ttk as ttk
from tkinter import filedialog
import requests
import json
import config


class Comandos:
    def __init__(self, master=None):
        self.frame = tk.Tk()
        self.frame.geometry("1200x650")
        self.frame.title("Proyecto - MIA 2023")

        self.frame_buttons = tk.Frame(master=self.frame, width=1200, height=80, bg="steel blue")
        self.frame_buttons.pack(fill="y")

        self.cargar_archivo = tk.Entry(master=self.frame_buttons,font=("Century",16), width=50)
        self.cargar_archivo.place(x=20, y=20)

        self.button_cargar= tk.Button(master=self.frame_buttons, text= "Cargar", 
                                      font=("Century", 14),
                                      bg = "black",
                                      fg = "white",
                                      command=self.exec_file)
        self.button_cargar.place(x=630,y=15)

        self.button_reporte= tk.Button(master=self.frame_buttons, text= "Reporte", 
                                      font=("Century", 14),
                                      bg = "black",
                                      fg = "white")
        self.button_reporte.place(x=1100,y=15)

        self.frame_consola = tk.Frame(master=self.frame, width=600, bg="navy")
        self.frame_consola.pack(fill=tk.BOTH,side=tk.LEFT, expand=True)

        self.label_consola = tk.Label(master=self.frame_consola, text= "Consola", 
                                      font=("Century", 20),
                                      bg = "navy",
                                      fg = "white")
        self.label_consola.place(x=20,y=20)

        self.consol = tk.Text(master=self.frame_consola, width=60, font=("Consolas",13), fg="white", bg="black", insertbackground='white')
        self.consol.place(x=20,y=60)
        self.consol.bind('<Return>', self.get_command)

        self.frame_comandos = tk.Frame(master=self.frame,width=600,bg="midnight blue")
        self.frame_comandos.pack(fill=tk.BOTH,side = tk.RIGHT, expand=True)
        self.label_comandos = tk.Label(master=self.frame_comandos, text= "Comandos", 
                                      font=("Century", 20),
                                      bg = "midnight blue",
                                      fg="white")
        self.label_comandos.place(x=20,y=20)
        self.comandos = tk.Text(master=self.frame_comandos, width=60, font=("Consolas",13), fg="white", bg="black", insertbackground='white')
        self.comandos.place(x=20,y=60)

    def console_print(self, data:str):
      self.comandos.insert('end', data+'\n')

    def exec_command(self, command:str):
      data = {
        'command': command
      }
      response = requests.post(config.server_url + '/interpret/', json=data)
      message = json.loads(response.text)['message']
      self.console_print('> '+message)

    def exec_file(self):
      file_path = filedialog.askopenfilename()
      if isinstance(file_path, str):
        with open(file_path) as commands_file:
          command = commands_file.readline().strip()
          while command:
            self.console_print('$ '+command)
            self.exec_command(command)
            command = commands_file.readline().strip()

    def get_command(self, arg):
      lineStart = 'end-1c linestart'
      lineEnd = 'end-1c lineend'
      command = self.consol.get(lineStart, lineEnd).encode().decode('unicode-escape')
      self.exec_command(command)

    def run(self):
        self.frame.mainloop()

if __name__ == "__main__":
  app = Comandos()
  app.run()