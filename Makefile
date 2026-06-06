# ==========================================
# Variables de configuración y rutas
# ==========================================
PYTHON = python
SRC_DIR = src
DATA_RAW = data/raw/estudiantes.csv
DATA_VALIDADO = data/interim/validado.csv
REPORTE_VALIDACION = data/interim/reporte_validacion.txt
DATA_IMPUTADO = data/interim/imputado.csv
DATA_TRANSFORMADO = data/processed/transformado.csv
RESUMEN = data/processed/resumen.txt
REPORTE_FINAL = reports/reporte_final.md

# ==========================================
# Objetivos que no producen archivos (.PHONY)
# ==========================================
.PHONY: all lint limpiar estado directorios

# ==========================================
# Objetivo Principal
# ==========================================
all: lint $(REPORTE_FINAL)

# ==========================================
# Calidad de Código
# ==========================================
lint:
	@echo "Ejecutando Ruff (Linter y Formateador)..."
	ruff check $(SRC_DIR)/
	ruff format --check $(SRC_DIR)/

# ==========================================
# Reglas del Pipeline (Grafo de Dependencias)
# ==========================================

# Regla auxiliar multiplataforma para crear las carpetas si no existen
directorios:
	@$(PYTHON) -c "import os; os.makedirs('data/interim', exist_ok=True); os.makedirs('data/processed', exist_ok=True); os.makedirs('reports', exist_ok=True)"

# Script 1: Validar
$(DATA_VALIDADO) $(REPORTE_VALIDACION): $(DATA_RAW) $(SRC_DIR)/validar.py | directorios
	$(PYTHON) $(SRC_DIR)/validar.py

# Script 2: Imputar
$(DATA_IMPUTADO): $(DATA_VALIDADO) $(SRC_DIR)/imputar.py | directorios
	$(PYTHON) $(SRC_DIR)/imputar.py

# Script 3: Transformar
$(DATA_TRANSFORMADO): $(DATA_IMPUTADO) $(SRC_DIR)/transformar.py | directorios
	$(PYTHON) $(SRC_DIR)/transformar.py

# Script 4: Resumir
$(RESUMEN): $(DATA_TRANSFORMADO) $(SRC_DIR)/resumir.py | directorios
	$(PYTHON) $(SRC_DIR)/resumir.py

# Script 5: Reporte Final (Dependencia Múltiple)
$(REPORTE_FINAL): $(DATA_TRANSFORMADO) $(RESUMEN) $(SRC_DIR)/reporte.py | directorios
	$(PYTHON) $(SRC_DIR)/reporte.py

# ==========================================
# Utilidades Multiplataforma
# ==========================================
limpiar:
	@echo "Limpiando archivos generados..."
	@$(PYTHON) -c "import os, glob; files = glob.glob('data/interim/*') + glob.glob('data/processed/*') + glob.glob('reports/*'); [os.remove(f) for f in files if os.path.isfile(f)]"
	@echo "Limpieza completada."

estado:
	@echo "--- Estado de los Archivos del Pipeline ---"
	@$(PYTHON) -c "import os; files=[('$(DATA_RAW)', 'CRUDO'), ('$(DATA_VALIDADO)', 'INTERMEDIO'), ('$(REPORTE_VALIDACION)', 'INTERMEDIO'), ('$(DATA_IMPUTADO)', 'INTERMEDIO'), ('$(DATA_TRANSFORMADO)', 'PROCESADO'), ('$(RESUMEN)', 'PROCESADO'), ('$(REPORTE_FINAL)', 'REPORTE')]; [print(f'[OK] {f[0]} ({f[1]})' if os.path.exists(f[0]) else f'[ ] {f[0]} (FALTA)') for f in files]"