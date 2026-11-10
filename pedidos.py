"""@file pedidos.py
@brief Define itens do cardápio, métodos de pagamento e pedidos do RU.
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
    CARTAO = "Cartão"
    CARTEIRA_DIGITAL = "Carteira digital"
    DINHEIRO_ESPECIE = "Dinheiro em espécie"


@dataclass(frozen=True)
class ItemCardapio:
    """@brief Item independente que pode ser incluído em pedidos.

    @param id_item Identificador único do item no cardápio.
    @param nome Nome apresentado ao usuário.
    @param preco Preço unitário em reais.
    @throws ValueError Se o preço for negativo.
    """

    id_item: int
    nome: str
    preco: float

    def __post_init__(self) -> None:
        """@brief Valida os dados do item após sua criação."""
        if self.preco < 0:
            raise ValueError("O preço não pode ser negativo.")


class Pedido:
    """@brief Representa um pedido feito por um usuário.

    @details Agrega referências a itens do cardápio e calcula o valor total.
    O código de retirada é gerado automaticamente na criação.
    @param id_pedido Identificador do pedido.
    @param usuario Usuário associado ao pedido; pode ser omitido.
    """

    def __init__(self, id_pedido: int, usuario: Usuario | None = None) -> None:
        self.id_pedido = id_pedido
        self.usuario = usuario
        self.codigo_retirada = token_hex(3).upper()
        self.status = "aguardando_pagamento"
        self.itens: list[tuple[ItemCardapio, int]] = []
        self.metodo_pagamento: MetodoPagamento | None = None
        if usuario is not None:
            usuario.pedidos.append(self)

    @property
    def valor_total(self) -> float:
        """@brief Calcula o total com base nos itens e suas quantidades.
        @return Valor total do pedido em reais.
        """
        return sum(item.preco * quantidade for item, quantidade in self.itens)

    def adicionar_item(self, item: ItemCardapio, quantidade: int = 1) -> None:
        """@brief Adiciona um item do cardápio ao pedido.

        @param item Item que será agregado ao pedido.
        @param quantidade Número de unidades; o padrão é 1.
        @throws ValueError Se a quantidade não for maior que zero.
        """
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")
        self.itens.append((item, quantidade))

    def registrar_pagamento(self, metodo: MetodoPagamento) -> None:
        """@brief Registra o método escolhido e atualiza o status do pedido.

        @param metodo Meio de pagamento utilizado.
        @note Este método apenas registra a escolha; não realiza cobrança real.
        """
        self.metodo_pagamento = metodo
        self.status = "aguardando_retirada"
