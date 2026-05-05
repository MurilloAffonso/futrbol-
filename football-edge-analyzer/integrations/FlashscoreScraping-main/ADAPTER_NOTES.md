# Como usar este scraper dentro do Football Edge Analyzer

Este diretório contém o projeto enviado no ZIP original. Ele coleta resultados e estatísticas em JSON/CSV.

No MVP, o backend não chama diretamente o Playwright. O fluxo recomendado é:

```bash
cd integrations/FlashscoreScraping-main
npm install
npx playwright install-deps chromium
npm run start country=brazil league=serie-a-2023 fileType=json-array concurrency=3 saveInterval=10
```

Depois envie o JSON gerado para:

```text
POST /import/flashscore-json
```

No futuro, podemos criar um job no backend para executar o coletor em ambiente controlado.
