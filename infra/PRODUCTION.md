# Publicação em produção

O site deve ser publicado exclusivamente a partir de um commit autorizado da
branch `main`, usando `scripts/deploy-production.sh`. Não copie arquivos
diretamente para a árvore da aplicação.

## Sequência preparada

1. Confirmar `A`/`CNAME` de `plansmart.com.br` e `www.plansmart.com.br` para
   `191.252.93.136`.
2. Clonar o repositório em `/opt/plansmart/sistemas/landingpage` na branch
   `main`.
3. Instalar o arquivo Nginx versionado, validar com `nginx -t` e habilitar o
   site.
4. Emitir o certificado TLS após a propagação do DNS.
5. Executar `scripts/deploy-production.sh <commit-autorizado>`.
6. Validar HTTP→HTTPS, conteúdo, ativos estáticos, logs e telas desktop/móvel.

## Rollback preparado

- DNS: restaurar os registros anteriores (`191.252.177.64`) enquanto estiverem
  dentro da janela de rollback aprovada.
- Nginx: restaurar o backup do arquivo anterior e executar `nginx -t` antes do
  reload.
- Código: promover um commit anterior por novo fluxo autorizado; o script não
  faz `reset`, `clean` ou sobrescrita destrutiva.
