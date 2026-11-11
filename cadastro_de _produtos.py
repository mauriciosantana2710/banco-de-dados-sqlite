import pyodbc
#importação de módulos para construção da tela
from tkinter import *
from tkinter import ttk

#----------------------------------------------------------------------------#
# PALETA DE CORES DA APLICAÇÃO
#----------------------------------------------------------------------------#
# Login: amarelo claro
COR_LOGIN_FUNDO = "#FFF1B8"
COR_LOGIN_SAIR = "#F2D675"
COR_LOGIN_SAIR_HOVER = "#E8C95A"

# Demais telas: creme suave, que combina com o amarelo do login
COR_FUNDO = "#FAF5E4"
COR_PAINEL = "#FFFFFF"
COR_TEXTO = "#2B2B20"

# Tabela
COR_CABECALHO = "#E9DDA8"
COR_LINHA_PAR = "#FFFFFF"
COR_LINHA_IMPAR = "#F6EFD2"
COR_SELECAO = "#2F6B3C"

# Botões (verde = ação principal, vermelho = perigo, bege = neutro)
COR_VERDE = "#2F6B3C"
COR_VERDE_HOVER = "#245530"
COR_VERMELHO = "#B3382C"
COR_VERMELHO_HOVER = "#942D23"
COR_NEUTRO = "#E6DFC4"
COR_NEUTRO_HOVER = "#D8CFA9"

ESTILOS_BOTAO = {
    "principal": (COR_VERDE, COR_VERDE_HOVER, "#FFFFFF"),
    "perigo": (COR_VERMELHO, COR_VERMELHO_HOVER, "#FFFFFF"),
    "neutro": (COR_NEUTRO, COR_NEUTRO_HOVER, COR_TEXTO),
}

