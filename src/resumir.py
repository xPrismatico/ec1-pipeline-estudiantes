import polars as pl


def resumir_datos(ruta_entrada: str, ruta_txt: str) -> None:
    """Genera un resumen estadístico del curso exportado en texto plano."""
    df: pl.DataFrame = pl.read_csv(ruta_entrada)

    # Cálculos estadísticos
    total_estudiantes: int = df.height
    promedio_general: float = df["promedio"].mean()
    nota_min: float = df["promedio"].min()
    nota_max: float = df["promedio"].max()
    pct_aprobados: float = (df["aprobado"].sum() / total_estudiantes) * 100
    asis_promedio: float = df["asistencia"].mean()

    # Conteo por categoría
    conteo_cat: pl.DataFrame = df.group_by("categoria").len()

    with open(ruta_txt, "w", encoding="utf-8") as f:
        f.write("=== RESUMEN ESTADISTICO DEL CURSO ===\n")
        f.write(f"Total de estudiantes: {total_estudiantes}\n")
        f.write(f"Promedio general del curso: {promedio_general:.2f}\n")
        f.write(f"Nota mínima individual (Promedio): {nota_min:.2f}\n")
        f.write(f"Nota máxima individual (Promedio): {nota_max:.2f}\n")
        f.write(f"Porcentaje de aprobados: {pct_aprobados:.1f}%\n")
        f.write(f"Promedio de asistencia: {asis_promedio:.1f}%\n")

        f.write("\nConteo por categoría:\n")
        # Extraer filas del dataframe agrupado
        for fila in conteo_cat.iter_rows():
            f.write(f" - {fila[0]}: {fila[1]}\n")


if __name__ == "__main__":
    resumir_datos("data/processed/transformado.csv", "data/processed/resumen.txt")