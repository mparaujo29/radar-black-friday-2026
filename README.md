# Radar Black Friday 2026

Site estático para hospedar em GitHub Pages, Netlify ou Cloudflare Pages.

## Publicação
Envie `index.html` e `prices.json` para um repositório GitHub e ative GitHub Pages nas configurações (Deploy from branch, raiz). O GitHub fornecerá um endereço público. Também é possível arrastar a pasta para o Netlify Drop.

## Atualização automática
O site consulta `prices.json` ao abrir e quando o usuário clica em **Atualizar dados**. Para executar a coleta a cada 3 horas, é necessário criar um serviço externo autorizado que consulte APIs ou feeds de preços das lojas e publique novas cotações em `prices.json`. A tarefa de alertas do ChatGPT **não escreve** nesse arquivo.

Formato de exemplo para `prices.json` (dados ilustrativos, não inserir como preços reais):
```json
{"quotes":[{"id":"seed-0","name":"PlayStation 5","date":"2026-11-23T15:00:00-03:00","price":2800,"reference":3500,"store":"Loja Exemplo","source_url":"https://example.com/produto"}]}
```

Somente registrar `reference` quando houver fonte histórica confiável. A rotina externa deve validar variante, preço, disponibilidade e origem. A hospedagem estática não oferece sincronização dos produtos adicionados em aparelhos diferentes: eles ficam no localStorage do navegador. Para cadastro compartilhado e atualização automática integral, usar banco de dados/autenticação e API de preços.
