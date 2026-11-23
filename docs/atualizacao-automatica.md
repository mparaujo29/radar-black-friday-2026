# Próxima etapa: coleta e preços verificáveis

A tarefa ChatGPT não alimenta o site. O site consulta `prices.json`. Para automatizar a coleta a cada 3 horas, será necessário conectar API ou feed autorizado de varejista/comparador e implementar um workflow que atualize o arquivo sem gerar preços fictícios. Para cada cotação, use `id`, `name`, `date`, `price`, `store`, `source_url`; para marcar desconto verificado, inclua `reference`, `reference_verified: true` e `reference_source_url` com fonte verificável. Referências sem fonte não produzem alerta de desconto no painel.

Para adicionar produtos de qualquer aparelho sem backend: clique em **Exportar catálogo JSON**, depois substitua `products.json` no GitHub e faça commit. A alteração estará disponível aos demais aparelhos após o deploy, com a ressalva de que a fusão preserva itens já cadastrados localmente. Cadastro e edição em tempo real entre aparelhos exigem autenticação e banco de dados.

O site recarrega o feed quando é aberto, via botão, e automaticamente a cada 3 horas enquanto a aba está aberta. Isso NÃO é coleta automática. Não publicar tokens de acesso no repositório.