def criar_botao(master, texto, comando, tipo="principal", largura=12):
    #botão padronizado: mesmo tamanho de fonte, cor por tipo e efeito ao passar o mouse
    cor, cor_hover, cor_texto = ESTILOS_BOTAO[tipo]
    botao = Button(master, text=texto, command=comando, font="Cambria 12 bold",
                   bg=cor, fg=cor_texto, activebackground=cor_hover, activeforeground=cor_texto,
                   relief="flat", bd=0, cursor="hand2", width=largura, pady=6)
    botao.bind("<Enter>", lambda e: botao.config(bg=cor_hover))
    botao.bind("<Leave>", lambda e: botao.config(bg=cor))
    return botao

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

        #limpar da treeview
        def limpa_dados():
            for i in treeview.get_children():
                treeview.delete(i)

        def lista_dados():
            #limpar valores
            limpa_dados()

            #executa valores retornados pelo comando SQL na variável
            cursor.execute("SELECT * From Produtos")
            #armazenar pelo comando sql em valores(variável)

            valores = cursor.fetchall()
            #exibição extraída do bd
            for posicao, linha in enumerate(valores):
                #linhas alternadas facilitam a leitura
                treeview.insert("", "end", values=(linha[0], linha[1], linha[2], linha[3]),
                                tags=("par" if posicao % 2 == 0 else "impar",))


        #janela nova para programa principal
        janela = Tk()
        janela.title("Cadastro de Produtos")
        janela.configure(bg=COR_FUNDO)
        #janela.attributes("-fullscreen", True)

        #a tabela (coluna 0) ocupa todo o espaço extra da janela
        janela.grid_columnconfigure(0, weight=1)
        janela.grid_rowconfigure(1, weight=1)

        #barra de pesquisa (linha 0)
        frame_filtros = Frame(janela, bg=COR_FUNDO)
        frame_filtros.grid(row=0, column=0, sticky="EW", padx=15, pady=(15, 5))
        frame_filtros.grid_columnconfigure(1, weight=1)

        Label(frame_filtros, text="Pesquisar por nome", font="Cambria 12", bg=COR_FUNDO, fg=COR_TEXTO).grid(row=0, column=0, padx=(0, 8))
        pesquisa_nome = Entry(frame_filtros, font="Cambria 12", relief="solid", bd=1)
        pesquisa_nome.grid(row=0, column=1, sticky="EW", ipady=3)

        def cadastrar():
            #nova janela em segundo plano
            janela_cadastrar = Toplevel(janela)
            janela_cadastrar.title("Cadastrar Produto")

            largura, altura = 460, 270
            pos_x = (janela_cadastrar.winfo_screenwidth() - largura) // 2
            pos_y = (janela_cadastrar.winfo_screenheight() - altura) // 2
            janela_cadastrar.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")
            janela_cadastrar.config(bg=COR_FUNDO)
            janela_cadastrar.resizable(False, False)

            #campos: coluna 0 = rótulo (largura fixa), coluna 1 = campo (ocupa o restante)
            janela_cadastrar.grid_columnconfigure(1, weight=1)

            #nome do produto
            Label(janela_cadastrar, text="Nome do Produto", font="Cambria 12", bg=COR_FUNDO, fg=COR_TEXTO, anchor="w", width=15).grid(row=0, column=0, padx=(20, 5), pady=(20, 8), sticky="W")
            nome_produto_cadastrar = Entry(janela_cadastrar, font="Cambria 12", relief="solid", bd=1)
            nome_produto_cadastrar.grid(row=0, column=1, padx=(5, 20), pady=(20, 8), sticky="EW", ipady=3)
            #descrição do produto
            Label(janela_cadastrar, text="Descrição", font="Cambria 12", bg=COR_FUNDO, fg=COR_TEXTO, anchor="w", width=15).grid(row=1, column=0, padx=(20, 5), pady=8, sticky="W")
            descricao_produto_cadastrar = Entry(janela_cadastrar, font="Cambria 12", relief="solid", bd=1)
            descricao_produto_cadastrar.grid(row=1, column=1, padx=(5, 20), pady=8, sticky="EW", ipady=3)
            #preço do produto
            Label(janela_cadastrar, text="Preço", font="Cambria 12", bg=COR_FUNDO, fg=COR_TEXTO, anchor="w", width=15).grid(row=2, column=0, padx=(20, 5), pady=8, sticky="W")
            preco_produto_cadastrar = Entry(janela_cadastrar, font="Cambria 12", relief="solid", bd=1)
            preco_produto_cadastrar.grid(row=2, column=1, padx=(5, 20), pady=8, sticky="EW", ipady=3)

            def salvar_dados():

                #tupla valores
                novo_produto_cadastrar = (nome_produto_cadastrar.get(), descricao_produto_cadastrar.get(), preco_produto_cadastrar.get())
                #inserção dos valores
                cursor.execute("INSERT INTO Produtos (Nome, Descricao, Preco) VALUES (?, ?, ?)", novo_produto_cadastrar)
                #salvar
                conexao.commit()
                #listagem e atualização na treeview
                filtrar_dados()
                #fechar
                janela_cadastrar.destroy()

            #botões lado a lado, alinhados à direita
            frame_botoes_cadastrar = Frame(janela_cadastrar, bg=COR_FUNDO)
            frame_botoes_cadastrar.grid(row=3, column=0, columnspan=2, sticky="E", padx=20, pady=(15, 20))

            criar_botao(frame_botoes_cadastrar, "Salvar", salvar_dados, "principal").grid(row=0, column=0, padx=(0, 10))
            criar_botao(frame_botoes_cadastrar, "Cancelar", janela_cadastrar.destroy, "neutro").grid(row=0, column=1)

        #-------------------------------------------------------------------------#
        #Estilo Treeview (o tema precisa ser definido antes de configurar os estilos)
        style = ttk.Style(janela)
        style.theme_use("default")
        style.configure("mystyle.Treeview", font="Cambria 12", rowheight=30,
                        background=COR_LINHA_PAR, fieldbackground=COR_LINHA_PAR,
                        foreground=COR_TEXTO, borderwidth=0)
        style.configure("mystyle.Treeview.Heading", font="Cambria 12 bold",
                        background=COR_CABECALHO, foreground=COR_TEXTO, relief="flat", padding=6)
        style.map("mystyle.Treeview",
                  background=[("selected", COR_SELECAO)],
                  foreground=[("selected", "#FFFFFF")])
        style.map("mystyle.Treeview.Heading", background=[("active", "#DCCF8E")])

        #tabela + barra de rolagem (linha 1)
        frame_tabela = Frame(janela, bg=COR_FUNDO)
        frame_tabela.grid(row=1, column=0, sticky="NSEW", padx=15, pady=5)
        frame_tabela.grid_columnconfigure(0, weight=1)
        frame_tabela.grid_rowconfigure(0, weight=1)

        treeview = ttk.Treeview(frame_tabela, style="mystyle.Treeview", show="headings")
        barra_rolagem = ttk.Scrollbar(frame_tabela, orient="vertical", command=treeview.yview)
        treeview.configure(yscrollcommand=barra_rolagem.set)
        barra_rolagem.grid(row=0, column=1, sticky="NS")
        #cores das linhas alternadas
        treeview.tag_configure("par", background=COR_LINHA_PAR)
        treeview.tag_configure("impar", background=COR_LINHA_IMPAR)

        #colunas treeview

        colunas = ["ID", "Nome", "Descrição", "Preço"]
        treeview["columns"] = colunas

        #listar valores do bd na treeview
        lista_dados()

        #Heading/cabeçalho

        for col in colunas:
            treeview.heading(col, text= col)

        #larguras proporcionais ao conteúdo: ID estreito, descrição larga, preço alinhado à direita
        treeview.column("ID", width=60, minwidth=50, stretch=False, anchor="center")
        treeview.column("Nome", width=220, minwidth=120, anchor="w")
        treeview.column("Descrição", width=360, minwidth=150, anchor="w")
        treeview.column("Preço", width=110, minwidth=80, stretch=False, anchor="e")

        #treeview na tela
        treeview.grid(row=0, column=0, sticky="NSEW")

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

            largura, altura = 460, 270
            pos_x = (janela_edicao.winfo_screenwidth() - largura) // 2
            pos_y = (janela_edicao.winfo_screenheight() - altura) // 2
            janela_edicao.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")
            janela_edicao.config(bg=COR_FUNDO)
            janela_edicao.resizable(False, False)

            #mesma estrutura da janela de cadastro: rótulo fixo + campo expansível
            janela_edicao.grid_columnconfigure(1, weight=1)

            #nome do produto
            Label(janela_edicao, text="Nome do Produto", font="Cambria 12", bg=COR_FUNDO, fg=COR_TEXTO, anchor="w", width=15).grid(row=0, column=0, padx=(20, 5), pady=(20, 8), sticky="W")
            nome_produto_edicao = Entry(janela_edicao, font="Cambria 12", relief="solid", bd=1)
            nome_produto_edicao.grid(row=0, column=1, padx=(5, 20), pady=(20, 8), sticky="EW", ipady=3)
            #descrição do produto
            Label(janela_edicao, text="Descrição", font="Cambria 12", bg=COR_FUNDO, fg=COR_TEXTO, anchor="w", width=15).grid(row=1, column=0, padx=(20, 5), pady=8, sticky="W")
            descricao_produto_edicao = Entry(janela_edicao, font="Cambria 12", relief="solid", bd=1)
            descricao_produto_edicao.grid(row=1, column=1, padx=(5, 20), pady=8, sticky="EW", ipady=3)
            #preço do produto
            Label(janela_edicao, text="Preço", font="Cambria 12", bg=COR_FUNDO, fg=COR_TEXTO, anchor="w", width=15).grid(row=2, column=0, padx=(20, 5), pady=8, sticky="W")
            preco_produto_edicao = Entry(janela_edicao, font="Cambria 12", relief="solid", bd=1)
            preco_produto_edicao.grid(row=2, column=1, padx=(5, 20), pady=8, sticky="EW", ipady=3)

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
                filtrar_dados()
                #fechar
                janela_edicao.destroy()

            def deletar_registro():
                #id do registro
                selected_item = treeview.selection()[0]

                id_selecionado = treeview.item(selected_item)['values'][0]
                #comando para deletar
                cursor.execute("DELETE FROM Produtos WHERE ID = ?", (id_selecionado,))

                conexao.commit()

                janela_edicao.destroy()
                #atualiza
                filtrar_dados()
            #três botões na mesma linha: Deletar à esquerda (isolado por ser destrutivo), Cancelar e Editar à direita
            frame_botoes_edicao = Frame(janela_edicao, bg=COR_FUNDO)
            frame_botoes_edicao.grid(row=3, column=0, columnspan=2, sticky="EW", padx=20, pady=(15, 20))
            frame_botoes_edicao.grid_columnconfigure(1, weight=1)

            criar_botao(frame_botoes_edicao, "Deletar", deletar_registro, "perigo", largura=10).grid(row=0, column=0, sticky="W")
            criar_botao(frame_botoes_edicao, "Cancelar", janela_edicao.destroy, "neutro", largura=10).grid(row=0, column=2, padx=(0, 10))
            criar_botao(frame_botoes_edicao, "Editar", salvar_edicao, "principal", largura=10).grid(row=0, column=3)

        #duplo clique para editar
        treeview.bind("<Double-1>", editar_dados)


        def filtrar_dados(event=None):
            #texto digitado na caixa de pesquisa (sem espaços nas pontas)
            texto = pesquisa_nome.get().strip()

            #caixa vazia: mostra todos os produtos
            if texto == "":
                lista_dados()
                return

            #busca pelo nome, em qualquer parte do texto, sem diferenciar maiúsculas/minúsculas
            cursor.execute("SELECT * FROM Produtos WHERE Nome LIKE ?", ('%' + texto + '%',))
            produtos = cursor.fetchall()

            limpa_dados()

            for posicao, dado in enumerate(produtos):
                treeview.insert("", "end", values=(dado[0], dado[1], dado[2], dado[3]),
                                tags=("par" if posicao % 2 == 0 else "impar",))

        #pesquisa letra a letra
        pesquisa_nome.bind('<KeyRelease>', filtrar_dados)

        def deletar():

            #id do registro
            selected_item = treeview.selection()[0]
            id_selecionado = treeview.item(selected_item)['values'][0]
            #comando para deletar
            cursor.execute("DELETE FROM Produtos WHERE ID = ?", (id_selecionado,))
            conexao.commit()
            #atualiza
            filtrar_dados()


        #barra de botões (linha 2), alinhada à direita abaixo da tabela
        frame_botoes = Frame(janela, bg=COR_FUNDO)
        frame_botoes.grid(row=2, column=0, sticky="E", padx=15, pady=(5, 15))

        criar_botao(frame_botoes, "Novo", cadastrar, "principal", largura=12).grid(row=0, column=0, padx=(0, 10))
        criar_botao(frame_botoes, "Deletar", deletar, "perigo", largura=12).grid(row=0, column=1)


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
janela_principal.config(bg=COR_LOGIN_FUNDO)

