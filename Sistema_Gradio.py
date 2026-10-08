import gradio as gr
import pandas as pd
import os
from datetime import datetime

ARQUIVO_CSV = "pacientes.csv"
COLUNAS = ["Data do Cadastro", "Nome", "Idade", "Convênio",  "Cidade", "Estado", "Prioridade", "Motivo da Consulta"]

def cadastrar_paciente(nome, idade, convenio, cidade, estado, prioridade, motivo):
    # if os.path.exists(ARQUIVO_CSV):                 # Verifica se o arquivo já existe e se o nome já foi cadastrado
    #     df_existente = pd.read_csv(ARQUIVO_CSV)     # Normaliza removendo espaços extras e comparando em minúsculas (opcional)
    #     if (not df_existente.empty  and  (df_existente["Nome"].str.strip().str.lower() == nome.strip().lower()).any()):
    #         return (
    #             f"Erro: O paciente '{nome}' já está cadastrado!",
    #         )

    linha = {
        "Data do Cadastro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Nome": nome,
        "Idade": idade,
        "Convênio": convenio,
        "Cidade": (cidade or "").strip(),
        "Estado": (estado or "").strip(),
        "Prioridade": prioridade,
        "Motivo da Consulta": motivo,
    }

    novo = pd.DataFrame([linha])
    if os.path.exists(ARQUIVO_CSV):
        novo.to_csv(ARQUIVO_CSV, mode="a", header=False, index=False)
    else:
        novo.to_csv(ARQUIVO_CSV, mode="w", header=True, index=False)
    return (
        "Paciente cadastrado com sucesso!", 
        pd.read_csv(ARQUIVO_CSV).tail(5) 
    #     "",     #Nome
    #     None,   #Idade (ou 0)
    #     None,   #Convênio
    #     "",     #Cidade
    #     None,   #Estado
    #     1,      #Prioridade (ou o valor padrão do seu slider)
    #     "",     #Motivo
    )

with gr.Blocks() as demo:
    gr.Markdown("## Cadastro de Pacientes")
    nome = gr.Textbox(label="Nome do paciente")
    idade = gr.Number(label="Idade")
    convenio = gr.Dropdown(
        ["Particular", "Unimed", "Bradesco Saúde", "SulAmérica", "Outro"],
        label="Convênio",
    )
    cidade = gr.Textbox(label="Cidade")
    estado = gr.Dropdown(
        ["-", "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"],
        label="Estado"
    )
    prioridade = gr.Slider(1, 5, step=1, label="Prioridade do atendimento")
    motivo = gr.Textbox(label="Motivo da consulta / observações", lines=3)
    botao = gr.Button("Cadastrar")
    saida_msg = gr.Textbox(label="Status", interactive=False)
    tabela = gr.Dataframe(label="Últimos 5 pacientes cadastrados")
    botao.click(
        cadastrar_paciente,
        inputs=[nome, idade, convenio, cidade, estado, prioridade, motivo],
        outputs=[saida_msg, tabela],
    )
    
demo.launch(share=False)  # Definir share=True para compartilhar publicamente