#
# Authors:
# Lucas Bernacer Soriano,
# Javier Vela
#
# Copyright (c) 2021, Capgemini Engineering
#

import tkinter as tk
from tkinter import filedialog
from functools import partial
from GRIETA_Lengths import GRIETA_Critical_Lengths

import os


class run_GUI():

    def __init__(self, master):
        # INICIALIZAR TKINTER: PARA PONER EN LA INTERFAZ GRÁFICA LOS DIFERENTES BOTONES/CUADROS DE TEXTO

        # Comandos para inicializarla
        self.master = master
        self.master.title("GRIETA v1.0")
        self.master.resizable(False, False)
        self.master.update()

        # Botones selección caso
        self.case= tk.IntVar()
        self.case_create = tk.Radiobutton(self.master, text='Compute Critical Crack Lengths', variable=self.case, value=1)
        self.case_create.grid(row = 0, column = 0, padx = 10, pady = (10,0), sticky=tk.W)

        # Boton de ayuda
        # Comentado porque en este caso la ayuda está en el archivo Excel
        # self.help = tk.Button(self.master, text="HELP", command=self.open_help)
        # self.help.grid(row=1, column=1, padx=10, pady = 10)

        # Bloques de entrada
        self.label_dic, self.button_dic, self.entry_dic  = {}, {}, {}
        self.count = 0
        self.create_block('input_file','file', 'Input file:', 2, 0)
        self.create_block('data_folder', 'folder', 'Data folder:', 3, 0)
        self.create_block('output_folder','folder', 'Output folder:', 4, 0)
        self.create_block('output_name','entry', 'Output txt filename:', 5, 0)

        # Botón de generar
        self.generate_button = tk.Button(self.master, text='Generate', command=self.generate)
        self.generate_button.grid(row=6, column=0, columnspan = 2, sticky = tk.W+tk.E, padx = (10,0), pady = (10,10))

        # Texto de salida y barra
        self.scrollbar = tk.Scrollbar(orient="vertical")
        self.output_print = tk.Text(self.master, yscrollcommand=self.scrollbar.set,  height=3, width = 10)
        self.output_print.configure(state='disabled')
        self.output_print.grid(row=7, column=0, columnspan=2, sticky=tk.W + tk.E, padx = 10, pady = (10,20))
        self.scrollbar.config(command=self.output_print.yview)
        self.scrollbar.grid(row=7, column=2, sticky=tk.N + tk.S + tk.W, padx = 10)

        self.label_version = tk.Label(self.master, text="© Capgemini Engineering")
        self.label_version.grid(row=8, column=0)

    def askfilename(self, entry):
        # FUNCION PARA QUE PREGUNTE POR UN ARCHIVO
        file_name = filedialog.askopenfilename()
        self.entry_dic[entry].configure(state=tk.NORMAL)
        self.entry_dic[entry].delete(0, "end")
        self.entry_dic[entry].insert(0, file_name)
        self.entry_dic[entry].configure(state=tk.DISABLED)

    def askdirectory(self, entry):
        # FUNCION PARA QUE PREGUNTE POR UNA CARPETA
        dir_path = filedialog.askdirectory()
        self.entry_dic[entry].configure(state=tk.NORMAL)
        self.entry_dic[entry].delete(0, "end")
        self.entry_dic[entry].insert(0, dir_path)
        self.entry_dic[entry].configure(state=tk.DISABLED)

    def create_block(self, id, type, label_text, row, column):
        # FUNCIÓN PARA CREAR LOS DIFERENTES BLOQUES DE ENTRADA
        label = tk.Label(self.master, text= label_text)
        label.grid(row=row, column=column, sticky=tk.W, padx = 10)
        self.label_dic.update({id:label})
        if type == 'file':
            button = tk.Button(self.master, text="...", command=partial(self.askfilename, entry=id))
            button.grid(row=row, column=column + 2, sticky=tk.W, padx = 10)
            self.button_dic.update({id:button})
        elif type == 'folder':
            button = tk.Button(self.master, text="...", command=partial(self.askdirectory, entry=id))
            button.grid(row=row, column=column + 2, sticky=tk.W, padx = 10)
            self.button_dic.update({id:button})
        if type == 'entry':
            entry = tk.Entry(self.master)
        else:
            entry = tk.Entry(self.master, state="disabled")
        entry.grid(row=row, column=column+1, sticky=tk.W)
        self.entry_dic.update({id:entry})
        self.count = self.count +1

    def generate(self):
        # FUNCIÓN PARA QUE SE CORRA EL EJECUTABLE

        # Forma de comprobar diferentes errores si está vacío
        self.warning_print = ""
        self.output_print.configure(state='normal')
        self.output_print.delete(1.0, tk.END)
        for i in self.entry_dic.keys():
            warning = self.check_empty(self.entry_dic[i], i)
            if warning:
                self.warning_print = self.warning_print + warning + "\n"
        # Si hay algún error se escribe en la caja
        self.write_in_txt(self.warning_print, self.output_print)

        # Obtener los diferentes datos de archivo/carpetas de los espacios dejados
        file_name = self.entry_dic['input_file'].get()
        dir_path = self.entry_dic['output_folder'].get()
        output_name = self.entry_dic['output_name'].get()
        data_folder = self.entry_dic['data_folder'].get()

        if self.warning_print == "":
            if self.case.get() == 1:
                try:
                    # Inicialización de la clase GRIETA
                    GRIETA = GRIETA_Critical_Lengths(Excel_file=file_name, folder_data= data_folder)
                    # Se leen los diferentes archivos
                    DATA = GRIETA.Read_files()
                    # Se extraen las longitudes críticas y se escriben resultados en Excel y txt
                    GRIETA.Compute_Critical_Crack_Lengths(df_all = DATA, output_folder = dir_path, txt_name = output_name)
                    # Se escribe en el cuadro del exe que ya se ha realizado el análisis
                    self.write_in_txt("The files have been read and the txt has been filled", self.output_print)
                except:
                    # Hay algún error de que falta un documento o no se ha seleccionado la opción
                    self.write_in_txt("Error: Mistake in the input information.", self.output_print)

            else:
                # Error porque no se ha seleccionado la opción
                self.write_in_txt("Error: Select one of the program options.", self.output_print)

        self.warning_print = ""

    def open_help(self):
        # FUNCIÓN PARA ABRIR EL DOCUMENTO DE AYUDA
        try:
            os.system("GRIETA_Help.pdf")
        except:
            self.write_in_txt("Error: Couldn't open the README file.", self.output_print)

    def write_in_txt(self, txt, object):
        # FUNCIÓN PARA ESCRIBIR EN LA CAJA DE TEXTO DEL EJECUTABLE
        object.configure(state='normal')
        object.delete(1.0, tk.END)
        object.insert(tk.END, txt)
        object.configure(state='disabled')

    def check_empty(self, input, field):
        # FUNCIÓN QUE COMPRUEBA SI ALGÚN CAMPO ESTÁ VACÍO
        warning = ""
        if not input.get():
            warning = "Error: %s has not been selected." % (field.replace("_"," "))
        return warning

if __name__ == '__main__':
    # CORRER LA CLASE DEL GUI
    root = tk.Tk()
    app = run_GUI(root)
    root.mainloop()