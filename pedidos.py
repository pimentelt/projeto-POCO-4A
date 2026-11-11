"""file pedidos.py
brief Define itens do cardápio, métodos de pagamento, pedidos do RU e um cardápio centralizado.
"""

from dataclasses import dataclass
from enum import Enum
from secrets import token_hex
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from usuarios import Usuario


class MetodoPagamento(Enum):
    """@brief Opções de pagamento previstas pelo sistema.
    @details A enumeração descreve meios disponíveis; não integra serviços financeiros.
    """

    PIX = "Pix"
    CARTAO = "Cartão de Débito/Crédito"
    DINHEIRO_ESPECIE = "Dinheiro em espécie"


class ItemCardapio:
    """brief Item independente que pode ser incluído em pedidos.

    param id_item Identificador único do item no cardápio.
    param nome Nome apresentado ao usuário.
    param preco Preço unitário em reais.
    """

    
    def __init__(self, id_item: int, nome: str, preco: float) -> None:
        if preco < 0:
            raise ValueError("O preço do item não pode ser negativo.")
        self._id_item = id_item
        self._nome = nome
        self._preco = float(preco)

    @property
    def id_item(self) -> int:
        "brief Identificador do item"
        return self._id_item

    @property
    def nome(self) -> str:
        "brief Nome do item"
        return self._nome

    @property
    def preco(self) -> float:
        "brief Preço unitário em reais"
        return self._preco


class Pedido:
    "brief Representa um pedido feito por um usuário"
   
    

    def __init__(self, id_pedido: int, usuario: "Usuario")-> None:
        self._id_pedido = id_pedido
        self._usuario = usuario
        self._codigo_retirada = token_hex(3).upper()
        self._status = "aguardando_pagamento"
        self._itens: list[tuple[ItemCardapio, int]] = []
        self._metodo_pagamento: MetodoPagamento | None = None
        
        if usuario is not None:
            usuario.adicionar_pedido(self)

    @property
    def id_pedido(self) -> int:
        "brief Identificador do pedido"
        return self._id_pedido

    @property
    def usuario(self) -> "Usuario":
        "brief Usuário proprietário do pedido"
        return self._usuario

    @property
    def codigo_retirada(self) -> str:
        "brief Código gerado para validação de retirada"
        return self._codigo_retirada

    @property
    def status(self) -> str:
        """@brief Status atual do pedido."""
        return self._status

    @status.setter
    def status(self, novo_status: str) -> None:
        "brief Atualiza o status do pedido"
        self._status = novo_status

    @property
    def itens(self) -> list[tuple[ItemCardapio, int]]:
        "brief Lista de itens e suas respectivas quantidades."
        return list(self._itens)

    @property
    def metodo_pagamento(self) -> MetodoPagamento | None:
        "brief Método de pagamento utilizado"
        return self._metodo_pagamento

    @property
    def valor_total(self) -> float:
        """brief Calcula o total com base nos itens e quantidades.
        return Valor total do pedido em reais.
        """
        return round(sum(item.preco * qty for item, qty in self._itens), 2)

    def adicionar_item(self, item: ItemCardapio, quantidade: int = 1) -> None:
        """brief Adiciona um item do cardápio ao pedido.

        param item Instância de ItemCardapio.
        param quantidade Quantidade a adicionar.
        throws ValueError Se quantidade <= 0.
        """
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")
        self._itens.append((item, quantidade))

    def registrar_pagamento(self, metodo: MetodoPagamento) -> None:
        """brief Registra o método escolhido e atualiza o status.
           param metodo Meio de pagamento utilizado.
        """
        self._metodo_pagamento = metodo
        self._status = "aguardando_retirada"

class Cardapio:
    "um gerenciador central com todos os itens presentes no cardápio"
    "para não ser necessário adicionar manualmente o codigo, o nome e o preço individualmente"

    def __init__(self) -> None:
        "Cria uma lista interna para guardar os itens disponíveis"
        self._itens_disponiveis: list[ItemCardapio] = []

    def adicionar_item(self, item: ItemCardapio) -> None:
        "brief Adiciona um novo item ao cardápio oficial."
        self._itens_disponiveis.adicionarItem(item)

    @property
    def itens(self) -> list[ItemCardapio]:
        "brief Retorna uma cópia da lista de itens do cardápio."
        return list(self._itens_disponiveis)

    def buscar_por_id(self, id_item: int) -> ItemCardapio | None:
        "brief Procura um item no cardápio pelo seu ID"
        for item in self._itens_disponiveis:
            if item.id_item == id_item:
                return item
        return None  # Retorna None se não encontrar

    """ essa parte será incluída na interface gráfica posteriormente desenvolvida
    def listar_cardapio(self) -> None:
        print("--- CARDÁPIO DO RU ---")
        for item in self._itens_disponiveis:
            print(f"[{item.id_item}] {item.nome} - R$ {item.preco:.2f}")
            """