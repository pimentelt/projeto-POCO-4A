"""@file interface_ru.py
@brief Interface gráfica do Sistema Digital do Restaurante Universitário (UTFPR).
@details Integra as classes de domínio (usuarios, pedidos e caixa) utilizando
         Tkinter, tratamento de exceções e os padrões Factory Method e Singleton.
"""

import os
import tkinter as tk
from tkinter import messagebox

from caixa import CaixaRU
from pedidos import Cardapio, ItemCardapio, MetodoPagamento, Pedido
from usuarios import Aluno, Externo, Servidor, Usuario


# =====================================================================
# PADRÕES DE PROJETO (Factory Method e Singleton)
# =====================================================================

class FabricaUsuario:
    """@brief Factory Method responsável por instanciar os perfis de usuário do RU."""

    @staticmethod
    def criar_usuario(perfil: str, nome: str, email: str, identificador: str) -> Usuario:
        """@brief Cria uma subclasse de Usuario conforme o perfil selecionado.

        @param perfil Tipo de vínculo ('Aluno', 'Servidor' ou 'Externo').
        @param nome Nome completo do usuário.
        @param email E-mail institucional ou pessoal.
        @param identificador RA (7 dígitos), ID funcional (8 dígitos) ou código externo.
        @return Instância concreta de Usuario.
        @throws ValueError Se algum campo estiver vazio ou o perfil for desconhecido.
        """
        nome_limpo = nome.strip()
        email_limpo = email.strip()
        id_limpo = identificador.strip()

        if not nome_limpo:
            raise ValueError("Informe o nome completo do usuário.")
        if not email_limpo or "@" not in email_limpo:
            raise ValueError("Informe um endereço de e-mail válido.")
        if not id_limpo:
            raise ValueError("Informe o RA, ID funcional ou código de identificação.")

        if perfil == "Aluno":
            return Aluno(nome_limpo, email_limpo, id_limpo)
        if perfil == "Servidor":
            return Servidor(nome_limpo, email_limpo, id_limpo)
        if perfil == "Externo":
            return Externo(nome_limpo, email_limpo, id_limpo)

        raise ValueError(f"Perfil de usuário desconhecido: {perfil}")


class SistemaRU:
    """@brief Singleton que centraliza o estado operacional do Restaurante Universitário."""

    _instancia_unica: "SistemaRU | None" = None

    def __init__(self) -> None:
        self.cardapio = self._carregar_cardapio_padrao()
        self.caixa = CaixaRU()
        self.pedidos_realizados: list[Pedido] = []
        self.proximo_id_pedido = 1

    @classmethod
    def obter_instancia(cls) -> "SistemaRU":
        """@brief Retorna sempre a mesma instância do sistema do RU."""
        if cls._instancia_unica is None:
            cls._instancia_unica = SistemaRU()
        return cls._instancia_unica

    def _carregar_cardapio_padrao(self) -> Cardapio:
        """@brief Inicializa o cardápio oficial com os itens disponíveis no RU."""
        cardapio_ru = Cardapio()
        cardapio_ru.adicionar_item(ItemCardapio(1, "Prato do Dia", 12.50))
        cardapio_ru.adicionar_item(ItemCardapio(2, "Água s/ gás", 3.00))
        cardapio_ru.adicionar_item(ItemCardapio(3, "Água c/ gás", 3.50))
        cardapio_ru.adicionar_item(ItemCardapio(4, "Salgados Assados", 6.50))
        cardapio_ru.adicionar_item(ItemCardapio(5, "Salgados Fritos", 5.00))
        cardapio_ru.adicionar_item(ItemCardapio(6, "Bolo Gelado", 10.00))
        cardapio_ru.adicionar_item(ItemCardapio(7, "Suco Natural de Laranja (300ml)", 3.50))
        cardapio_ru.adicionar_item(ItemCardapio(8, "Suco Natural de Uva (300ml)", 3.00))
        cardapio_ru.adicionar_item(ItemCardapio(9, "Refrigerante Lata (Coca, Fanta, Guaraná)", 5.00))
        cardapio_ru.adicionar_item(ItemCardapio(10, "Bombom", 3.00))
        return cardapio_ru

    def iniciar_pedido(self, usuario: Usuario) -> Pedido:
        """@brief Cria um novo pedido numerado e o registra no histórico do sistema."""
        novo_pedido = Pedido(self.proximo_id_pedido, usuario)
        self.proximo_id_pedido += 1
        self.pedidos_realizados.append(novo_pedido)
        return novo_pedido


