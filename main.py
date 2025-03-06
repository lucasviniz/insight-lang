import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import numpy as np
import tkinter as tk
from tkinter import ttk

df = pd.read_csv("survey_results_public.csv")

def contar_linguagens(coluna):
    all_languages = ";".join(df[coluna].dropna()).split(";")
    language_counts = Counter(all_languages)
    df_languages = pd.DataFrame(language_counts.items(), columns=["Linguagem", "Quantidade"])
    return df_languages.sort_values(by="Quantidade", ascending=False)

df_used = contar_linguagens("LanguageHaveWorkedWith")
df_wanted = contar_linguagens("LanguageWantToWorkWith")

df_comparacao = pd.merge(df_used, df_wanted, on="Linguagem", how="outer", suffixes=("_Usada", "_Desejada")).fillna(0)

df_top20 = df_comparacao.nlargest(20, "Quantidade_Usada")

num_linguagens = len(df_top20)
palette = sns.color_palette("husl", num_linguagens)
color_map = {df_top20["Linguagem"].iloc[i]: palette[i] for i in range(num_linguagens)}

def mostrar_grafico_mais_usadas():
    plt.figure(figsize=(10, 5))
    sns.barplot(x=df_used["Quantidade"][:10], y=df_used["Linguagem"][:10], palette="viridis")
    plt.title("Top 10 mais usadas - Stack Overflow")
    plt.xlabel("Quantidade de dev's")
    plt.ylabel("Linguagem")
    plt.show()

def mostrar_grafico_mais_desejadas():
    plt.figure(figsize=(10, 5))
    sns.barplot(x=df_wanted["Quantidade"][:10], y=df_wanted["Linguagem"][:10], palette="magma")
    plt.title("Top 10 linguagens que os dev's querem aprender")
    plt.xlabel("Quantidade de dev's")
    plt.ylabel("Linguagem")
    plt.show()

def mostrar_grafico_comparacao():
    plt.figure(figsize=(12, 6))

    plt.plot(df_top20["Linguagem"], df_top20["Quantidade_Usada"], marker="o", linestyle="-", linewidth=2, color="blue", label="Usada")
    plt.plot(df_top20["Linguagem"], df_top20["Quantidade_Desejada"], marker="o", linestyle="-", linewidth=2, color="red", label="Desejada")

    for i, linguagem in enumerate(df_top20["Linguagem"]):
        cor = color_map[linguagem]
        plt.scatter(linguagem, df_top20["Quantidade_Usada"].iloc[i], color=cor, s=100, edgecolors="black", linewidth=1, zorder=2)
        plt.scatter(linguagem, df_top20["Quantidade_Desejada"].iloc[i], color=cor, s=100, edgecolors="black", linewidth=1, zorder=2)

    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Linguagens")
    plt.ylabel("Quantidade de desenvolvedores")
    plt.title("Top 20 linguagens: Uso vs Interesse")
    plt.legend(title="Legenda", loc="upper right")
    plt.grid(True)

    plt.show()

janela = tk.Tk()
janela.title("Análise de linguagens - Stack Overflow 2023")
janela.geometry("400x300")
janela.configure(bg="#2c3e50")

titulo = tk.Label(janela, text="Escolha um gráfico para visualizar:", font=("Arial", 14, "bold"), fg="white", bg="#2c3e50")
titulo.pack(pady=20)

estilo = {"font": ("Arial", 12, "bold"), "width": 30, "height": 2, "fg": "white", "bg": "#3498db", "bd": 0, "activebackground": "#2980b9"}

btn_usadas = tk.Button(janela, text="Linguagens mais usadas", command=mostrar_grafico_mais_usadas, **estilo)
btn_usadas.pack(pady=5)

btn_desejadas = tk.Button(janela, text="Linguagens mais desejadas", command=mostrar_grafico_mais_desejadas, **estilo)
btn_desejadas.pack(pady=5)

btn_comparacao = tk.Button(janela, text="Comparar uso vs interesse", command=mostrar_grafico_comparacao, **estilo)
btn_comparacao.pack(pady=5)

janela.mainloop()
