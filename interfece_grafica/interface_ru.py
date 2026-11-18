"""@file interface_ru.py
@brief Interface gráfica responsiva do Sistema Digital do Restaurante Universitário (UTFPR).
@details Comunica-se exclusivamente com as classes da pasta 'logica', sem duplicar
            regras de negócio na camada visual.
"""

import os
import sys
import tkinter as tk
from tkinter import messagebox

RAIZ_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_BACKEND = os.path.join(RAIZ_PROJETO, "back_end")
for caminho in (RAIZ_PROJETO, PASTA_BACKEND):
    if caminho not in sys.path:
        sys.path.insert(0, caminho)

from back_end.caixa import CaixaRU
from back_end.pedidos import MetodoPagamento, Pedido, criar_cardapio_padrao
from back_end.usuarios import Aluno, Externo, Servidor, Usuario


class TelaSistemaRU(tk.Tk):
    """@brief Janela principal responsiva do protótipo gráfico do RU."""

    LARGURA_QUEBRA_MOBILE  =  760

    def __init__(self) -> None:
        super().__init__()
        self.title("Sistema Digital do RU — UTFPR")

        # Instanciação direta dos objetos da camada de lógica
        self.cardapio  =  criar_cardapio_padrao()
        self.caixa  =  CaixaRU()
        self.pedido_atual: Pedido | None  =  None
        self.proximo_id_pedido  =  1

        self._logo_original: tk.PhotoImage | None  =  None
        self.imagem_logo: tk.PhotoImage | None  =  None
        self._fator_logo_atual: int | None  =  None
        self._modo_layout_atual: str | None  =  None
        self._ultima_largura: int  =  0

        self._configurar_geometria_adaptativa()
        self._criar_container_rolavel()
        self._montar_cabecalho()
        self._montar_area_principal()
        self._montar_rodape()
        self._preencher_lista_cardapio()

        self.bind("<Configure>", self._ao_redimensionar_janela)

    def _configurar_geometria_adaptativa(self) -> None:
        """@brief Ajusta o tamanho inicial da janela conforme a resolução do aparelho."""
        largura_aparelho  =  self.winfo_screenwidth()
        altura_aparelho  =  self.winfo_screenheight()

        largura_inicial  =  min(1020, max(340, int(largura_aparelho * 0.92)))
        altura_inicial  =  min(740, max(480, int(altura_aparelho * 0.88)))

        pos_x  =  max(0, (largura_aparelho - largura_inicial) // 2)
        pos_y  =  max(0, (altura_aparelho - altura_inicial) // 2)

        self.geometry(f"{largura_inicial}x{altura_inicial}+{pos_x}+{pos_y}")
        self.minsize(330, 460)

    def _criar_container_rolavel(self) -> None:
        """@brief Cria área com rolagem vertical para telas pequenas (celular/tablet)."""
        self.canvas_principal  =  tk.Canvas(self, highlightthickness = 0)
        self.barra_rolagem  =  tk.Scrollbar(
            self, orient = "vertical", command = self.canvas_principal.yview
        )
        self.canvas_principal.configure(yscrollcommand = self.barra_rolagem.set)

        self.barra_rolagem.pack(side = "right", fill = "y")
        self.canvas_principal.pack(side = "left", fill = "both", expand = True)

        self.painel_rolavel  =  tk.Frame(self.canvas_principal)
        self._id_janela_canvas  =  self.canvas_principal.create_window(
            (0, 0), window = self.painel_rolavel, anchor = "nw"
        )

        self.painel_rolavel.bind(
            "<Configure>",
            lambda _e: self.canvas_principal.configure(
                scrollregion = self.canvas_principal.bbox("all")
            ),
        )
        self.canvas_principal.bind(
            "<Configure>",
            lambda e: self.canvas_principal.itemconfig(
                self._id_janela_canvas, width = e.width
            ),
        )

        self.bind_all("<MouseWheel>", self._rolar_com_mouse)
        self.bind_all("<Button-4>", lambda _e: self.canvas_principal.yview_scroll(-1, "units"))
        self.bind_all("<Button-5>", lambda _e: self.canvas_principal.yview_scroll(1, "units"))

    def _rolar_com_mouse(self, evento: tk.Event) -> None:
        """@brief Permite rolar a tela verticalmente com o mouse ou touchpad."""
        if self.canvas_principal.bbox("all"):
            self.canvas_principal.yview_scroll(int(-1 * (evento.delta / 120)), "units")

    def _montar_cabecalho(self) -> None:
        """@brief Posiciona a logo da UTFPR e o título institucional no topo da janela."""
        painel_superior  =  tk.Frame(self.painel_rolavel, padx = 12, pady = 10)
        painel_superior.pack(side = "top", fill = "x")

        pasta_gui  =  os.path.dirname(os.path.abspath(__file__))
        caminhos_possiveis  =  [
            os.path.join(pasta_gui, "UTFPR-Logo.png"),
            os.path.join(RAIZ_PROJETO, "UTFPR-Logo.png"),
        ]

        for caminho in caminhos_possiveis:
            if os.path.exists(caminho):
                try:
                    self._logo_original  =  tk.PhotoImage(file = caminho)
                    break
                except tk.TclError:
                    self._logo_original  =  None

        self.rotulo_logo  =  tk.Label(painel_superior)
        self.rotulo_logo.pack(side = "top")
        self._atualizar_escala_logo(self.winfo_screenwidth())

        self.rotulo_titulo  =  tk.Label(
            painel_superior,
            text = "Sistema Digital do Restaurante Universitário — Pedidos e Caixa",
            font = ("Arial", 12, "bold"),
            justify = "center",
            pady = 6,
        )
        self.rotulo_titulo.pack(side = "top", fill = "x")

    def _atualizar_escala_logo(self, largura_disponivel: int) -> None:
        """@brief Ajusta proporcionalmente a logo da UTFPR para não cortar nas bordas."""
        if self._logo_original is None:
            self.rotulo_logo.config(
                text = "UTFPR — Universidade Tecnológica Federal do Paraná",
                font = ("Arial", 11, "bold"),
            )
            return

        largura_alvo  =  min(240, max(130, int(largura_disponivel * 0.45)))
        fator_escala  =  max(1, self._logo_original.width() // largura_alvo)

        if fator_escala != self._fator_logo_atual:
            self._fator_logo_atual  =  fator_escala
            self.imagem_logo  =  self._logo_original.subsample(fator_escala, fator_escala)
            self.rotulo_logo.config(image = self.imagem_logo)

    def _montar_area_principal(self) -> None:
        """@brief Cria os dois blocos principais que alternam entre 1 e 2 colunas."""
        self.painel_conteudo  =  tk.Frame(self.painel_rolavel, padx = 14, pady = 4)
        self.painel_conteudo.pack(expand = True, fill = "both")

        # ---------------- BLOCO 1: USUÁRIO E CARDÁPIO ----------------
        self.painel_esquerda  =  tk.LabelFrame(
            self.painel_conteudo,
            text = " 1. Identificação do Usuário e Cardápio ",
            font = ("Arial", 10, "bold"),
            padx = 10,
            pady = 8,
        )
        self.painel_esquerda.columnconfigure(1, weight = 1)

        tk.Label(self.painel_esquerda, text = "Perfil:").grid(row = 0, column = 0, sticky = "w", pady = 4)
        self.perfil_selecionado  =  tk.StringVar(value = "Aluno")
        self.seletor_perfil  =  tk.OptionMenu(
            self.painel_esquerda,
            self.perfil_selecionado,
            "Aluno",
            "Servidor",
            "Externo",
            command = self._atualizar_dica_identificador,
        )
        self.seletor_perfil.grid(row = 0, column = 1, sticky = "ew", padx = (6, 0), pady = 4)

        tk.Label(self.painel_esquerda, text = "Nome Completo:").grid(
            row = 1, column = 0, sticky = "w", pady = 4
        )
        self.campo_nome  =  tk.Entry(self.painel_esquerda, width = 14)
        self.campo_nome.grid(row = 1, column = 1, sticky = "ew", padx = (6, 0), pady = 4)

        tk.Label(self.painel_esquerda, text = "E-mail:").grid(row = 2, column = 0, sticky = "w", pady = 4)
        self.campo_email  =  tk.Entry(self.painel_esquerda, width = 14)
        self.campo_email.grid(row = 2, column = 1, sticky = "ew", padx = (6, 0), pady = 4)

        self.rotulo_identificador  =  tk.Label(self.painel_esquerda, text = "RA (7 dígitos):")
        self.rotulo_identificador.grid(row = 3, column = 0, sticky = "w", pady = 4)
        self.campo_identificador  =  tk.Entry(self.painel_esquerda, width = 14)
        self.campo_identificador.grid(row = 3, column = 1, sticky = "ew", padx = (6, 0), pady = 4)

        tk.Label(
            self.painel_esquerda,
            text = "Itens Disponíveis no Cardápio:",
            font = ("Arial", 9, "bold"),
        ).grid(row = 4, column = 0, columnspan = 2, sticky = "w", pady = (10, 4))

        self.lista_cardapio  =  tk.Listbox(self.painel_esquerda, height = 9, width = 20)
        self.lista_cardapio.grid(row = 5, column = 0, columnspan = 2, sticky = "nsew", pady = 4)

        painel_qtd  =  tk.Frame(self.painel_esquerda)
        painel_qtd.grid(row = 6, column = 0, columnspan = 2, sticky = "ew", pady = 8)

        tk.Label(painel_qtd, text = "Qtd:").pack(side = "left")
        self.campo_quantidade  =  tk.Entry(painel_qtd, width = 5)
        self.campo_quantidade.insert(0, "1")
        self.campo_quantidade.pack(side = "left", padx = 6)

        self.botao_adicionar  =  tk.Button(
            painel_qtd,
            text = "Adicionar ao Pedido",
            bg = "#FFCC00",
            fg = "#111111",
            font = ("Arial", 9, "bold"),
            command = self.adicionar_item_ao_pedido,
        )
        self.botao_adicionar.pack(side = "right", fill = "x", expand = True)

        # ---------------- BLOCO 2: RESUMO, PAGAMENTO E RETIRADA ----------------
        self.painel_direita  =  tk.LabelFrame(
            self.painel_conteudo,
            text = " 2. Resumo do Pedido, Pagamento e Retirada ",
            font = ("Arial", 10, "bold"),
            padx = 10,
            pady = 8,
        )

        self.rotulo_usuario_ativo  =  tk.Label(
            self.painel_direita, text = "Usuário: Nenhum pedido iniciado", anchor = "w", justify = "left"
        )
        self.rotulo_usuario_ativo.pack(fill = "x", pady = 2)

        self.rotulo_status_pedido  =  tk.Label(
            self.painel_direita,
            text = "Status: Aguardando itens",
            font = ("Arial", 9, "bold"),
            fg = "#444444",
            anchor = "w",
            justify = "left",
        )
        self.rotulo_status_pedido.pack(fill = "x", pady = 2)

        self.lista_itens_pedido  =  tk.Listbox(self.painel_direita, height = 7, width = 20)
        self.lista_itens_pedido.pack(fill = "both", expand = True, pady = 6)

        self.rotulo_valor_total  =  tk.Label(
            self.painel_direita,
            text = "Total do Pedido: R$ 0,00",
            font = ("Arial", 11, "bold"),
            anchor = "e",
        )
        self.rotulo_valor_total.pack(fill = "x", pady = 4)

        quadro_pagamento  =  tk.LabelFrame(self.painel_direita, text = " Pagamento ", padx = 8, pady = 6)
        quadro_pagamento.pack(fill = "x", pady = 6)
        quadro_pagamento.columnconfigure(1, weight = 1)

        tk.Label(quadro_pagamento, text = "Forma:").grid(row = 0, column = 0, sticky = "w", pady = 3)
        self.metodo_selecionado  =  tk.StringVar(value = MetodoPagamento.DINHEIRO_ESPECIE.value)
        self.seletor_pagamento  =  tk.OptionMenu(
            quadro_pagamento,
            self.metodo_selecionado,
            MetodoPagamento.DINHEIRO_ESPECIE.value,
            MetodoPagamento.PIX.value,
            MetodoPagamento.CARTAO.value,
            command = self._ao_trocar_forma_pagamento,
        )
        self.seletor_pagamento.grid(row = 0, column = 1, sticky = "ew", padx = (6, 0), pady = 3)

        tk.Label(quadro_pagamento, text = "Valor Recebido (R$):").grid(
            row = 1, column = 0, sticky = "w", pady = 3
        )
        self.campo_valor_pago  =  tk.Entry(quadro_pagamento, width = 12)
        self.campo_valor_pago.grid(row = 1, column = 1, sticky = "ew", padx = (6, 0), pady = 3)
        self.campo_valor_pago.bind("<Return>", lambda _e: self.processar_pagamento())

        self.botao_pagar  =  tk.Button(
            quadro_pagamento,
            text = "Confirmar Pagamento",
            command = self.processar_pagamento,
        )
        self.botao_pagar.grid(row = 2, column = 0, columnspan = 2, sticky = "ew", pady = (6, 2))

        quadro_retirada  =  tk.LabelFrame(
            self.painel_direita, text = " Validação de Retirada (CaixaRU) ", padx = 8, pady = 6
        )
        quadro_retirada.pack(fill = "x", pady = 6)
        quadro_retirada.columnconfigure(1, weight = 1)

        tk.Label(quadro_retirada, text = "Código Retirada:").grid(
            row = 0, column = 0, sticky = "w", pady = 3
        )
        self.campo_codigo_retirada  =  tk.Entry(quadro_retirada, width = 14)
        self.campo_codigo_retirada.grid(row = 0, column = 1, sticky = "ew", padx = (6, 0), pady = 3)
        self.campo_codigo_retirada.bind("<Return>", lambda _e: self.confirmar_entrega_pedido())

        self.botao_retirar  =  tk.Button(
            quadro_retirada,
            text = "Confirmar Retirada da Refeição",
            command = self.confirmar_entrega_pedido,
        )
        self.botao_retirar.grid(row = 1, column = 0, columnspan = 2, sticky = "ew", pady = (6, 2))

    def _montar_rodape(self) -> None:
        """@brief Exibe mensagens de feedback e botão para iniciar novo atendimento."""
        painel_inferior  =  tk.Frame(self.painel_rolavel, padx = 14, pady = 10)
        painel_inferior.pack(side = "bottom", fill = "x")
        painel_inferior.columnconfigure(0, weight = 1)

        self.rotulo_mensagem_sistema  =  tk.Label(
            painel_inferior,
            text = "Preencha os dados do usuário e selecione um item do cardápio para começar.",
            fg = "#333333",
            anchor = "w",
            justify = "left",
        )
        self.rotulo_mensagem_sistema.grid(row = 0, column = 0, sticky = "ew", padx = (0, 8))

        self.botao_novo_atendimento  =  tk.Button(
            painel_inferior,
            text = "Novo Atendimento",
            command = self.reiniciar_atendimento,
        )
        self.botao_novo_atendimento.grid(row = 0, column = 1, sticky = "e")

    def _ao_redimensionar_janela(self, evento: tk.Event) -> None:
        """@brief Alterna entre 1 coluna (mobile/tablet) e 2 colunas (notebook)."""
        if evento.widget is not self:
            return

        largura_atual  =  evento.width
        if largura_atual == self._ultima_largura:
            return
        self._ultima_largura  =  largura_atual

        self._atualizar_escala_logo(largura_atual)
        self.rotulo_titulo.config(wraplength = max(260, largura_atual - 40))
        self.rotulo_mensagem_sistema.config(wraplength = max(180, largura_atual - 180))

        largura_bloco  =  (
            largura_atual - 50
            if largura_atual < self.LARGURA_QUEBRA_MOBILE
            else (largura_atual // 2) - 50
        )
        self.rotulo_usuario_ativo.config(wraplength = max(220, largura_bloco))
        self.rotulo_status_pedido.config(wraplength = max(220, largura_bloco))

        novo_modo  =  (
            "coluna_unica"
            if largura_atual < self.LARGURA_QUEBRA_MOBILE
            else "duas_colunas"
        )

        if novo_modo != self._modo_layout_atual:
            self._modo_layout_atual  =  novo_modo
            if novo_modo == "coluna_unica":
                self.painel_conteudo.columnconfigure(0, weight = 1, uniform = "")
                self.painel_conteudo.columnconfigure(1, weight = 0, uniform = "")
                self.painel_esquerda.grid(row = 0, column = 0, sticky = "nsew", padx = 0, pady = (0, 10))
                self.painel_direita.grid(row = 1, column = 0, sticky = "nsew", padx = 0, pady = (0, 6))
            else:
                self.painel_conteudo.columnconfigure(0, weight = 1, uniform = "colunas")
                self.painel_conteudo.columnconfigure(1, weight = 1, uniform = "colunas")
                self.painel_esquerda.grid(row = 0, column = 0, sticky = "nsew", padx = (0, 8), pady = 0)
                self.painel_direita.grid(row = 0, column = 1, sticky = "nsew", padx = (8, 0), pady = 0)

    def _preencher_lista_cardapio(self) -> None:
        """@brief Carrega os itens do cardápio da camada lógica na lista visual."""
        self.lista_cardapio.delete(0, tk.END)
        for item in self.cardapio.itens:
            self.lista_cardapio.insert(
                tk.END, f"[{item.id_item:02d}] {item.nome} — R$ {item.preco:.2f}"
            )

    def _atualizar_dica_identificador(self, perfil: str) -> None:
        """@brief Atualiza o rótulo do campo identificador conforme o perfil."""
        if perfil == "Aluno":
            self.rotulo_identificador.config(text = "RA (7 dígitos):")
        elif perfil == "Servidor":
            self.rotulo_identificador.config(text = "ID Servidor (8 dígitos):")
        else:
            self.rotulo_identificador.config(text = "Código Externo:")

    def _ao_trocar_forma_pagamento(self, _metodo: str) -> None:
        """@brief Atualiza o valor preenchido ao alternar a forma de pagamento."""
        if self.pedido_atual is not None and self.pedido_atual.status == "aguardando_pagamento":
            self._preencher_valor_a_pagar()

    def _preencher_valor_a_pagar(self) -> None:
        """@brief Preenche o campo Valor Recebido com o total calculado pelo Pedido."""
        if self.pedido_atual is None:
            return
        self.campo_valor_pago.delete(0, tk.END)
        self.campo_valor_pago.insert(0, f"{self.pedido_atual.valor_total:.2f}")

    def _criar_usuario_selecionado(self) -> Usuario:
        """@brief Instancia diretamente a subclasse correspondente ao perfil escolhido."""
        perfil  =  self.perfil_selecionado.get()
        nome  =  self.campo_nome.get()
        email  =  self.campo_email.get()
        identificador  =  self.campo_identificador.get()

        if perfil == "Aluno":
            return Aluno(nome, email, identificador)
        if perfil == "Servidor":
            return Servidor(nome, email, identificador)
        return Externo(nome, email, identificador)

    def adicionar_item_ao_pedido(self) -> None:
        """@brief Ouvinte do botão Adicionar: delega criação e validação à camada lógica."""
        selecao  =  self.lista_cardapio.curselection()
        if not selecao:
            self.mostrar_erro("Selecione um item do cardápio antes de adicionar.")
            return

        try:
            quantidade  =  int(self.campo_quantidade.get().strip())
        except ValueError:
            self.mostrar_erro("A quantidade deve ser um número inteiro válido.")
            return

        try:
            if self.pedido_atual is None:
                usuario  =  self._criar_usuario_selecionado()
                self.pedido_atual  =  Pedido(self.proximo_id_pedido, usuario)
                self.proximo_id_pedido += 1
                self._alternar_campos_usuario(habilitado = False)

            indice_selecionado  =  selecao[0]
            item_escolhido  =  self.cardapio.itens[indice_selecionado]
            self.pedido_atual.adicionar_item(item_escolhido, quantidade)

            self._atualizar_resumo_pedido()
            self._preencher_valor_a_pagar()
            self.rotulo_mensagem_sistema.config(
                text = f"Item [{item_escolhido.id_item:02d}] '{item_escolhido.nome}' (x{quantidade}) "
                        f"vinculado a {self.pedido_atual.usuario.gerar_codigo_identificacao()}.",
                fg = "#006600",
            )
        except ValueError as erro:
            self.mostrar_erro(str(erro))

    def _obter_enum_pagamento(self, texto_metodo: str) -> MetodoPagamento:
        """@brief Converte o texto selecionado na tela para o Enum MetodoPagamento."""
        for metodo in MetodoPagamento:
            if metodo.value == texto_metodo:
                return metodo
        raise ValueError(f"Forma de pagamento inválida: {texto_metodo}")

    def processar_pagamento(self) -> None:
        """@brief Ouvinte do pagamento: envia os dados ao CaixaRU e exibe o retorno."""
        if self.pedido_atual is None:
            self.mostrar_erro("Inicie um pedido adicionando itens antes de pagar.")
            return

        texto_valor  =  self.campo_valor_pago.get().strip().replace(",", ".")
        try:
            valor_recebido  =  float(texto_valor)
        except ValueError:
            self.mostrar_erro("Informe um valor numérico válido no campo 'Valor Recebido (R$)'.")
            return

        try:
            metodo_enum  =  self._obter_enum_pagamento(self.metodo_selecionado.get())
            troco  =  self.caixa.registrar_pagamento_pedido(
                self.pedido_atual, metodo_enum, valor_recebido
            )

            self._atualizar_resumo_pedido()
            codigos_itens  =  ", ".join(
                f"[{item.id_item:02d}] {item.nome} (x{qtd})"
                for item, qtd in self.pedido_atual.itens
            )

            detalhe_troco  =  (
                f"\nTroco: R$ {troco:.2f}"
                if metodo_enum == MetodoPagamento.DINHEIRO_ESPECIE
                else ""
            )

            messagebox.showinfo(
                "Pagamento Confirmado — RU UTFPR",
                f"Pagamento via {metodo_enum.value} confirmado!{detalhe_troco}\n\n"
                f"Vínculo do Usuário: {self.pedido_atual.usuario.gerar_codigo_identificacao()}\n"
                f"Produtos Comprados: {codigos_itens}\n"
                f"Código para retirada no balcão: {self.pedido_atual.codigo_retirada}",
            )
            self.campo_codigo_retirada.focus()
        except ValueError as erro:
            self.mostrar_erro(str(erro))

    def confirmar_entrega_pedido(self) -> None:
        """@brief Ouvinte da retirada: delega a conferência do código ao CaixaRU."""
        if self.pedido_atual is None:
            self.mostrar_erro("Nenhum pedido ativo para retirada.")
            return

        codigo_digitado  =  self.campo_codigo_retirada.get()
        try:
            self.caixa.confirmar_retirada(self.pedido_atual, codigo_digitado)
            self._atualizar_resumo_pedido()
            self.rotulo_mensagem_sistema.config(
                text = f"Pedido #{self.pedido_atual.id_pedido} retirado por "
                        f"{self.pedido_atual.usuario.gerar_codigo_identificacao()}!",
                fg = "#006600",
            )
            messagebox.showinfo(
                "Retirada Confirmada",
                f"Refeição liberada para {self.pedido_atual.usuario.nome}!\n"
                f"Identificação vinculada: {self.pedido_atual.usuario.gerar_codigo_identificacao()}\n"
                f"Código validado: {self.pedido_atual.codigo_retirada}",
            )
        except ValueError as erro:
            self.mostrar_erro(str(erro))

    def _atualizar_resumo_pedido(self) -> None:
        """@brief Atualiza os elementos visuais com o estado atual do objeto Pedido."""
        if self.pedido_atual is None:
            return

        usuario  =  self.pedido_atual.usuario
        codigo_usuario  =  usuario.gerar_codigo_identificacao()

        self.rotulo_usuario_ativo.config(
            text = f"Usuário: {usuario.nome} ({codigo_usuario})"
        )
        self.rotulo_status_pedido.config(
            text = f"Status: {self.pedido_atual.status.replace('_', ' ').upper()} | "
                    f"Código: {self.pedido_atual.codigo_retirada}"
        )

        self.lista_itens_pedido.delete(0, tk.END)
        for item, qtd in self.pedido_atual.itens:
            subtotal  =  item.preco * qtd
            self.lista_itens_pedido.insert(
                tk.END,
                f"[{codigo_usuario} | Item {item.id_item:02d}] {qtd}x {item.nome} — R$ {subtotal:.2f}",
            )

        self.rotulo_valor_total.config(
            text = f"Total do Pedido: R$ {self.pedido_atual.valor_total:.2f}"
        )

    def _alternar_campos_usuario(self, habilitado: bool) -> None:
        """@brief Bloqueia ou libera os campos cadastrais durante um pedido aberto."""
        estado  =  "normal" if habilitado else "disabled"
        self.campo_nome.config(state = estado)
        self.campo_email.config(state = estado)
        self.campo_identificador.config(state = estado)
        self.seletor_perfil.config(state = estado)

    def reiniciar_atendimento(self) -> None:
        """@brief Limpa os campos da tela para iniciar um novo atendimento."""
        self.pedido_atual  =  None
        self._alternar_campos_usuario(habilitado = True)

        self.campo_nome.delete(0, tk.END)
        self.campo_email.delete(0, tk.END)
        self.campo_identificador.delete(0, tk.END)
        self.campo_valor_pago.delete(0, tk.END)
        self.campo_codigo_retirada.delete(0, tk.END)
        self.campo_quantidade.delete(0, tk.END)
        self.campo_quantidade.insert(0, "1")

        self.lista_itens_pedido.delete(0, tk.END)
        self.rotulo_usuario_ativo.config(text = "Usuário: Nenhum pedido iniciado")
        self.rotulo_status_pedido.config(text = "Status: Aguardando itens")
        self.rotulo_valor_total.config(text = "Total do Pedido: R$ 0,00")
        self.rotulo_mensagem_sistema.config(
            text = "Pronto para novo atendimento.", fg = "#333333"
        )
        self.campo_nome.focus()

    def mostrar_erro(self, mensagem: str) -> None:
        """@brief Exibe exceções capturadas da camada lógica em diálogo visual."""
        self.rotulo_mensagem_sistema.config(text = mensagem, fg = "#CC0000")
        messagebox.showerror("Atenção — Sistema RU UTFPR", mensagem)


if __name__ == "__main__":
    TelaSistemaRU().mainloop()
