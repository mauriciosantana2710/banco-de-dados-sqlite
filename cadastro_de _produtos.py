import pyodbc
#importação de módulos para construção da tela
from tkinter import *
from tkinter import ttk
#valores = cursor.fetchall() #fetchall - Passa os dados do banco de dados para a variável
def verifica_credencial():


    #print(pyodbc.drivers()) #visualização dos drivers disponíveis
    conexao = pyodbc.connect("Driver={SQLite3 ODBC Driver}; Server=localhost; Database=Projeto_Compras.db")
    cursor = conexao.cursor() #Ferramenta para executar comandos no SQL
    #cursor.execute("Select * From Usuarios Where Nome = ? AND Senha = ?", (nome_usuario_entry.get(), senha_entry.get()))
#login
janela_principal = Tk()
janela_principal.title("Login")
janela_principal.config(bg="#F0CE37")

titulo_lbl = Label(janela_principal, text="Tela de Login",
                   font="Cambria 25",
                   fg="#0c2513",
                   bg="#F5DF7F")

janela_principal.columnconfigure(0, weight=1)
janela_principal.columnconfigure(1, weight=1)
titulo_lbl.grid(row=0, column=0, columnspan=2, padx=10, pady=20, sticky="ew") #sticky - expande para as laterais ocupando espaços em branco com nswe (norte, sul, leste, oeste)
#campos de entrada de dados
nome_usuario_entry = Entry(janela_principal, font="Cambria, 18")
nome_usuario_entry.grid(row=1, column=1, pady=10)

senha_entry = Entry(janela_principal, font="Cambria, 18")
senha_entry.grid(row=2, column=1, pady=10)




janela_principal.mainloop() #inicia a janela na tela