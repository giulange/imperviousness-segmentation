import marimo

app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # 06 · Training YOLO-seg

        Allena su A100. Se la GPU è in MIG, pinna automaticamente una slice
        (10 GB): tieni `imgsz=480` e `batch` piccolo. Parametri: `train`.
        """
    )
    return


@app.cell
def _():
    from impervious.params import load_params
    from impervious import model

    P = load_params()
    return P, model


@app.cell
def _(P, model):
    mig = model.first_mig_uuid()
    print("MIG slice:", mig or "nessuna (GPU intera)")
    return (mig,)


@app.cell
def _(P, mig, model):
    # avvia il training (togli il commento)
    # results = model.train(
    #     f"datasets/{P.dataset['name']}.yaml",
    #     model=P.train["model"], epochs=P.train["epochs"],
    #     imgsz=P.train["imgsz"], batch=P.train["batch"],
    #     workers=P.train["workers"], cache=P.train["cache"], mig_uuid=mig,
    # )
    # results
    return


if __name__ == "__main__":
    app.run()
