# Flashscore Authorized Provider

Fluxo MVP autorizado:
1. Receber JSON exportado por integracao autorizada.
2. Normalizar nomes de times (lowercase + trim).
3. Evitar duplicidade por `matchId` externo.
4. Salvar relatorio em `ImportedFile` e evento em `SyncLog`.
5. Campos ausentes viram `null`/`unavailable`.
