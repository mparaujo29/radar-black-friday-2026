# Coleta automática e preços verificáveis

A tarefa ChatGPT não alimenta o site. O site consulta `prices.json`. A coleta está implementada com SerpApi/Google Shopping Brasil no GitHub Actions, **às 08h e 20h (horário de Brasília)**, para três produtos em `monitoring.json`. A chave `SERPAPI_API_KEY` deve ser mantida em GitHub Actions secrets. A conta gratuita tem 250 pesquisas/mês e o coletor aplica um limite preventivo de 220. A rotina só grava cotações quando possui dados compatíveis com os filtros. Para cada cotação, use `id`, `name`, `date`, `price`, `store`, `source_url`; para marcar desconto verificado, inclua `reference`, `reference_verified: true` e `reference_source_url` com fonte verificável. Referências sem fonte não produzem alerta de desconto no painel.

Para adicionar produtos de qualquer aparelho sem backend: clique em **Exportar catálogo JSON**, depois substitua `products.json` no GitHub e faça commit. A alteração estará disponível aos demais aparelhos após o deploy, com a ressalva de que a fusão preserva itens já cadastrados localmente. Cadastro e edição em tempo real entre aparelhos exigem autenticação e banco de dados.

O site recarrega o feed quando é aberto, via botão, e automaticamente a cada 12 horas enquanto a aba está aberta. Isso NÃO é coleta automática. Não publicar tokens de acesso no repositório.
