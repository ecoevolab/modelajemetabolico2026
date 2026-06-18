# Curso Modelaje Metabólico 2026

## 1. **Configuración de COMETS en DockerDesktop**
##### i. Contenedor de COMETS en DockerDesktop
```texto
dukovski/comets-lab:1.0
```
##### ii. Crear imagen
Host port: 8888

##### ii. Instalar git
apt-get update

apt-get install git

git --version

##### iii. Clonar repositorio
git clone https://github.com/ecoevolab/modelajemetabolico2026.git

## 2. **Ejemplo**
Revisa la configuración de la funcion sim_syncom_comets.py

```text
!python3 /workspace/modelajemetabolico2026/scr/sim_syncom_comets.py --h
```
##### i. Crecimiento aislado
   a) Simular el crecimiento de solo una bacateria en el tiempo
```texto
!python3 /workspace/modelajemetabolico2026/scr/sim_syncom_comets.py \
--gem_path /workspace/modelajemetabolico2026/modelos \
--strains Escherichia_coli \
--initial_mass 1e-5 \
--cycles 3500 \
--media  m9 \
--outdir ./ecoli
```

  b) ¿Cómo crece la bacteria? Graficar su biomasa en el tiempo.
```texto
import pandas as pd
import matplotlib.pyplot as plt

# Cargar archivo
biomasa = pd.read_csv(
    "/workspace/ecoli/biomass.txt",
    sep=r"\s+",
    header=None
)

# Renombrar columnas
biomasa.columns = [
    "ciclo",
    "col2",
    "col3",
    "modelo",
    "biomasa"
]

# Convertir ciclos a horas
biomasa["hora"] = biomasa["ciclo"] * 0.1

# Graficar
plt.figure(figsize=(8, 5))

plt.plot(
    biomasa["hora"],
    biomasa["biomasa"],
    linewidth=2,
    color="green"
)

plt.xlabel("Tiempo (h)", fontsize=13)
plt.ylabel("Biomasa (gDW)", fontsize=13)
plt.title(r"Curva de crecimiento de $\mathit{Escherichia\ coli}$")
plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    "/workspace/ecoli/curva_crecimiento.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
```

  c) ¿Cómo cambia el consumo de glucosa durante el crecimiento de E. coli? 

```texto
import matplotlib.pyplot as plt
import pandas as pd

# Cargar datos
flujos = "/workspace/ecoli/Escherichia_coli_exchange_fluxes.tsv"

df_flujos = pd.read_csv(
    flujos,
    sep="\t"
)

# Convertir ciclos a horas (COMETS: 1 ciclo = 0.1 h)
df_flujos["hora"] = df_flujos["cycle"] * 0.1

# Seleccionar metabolito
metabolito_seleccionado = "EX_glc__D_e"

# Revisar si el metabolito existe
if metabolito_seleccionado not in df_flujos.columns:
    print(f"Error: {metabolito_seleccionado} no existe.")

else:
    plt.figure(figsize=(8, 5))

    plt.plot(
        df_flujos["hora"],
        df_flujos[metabolito_seleccionado],
        linewidth=2,
        color="orange"
    )

    plt.title(
        "Flujo de glucosa",
        fontweight="bold"
    )

    plt.xlabel("Tiempo (h)")
    plt.ylabel("Flux (mmol/gDW/h)")

    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()
```
  c) ¿Cómo cambia el consumo de etanol durante el crecimiento de E. coli? 
```text
import matplotlib.pyplot as plt
import pandas as pd

# Cargar datos
flujos = "/workspace/ecoli/Escherichia_coli_exchange_fluxes.tsv"

df_flujos = pd.read_csv(
    flujos,
    sep="\t"
)

# Convertir ciclos a horas (COMETS: 1 ciclo = 0.1 h)
df_flujos["hora"] = df_flujos["cycle"] * 0.1

# Seleccionar metabolito
metabolito_seleccionado = "EX_etoh_e"

# Revisar si el metabolito existe
if metabolito_seleccionado not in df_flujos.columns:
    print(f"Error: {metabolito_seleccionado} no existe.")

else:
    plt.figure(figsize=(8, 5))

    plt.plot(
        df_flujos["hora"],
        df_flujos[metabolito_seleccionado],
        linewidth=2,
        color="orange"
    )

    plt.title(
        "Flujo de etanol",
        fontweight="bold"
    )

    plt.xlabel("Tiempo (h)")
    plt.ylabel("Flux (mmol/gDW/h)")

    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()
```
   
   e) ¿De qué depende el crecimiento de una bacteria? Comparar cómo cambia la biomasa de una misma bacteria 
   si cambia el medio de cultivo.
```text 
# Comparación de E. coli creciendo en medio M9 y en medio LB
import pandas as pd
import matplotlib.pyplot as plt

# Archivo 1
biomasa1 = pd.read_csv(
    "/workspace/ecoli/biomass.txt",
    sep=r"\s+",
    header=None
)

# Archivo 2
biomasa2 = pd.read_csv(
    "/workspace/modelajemetabolico2026/simulaciones/Ecoli_lb/biomass.txt",
    sep=r"\s+",
    header=None
)

# Renombrar columnas
columnas = [
    "ciclo",
    "col2",
    "col3",
    "modelo",
    "biomasa"
]

biomasa1.columns = columnas
biomasa2.columns = columnas

# Convertir ciclos a horas (COMETS: 1 ciclo = 0.1 h)
biomasa1["hora"] = biomasa1["ciclo"] * 0.1
biomasa2["hora"] = biomasa2["ciclo"] * 0.1

# Graficar
plt.figure(figsize=(8, 5))

plt.plot(
    biomasa1["hora"],
    biomasa1["biomasa"],
    linewidth=2,
    color="green",
    label="Medio M9"
)

plt.plot(
    biomasa2["hora"],
    biomasa2["biomasa"],
    linewidth=2,
    color="gold",
    label="Medio LB"
)

plt.xlabel("Tiempo (h)", fontsize=13)
plt.ylabel("Biomasa (gDW)", fontsize=13)
plt.title(
    r"Comparación de curvas de crecimiento de $\mathit{Escherichia\ coli}$"
)

plt.legend()
plt.grid(True, alpha=0.3)

# Marcas cada 10 horas
tiempo_max = max(
    biomasa1["hora"].max(),
    biomasa2["hora"].max()
)

plt.tight_layout()


plt.show()
```
## 3. Ejercicio

a). En la carpeta de modelos dentro `modelajemetabolico2026` encontrarás diferentes modelos metabólicos.
    
  * Simula el crecimiento aislado de *Bacillus_subtilis*, grafica como cambia su biomasa en el tiempo. 
  
  * Simula el crecimiento de una comunidad de dos bacterias, usa los modelos metabólicos de *Escherichia_coli* y *Bacillus_subtilis* que encontrarás en la carpeta `modelos`.
  Grafica, con ayuda del siguiente código, como cambian las biomasas de ambas bacterias cuando se encuentran en interacción.
  
  * Compara con curvas de crecimiento como cambia cada el crecimiento cuando está creciendo de manera aislada vs como cambia cuando están en comunidad.
  
  



