# Sicurezza — gestione credenziali

Tutti i segreti stanno in **`.env`** (mai committato, vedi `.env.example`) e si
leggono via `impervious.config`. Nessuna credenziale nel codice o nei notebook.

## Runbook (ordine consigliato)

1. **Ruota le password compromesse** (erano in chiaro nella history):
   - PostGIS `osm` (utente `giuliano`) → nuova password nel `.env` + `scripts/postgis_up.sh`.
   - DB LandSupport (`postgres@192.168.30.11`) → **infrastruttura di terzi**: avvisa
     chi la gestisce, la vecchia password va cambiata.
   - Vecchi account SciHub / PRISMA → dismessi (non più usati).
   La rotazione è la cosa più importante: rende inutili i segreti già trapelati.

2. **Installa il pre-commit hook** (blocca futuri segreti):
   ```bash
   bash scripts/install_hooks.sh      # usa detect-secrets (nell'env Pixi)
   ```

3. **Scrub della history** (rimuove i segreti dai commit passati) — solo al rilascio:
   ```bash
   bash scripts/scrub_history.sh      # crea backup, riscrive la history
   # poi (coordinato):
   git remote add origin git@github.com:giulange/imperviousness-segmentation.git
   git push --force --all && git push --force --tags
   ```
   ⚠️ Riscrive tutti gli hash e richiede force-push su `main` e sul branch.
   Da fare **dopo** aver ruotato le password e verificato il backup bundle.

## Cosa contiene `.env`
Vedi `.env.example`: credenziali PostGIS, account CDSE, chiavi S3 EODATA (per la
lettura COG dal bucket CDSE).
