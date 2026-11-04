import pyodbc
#importação de módulos para construção da tela
from tkinter import *
from tkinter import ttk

def verifica_credencial():


    #print(pyodbc.drivers()) #visualização dos drivers disponíveis
    conexao = pyodbc.connect("Driver={SQLite3 ODBC Driver}; Server=localhost; Database=Projeto_Compras.db")
    cursor = conexao.cursor() #Ferramenta para executar comandos no SQL
    cursor.execute("Select * From Usuarios Where Usuario = ? AND Senha = ?", (nome_usuario_entry.get(), senha_entry.get()))
    #recebe query
    usuario = cursor.fetchall() #fetchall - Passa os dados do banco de dados para a variável

    if usuario:
        print("Logged in")
        janela_principal.destroy() #encerra o login
        #janela nova para programa principal
        janela = Tk()
        janela.title("Cadastro de Produtos")
        janela.configure(bg="#F5F5F5")
        janela.attributes("-fullscreen", True)

        Label(janela, text = "Nome do Produto", font = "Cambria 16", bg = "#F5F5F5").grid(row = 0, column = 2, padx = 10, pady = 10)

        nome_produto = ttk.Combobox(janela, font = "Cambria 16")
        nome_produto.grid(row = 0, column = 3, padx = 10, pady = 10, sticky= "NSEW")
        #----------------------------------------------------------------------#
        menu_barra = Menu(janela)
        janela.config(menu = menu_barra)
        menu_arquivo = Menu(menu_barra, tearoff = 0)
        menu_barra.add_cascade(label = "Arquivo", menu = menu_arquivo)
        #opção cadastrar
        menu_arquivo.add_command(label= "Cadastrar", command = janela.destroy)
        #opção sair
        menu_arquivo.add_command(label = "Sair", command = janela.destroy)
        #inicia janela
        janela.mainloop()



        #fecha conexao com o banco de dados
        cursor.close()
        conexao.close()






    else:
        message_lbl.config(text="Usuário ou senha incorretos")



#login
janela_principal = Tk()
janela_principal.title("Login")
janela_principal.config(bg="#F0CE37")

#tamanho da janela e posição no centro da tela
largura, altura = 400, 380
pos_x = (janela_principal.winfo_screenwidth() - largura) // 2
pos_y = (janela_principal.winfo_screenheight() - altura) // 2
janela_principal.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

titulo_lbl = Label(janela_principal, text="Tela de Login",
                   font="Cambria 25",
                   fg="#0c2513",
                   bg="#F0CE37")

janela_principal.columnconfigure(0, weight=1)
janela_principal.columnconfigure(1, weight=1)
#linhas 0 e 9 vazias com weight=1 empurram o conteúdo para o centro vertical
janela_principal.rowconfigure(0, weight=1)
janela_principal.rowconfigure(10, weight=1)
titulo_lbl.grid(row=1, column=0, columnspan=2, pady=20)
#campos de entrada de dados

senha_lbl = Label(janela_principal, text="Senha", font="Cambria 12", fg="Black", bg="#F0CE37")
nome_usuario_lbl = Label(janela_principal, text="Usuário", font="Cambria 12", fg="Black", bg="#F0CE37")
nome_usuario_lbl.grid(row=2, column=0, columnspan=2, pady=(10, 5))
senha_lbl.grid(row=4, column=0, columnspan=2, pady=(10, 5))

nome_usuario_entry = Entry(janela_principal, font="Cambria 14", width=20)
nome_usuario_entry.grid(row=3, column=0, columnspan=2, pady=(0, 10))


senha_entry = Entry(janela_principal, font="Cambria 14", width=20, show="•")
senha_entry.grid(row=5, column=0, columnspan=2, pady=(0, 5))

#alterna entre mostrar e esconder o texto da senha
def alternar_senha():
    if senha_entry.cget("show") == "":
        senha_entry.config(show="•")
        mostrar_btn.config(text="Mostrar senha")
    else:
        senha_entry.config(show="")
        mostrar_btn.config(text="Ocultar senha")

mostrar_btn = Button(janela_principal, text="Mostrar senha",
                     font="Cambria 10",
                     fg="#0c2513",
                     bg="#F0CE37",
                     activebackground="#F0CE37",
                     relief="flat",
                     cursor="hand2",
                     command=alternar_senha)
mostrar_btn.grid(row=6, column=0, columnspan=2)

#mensagem de erro de login (criada vazia, o texto é preenchido em verifica_credencial)
message_lbl = Label(janela_principal, text="",
                    font="Cambria 11",
                    fg="#8B1A1A",
                    bg="#F0CE37")
message_lbl.grid(row=7, column=0, columnspan=2, pady=(5, 0))
#Confirma e acessa
entrar_btn = Button(janela_principal, text="Entrar",
                    font="Cambria 12 bold",
                    fg="#F0CE37",
                    bg="#0c2513",
                    activeforeground="#F0CE37",
                    activebackground="#1d4a2a",
                    width=15,
                    cursor="hand2",
                    command=verifica_credencial)
entrar_btn.grid(row=8, column=0, columnspan=2, pady=(10, 0))
#sai do programa
sair_btn = Button(janela_principal, text="Sair",
                  font="Cambria 12 bold",
                  fg="#0c2513",
                  bg="#F5DF7F",
                  activeforeground="#0c2513",
                  activebackground="#E8D06A",
                  width=15,
                  cursor="hand2",
                  command=janela_principal.destroy)
sair_btn.grid(row=9, column=0, columnspan=2, pady=(8, 0))




janela_principal.mainloop() #inicia a janela na tela