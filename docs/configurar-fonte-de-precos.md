# Configurar atualização automática a cada 3 horas

O workflow `.github/workflows/atualizar-precos.yml` é executado pelo GitHub Actions em intervalos aproximados de três horas (UTC). O agendamento pode atrasar. Ele também pode ser acionado manualmente em **Actions > Atualizar preços - a cada 3 horas > Run workflow**.

**Atenção:** o workflow não pesquisa a internet nem extrai preços de lojas por conta própria. Ele importa dados de um endpoint HTTPS autorizado que retorne JSON. Sem `PRICE_FEED_URL`, o job termina sem alterar os preços. O ChatGPT não envia resultados para esse endpoint.

## Configuração

1. Contrate ou configure uma API/serviço autorizado que disponibilize cotações para os produtos cadastrados.
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
