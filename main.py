"""@file main.py
@brief Ponto de entrada da demonstração do sistema do RU.
"""

from caixa import CaixaRU
from pedidos import ItemCardapio, Pedido
from usuarios import Aluno


def main() -> None:
    """@brief Executa um exemplo de pedido, pagamento e retirada.
    @details Cria dados temporários e imprime o resultado no terminal.
    """
    usuario = Aluno("Ana", "ana@example.com", "123456")
    prato = ItemCardapio(1, "Refeição do dia", 12.50)
    suco = ItemCardapio(2, "Suco", 3.50)

    pedido = Pedido(1, usuario)
    pedido.adicionar_item(prato)
    pedido.adicionar_item(suco, quantidade=2)

    caixa = CaixaRU()
    troco = caixa.receber_pagamento_especie(pedido, valor=20.00)
    print(f"Usuário: {usuario.gerar_codigo_identificacao()}")
    print(f"Total: R$ {pedido.valor_total:.2f} | Troco: R$ {troco:.2f}")
    print(f"Código de retirada: {pedido.codigo_retirada}")
    caixa.confirmar_retirada(pedido, pedido.codigo_retirada)
    print(f"Status do pedido: {pedido.status}")


if __name__ == "__main__":
    main()
