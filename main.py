import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Função para calcular lucro
def calcular_lucro():
    try:
        receita = float(entry_receita.get())
        custo = float(entry_custo.get())
        lucro = receita - custo
        margem_lucro = (lucro / receita) * 100 if receita > 0 else 0
        
        label_lucro_valor.config(text=f"R$ {lucro:.2f}")
        label_margem_valor.config(text=f"{margem_lucro:.2f}%")
        
        historico.append((produto_var.get(), receita, custo, lucro, margem_lucro))
        atualizar_tabela()
        atualizar_grafico()
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira valores válidos.")

# Função para salvar os dados em Excel
def salvar_excel():
    df = pd.DataFrame(historico, columns=["Produto", "Receita", "Custo", "Lucro", "Margem (%)"])
    df.to_excel("lucro_calculado.xlsx", index=False)
    messagebox.showinfo("Sucesso", "Dados salvos com sucesso!")

# Atualizar a tabela de histórico
def atualizar_tabela():
    for row in tree.get_children():
        tree.delete(row)
    for item in historico:
        tree.insert("", "end", values=item)

# Atualizar gráfico
def atualizar_grafico():
    ax.clear()
    df = pd.DataFrame(historico, columns=["Produto", "Receita", "Custo", "Lucro", "Margem (%)"])
    if not df.empty:
        df.plot(kind='bar', x='Produto', y=['Receita', 'Custo', 'Lucro'], ax=ax)
    ax.set_title("Desempenho dos Produtos")
    canvas.draw()

# Configuração da interface
tk_app = tk.Tk()
tk_app.title("Calculadora de Lucro")
tk_app.geometry("800x500")

frame_top = tk.Frame(tk_app)
frame_top.pack(pady=10)

# Entradas de dados
tk.Label(frame_top, text="Produto:").grid(row=0, column=0)
produto_var = tk.StringVar()
entry_produto = ttk.Entry(frame_top, textvariable=produto_var)
entry_produto.grid(row=0, column=1)

tk.Label(frame_top, text="Receita:").grid(row=1, column=0)
entry_receita = ttk.Entry(frame_top)
entry_receita.grid(row=1, column=1)

tk.Label(frame_top, text="Custo:").grid(row=2, column=0)
entry_custo = ttk.Entry(frame_top)
entry_custo.grid(row=2, column=1)

btn_calcular = ttk.Button(frame_top, text="Calcular", command=calcular_lucro)
btn_calcular.grid(row=3, column=1, pady=5)

# Resultado
tk.Label(tk_app, text="Lucro Bruto:").pack()
label_lucro_valor = tk.Label(tk_app, text="R$ 0.00", font=("Arial", 12, "bold"))
label_lucro_valor.pack()

tk.Label(tk_app, text="Margem de Lucro:").pack()
label_margem_valor = tk.Label(tk_app, text="0.00%", font=("Arial", 12, "bold"))
label_margem_valor.pack()

# Histórico de cálculos
frame_hist = tk.Frame(tk_app)
frame_hist.pack()

columns = ("Produto", "Receita", "Custo", "Lucro", "Margem (%)")
tree = ttk.Treeview(frame_hist, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.pack()

btn_salvar = ttk.Button(tk_app, text="Salvar em Excel", command=salvar_excel)
btn_salvar.pack(pady=5)

# Gráfico
fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, master=tk_app)
canvas.get_tk_widget().pack()

historico = []

# Rodar a aplicação
tk_app.mainloop()
