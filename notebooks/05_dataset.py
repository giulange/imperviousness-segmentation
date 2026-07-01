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
        # 05 · Dataset YOLO

        Divide i tile annotati in train/val/test e scrive il `data.yaml`.
        Parametri: `dataset`.
        """
    )
    return


@app.cell
def _():
    from impervious.params import load_params
    from impervious import dataset

    P = load_params()
    return P, dataset


@app.cell
def _(P, dataset):
    tiles_dir = "annotations/tiles"
    out_dir = f"datasets/{P.dataset['name']}"

    counts = dataset.split_train_val_test(
        tiles_dir, out_dir, ratios=P.dataset["split"], seed=P.dataset["seed"],
    )
    yaml_path = dataset.write_data_yaml(
        f"datasets/{P.dataset['name']}.yaml", out_dir, P.dataset["classes"],
    )
    print("split:", counts)
    print("yaml:", yaml_path)
    return


if __name__ == "__main__":
    app.run()
