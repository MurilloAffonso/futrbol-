# Integrações

Coloque aqui ferramentas externas autorizadas, como o scraper FlashscoreScraping enviado.

Recomendação:

```text
integrations/
  FlashscoreScraping-main/
```

Fluxo:

1. Rodar o scraper autorizado para gerar JSON.
2. Enviar esse JSON para `POST /import/flashscore-json`.
3. Usar o backend para normalizar e analisar os dados.
