# Operação final da Black Friday 2026 — 10 itens

## Janela de funcionamento
- Data-limite: **sexta-feira, 27/11/2026**, horário de Brasília.
- Rodadas principais às **08h17 e 20h17**, reservas às **08h47 e 20h47**.
- A reserva pula a coleta se uma rodada anterior tiver concluído na última hora.
- O passo `scripts/should_run.py` **bloqueia todas as consultas da SerpApi após 27/11/2026**, inclusive execuções manuais depois do encerramento.
- Após a reserva noturna de 27/11 (a partir de 20h47), o próprio workflow tenta se **desativar no GitHub**, usando `actions: write`. Se não conseguir, a trava de data continua protegendo os créditos. GitHub Actions não garante pontualidade.
- A tarefa do ChatGPT é separada deste workflow, e não alimenta diretamente os gráficos.

## Os 10 produtos e as variantes adotadas
O arquivo `monitoring.json` contém 10 entradas habilitadas. Algumas variantes foram **definidas provisoriamente** porque o usuário não havia especificado todos os detalhes:

| ID | Produto | Variante pesquisada |
|---|---|---|
| seed-0 | PlayStation 5 | Slim com leitor de discos, 1 TB, provisória |
| seed-1 | Galaxy S26 Ultra | 256 GB |
| seed-2 | Tab S10 FE (anteriormente escrito "Tab 10 SE") | Wi-Fi, 128 GB, provisória |
| seed-3 | Tab S10 FE+ (anteriormente escrito "Tab 10 SE Plus") | Wi-Fi, 128 GB, provisória |
| seed-4 | Tab S10 Lite (anteriormente escrito "Tab 10 Lite 8 GB") | 8 GB RAM + 256 GB armazenamento, Wi-Fi, provisória |
| seed-5 | iPhone 17 | 256 GB |
| seed-6 | iPhone 17 Pro Max | 256 GB, provisória |
| seed-7 | Galaxy Z Fold8 | 256 GB, provisória |
| seed-8 | Purificador Electrolux PE12G | Unidade completa |
| seed-9 | LG Dual Inverter Frio 12.000 BTUs 220 V | S3-Q12JA31L, provisória |

Referências de nomenclatura:
- Samsung Galaxy Tab S10 FE/FE+: https://www.samsung.com/br/tablets/galaxy-tab-s/galaxy-tab-s10-fe/
- Galaxy Tab S10 Lite 8GB/256GB: https://www.samsung.com/br/tablets/galaxy-tab-s/galaxy-tab-s10-lite-gray-256gb-sm-x400nzahzto/
- LG S3-Q12JA31L: https://www.lg.com/br/ar-condicionado-residencial/dual-inverter-split/s3-q12ja31l/
- Galaxy Z Fold8 256GB: https://news.samsung.com/br/samsung-apresenta-os-novos-galaxy-z-fold8-galaxy-z-fold8-ultra-e-galaxy-z-flip8-no-brasil

## Limites de crédito
10 pesquisas/rodada × 2 rodadas/dia = **20/dia**; de 25 a 27/11, **60 pesquisas** planejadas, mais buscas extras se rodadas ou testes forem executados manualmente.
O script consulta a SerpApi para saber a franquia restante e limita o consumo total mensal a **220 consultas**, deixando margem frente ao plano de 250. Se houver menos créditos, pode pesquisar apenas parte do catálogo, e os demais ficam sem cotação.

## Qualidade e descontos
- Cada pesquisa busca Google Shopping Brasil. Preços que não correspondam à variante, ou que aparentem acessórios/usados, são ignorados.
- `min_price` é somente barreira conservadora contra anúncios de acessórios, **não referência histórica de preço**.
- A coleta não garante que todas as 10 pesquisas encontrem anúncios válidos. Muitos resultados de anúncios não incluem memória, modelo exato ou URL adequada.
- **Nenhum desconto de 15% é confirmado apenas por preço riscado**. O sistema ainda não dispõe de fonte histórica independente para validar esse percentual automaticamente.
- Preços anunciados não incluem necessariamente frete nem representam disponibilidade confirmada no checkout.

## Verificar
1. Abra https://github.com/mparaujo29/radar-black-friday-2026/actions
2. Selecione `Black Friday 10 produtos - até 27-11`.
3. Após a execução, confira `status.json` e `prices.json` na branch main.
4. Abra https://mparaujo29.github.io/radar-black-friday-2026/ e clique em **Atualizar dados**.
5. Para evitar gastar créditos, **não acione Run workflow sem necessidade**.
