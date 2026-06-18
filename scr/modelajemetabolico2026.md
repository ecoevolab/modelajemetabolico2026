##### i. Crecimiento aislado
   a) Simular el crecimiento de solo una bacateria en el tiempo
```texto
# Simulación de crecimiento aislado de E. coli en medio m9
!python3 /workspace/ModelajeMetabolico/scr/sim_syncom_comets.py \
--gem_path /workspace/ModelajeMetabolico/modelos \
--strains Escherichia_coli \
--initial_mass 1e-5 \
--cycles 3500 \
--media  m9 \
--outdir ./ecoli
```

  b) ¿Cómo crece la bacteria? Graficar su biomasa en el tiempo.
```texto
# Gráfica biomasaxtiempo de E. coli 
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

# Graficar
plt.figure(figsize=(8, 5))

plt.plot(
    biomasa["ciclo"],
    biomasa["biomasa"],
    linewidth=2,
    color='green'
)

plt.xlabel("Ciclos", fontsize=13)
plt.ylabel("Biomasa (gDW)", fontsize=13)
plt.title("Curva de crecimiento de Rhodococcus erythropolis")

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
# Graficar metabolítos de interés (glc, etoh)
import matplotlib.pyplot as plt
import pandas as pd

# Cargar datos
flujos = "/workspace/ecoli/Escherichia_coli_exchange_fluxes.tsv"

df_flujos = pd.read_csv(
    flujos,
    sep="\t"
)

# Seleccionar metabolito
metabolito_seleccionado = "EX_etoh_e"

# Revisar si el metabolito existe
if metabolito_seleccionado not in df_flujos.columns:
    print(f"Error: {metabolito_seleccionado} no existe.")

else:
    plt.figure(figsize=(8, 5))

    plt.plot(
        df_flujos["cycle"],
        df_flujos[metabolito_seleccionado],
        linewidth=2,
        color='orange'
    )

    plt.title(
        f"Flujo de {metabolito_seleccionado}",
        fontweight="bold"
    )

    plt.xlabel("Ciclo")
    plt.ylabel("Flux")

    plt.tight_layout()
    plt.show()
```

   
   e) ¿De qué depende el crecimiento de una bacteria? Comparar cómo cambia la biomasa de una misma bacteria 
   si cambia el medio de cultivo.
```text 
# Comparación de E. coli creciendo en medio m9 y en medio LB
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
    "/workspace/ModelajeMetabolico/simulaciones/Ecoli_lb/biomass.txt",
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

# Graficar
plt.figure(figsize=(8, 5))

plt.plot(
    biomasa1["ciclo"],
    biomasa1["biomasa"],
    linewidth=2,
    color="green",
    label="medio m9"
)

plt.plot(
    biomasa2["ciclo"],
    biomasa2["biomasa"],
    linewidth=2,
    color='yellow',
    label="medio lb"
)

plt.xlabel("Ciclos", fontsize=13)
plt.ylabel("Biomasa (gDW)", fontsize=13)
plt.title("Comparación de curvas de crecimiento")

plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    "/workspace/ecoli/comparacion_crecimiento.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
```

## 3. Ejercicio

a). En la carpeta de modelos dentro `modelajemetabolico2026` encontrarás diferentes modelos metabólicos.
    
  * Simula el crecimiento aislado de *Bacillus_subtilis*, grafica como cambia su biomasa en el tiempo.
    
    ```text
    # Crecimiento aislado de B. subtilis en medio m9
    !python3 /workspace/ModelajeMetabolico/scr/sim_syncom_comets.py \
    --gem_path /workspace/ModelajeMetabolico/modelos \
    --strains  Bacillus_subtilis \
    --initial_mass 1e-5 \
    --cycles 3500 \
    --media  m9 \
    --outdir ./bsubtilis
    ```
  
