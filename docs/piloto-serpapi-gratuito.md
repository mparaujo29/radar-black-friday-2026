# Piloto gratuito: SerpApi + Google Shopping Brasil

O piloto de coleta via SerpApi/Google Shopping Brasil foi executado em 23/11/2026. Ele só volta a consultar preços enquanto a chave de API estiver configurada e houver créditos disponíveis. A chave nunca deve ser colocada em arquivos públicos. Nunca forneça a chave no chat ou em arquivos públicos.

## Ative em 5 passos

1. Crie uma conta gratuita em https://serpapi.com/users/sign_up e verifique o limite vigente em https://serpapi.com/pricing .
2. No painel SerpApi, localize sua **API Key**. Não a copie para o código nem a compartilhe.
3. Abra **GitHub > repositório radar-black-friday-2026 > Settings > Secrets and variables > Actions > New repository secret**.
4. Em **Name**, informe `SERPAPI_API_KEY`; em **Secret**, cole a chave pessoal e clique em **Add secret**.
5. No repositório GitHub, entre em **Actions > Atualizar preços - 08h e 20h > Run workflow** para testar. Depois confira os logs e o arquivo `prices.json`.

Também verifique em **Settings > Actions > General > Workflow permissions** se o workflow pode usar permissão de escrita (`contents: write`). O GitHub Pages pode demorar alguns minutos para publicar a alteração.

## O que será consultado no piloto

| Produto monitorado | Modelo considerado | ID |
|---|---|---|
| Samsung Galaxy S26 Ultra | 256 GB | seed-1 |
| iPhone 17 | 256 GB | seed-5 |
| Purificador Electrolux PE12G | PE12G | seed-8 |

Os modelos de 256 GB são uma escolha inicial técnica, não uma preferência confirmada do usuário. Pode alterar a consulta em `monitoring.json`. Os outros sete produtos continuam no catálogo, mas não serão consultados automaticamente neste piloto.

## Franquia e frequência

O plano gratuito anunciado pela SerpApi é de **250 consultas/mês**. Para manter uma margem, o programa interrompe pesquisas quando o uso mensal da conta chega a **220** (ou quando os créditos acabarem). Cada execução agendada pode gastar até **3 consultas**, uma por produto. A coleta agora ocorre **às 08h e 20h (Brasília)**: são 2 execuções/dia × 3 produtos = **6 consultas/dia**, ou **180 consultas em 30 dias** (186 em 31 dias). Essa frequência cabe no plano gratuito, desde que a conta não consuma consultas adicionais em outros processos. A frequência anterior de 3 em 3 horas precisaria de aproximadamente 720 consultas/mês e não caberia no plano. Dez produtos a 2 vezes/dia exigiriam aproximadamente 600 consultas/mês. Os agendamentos GitHub Actions podem atrasar. Os agendamentos GitHub Actions podem atrasar.

## Dados e verificação

A primeira execução encontrou um valor de R$ 116,30 atribuído ao Electrolux PE12G; como não foi possível validar que se tratava do equipamento completo, ele foi colocado em `data/quarantine.json`, retirado das cotações exibidas e sujeito a filtros conservadores de modelo e valor. Esse limiar é **triagem de qualidade**, não um preço de referência nem prova de desconto. O coletor consulta **Google Shopping Brasil** usando a API SerpApi. Ele só aceita resultados com correspondência de modelo, preço em reais, loja identificada e URL HTTPS. Registra a melhor correspondência encontrada entre as ofertas fornecidas, não necessariamente o menor preço da internet. O sistema registra preços observados; **não inventa uma referência de desconto**. Um desconto ≥15% só será validado se houver fonte histórica confiável adicionada separadamente. O valor exibido pode mudar na loja ou não incluir frete.

A API nunca garante estoque, preço final no checkout ou cobertura de todas as lojas. Consulte o link original antes de comprar.

## Adicionar mais itens à coleta

1. Cadastre o produto em `products.json`, com ID único.
2. Adicione uma entrada em `monitoring.json`, contendo esse ID, `query`, `must`, `exclude` e, quando preciso, `storage_gb`.
3. Não adicione todos os produtos sem rever a franquia mensal da SerpApi.
4. O site inclui um formulário de cadastro local e exportação JSON, mas **ainda não sincroniza automaticamente novos itens com o GitHub**.

## Custos e segurança

Sem `SERPAPI_API_KEY`, não há consultas. Com a chave configurada, o código consulta primeiro a API gratuita de conta (sem consumo de franquia) e aplica limite mensal de 220 buscas. Se não puder verificar a quota, não pesquisa. O GitHub Actions pode ser usado em repositório público; custos e limites dependem do plano da conta GitHub. Não armazene segredos em repositórios públicos.
