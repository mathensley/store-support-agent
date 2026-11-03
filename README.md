# Agente de atendimento — Empório da Música

Projeto em Python para o desafio de atendimento por mensagens de texto.

## Ambiente

Requer Python 3.12 e [`uv`](https://docs.astral.sh/uv/).

```powershell
uv sync
```

A chave da API OpenAI deve ser fornecida por `OPENAI_API_KEY` no ambiente quando o agente for executado, exemplo em `.env.example`.

## Decisões inciais de arquitetura

- Um agente LangChain via CLI com ferramentas específicas para consultar os dados. O estado da conversa é salvo com `InMemorySaver`. Isso preserva o contexto em tempo de execução, porém as informações serão perdidas ao reiniciar ou perder a sessão.
- Uma limitação está no fato dos dados serem estáticos então o agente poderá responder bem para esse cenário, mas numa situação com uma base de dados cada vez maior e sempre atualizando é outro contexto que requeriria soluções diferentes. Nesse caso, os CSVs são pequenos, então inicialmente não vejo necessidade de algo mais complexo como um Text2SQL, mas terá de ser validado posteriormente com testes.
- As políticas estão em um PDF de oito páginas. `pypdf` é suficiente para carregar e buscar seções ou páginas relevantes, preservando a origem da resposta. Da mesma forma que os CSVs, para esse caso, talvez embeddings e banco vetorial para RAG talvez não seja necessário, mas preciso validar após uma demo inicial pequena.
- Considerar, dependendo do desenvolver, containerizar tudo em um Docker. Facilita a execução e reprodutibilidade também.