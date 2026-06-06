import polars as pl


def imputar_datos(ruta_entrada: str, ruta_salida: str) -> None:
    """Imputa valores nulos: mediana en notas, media redondeada en asist."""
    df: pl.DataFrame = pl.read_csv(ruta_entrada)

    columnas_notas: list[str] = ["nota1", "nota2", "nota3"]

    # Imputación idiomática combinando comprensiones de listas en Polars
    df_imputado: pl.DataFrame = df.with_columns(
        [
            pl.col(col_nota).fill_null(pl.median(col_nota))
            for col_nota in columnas_notas
        ]
        + [
            pl.col("asistencia").fill_null(
                pl.mean("asistencia").round(0).cast(pl.Int64)
            )
        ]
    )

    df_imputado.write_csv(ruta_salida)


if __name__ == "__main__":
    imputar_datos(
        "data/interim/validado.csv",
        "data/interim/imputado.csv"
    )