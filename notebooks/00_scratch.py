import marimo

__generated_with = "0.23.11"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 00 · Scratch

    Blocco appunti per prove veloci ed esplorazione. Tutto l'ambiente è
    disponibile: importa da `impervious` e sperimenta liberamente.
    """)
    return


@app.cell
def _():
    from impervious.params import load_params
    from impervious.config import settings, pg_engine
    from impervious import acquire, nuts, osm, db, raster, annotate, dataset, model

    P = load_params()
    return (P,)


@app.cell
def _(P):
    # esempio: guarda i parametri caricati
    P.tiles
    return


if __name__ == "__main__":
    app.run()
