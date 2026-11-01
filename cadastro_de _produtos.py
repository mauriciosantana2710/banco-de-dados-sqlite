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

#tamanho da janela e posição no centro da tela
largura, altura = 400, 320
pos_x = (janela_principal.winfo_screenwidth() - largura) // 2
pos_y = (janela_principal.winfo_screenheight() - altura) // 2
janela_principal.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

titulo_lbl = Label(janela_principal, text="Tela de Login",
                   font="Cambria 25",
                   fg="#0c2513",
                   bg="#F0CE37")

janela_principal.columnconfigure(0, weight=1)
janela_principal.columnconfigure(1, weight=1)
#linhas 0 e 6 vazias com weight=1 empurram o conteúdo para o centro vertical
janela_principal.rowconfigure(0, weight=1)
janela_principal.rowconfigure(6, weight=1)
titulo_lbl.grid(row=1, column=0, columnspan=2, pady=20)
#campos de entrada de dados
senha_lbl = Label(janela_principal, text="Senha", font="Cambria 12", fg="Black", bg="#F0CE37")
nome_usuario_lbl = Label(janela_principal, text="Usuário", font="Cambria 12", fg="Black", bg="#F0CE37")
nome_usuario_lbl.grid(row=2, column=0, columnspan=2, pady=(10, 5))
senha_lbl.grid(row=4, column=0, columnspan=2, pady=(10, 5))

nome_usuario_entry = Entry(janela_principal, font="Cambria 14", width=20)
nome_usuario_entry.grid(row=3, column=0, columnspan=2, pady=(0, 10))


senha_entry = Entry(janela_principal, font="Cambria 14", width=20)
senha_entry.grid(row=5, column=0, columnspan=2, pady=(0, 10))




janela_principal.mainloop() #inicia a janela na tela