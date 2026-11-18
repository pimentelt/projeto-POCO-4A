"""@file pedidos.py
@brief Define itens do cardápio, métodos de pagamento, pedidos do RU e o cardápio.
"""

from enum import Enum
from secrets import token_hex
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from back_end.usuarios import Usuario


class MetodoPagamento(Enum):
    """@brief Opções de pagamento previstas pelo sistema."""

    PIX = "Pix"
    CARTAO = "Cartão de Débito/Crédito"
    DINHEIRO_ESPECIE = "Dinheiro em espécie"


class ItemCardapio:
    """@brief Item independente que pode ser incluído em pedidos."""

    def __init__(self, id_item: int, nome: str, preco: float) -> None:
        if preco < 0:
            raise ValueError("O preço do item não pode ser negativo.")
        self._id_item = id_item
        self._nome = nome
        self._preco = float(preco)

    @property
    def id_item(self) -> int:
        """@brief Identificador do item."""
        return self._id_item

    @property
    def nome(self) -> str:
        """@brief Nome do item."""
        return self._nome

    @property
    def preco(self) -> float:
        """@brief Preço unitário em reais."""
        return self._preco


class Pedido:
    """@brief Representa um pedido feito por um usuário."""

    def __init__(self, id_pedido: int, usuario: "Usuario") -> None:
        self._id_pedido = id_pedido
        self._usuario = usuario
        identificacao_usuario = (
            usuario.gerar_codigo_identificacao()
            if usuario is not None
            else "AVULSO"
        )
        self._codigo_retirada = f"{identificacao_usuario}-{token_hex(2).upper()}"
        self._status = "aguardando_pagamento"
        self._itens: list[tuple[ItemCardapio, int]] = []
        self._metodo_pagamento: MetodoPagamento | None = None

        if usuario is not None:
            usuario.adicionar_pedido(self)

    @property
    def id_pedido(self) -> int:
        """@brief Identificador do pedido."""
        return self._id_pedido

    @property
    def usuario(self) -> "Usuario":
        """@brief Usuário proprietário do pedido."""
        return self._usuario

    @property
    def codigo_retirada(self) -> str:
        """@brief Código vinculado ao usuário para validação de retirada."""
        return self._codigo_retirada

    @property
    def status(self) -> str:
        """@brief Status atual do pedido."""
        return self._status

    @status.setter
    def status(self, novo_status: str) -> None:
        """@brief Atualiza o status do pedido."""
        self._status = novo_status

    @property
    def itens(self) -> list[tuple[ItemCardapio, int]]:
        """@brief Lista de itens e suas respectivas quantidades."""
        return list(self._itens)

    @property
    def metodo_pagamento(self) -> MetodoPagamento | None:
        """@brief Método de pagamento utilizado."""
        return self._metodo_pagamento

    @property
    def valor_total(self) -> float:
        """@brief Calcula o total com base nos itens e quantidades."""
        return round(sum(item.preco * qtd for item, qtd in self._itens), 2)

    def adicionar_item(self, item: ItemCardapio, quantidade: int = 1) -> None:
        """@brief Adiciona um item do cardápio ao pedido."""
        if self._status != "aguardando_pagamento":
            raise ValueError("Este pedido já foi finalizado. Inicie um novo atendimento.")
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")
        self._itens.append((item, quantidade))

    def registrar_pagamento(self, metodo: MetodoPagamento) -> None:
        """@brief Registra o método escolhido e atualiza o status."""
        self._metodo_pagamento = metodo
        self._status = "aguardando_retirada"


class Cardapio:
    """@brief Gerenciador central com todos os itens presentes no cardápio."""

    def __init__(self) -> None:
        self._itens_disponiveis: list[ItemCardapio] = []

    def adicionar_item(self, item: ItemCardapio) -> None:
        """@brief Adiciona um novo item ao cardápio oficial."""
        self._itens_disponiveis.append(item)

    @property
    def itens(self) -> list[ItemCardapio]:
        """@brief Retorna uma cópia da lista de itens do cardápio."""
        return list(self._itens_disponiveis)

    def buscar_por_id(self, id_item: int) -> ItemCardapio | None:
        """@brief Procura um item no cardápio pelo seu ID."""
        for item in self._itens_disponiveis:
            if item.id_item == id_item:
                return item
        return None


def criar_cardapio_padrao() -> Cardapio:
    """@brief Monta e devolve um objeto Cardapio com os itens padrão do RU."""
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