#tamanho da janela e posição no centro da tela
largura, altura = 400, 380
pos_x = (janela_principal.winfo_screenwidth() - largura) // 2
pos_y = (janela_principal.winfo_screenheight() - altura) // 2
janela_principal.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

titulo_lbl = Label(janela_principal, text="Tela de Login",
                   font="Cambria 25",
                   fg="#0c2513",
                   bg=COR_LOGIN_FUNDO)

janela_principal.columnconfigure(0, weight=1)
janela_principal.columnconfigure(1, weight=1)
#linhas 0 e 9 vazias com weight=1 empurram o conteúdo para o centro vertical
janela_principal.rowconfigure(0, weight=1)
janela_principal.rowconfigure(10, weight=1)
titulo_lbl.grid(row=1, column=0, columnspan=2, pady=20)
#campos de entrada de dados

senha_lbl = Label(janela_principal, text="Senha", font="Cambria 12", fg="Black", bg=COR_LOGIN_FUNDO)
nome_usuario_lbl = Label(janela_principal, text="Usuário", font="Cambria 12", fg="Black", bg=COR_LOGIN_FUNDO)
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
                     bg=COR_LOGIN_FUNDO,
                     activebackground=COR_LOGIN_FUNDO,
                     relief="flat",
                     cursor="hand2",
                     command=alternar_senha)
