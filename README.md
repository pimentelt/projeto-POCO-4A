# Sistema Digital do Restaurante Universitário

Projeto acadêmico em Python para modelar um sistema de pedidos e retirada no Restaurante Universitário (RU). A proposta é reduzir filas e o uso de fichas impressas com pedidos digitais, pagamentos e validação por código na retirada.

> **Protótipo acadêmico:** este projeto demonstra conceitos de Programação Orientada a Objetos. Não se conecta a banco de dados, aplicativo, PIX ou operadoras de cartão; pagamentos e pedidos não são reais.

## Proposta

O sistema prevê cadastro de alunos por RA, servidores por ID e público externo por código. O usuário poderá montar um pedido com itens do cardápio, pagar antecipadamente por PIX, cartão ou carteira digital, e apresentar um código digital para retirar a refeição. O pagamento em dinheiro permanece presencial, no caixa.

## Divisão das classes

1. **Usuários e carteira digital** — `Usuario` é a classe abstrata. `Aluno`, `Servidor` e `Externo` herdam dela; cada usuário possui uma `CarteiraDigital`. (Na sprint 2 retiramos a 'CarteiraDigital' pois seria muito burocrático para o Restaurante Universitário )
2. **Pedido, itens do cardápio e Cardápio** — `Pedido` reúne itens existentes do cardápio e calcula o total. O código de retirada é gerado ao criar o pedido.
3. **Caixa e pagamento** — `CaixaRU` recebe pagamento em espécie, confere o código de retirada e confirma a entrega. `MetodoPagamento` enumera as opções previstas.

## Conceitos de POO

- **Herança e abstração:** `Aluno`, `Servidor` e `Externo` especializam `Usuario`, que define um contrato abstrato para gerar identificação.
- **Composição:** cada instância de `Usuario` cria e mantém sua `CarteiraDigital`. (Na sprint 2 retiramos a 'CarteiraDigital' pois seria muito burocrático para o Restaurante Universitário )
- **Agregação:** `Pedido` guarda referências a `ItemCardapio`; os itens também podem existir fora dos pedidos.
- **Associação:** um `Usuario` pode estar associado a vários `Pedido`; cada pedido também mantém referência ao usuário que o criou.
- **Dependência:** `CaixaRU` usa `Pedido` e `MetodoPagamento` para registrar pagamento em espécie e validar a retirada.

## Estrutura

```text
projeto-poo/
├── README.md
├── Doxyfile      # configuração para gerar a documentação
├── main.py       # demonstração de uso
├── usuarios.py   # Usuario, subclasses e CarteiraDigital
├── pedidos.py    # Pedido, ItemCardapio e MetodoPagamento
└── caixa.py      # pagamento em espécie e retirada
```

## Como executar

Requer Python 3.10 ou superior. No terminal, dentro da pasta do projeto:

```bash
python main.py
```

O exemplo cria um aluno, monta um pedido, simula o pagamento em dinheiro e confirma a retirada usando o código gerado.

## Documentação do código

As classes e métodos usam comentários no estilo Doxygen, com tags como `@brief`, `@details`, `@param`, `@return`, `@throws` e `@note`. Com o [Doxygen](https://www.doxygen.nl/) instalado, gere a documentação HTML na pasta `docs/html`:

```bash
doxygen Doxyfile
```

## Próximos passos

- Implementar o pagamento simulado por carteira digital, PIX e cartão.
- Adicionar persistência de dados e interface para o usuário.
- Tratar valores monetários com `Decimal` e definir regras de negócio em conjunto com o grupo.
