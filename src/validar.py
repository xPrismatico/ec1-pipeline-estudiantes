import polars as pl


def validar_datos(ruta_entrada: str, ruta_csv: str, ruta_txt: str) -> None:
    """Lee y valida el dataset de estudiantes, identificando nulos y anomalías."""
    df: pl.DataFrame = pl.read_csv(ruta_entrada)

    # 1. Crear columna tiene_faltantes
    df_validado: pl.DataFrame = df.with_columns(
        pl.any_horizontal(pl.all().is_null()).alias("tiene_faltantes")
    )
    df_validado.write_csv(ruta_csv)

    # 2. Análisis para el reporte
    nulos_por_columna: dict[str, int] = df.null_count().to_dicts()[0]

    # Usamos df_validado
    filas_con_nulos: pl.DataFrame = df_validado.filter(pl.col("tiene_faltantes"))
    nombres_nulos: list[str] = filas_con_nulos["nombre"].to_list()

    # 3. Detección de anomalías (fuera de rango)
    condicion_notas = (
        ((pl.col("nota1") < 1.0) | (pl.col("nota1") > 7.0))
        | ((pl.col("nota2") < 1.0) | (pl.col("nota2") > 7.0))
        | ((pl.col("nota3") < 1.0) | (pl.col("nota3") > 7.0))
    )
    anomalias_notas: pl.DataFrame = df.filter(condicion_notas)
    nombres_anomalos_notas: list[str] = anomalias_notas["nombre"].to_list()

    condicion_asis = (pl.col("asistencia") < 0) | (pl.col("asistencia") > 100)
    anomalias_asis: pl.DataFrame = df.filter(condicion_asis)
    nombres_anomalos_asis: list[str] = anomalias_asis["nombre"].to_list()

    # 4. Escribir el reporte en texto plano
    with open(ruta_txt, "w", encoding="utf-8") as f:
        f.write("=== REPORTE DE VALIDACION ===\n")
        f.write("1. Valores faltantes por columna:\n")
        for col, cantidad in nulos_por_columna.items():
            if cantidad > 0:
                f.write(f"   - {col}: {cantidad}\n")

        f.write("\n2. Estudiantes con valores faltantes:\n")
        f.write(f"{', '.join(nombres_nulos) if nombres_nulos else 'Ninguno'}\n")

        f.write("\n3. Anomalías detectadas (fuera de rango):\n")
        if nombres_anomalos_notas:
            f.write(f"-Notas anómalas: {', '.join(nombres_anomalos_notas)}\n")
        if nombres_anomalos_asis:
            f.write(f"-Asisten. anómala: {', '.join(nombres_anomalos_asis)}\n")
        if not nombres_anomalos_notas and not nombres_anomalos_asis:
            f.write(f"-No se detectaron valores fuera del rango esperado.\n")


if __name__ == "__main__":
    validar_datos(
        "data/raw/estudiantes.csv",
        "data/interim/validado.csv",
        "data/interim/reporte_validacion.txt",
    )