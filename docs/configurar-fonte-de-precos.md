# Configurar atualização automática às 08h e 20h

O workflow `.github/workflows/atualizar-precos.yml` é executado pelo GitHub Actions às 11h e 23h UTC (08h e 20h, horário de Brasília). O agendamento pode atrasar. Ele também pode ser acionado manualmente em **Actions > Atualizar preços - 08h e 20h > Run workflow**.

**Atenção:** o workflow já inclui coleta gratuita pelo Google Shopping Brasil via SerpApi, desde que `SERPAPI_API_KEY` esteja em Actions secrets. A fonte opcional externa `PRICE_FEED_URL` continua suportada. Sem nenhuma fonte, o job não altera preços. O ChatGPT não envia resultados para esse endpoint.

## Configuração

1. Use a SerpApi gratuita com o segredo `SERPAPI_API_KEY` (recomendado para o piloto de três produtos) ou configure uma API adicional de preços autorizada.
2. No repositório, abra **Settings > Secrets and variables > Actions > New repository secret**.
3. Crie o segredo `PRICE_FEED_URL` com o endereço HTTPS completo do endpoint JSON.
4. Se o serviço usar autenticação Bearer, crie também `PRICE_FEED_TOKEN`.
5. Em **Settings > Actions > General > Workflow permissions**, permita escrita para o GitHub Actions quando necessário. O workflow usa `contents: write`.
6. Execute manualmente e confira os logs. Os arquivos `prices.json` e `data/history.json` só são alterados se houver dados novos válidos.

## Contrato do feed

```json
{
  "quotes": [
    {
      "id": "seed-0",
      "name": "PlayStation 5",
      "date": "2026-11-23T15:00:00-03:00",
      "price": 2800,
      "store": "Loja Exemplo",
      "source_url": "https://example.com/oferta",
      "reference": 3500,
      "reference_verified": true,
      "reference_source_url": "https://example.com/historico"
    }
  ]
}
```

Os valores acima são **fictícios e servem somente para ilustrar o formato**. Não os publique como cotações reais.

O campo `id` deve coincidir com o `products.json`. A referência só será marcada como verificada se houver `reference_verified: true` e uma URL HTTPS de referência. A validade factual das fontes deve ser garantida pelo provedor e revisada periodicamente.

## Limitações

A rotina não garante que a página da loja esteja acessível, que a oferta continue ativa ou que a fonte tenha histórico verdadeiro. Não publique tokens ou chaves de API em arquivos públicos. O site continua com cadastro local e exportação manual de catálogo; sincronização automática de produtos entre dispositivos exige backend e autenticação.