# =====================================================================
# INTERFACE GRÁFICA (Tkinter com Layout, Eventos e Exceções)
# =====================================================================

class TelaSistemaRU(tk.Tk):
    """@brief Janela principal do protótipo gráfico do Restaurante Universitário."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Sistema Digital do RU — UTFPR")
        self.geometry("860x660")
        self.minsize(820, 620)

        self.sistema = SistemaRU.obter_instancia()
        self.pedido_atual: Pedido | None = None
        self.imagem_logo: tk.PhotoImage | None = None

        self._montar_cabecalho()
        self._montar_area_principal()
        self._montar_rodape()
        self._preencher_lista_cardapio()

    def _montar_cabecalho(self) -> None:
        """@brief Posiciona a logo da UTFPR e o título institucional no topo da janela."""
        painel_superior = tk.Frame(self, pady=10)
        painel_superior.pack(side="top", fill="x")

        caminho_logo = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "UTFPR-Logo.png"
        )
        try:
            logo_original = tk.PhotoImage(file=caminho_logo)
            fator_escala = max(1, logo_original.width() // 250)
            self.imagem_logo = logo_original.subsample(fator_escala, fator_escala)

            rotulo_logo = tk.Label(painel_superior, image=self.imagem_logo)
            rotulo_logo.pack(side="top")
        except tk.TclError:
            rotulo_logo = tk.Label(
                painel_superior,
                text="UTFPR — Universidade Tecnológica Federal do Paraná",
                font=("Arial", 11, "bold"),
            )
            rotulo_logo.pack(side="top")

        rotulo_titulo = tk.Label(
            painel_superior,
            text="Sistema Digital do Restaurante Universitário — Pedidos e Caixa",
            font=("Arial", 13, "bold"),
            pady=6,
        )
        rotulo_titulo.pack(side="top")

    def _montar_area_principal(self) -> None:
        """@brief Divide a tela em duas colunas: montagem do pedido e operações do caixa."""
        painel_conteudo = tk.Frame(self, padx=15, pady=5)
        painel_conteudo.pack(expand=True, fill="both")
        painel_conteudo.columnconfigure(0, weight=1)
        painel_conteudo.columnconfigure(1, weight=1)

        # ---------------- COLUNA ESQUERDA: USUÁRIO E CARDÁPIO ----------------
        painel_esquerda = tk.LabelFrame(
            painel_conteudo,
            text=" 1. Identificação do Usuário e Cardápio ",
            font=("Arial", 10, "bold"),
            padx=12,
            pady=10,
        )
        painel_esquerda.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        tk.Label(painel_esquerda, text="Perfil:").grid(row=0, column=0, sticky="w", pady=4)
        self.perfil_selecionado = tk.StringVar(value="Aluno")
        self.seletor_perfil = tk.OptionMenu(
            painel_esquerda,
            self.perfil_selecionado,
            "Aluno",
            "Servidor",
            "Externo",
            command=self._atualizar_dica_identificador,
        )
        self.seletor_perfil.config(width=22)
        self.seletor_perfil.grid(row=0, column=1, sticky="w", pady=4)

        tk.Label(painel_esquerda, text="Nome Completo:").grid(row=1, column=0, sticky="w", pady=4)
        self.campo_nome = tk.Entry(painel_esquerda, width=28)
        self.campo_nome.grid(row=1, column=1, sticky="w", pady=4)

        tk.Label(painel_esquerda, text="E-mail:").grid(row=2, column=0, sticky="w", pady=4)
        self.campo_email = tk.Entry(painel_esquerda, width=28)
        self.campo_email.grid(row=2, column=1, sticky="w", pady=4)

        self.rotulo_identificador = tk.Label(painel_esquerda, text="RA (7 dígitos):")
        self.rotulo_identificador.grid(row=3, column=0, sticky="w", pady=4)
        self.campo_identificador = tk.Entry(painel_esquerda, width=28)
        self.campo_identificador.grid(row=3, column=1, sticky="w", pady=4)

        tk.Label(
            painel_esquerda,
            text="Itens Disponíveis no Cardápio:",
            font=("Arial", 9, "bold"),
        ).grid(row=4, column=0, columnspan=2, sticky="w", pady=(10, 4))

        self.lista_cardapio = tk.Listbox(painel_esquerda, height=10, width=44)
        self.lista_cardapio.grid(row=5, column=0, columnspan=2, sticky="ew", pady=4)

        painel_qtd = tk.Frame(painel_esquerda)
        painel_qtd.grid(row=6, column=0, columnspan=2, sticky="ew", pady=8)

        tk.Label(painel_qtd, text="Quantidade:").pack(side="left")
        self.campo_quantidade = tk.Entry(painel_qtd, width=6)
        self.campo_quantidade.insert(0, "1")
        self.campo_quantidade.pack(side="left", padx=6)

        self.botao_adicionar = tk.Button(
            painel_qtd,
            text="Adicionar ao Pedido",
            bg="#FFCC00",
            fg="#111111",
            font=("Arial", 9, "bold"),
            command=self.adicionar_item_ao_pedido,
        )
        self.botao_adicionar.pack(side="right")

        # ---------------- COLUNA DIREITA: RESUMO, PAGAMENTO E RETIRADA ----------------
        painel_direita = tk.LabelFrame(
            painel_conteudo,
            text=" 2. Resumo do Pedido, Pagamento e Retirada ",
            font=("Arial", 10, "bold"),
            padx=12,
            pady=10,
        )
        painel_direita.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        self.rotulo_usuario_ativo = tk.Label(
            painel_direita, text="Usuário: Nenhum pedido iniciado", anchor="w"
        )
        self.rotulo_usuario_ativo.pack(fill="x", pady=2)

        self.rotulo_status_pedido = tk.Label(
            painel_direita,
            text="Status: Aguardando itens",
            font=("Arial", 9, "bold"),
            fg="#444444",
            anchor="w",
        )
        self.rotulo_status_pedido.pack(fill="x", pady=2)

        self.lista_itens_pedido = tk.Listbox(painel_direita, height=8, width=44)
        self.lista_itens_pedido.pack(fill="x", pady=6)

        self.rotulo_valor_total = tk.Label(
            painel_direita,
            text="Total do Pedido: R$ 0,00",
            font=("Arial", 11, "bold"),
            anchor="e",
        )
        self.rotulo_valor_total.pack(fill="x", pady=4)

        # Subpainel de Pagamento
        quadro_pagamento = tk.LabelFrame(painel_direita, text=" Pagamento ", padx=8, pady=6)
        quadro_pagamento.pack(fill="x", pady=6)

        tk.Label(quadro_pagamento, text="Forma:").grid(row=0, column=0, sticky="w", pady=3)
        self.metodo_selecionado = tk.StringVar(value=MetodoPagamento.DINHEIRO_ESPECIE.value)
        self.seletor_pagamento = tk.OptionMenu(
            quadro_pagamento,
            self.metodo_selecionado,
            MetodoPagamento.DINHEIRO_ESPECIE.value,
            MetodoPagamento.PIX.value,
            MetodoPagamento.CARTAO.value,
        )
        self.seletor_pagamento.config(width=22)
        self.seletor_pagamento.grid(row=0, column=1, sticky="w", pady=3)

        tk.Label(quadro_pagamento, text="Valor Recebido (R$):").grid(
            row=1, column=0, sticky="w", pady=3
        )
        self.campo_valor_pago = tk.Entry(quadro_pagamento, width=15)
        self.campo_valor_pago.grid(row=1, column=1, sticky="w", pady=3)
        self.campo_valor_pago.bind("<Return>", lambda evento: self.processar_pagamento())

        self.botao_pagar = tk.Button(
            quadro_pagamento,
            text="Confirmar Pagamento",
            command=self.processar_pagamento,
        )
        self.botao_pagar.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(6, 2))

        # Subpainel de Retirada no Balcão
        quadro_retirada = tk.LabelFrame(
            painel_direita, text=" Validação de Retirada (CaixaRU) ", padx=8, pady=6
        )
        quadro_retirada.pack(fill="x", pady=6)

        tk.Label(quadro_retirada, text="Código de Retirada:").grid(
            row=0, column=0, sticky="w", pady=3
        )
        self.campo_codigo_retirada = tk.Entry(quadro_retirada, width=15)
        self.campo_codigo_retirada.grid(row=0, column=1, sticky="w", pady=3)
        self.campo_codigo_retirada.bind("<Return>", lambda evento: self.confirmar_entrega_pedido())

        self.botao_retirar = tk.Button(
            quadro_retirada,
            text="Confirmar Retirada da Refeição",
            command=self.confirmar_entrega_pedido,
        )
        self.botao_retirar.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(6, 2))

    def _montar_rodape(self) -> None:
        """@brief Exibe mensagens de feedback e botão para iniciar novo atendimento."""
        painel_inferior = tk.Frame(self, padx=15, pady=10)
        painel_inferior.pack(side="bottom", fill="x")

        self.rotulo_mensagem_sistema = tk.Label(
            painel_inferior,
            text="Preencha os dados do usuário e selecione um item do cardápio para começar.",
            fg="#333333",
        )
        self.rotulo_mensagem_sistema.pack(side="left")

        self.botao_novo_atendimento = tk.Button(
            painel_inferior,
            text="Novo Atendimento",
            command=self.reiniciar_atendimento,
        )
        self.botao_novo_atendimento.pack(side="right")

    def _preencher_lista_cardapio(self) -> None:
        """@brief Carrega os objetos ItemCardapio do Singleton dentro do Listbox."""
        self.lista_cardapio.delete(0, tk.END)
        for item in self.sistema.cardapio.itens:
            self.lista_cardapio.insert(
                tk.END, f"[{item.id_item:02d}] {item.nome} — R$ {item.preco:.2f}"
            )

    def _atualizar_dica_identificador(self, perfil: str) -> None:
        """@brief Atualiza o rótulo do identificador conforme o perfil escolhido."""
        if perfil == "Aluno":
            self.rotulo_identificador.config(text="RA (7 dígitos):")
        elif perfil == "Servidor":
            self.rotulo_identificador.config(text="ID Servidor (8 dígitos):")
        else:
            self.rotulo_identificador.config(text="Código Externo:")

    def adicionar_item_ao_pedido(self) -> None:
        """@brief Ouvinte do botão Adicionar: valida usuário/item e inclui no pedido."""
        selecao = self.lista_cardapio.curselection()
        if not selecao:
            self.mostrar_erro("Selecione um item do cardápio antes de adicionar.")
            return

        try:
            quantidade = int(self.campo_quantidade.get().strip())
        except ValueError:
            self.mostrar_erro("A quantidade deve ser um número inteiro válido.")
            return

        try:
            # Se ainda não há pedido aberto, instancia o usuário via Factory Method
            if self.pedido_atual is None:
                usuario = FabricaUsuario.criar_usuario(
                    perfil=self.perfil_selecionado.get(),
                    nome=self.campo_nome.get(),
                    email=self.campo_email.get(),
                    identificador=self.campo_identificador.get(),
                )
                self.pedido_atual = self.sistema.iniciar_pedido(usuario)
                self._alternar_campos_usuario(habilitado=False)

            if self.pedido_atual.status != "aguardando_pagamento":
                raise ValueError("Este pedido já foi pago. Clique em 'Novo Atendimento'.")

            indice_selecionado = selecao[0]
            item_escolhido = self.sistema.cardapio.itens[indice_selecionado]
            self.pedido_atual.adicionar_item(item_escolhido, quantidade)

            self._atualizar_resumo_pedido()
            self.rotulo_mensagem_sistema.config(
                text=f"Item '{item_escolhido.nome}' (x{quantidade}) adicionado ao pedido.",
                fg="#006600",
            )
        except ValueError as erro:
            self.mostrar_erro(str(erro))

    def processar_pagamento(self) -> None:
        """@brief Ouvinte do pagamento: delega ao CaixaRU ou registra pagamento digital."""
        if self.pedido_atual is None or not self.pedido_atual.itens:
            self.mostrar_erro("Adicione pelo menos um item ao pedido antes de pagar.")
            return

        forma_escolhida = self.metodo_selecionado.get()

        try:
            if forma_escolhida == MetodoPagamento.DINHEIRO_ESPECIE.value:
                texto_valor = self.campo_valor_pago.get().strip().replace(",", ".")
                try:
                    valor_recebido = float(texto_valor)
                except ValueError:
                    self.mostrar_erro("Informe um valor numérico válido recebido em dinheiro.")
                    return

                troco = self.sistema.caixa.receber_pagamento_especie(
                    self.pedido_atual, valor_recebido
                )
                detalhe_pagamento = f"Pagamento em dinheiro confirmado!\nTroco: R$ {troco:.2f}"
            else:
                if self.pedido_atual.status != "aguardando_pagamento":
                    raise ValueError("Este pedido não está aguardando pagamento.")
                metodo_enum = (
                    MetodoPagamento.PIX
                    if forma_escolhida == MetodoPagamento.PIX.value
                    else MetodoPagamento.CARTAO
                )
                self.pedido_atual.registrar_pagamento(metodo_enum)
                detalhe_pagamento = f"Pagamento via {forma_escolhida} confirmado!"

            self._atualizar_resumo_pedido()
            messagebox.showinfo(
                "Pagamento Confirmado — RU UTFPR",
                f"{detalhe_pagamento}\n\n"
                f"Código para retirada no balcão: {self.pedido_atual.codigo_retirada}",
            )
        except ValueError as erro:
            self.mostrar_erro(str(erro))

    def confirmar_entrega_pedido(self) -> None:
        """@brief Ouvinte da retirada: valida o código no CaixaRU e conclui o pedido."""
        if self.pedido_atual is None:
            self.mostrar_erro("Nenhum pedido ativo para retirada.")
            return

        codigo_digitado = self.campo_codigo_retirada.get()
        try:
            self.sistema.caixa.confirmar_retirada(self.pedido_atual, codigo_digitado)
            self._atualizar_resumo_pedido()
            self.rotulo_mensagem_sistema.config(
                text=f"Pedido #{self.pedido_atual.id_pedido} retirado com sucesso!",
                fg="#006600",
            )
            messagebox.showinfo(
                "Retirada Confirmada",
                f"Refeição liberada para {self.pedido_atual.usuario.nome}!\n"
                f"Identificação: {self.pedido_atual.usuario.gerar_codigo_identificacao()}",
            )
        except ValueError as erro:
            self.mostrar_erro(str(erro))

    def _atualizar_resumo_pedido(self) -> None:
        """@brief Sincroniza os rótulos e a lista da coluna direita com o estado do Pedido."""
        if self.pedido_atual is None:
            return

        usuario = self.pedido_atual.usuario
        self.rotulo_usuario_ativo.config(
            text=f"Usuário: {usuario.nome} ({usuario.gerar_codigo_identificacao()})"
        )
        self.rotulo_status_pedido.config(
            text=f"Status: {self.pedido_atual.status.replace('_', ' ').upper()} | "
                 f"Código: {self.pedido_atual.codigo_retirada}"
        )

        self.lista_itens_pedido.delete(0, tk.END)
        for item, qtd in self.pedido_atual.itens:
            subtotal = item.preco * qtd
            self.lista_itens_pedido.insert(
                tk.END, f"{qtd}x {item.nome} — R$ {subtotal:.2f}"
            )

        self.rotulo_valor_total.config(
            text=f"Total do Pedido: R$ {self.pedido_atual.valor_total:.2f}"
        )

    def _alternar_campos_usuario(self, habilitado: bool) -> None:
        """@brief Bloqueia ou libera os campos cadastrais durante um pedido aberto."""
        estado = "normal" if habilitado else "disabled"
        self.campo_nome.config(state=estado)
        self.campo_email.config(state=estado)
        self.campo_identificador.config(state=estado)
        self.seletor_perfil.config(state=estado)

    def reiniciar_atendimento(self) -> None:
        """@brief Limpa a tela para iniciar o atendimento de um próximo usuário."""
        self.pedido_atual = None
        self._alternar_campos_usuario(habilitado=True)

        self.campo_nome.delete(0, tk.END)
        self.campo_email.delete(0, tk.END)
        self.campo_identificador.delete(0, tk.END)
        self.campo_valor_pago.delete(0, tk.END)
        self.campo_codigo_retirada.delete(0, tk.END)
        self.campo_quantidade.delete(0, tk.END)
        self.campo_quantidade.insert(0, "1")

        self.lista_itens_pedido.delete(0, tk.END)
        self.rotulo_usuario_ativo.config(text="Usuário: Nenhum pedido iniciado")
        self.rotulo_status_pedido.config(text="Status: Aguardando itens")
        self.rotulo_valor_total.config(text="Total do Pedido: R$ 0,00")
        self.rotulo_mensagem_sistema.config(
            text="Pronto para novo atendimento.", fg="#333333"
        )
        self.campo_nome.focus()

    def mostrar_erro(self, mensagem: str) -> None:
        """@brief Traduz exceções de domínio ou validação em diálogos de erro."""
        self.rotulo_mensagem_sistema.config(text=mensagem, fg="#CC0000")
        messagebox.showerror("Atenção — Sistema RU UTFPR", mensagem)