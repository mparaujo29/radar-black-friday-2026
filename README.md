# Radar Black Friday 2026

Site estático para hospedar em GitHub Pages, Netlify ou Cloudflare Pages.

## Publicação
Envie `index.html` e `prices.json` para um repositório GitHub e ative GitHub Pages nas configurações (Deploy from branch, raiz). O GitHub fornecerá um endereço público. Também é possível arrastar a pasta para o Netlify Drop.

## Atualização automática
O site consulta `prices.json` ao abrir e quando o usuário clica em **Atualizar dados**. A coleta de preços por SerpApi/Google Shopping Brasil está programada para **08h e 20h, horário de Brasília**. O plano gratuito inclui 250 pesquisas/mês; o piloto monitora três produtos e usa um limite preventivo de 220 buscas/mês. Ela depende de `SERPAPI_API_KEY` em GitHub Actions secrets e registra somente cotações compatíveis com os filtros do coletor. A tarefa de alertas do ChatGPT **não escreve** nesse arquivo.

Formato de exemplo para `prices.json` (dados ilustrativos, não inserir como preços reais):
```json
{"quotes":[{"id":"seed-0","name":"PlayStation 5","date":"2026-11-23T15:00:00-03:00","price":2800,"reference":3500,"store":"Loja Exemplo","source_url":"https://example.com/produto"}]}
```

Somente registrar `reference` quando houver fonte histórica confiável. A rotina externa deve validar variante, preço, disponibilidade e origem. A hospedagem estática não oferece sincronização dos produtos adicionados em aparelhos diferentes: eles ficam no localStorage do navegador. Para cadastro compartilhado e atualização automática integral, usar banco de dados/autenticação e API de preços.

## Acompanhamento da coleta

Veja a rotina em `.github/workflows/atualizar-precos.yml` e o consumo de API nos logs de GitHub Actions. A coleta pode atrasar por agendamento. Os três produtos do piloto estão em `monitoring.json`; os dez produtos continuam em `products.json`. O site consulta o arquivo de cotações no GitHub e pode precisar de atualização da página.

Cotações suspeitas são preservadas em `data/quarantine.json` e excluídas do histórico exibido. Isso não cria uma referência de desconto de 15%; histórico independente e conferência da variante continuam necessários. O ChatGPT mantém sua tarefa de alertas separadamente.
