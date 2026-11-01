import pyodbc
print(pyodbc.drivers())
dadosConexao = ("Driver={SQLite3 ODBC Driver}; Server=localhost; Database=Projeto_Compras.db")

conexao = pyodbc.connect(dadosConexao)

print("Conectado")