"""file main.py
brief Ponto de entrada da demonstração do sistema do RU.
"""

from caixa import CaixaRU
from pedidos import ItemCardapio, Pedido, Cardapio
from usuarios import Aluno, Servidor, Externo


def main() -> None:
    """@brief Executa um exemplo de pedido, pagamento e retirada.
    @details Cria dados temporários e imprime o resultado no terminal.
    """
    "cardapio é uma calsse que agrupa os itens"
    cardapio_ru = Cardapio() 

    cardapio_ru.adicionar_item(ItemCardapio(1, "Prato do Dia", 12.50))
    cardapio_ru.adicionar_item(ItemCardapio(2, "Agua s/gas", 3.00))
    cardapio_ru.adicionar_item(ItemCardapio(3, "Agua c/gas", 3.50))
    cardapio_ru.adicionar_item(ItemCardapio(4, "Salgados assados", 6.50))
    cardapio_ru.adicionar_item(ItemCardapio(5, "Salgados Fritos", 5.00))
    cardapio_ru.adicionar_item(ItemCardapio(6, "Bolo Gelado", 10.00))
    cardapio_ru.adicionar_item(ItemCardapio(7, "Suco Natural de Laranja (300ml)", 3.50))
    cardapio_ru.adicionar_item(ItemCardapio(8, "Suco Natural de Uva (300ml)", 3.00))
    cardapio_ru.adicionar_item(ItemCardapio(9, "Refrigerante Lata(coca, fanta e guaraná)", 5.00))
    cardapio_ru.adicionar_item(ItemCardapio(10, "Bombom", 3.00))

    print("Exemplo Aluno fazendo pedido\n")
    usuario = Aluno("Ana", "ana@exemplo.com", "1234567")
    pedido = Pedido(1, usuario)
    pedido.adicionar_item(cardapio_ru.buscar_por_id(1), quantidade=1)
    pedido.adicionar_item(cardapio_ru.buscar_por_id(7), quantidade=1)

    caixa = CaixaRU()
    troco = caixa.receber_pagamento_especie(pedido, valor=20.00)
    print(f"Usuário: {usuario.gerar_codigo_identificacao()}")
    print(f"Total: R$ {pedido.valor_total:.2f} | Troco: R$ {troco:.2f}")
    print(f"Código de retirada: {pedido.codigo_retirada}")
    
    caixa.confirmar_retirada(pedido, pedido.codigo_retirada)
    print(f"Status do pedido: {pedido.status}")


    print("Exemplo Servidor fazendo pedido\n")
    usuario = Servidor("Luiz", "Luiz@exemplo.com", "1234567")
    pedido = Pedido(2, usuario)
    pedido.adicionar_item(cardapio_ru.buscar_por_id(4), quantidade=2)
    pedido.adicionar_item(cardapio_ru.buscar_por_id(3), quantidade=1)

    caixa = CaixaRU()
    troco = caixa.receber_pagamento_especie(pedido, valor=20.00)
    print(f"Usuário: {usuario.gerar_codigo_identificacao()}")
    print(f"Total: R$ {pedido.valor_total:.2f} | Troco: R$ {troco:.2f}")
    print(f"Código de retirada: {pedido.codigo_retirada}")
        
    caixa.confirmar_retirada(pedido, pedido.codigo_retirada)
    print(f"Status do pedido: {pedido.status}")

    print("Exemplo Externo fazendo pedido\n")
    usuario = Externo("Jose", "jose@exemplo.com", "1234567")
    pedido = Pedido(3, usuario)
    pedido.adicionar_item(cardapio_ru.buscar_por_id(1), quantidade=1)
    pedido.adicionar_item(cardapio_ru.buscar_por_id(6), quantidade=1)
    
    caixa = CaixaRU()
    troco = caixa.receber_pagamento_especie(pedido, valor=30.00)
    print(f"Usuário: {usuario.gerar_codigo_identificacao()}")
    print(f"Total: R$ {pedido.valor_total:.2f} | Troco: R$ {troco:.2f}")
    print(f"Código de retirada: {pedido.codigo_retirada}")
        
    caixa.confirmar_retirada(pedido, pedido.codigo_retirada)
    print(f"Status do pedido: {pedido.status}")


if __name__ == "__main__":
    main()
