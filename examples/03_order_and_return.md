# Order status and return policy

Recorded from the running agent with `MODEL=gpt-6-luna` and the supplied sample data. Tool calls are trace annotations, not customer-visible messages.

**Customer:** Qual o status do pedido 8?

**Tool call:** `consultar_pedidos` with `{"numero_pedido": 8}`

**Agent:**

O pedido 8 consta como enviado. O código de rastreio é **BRJL5544332BR** e a previsão de entrega registrada é **28/02/2026**. Como essas informações podem ter mudado, confirme o rastreio com a transportadora.

**Customer:** Comprei online e recebi o produto ontem. Posso devolver por arrependimento?

**Tool call:** `consultar_politicas` with `{"topico": "trocas_devolucoes"}`

**Agent:**

Sim. Como recebeu ontem, você está dentro do prazo de **7 dias corridos** para pedir a devolução por arrependimento, sem precisar justificar. O produto deve estar na embalagem original, sem sinais de uso e com todos os acessórios e manuais. O frete de devolução fica por conta da loja, e o reembolso é feito pela forma de pagamento original em até 10 dias úteis. **Política de Trocas e Devoluções, seção 4.1, página 4.**