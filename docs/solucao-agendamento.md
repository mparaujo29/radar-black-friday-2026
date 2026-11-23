# Diagnóstico e recuperação do monitoramento

O agendamento anterior às 08:00 e 20:00 usava o minuto zero de cada hora. A documentação oficial do GitHub informa que os disparos nesse minuto podem sofrer atrasos ou até ser descartados: https://docs.github.com/en/actions/how-tos/troubleshoot-workflows

## Novo agendamento
- Tentativa principal às **08:17 e 20:17**, horário de Brasília (UTC-3).
- Tentativa reserva às **08:47 e 20:47**.
- Se a tentativa principal tiver concluído com sucesso na última hora, a reserva termina sem consumir pesquisas SerpApi.
- Existe ainda **Actions > Atualizar preços - manhã e noite (com reserva) > Run workflow** para acionamento manual a qualquer momento.
- O GitHub não garante pontualidade: mesmo com a reserva, as execuções podem atrasar ou, raramente, não iniciar.

## Como interpretar o painel
O arquivo `status.json` exibe o horário de conclusão da rotina, **independentemente de ter encontrado uma oferta nova**.
O arquivo `prices.json` contém somente as cotações que passaram pelos filtros. Se não houver cotação segura, preços podem continuar antigos mesmo após uma execução bem-sucedida.

O painel lê ambos diretamente da branch `main`, via GitHub Raw. Ao abrir a página ou clicar em **Atualizar dados**, atualiza a consulta. Sua franquia de SerpApi não é consumida pela abertura do site.

## Se falhar
1. Abra https://github.com/mparaujo29/radar-black-friday-2026/actions .
2. Selecione **Atualizar preços - manhã e noite (com reserva)**.
3. Confira se existe execução no horário. Se não houver, GitHub não disparou o evento.
4. Se houver execução vermelha, clique nela para ver qual etapa falhou; nunca compartilhe sua API Key.
5. Para testar uma vez agora, clique **Run workflow** e aguarde a conclusão; depois verifique `status.json` e o painel.

## Proteção da franquia
Continuam **três produtos monitorados**, com até **6 pesquisas por dia** (180 em 30 dias), sujeitas ao limite preventivo de **220/mês**. A tentativa reserva não busca novamente se já houve execução concluída recentemente. O limite de 250 consultas é estabelecido pela franquia gratuita da SerpApi e pode variar conforme o plano.