mostrar_btn.grid(row=6, column=0, columnspan=2)

#mensagem de erro de login (criada vazia, o texto é preenchido em verifica_credencial)
message_lbl = Label(janela_principal, text="",
                    font="Cambria 11",
                    fg="#8B1A1A",
                    bg=COR_LOGIN_FUNDO)
message_lbl.grid(row=7, column=0, columnspan=2, pady=(5, 0))
#Confirma e acessa
entrar_btn = Button(janela_principal, text="Entrar",
                    font="Cambria 12 bold",
                    fg=COR_LOGIN_FUNDO,
                    bg="#0c2513",
                    activeforeground=COR_LOGIN_FUNDO,
                    activebackground="#1d4a2a",
                    width=15,
                    cursor="hand2",
                    command=verifica_credencial)
entrar_btn.grid(row=8, column=0, columnspan=2, pady=(10, 0))

#pressionar Enter nos campos de usuário/senha executa o login
senha_entry.bind("<Return>", lambda evento: verifica_credencial())
nome_usuario_entry.bind("<Return>", lambda evento: verifica_credencial())
#sai do programa
sair_btn = Button(janela_principal, text="Sair",
                  font="Cambria 12 bold",
                  fg="#0c2513",
                  bg=COR_LOGIN_SAIR,
                  activeforeground="#0c2513",
                  activebackground=COR_LOGIN_SAIR_HOVER,
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