```text
       # Gráfica biomasaxtiempo de B. subtilis 
import pandas as pd
import matplotlib.pyplot as plt
    
    # Cargar archivo
biomasa = pd.read_csv(
        "/workspace/bsubtilis/biomass.txt",
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
    
    # Graficar
plt.figure(figsize=(8, 5))
    
plt.plot(
        biomasa["ciclo"],
        biomasa["biomasa"],
        linewidth=2,
        color='red'
    )
    
plt.xlabel("Ciclos", fontsize=13)
plt.ylabel("Biomasa (gDW)", fontsize=13)
plt.title(r"Comparación de curvas de crecimiento de $\mathit{Bacillus\ subtilis}$")

plt.grid(True, alpha=0.3)
plt.tight_layout()
    
plt.savefig(
        "/workspace/bsubtilis/curva_crecimiento.png",
        dpi=300,
        bbox_inches="tight"
    )
    
plt.show()

    ```
  
  * Simula el crecimiento de una comunidad de dos bacterias, usa los modelos metabólicos de *Escherichia_coli* y *Bacillus_subtilis* que encontrarás en la carpeta `modelos`.
  Grafica, con ayuda del siguiente código, como cambian las biomasas de ambas bacterias cuando se encuentran en interacción.
  
  ```text
    # Crecimiento aislado de B. subtilis en medio m9
  !python3 /workspace/ModelajeMetabolico/scr/sim_syncom_comets.py \
  --gem_path /workspace/ModelajeMetabolico/modelos \
  --strains  Escherichia_coli Bacillus_subtilis \
  --initial_mass 1e-5 \
  --cycles 3500 \
  --media  m9 \
  --outdir ./ecoli_vs_bsubtilis
  ```
  
  ```text
      # Gráfica E. coli vs B. subtilis
import pandas as pd
import matplotlib.pyplot as plt

# Cargar archivo
biomasa = pd.read_csv(
    "/workspace/ecoli_vs_bsubtilis/biomass.txt",
    sep=r"\s+",
    header=None
)

# Renombrar columnas
biomasa.columns = [
    "ciclo",
    "x",
    "y",
    "modelo",
    "biomasa"
]

colores = {
    "Escherichia_coli.cmd": "green",
    "Bacillus_subtilis.cmd": "red"
}

# Graficar
plt.figure(figsize=(8, 5))

for modelo in biomasa["modelo"].unique():

    datos = biomasa[
        biomasa["modelo"] == modelo
    ]

    plt.plot(
        datos["ciclo"],
        datos["biomasa"],
        linewidth=2,
        color=colores[modelo],
        label=modelo.replace(".cmd", "")
    )

plt.xlabel("Ciclos", fontsize=13)
plt.ylabel("Biomasa (gDW)", fontsize=13)
plt.title("Curvas de crecimiento")

plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.show()
  ```
  * Compara con curvas de crecimiento como cambia cada el crecimiento cuando está creciendo de manera aislada vs como cambia cuando están en comunidad.
  
```text
import pandas as pd
import matplotlib.pyplot as plt

# E. coli aislada
biomasa1 = pd.read_csv(
    "/workspace/ecoli/biomass.txt",
    sep=r"\s+",
    header=None
)

# E. coli en interacción
biomasa2 = pd.read_csv(
    "/workspace/ecoli_vs_bsubtilis/biomass.txt",
    sep=r"\s+",
    header=None
)

# Nombres de columnas
columnas = [
    "ciclo",
    "col2",
    "col3",
    "modelo",
    "biomasa"
]

biomasa1.columns = columnas
biomasa2.columns = columnas

# Quedarse solo con E. coli
biomasa2 = biomasa2[
    biomasa2["modelo"] == "Escherichia_coli.cmd"
]

plt.figure(figsize=(8,5))

plt.plot(
    biomasa1["ciclo"],
    biomasa1["biomasa"],
    label=r"$\mathit{Escherichia\ coli}$ aislada",
    linewidth=2,
    color="green"
)

plt.plot(
    biomasa2["ciclo"],
    biomasa2["biomasa"],
    label=r"$\mathit{Escherichia\ coli}$ en interacción",
    linewidth=2,
    color="lightgreen"
)

plt.legend()
plt.grid(True, alpha=0.3)
plt.show()    
```

```text
# Gráfica B. subtilis aislada vs B. subtilis en interacción
import pandas as pd
import matplotlib.pyplot as plt

# B. subtilis aislada
biomasa1 = pd.read_csv(
    "/workspace/bsubtilis/biomass.txt",
    sep=r"\s+",
    header=None
)

# B. subtilis en interacción
biomasa2 = pd.read_csv(
    "/workspace/ecoli_vs_bsubtilis/biomass.txt",
    sep=r"\s+",
    header=None
)

# Nombres de columnas
columnas = [
    "ciclo",
    "col2",
    "col3",
    "modelo",
    "biomasa"
]

biomasa1.columns = columnas
biomasa2.columns = columnas

# Quedarse solo con B. subtilis
biomasa2 = biomasa2[
    biomasa2["modelo"] == "Bacillus_subtilis.cmd"
]

plt.figure(figsize=(8,5))

plt.plot(
    biomasa1["ciclo"],
    biomasa1["biomasa"],
    label=r"$\mathit{Bacillus\ subtilis}$ aislada",
    linewidth=2,
    color="red"
)

plt.plot(
    biomasa2["ciclo"],
    biomasa2["biomasa"],
    label=r"$\mathit{Bacillus\ subtilis}$ en interacción",
    linewidth=2,
    color="lightcoral"
)

plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```
