import polars as pl


def transformar_datos(ruta_entrada: str, ruta_salida: str) -> None:
    """Calcula promedios, estado de aprobación y categoría del estudiante."""
    df: pl.DataFrame = pl.read_csv(ruta_entrada)

    # Transformación idiomática en Polars
    df_transformado: pl.DataFrame = (
        df.with_columns(
            pl.mean_horizontal("nota1", "nota2", "nota3").round(2).alias("promedio")
        )
        .with_columns((pl.col("promedio") >= 4.0).alias("aprobado"))
        .with_columns(
            pl.when(pl.col("promedio") >= 6.0)
            .then(pl.lit("Destacado"))
            .when(pl.col("promedio") >= 4.0)
            .then(pl.lit("Aprobado"))
            .otherwise(pl.lit("Reprobado"))
            .alias("categoria")
        )
    )

    df_transformado.write_csv(ruta_salida)


if __name__ == "__main__":
    transformar_datos("data/interim/imputado.csv", "data/processed/transformado.csv")