import polars as pl
from datetime import datetime


def generar_reporte(ruta_csv: str, ruta_resumen: str, ruta_reporte: str) -> None:
    """Genera el reporte final en Markdown combinando datos y estadísticas."""
    df: pl.DataFrame = pl.read_csv(ruta_csv)

    # Leer el resumen de texto
    with open(ruta_resumen, "r", encoding="utf-8") as f:
        contenido_resumen: str = f.read()

    # Extraer información de imputaciones basada en el flag inicial
    filas_imputadas: pl.DataFrame = df.filter(pl.col("tiene_faltantes"))
    nombres_imputados: list[str] = filas_imputadas["nombre"].to_list()
    total_imputados: int = len(nombres_imputados)

    fecha_actual: str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    with open(ruta_reporte, "w", encoding="utf-8") as f:
        f.write(f"# Reporte Final de Resultados\n")
        f.write(f"**Fecha de generación:** {fecha_actual}\n\n")

        f.write("## 1. Resumen Estadístico\n")
        f.write("```text\n")
        f.write(contenido_resumen)
        f.write("\n```\n\n")

        f.write("## 2. Observaciones sobre Datos Imputados\n")
        f.write(f"Se imputaron datos para **{total_imputados}** estudiantes\n")
        if total_imputados > 0:
            f.write(f"Estudiantes afectados: {', '.join(nombres_imputados)}.\n\n")

        f.write("## 3. Tabla de Resultados\n")
        # Generar estructura de tabla Markdown dinámicamente
        columnas: list[str] = df.columns
        f.write("| " + " | ".join(columnas) + " |\n")
        f.write("|" + "|".join(["---"] * len(columnas)) + "|\n")

        for fila in df.iter_rows():
            fila_str = [str(val) if val is not None else "" for val in fila]
            f.write("| " + " | ".join(fila_str) + " |\n")


if __name__ == "__main__":
    generar_reporte(
        "data/processed/transformado.csv",
        "data/processed/resumen.txt",
        "reports/reporte_final.md",
    )