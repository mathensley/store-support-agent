# Combined pricing, delivery, and installment rules

Recorded from the running agent with `MODEL=gpt-6-luna` and the supplied store data. Tool calls are trace annotations, not customer-visible messages.

**Customer:** O ukulele Ohana CK-20 Concert está disponível? Qual é o preço promocional? Pagando no PIX, consigo acumular mais 5%?

**Tool call:** `buscar_produtos` with `{"busca": "Ohana CK-20 Concert", "categoria": "ukulele", "limite": 10, "preco_max_brl": null, "somente_disponiveis": false}`

**Tool call:** `consultar_politicas` with `{"topico": "pagamento"}`

**Tool call:** `consultar_politicas` with `{"topico": "promocoes"}`

**Agent:**

Sim! O Ohana CK-20 Concert Natural está disponível, com 6 unidades em estoque. O preço promocional é **R$ 439,20** (20% de desconto sobre o preço original de **R$ 549,00**).

O desconto de 5% no PIX **não acumula** com o preço promocional. (Formas de Pagamento, p. 3; Promoções e Descontos, p. 6.)

**Customer:** Se eu levar duas unidades para entrega em Campo Grande, quanto fica e o frete é grátis?

**Tool call:** `buscar_produtos` with `{"busca": "Ohana CK-20 Concert", "categoria": "ukulele", "limite": 10, "preco_max_brl": null, "somente_disponiveis": true}`

**Tool call:** `consultar_politicas` with `{"topico": "frete_entregas"}`

**Agent:**

Duas unidades ficam em **R$ 878,40** no preço promocional. Se o endereço estiver na região metropolitana de Campo Grande, o frete é **grátis** para pedidos acima de R$ 500; o total fica **R$ 878,40**. (Política de Frete e Entregas, pp. 4–5.)

**Customer:** E posso parcelar esse total em 6x sem juros?

**Tool call:** `consultar_politicas` with `{"topico": "pagamento"}`

**Agent:**

Sim! Os **R$ 878,40** podem ser parcelados em **6x de R$ 146,40 sem juros**. A parcela mínima para compras em 4 a 6 vezes é R$ 80. (Formas de Pagamento, p. 3.)