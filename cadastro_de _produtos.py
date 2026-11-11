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

        def lista_dados():
            #limpar valores
            for i in treeview.get_children():
                treeview.delete(i)

            #executa valores retornados pelo comando SQL na variável
            cursor.execute("SELECT * From Produtos")
            #armazenar pelo comando sql em valores(variável)

            valores = cursor.fetchall()
            #exibição extraída do bd
            for linha in valores:
                treeview.insert("", "end", values=(linha[0], linha[1], linha[2], linha[3]))


        #janela nova para programa principal
        janela = Tk()
        janela.title("Cadastro de Produtos")
        janela.configure(bg="#F5F5F5")
        #janela.attributes("-fullscreen", True)

        Label(janela, text = "Nome do Produto", font = "Cambria 16", bg = "#F5F5F5").grid(row = 0, column = 2, padx = 10, pady = 10)
        nome_produto = ttk.Combobox(janela, font = "Cambria 16")
        nome_produto.grid(row = 0, column = 3, padx = 10, pady = 10, sticky= "NSEW")

        #filtro em ordem crescente

        cursor.execute("SELECT DISTINCT Nome FROM Produtos ORDER BY Nome ASC")

        valores = cursor.fetchall()
        #lista retornados
        nomes_produtos = [valor[0] for valor in valores]

        nome_produto['values'] = nomes_produtos #define a lista de valores da combobox
        #----------------------------------------------------------------------------#

        Label(janela, text = "Descrição do Produto ", font = "Cambria 16", bg = "#F5F5F5").grid(row = 0, column = 5, padx = 10, pady = 10)
        descricao_produto = ttk.Combobox(janela, font = "Cambria 16")
        descricao_produto.grid(row = 0, column = 6, padx = 10, pady = 10, sticky= "NSEW")

        #filtro em ordem crescente
        
        cursor.execute("SELECT DISTINCT Descricao FROM Produtos ORDER BY Descricao ASC")
        
        valoresDescricao = cursor.fetchall()
        #lista retornados
        descricao_produtos = [valor[0] for valor in valoresDescricao]
        
        descricao_produto['values'] = descricao_produtos #define a lista de valores da combobox

        def cadastrar():
            #nova janela em segundo plano
            janela_cadastrar = Toplevel(janela)
            janela_cadastrar.title("Cadastrar Produto")

            largura, altura = 500, 200
            pos_x = (janela_cadastrar.winfo_screenwidth() - largura) // 2
            pos_y = (janela_cadastrar.winfo_screenheight() - altura) // 2
            janela_cadastrar.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")
            janela_cadastrar.config(bg="#F5F5F5")

            #nome do produto 
#-----------------------------------------------------------------------------------------
            Label(janela_cadastrar, text="Nome do Produto", font="Cambria 14", bg="#FFFFFF").grid(row=0, column=0, padx=10, pady=10, sticky="W")
            nome_produto_cadastrar = Entry(janela_cadastrar, font="Cambria 14")
            nome_produto_cadastrar.grid(row=0, column=1, padx=10, pady=10)
#-----------------------------------------------------------------------------------------------------------------------------
            #descrição do produto
            Label(janela_cadastrar, text="Descrição", font="Cambria 14", bg="#FFFFFF").grid(row=1, column=0, padx=10, pady=10, sticky="W")
            descricao_produto_cadastrar = Entry(janela_cadastrar, font="Cambria 14")
            descricao_produto_cadastrar.grid(row=1, column=1, padx=10, pady=10)
#------------------------------------------------------------------------------------------------------------------------------
            #preço do produto
            Label(janela_cadastrar, text="Preço", font="Cambria 14", bg="#FFFFFF").grid(row=2, column=0, padx=10, pady=10, sticky="W")
            preco_produto_cadastrar = Entry(janela_cadastrar, font="Cambria 14")
            preco_produto_cadastrar.grid(row=2, column=1, padx=10, pady=10)

            def salvar_dados():

                #tupla valores
                novo_produto_cadastrar = (nome_produto_cadastrar.get(), descricao_produto_cadastrar.get(), preco_produto_cadastrar.get());
                #inserção dos valores
                cursor.execute("INSERT INTO Produtos (Nome, Descricao, Preco) VALUES (?, ?, ?)", novo_produto_cadastrar)
                #salvar
                conexao.commit()
                #listagem e atualização na treeview
                lista_dados()
                #fechar
                janela_cadastrar.destroy()

            botao_salvar_dados = Button(janela_cadastrar, text="Salvar", command= salvar_dados, font="Cambria 20")
            botao_salvar_dados.grid(row=4, column=0, columnspan=2, sticky="NSEW", pady=5, padx=5)

            botao_cancelar = Button(janela_cadastrar, text="Cancelar", command= janela_cadastrar.destroy, font="Cambria 20")
            botao_cancelar.grid(row=5, column=0, columnspan=2, sticky="NSEW", pady=5, padx=5)

            for i in range(5):
                janela_cadastrar.grid_rowconfigure(i, weight=1)

            for i in range(2):
                janela_cadastrar.grid_columnconfigure(i, weight=1)








        botao_gravar = Button(janela, text="Novo", command= cadastrar, font="Cambria 26")
        botao_gravar.grid(row=5, column=0, columnspan=4, sticky="NSEW", pady=5)
        #-------------------------------------------------------------------------#
        #Estilo Treeview
        style = ttk.Style(janela)
        treeview = ttk.Treeview(janela, style="mystyle.Treeview")
        style.theme_use("default")
        style.configure("mystyle.Treeview", font="Cambria 12")

        #colunas treeview

        colunas = ["ID", "Nome", "Descrição", "Preço"]
        treeview["columns"] = colunas

        #listar valores do bd na treeview
        lista_dados()

        #Heading/cabeçalho

        for col in colunas:
            treeview.heading(col, text= col)


        #treeview na tela
        treeview.grid(row=4, column=0, columnspan=10, padx=5, pady=5, sticky="NSEW")
        #largura 0
        treeview.column("#0", width=0, stretch=False)

        #limpar da treeview
        def limpa_dados():

            for i in treeview.get_children():

                treeview.delete(i)

        #--------------------------------------------------------------------------#
        #Edição
        def editar_dados(event=None):

            #obtem o item selecionado; sai se nada estiver selecionado
            selecao = treeview.selection()
            if not selecao:
                return
            item_selecionado = selecao[0]
            #obtem os valores da linha selecionada
            valores_selecionados = treeview.item(item_selecionado)['values']
            #nova janela em segundo plano
            janela_edicao = Toplevel(janela)
            janela_edicao.title("Editar Produto")

            largura, altura = 500, 200
            pos_x = (janela_edicao.winfo_screenwidth() - largura) // 2
            pos_y = (janela_edicao.winfo_screenheight() - altura) // 2
            janela_edicao.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")
            janela_edicao.config(bg="#F5F5F5")

            #nome do produto
            Label(janela_edicao, text="Nome do Produto", font="Cambria 14", bg="#FFFFFF").grid(row=0, column=0, padx=10, pady=10, sticky="W")
            nome_produto_edicao = Entry(janela_edicao, font="Cambria 14")
            nome_produto_edicao.grid(row=0, column=1, padx=10, pady=10)
            #descrição do produto
            Label(janela_edicao, text="Descrição", font="Cambria 14", bg="#FFFFFF").grid(row=1, column=0, padx=10, pady=10, sticky="W")
            descricao_produto_edicao = Entry(janela_edicao, font="Cambria 14")
            descricao_produto_edicao.grid(row=1, column=1, padx=10, pady=10)
            #preço do produto
            Label(janela_edicao, text="Preço", font="Cambria 14", bg="#FFFFFF").grid(row=2, column=0, padx=10, pady=10, sticky="W")
            preco_produto_edicao = Entry(janela_edicao, font="Cambria 14")
            preco_produto_edicao.grid(row=2, column=1, padx=10, pady=10)

            #preenche os campos com os dados atuais (colunas: ID, Nome, Descrição, Preço)
            nome_produto_edicao.insert(0, valores_selecionados[1])
            descricao_produto_edicao.insert(0, valores_selecionados[2])
            preco_produto_edicao.insert(0, valores_selecionados[3])

            def salvar_edicao():

                novo_nome = nome_produto_edicao.get()
                nova_descricao = descricao_produto_edicao.get()
                novo_preco = preco_produto_edicao.get()

                #alteração dos dados
                cursor.execute("UPDATE Produtos SET Nome = ?, Descricao = ?, Preco = ? WHERE ID = ?",
                               (novo_nome, nova_descricao, novo_preco, valores_selecionados[0]))
                #salvar
                conexao.commit()
                #listagem e atualização na treeview
                lista_dados()
                #fechar
                janela_edicao.destroy()

            botao_salvar_edicao = Button(janela_edicao, text="Editar", command=salvar_edicao, font="Cambria 16", background="#008000", foreground="#FFFFFF")
            botao_salvar_edicao.grid(row=4, column=0, sticky="NSEW", pady=5, padx=5)
            def deletar_registro():
                #id do registro
                selected_item = treeview.selection()[0]

                id_selecionado = treeview.item(selected_item)['values'][0]
                #comando para deletar
                cursor.execute("DELETE FROM Produtos WHERE ID = ?", (id_selecionado,))

                conexao.commit()

                janela_edicao.destroy()





            #deletar
            botao_deletar_registro = Button(janela_edicao, text="Deletar", command=deletar_registro, font="Cambria 16", background="#FF0000", foreground="#FFFFFF")
            botao_deletar_registro.grid(row=4, column=1, sticky="NSEW", pady=5, padx=5)

            botao_cancelar_edicao = Button(janela_edicao, text="Cancelar", command=janela_edicao.destroy, font="Cambria 20")
            botao_cancelar_edicao.grid(row=5, column=0, pady=20, padx=20)

            for i in range(6):
                janela_edicao.grid_rowconfigure(i, weight=1)

            for i in range(2):
                janela_edicao.grid_columnconfigure(i, weight=1)

        #duplo clique para editar
        treeview.bind("<Double-1>", editar_dados)


        def filtrar_dados(nome_produto, descricao_produto):
            #verifica se combobox == vazio
            if nome_produto.get() == "" and descricao_produto.get() =="":

                lista_dados()
            #sair
                return
            #consulta dinâmica sql
            sql = "SELECT * FROM Produtos"

            parametros = []

            if nome_produto.get():
                sql += " WHERE Nome LIKE ?"

                parametros.append('%' + nome_produto.get() + '%')

            if descricao_produto.get():

                if nome_produto.get():

                    sql += " AND"

                else:

                    sql += " WHERE"

                sql+= " Descricao LIKE ?"

                parametros.append('%' + descricao_produto.get() + '%')

            cursor.execute(sql, tuple(parametros))

            produtos = cursor.fetchall()

            limpa_dados()

            for dado in produtos:

                treeview.insert("", "end", values=(dado[0],dado[1], dado[2], dado[3]))


            

        #filtro letra a letra
        nome_produto.bind('<KeyRelease>', lambda e: filtrar_dados(nome_produto, descricao_produto))

        descricao_produto.bind('<KeyRelease>', lambda e: filtrar_dados(nome_produto, descricao_produto))

        #-----------------------------------------------------------------------------------------------------
        #filtro ao selecionar o item
        nome_produto.bind('<<ComboboxSelected>>', lambda e: filtrar_dados(nome_produto, descricao_produto))

        descricao_produto.bind('<<ComboboxSelected>>', lambda e: filtrar_dados(nome_produto, descricao_produto))





        



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

for i in range(5):
    janela_principal.grid_rowconfigure(i, weight=1)

for i in range(2):
    janela_principal.grid_rowconfigure(i, weight=1)


entrar_btn.config(width=10)
sair_btn.config(width=10)



janela_principal.mainloop() #inicia a janela na tela