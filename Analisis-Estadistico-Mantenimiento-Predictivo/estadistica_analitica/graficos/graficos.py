from pathlib import Path
import matplotlib.pyplot as plt

CARPETA_AGRUPADOS = "Resultados_Graficos_Agrupados"
CARPETA_NO_AGRUPADOS = "Resultados_Graficos_No_Agrupados"

def crear_carpeta(nombre):
    carpeta = Path.cwd() / nombre
    carpeta.mkdir(parents=True, exist_ok=True)
    return carpeta

def guardar(fig, carpeta, nombre):
    fig.tight_layout()
    fig.savefig(carpeta / nombre)
    plt.close(fig)


def tipo_sesgo(g1):
    if g1 > 0.1:
        return "Positivo"
    if g1 < -0.1:
        return "Negativo"
    return "Simetrico"


def tipo_curtosis(k):
    if k > 0.1:
        return "Leptocurtica"
    if k < -0.1:
        return "Platicurtica"
    return "Mesocurtica"


def correlacion(x, y):
    n = len(x)
    mx = sum(x) / n
    my = sum(y) / n
    sxy = 0.0
    sxx = 0.0
    syy = 0.0
    for i in range(n):
        dx = x[i] - mx
        dy = y[i] - my
        sxy = sxy + dx * dy
        sxx = sxx + dx * dx
        syy = syy + dy * dy
    return sxy / (sxx * syy) ** 0.5


def poner_lineas_y_leyenda(ax, res):
    central = res["Tendencia central"]
    forma = res["Forma"]
    media = central["Media aritmetica"]
    mediana = central["Mediana"]
    moda = central["Moda"]
    g1 = forma["Sesgo de Fisher-Pearson (g1)"]
    k = forma["Exceso de curtosis (k)"]

    ax.axvline(media, color="red", linestyle="--", label=f"Media: {media:.2f}")
    ax.axvline(mediana, color="green", linestyle="-.", label=f"Mediana: {mediana:.2f}")
    ax.axvline(moda, color="orange", linestyle=":", linewidth=2, label=f"Moda: {moda:.2f}")
    # lineas vacias solo para escribir el texto en la leyenda
    ax.plot([], [], " ", label=f"Sesgo: {g1:.2f} ({tipo_sesgo(g1)})")
    ax.plot([], [], " ", label=f"Curtosis: {k:.2f} ({tipo_curtosis(k)})")
    ax.legend(title="Estadisticos", fontsize=8, loc="best")

#Histogramas
def histograma_no_agrupado(metrica, datos, res, k, carpeta):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(datos, bins=k, color="steelblue", edgecolor="black")
    poner_lineas_y_leyenda(ax, res)
    ax.set_title(f"Histograma de {metrica} (no agrupado)")
    ax.set_xlabel("Valor")
    ax.set_ylabel("Frecuencia")
    ax.grid(True, linestyle="--", alpha=0.5)
    guardar(fig, carpeta, f"Histograma_{metrica}.pdf")


def histograma_agrupado(metrica, tabla, res, carpeta):
    limites = []
    frecuencias = []
    for fila in tabla["clases"]:
        limites.append(fila["li"])
        frecuencias.append(fila["fi"])

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(limites, frecuencias, width=tabla["amplitud"], align="edge",
           color="seagreen", edgecolor="black")
    poner_lineas_y_leyenda(ax, res)
    ax.set_title(f"Histograma de {metrica} (agrupado, {tabla['total_clases']} clases)")
    ax.set_xlabel("Valor")
    ax.set_ylabel("Frecuencia")
    ax.grid(True, linestyle="--", alpha=0.5)
    guardar(fig, carpeta, f"Histograma_{metrica}.pdf")



#Boxplots
def boxplot_no_agrupado(metricas, continuas, resultados, carpeta):
    # un cuadro por metrica porque las escalas son muy distintas
    fig, ejes = plt.subplots(1, len(metricas), figsize=(4.5 * len(metricas), 5))
    for i in range(len(metricas)):
        m = metricas[i]
        ax = ejes[i]
        ax.boxplot(continuas[m], patch_artist=True,
                   boxprops=dict(facecolor="steelblue"),
                   medianprops=dict(color="black"),
                   flierprops=dict(marker="o", markersize=2,
                                   markerfacecolor="firebrick", markeredgecolor="firebrick"))
        media = resultados[m]["no_agrupado"]["Tendencia central"]["Media aritmetica"]
        ax.axhline(media, color="red", linestyle="--", label=f"Media: {media:.2f}")
        ax.set_title(f"Boxplot de {m}")
        ax.set_xticks([])
        ax.set_ylabel("Valor")
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.legend(fontsize=8, loc="upper right")
    guardar(fig, carpeta, "Boxplot_No_Agrupado.pdf")


def boxplot_agrupado(metricas, resultados, carpeta):
    fig, ejes = plt.subplots(1, len(metricas), figsize=(4.5 * len(metricas), 5))
    for i in range(len(metricas)):
        m = metricas[i]
        ax = ejes[i]
        res = resultados[m]["agrupado"]
        tabla = resultados[m]["tabla"]
        q1 = res["Cuantiles"]["Q1"]
        q2 = res["Cuantiles"]["Q2"]
        q3 = res["Cuantiles"]["Q3"]
        iqr = q3 - q1
        bajo = max(tabla["minimo"], q1 - 1.5 * iqr)
        alto = min(tabla["maximo"], q3 + 1.5 * iqr)

        estadisticas = [{"med": q2, "q1": q1, "q3": q3,
                         "whislo": bajo, "whishi": alto, "fliers": []}]
        ax.bxp(estadisticas, patch_artist=True,
               boxprops=dict(facecolor="seagreen"),
               medianprops=dict(color="black"))
        media = res["Tendencia central"]["Media aritmetica"]
        ax.axhline(media, color="red", linestyle="--", label=f"Media: {media:.2f}")
        ax.set_title(f"Boxplot de {m} (agrupado)")
        ax.set_xticks([])
        ax.set_ylabel("Valor")
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.legend(fontsize=8, loc="upper right")
    guardar(fig, carpeta, "Boxplot_Agrupado.pdf")

# 3. Dispersion
def dispersion(metricas, continuas, carpeta):
    pares = []
    for i in range(len(metricas)):
        for j in range(i + 1, len(metricas)):
            pares.append((metricas[i], metricas[j]))

    fig, ejes = plt.subplots(1, len(pares), figsize=(5 * len(pares), 4.5))
    for i in range(len(pares)):
        mx = pares[i][0]
        my = pares[i][1]
        r = correlacion(continuas[mx], continuas[my])
        ax = ejes[i]
        # rasterized para que el pdf no pese tanto con tantos puntos
        ax.scatter(continuas[mx], continuas[my], s=2, alpha=0.3, color="darkblue",
                   edgecolors="none", rasterized=True)
        ax.set_title(f"{mx} vs {my} (r = {r:.3f})")
        ax.set_xlabel(mx)
        ax.set_ylabel(my)
        ax.grid(True, linestyle="--", alpha=0.5)
    guardar(fig, carpeta, "Dispersion_Metricas.pdf")

# 4. Barras (variable categorica failure)
def barras_fallas(fallas, carpeta):
    sin_falla = fallas.count(0)
    con_falla = fallas.count(1)
    total = len(fallas)

    fig, ax = plt.subplots(figsize=(6, 4.5))
    barras = ax.bar(["Sin falla (0)", "Con falla (1)"], [sin_falla, con_falla],
                    color=["navy", "firebrick"], edgecolor="black")
    cantidades = [sin_falla, con_falla]
    for i in range(len(barras)):
        porcentaje = cantidades[i] / total * 100
        ax.text(barras[i].get_x() + barras[i].get_width() / 2, cantidades[i],
                f"{cantidades[i]}\n({porcentaje:.2f} %)", ha="center", va="bottom",
                fontweight="bold")
    ax.set_title("Frecuencia de fallas")
    ax.set_xlabel("Estado")
    ax.set_ylabel("Cantidad de registros")
    ax.set_ylim(0, max(cantidades) * 1.15)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    guardar(fig, carpeta, "Barras_Fallas.pdf")

# Funcion principal
def generar_graficos_eda(datos, resultados):
    continuas = datos["continuas"]
    discretas = datos["discretas"]
    metricas = list(resultados.keys())

    carpeta_ag = crear_carpeta(CARPETA_AGRUPADOS)
    carpeta_no = crear_carpeta(CARPETA_NO_AGRUPADOS)

    # 1. histogramas (uno por metrica y por enfoque)
    for m in metricas:
        tabla = resultados[m]["tabla"]
        histograma_no_agrupado(m, continuas[m], resultados[m]["no_agrupado"],
                               tabla["total_clases"], carpeta_no)
        histograma_agrupado(m, tabla, resultados[m]["agrupado"], carpeta_ag)

    # 2. boxplots
    boxplot_no_agrupado(metricas, continuas, resultados, carpeta_no)
    boxplot_agrupado(metricas, resultados, carpeta_ag)

    # 3. dispersion
    dispersion(metricas, continuas, carpeta_no)

    # 4. barras
    barras_fallas(discretas["failure"], carpeta_no)

    print("\nGraficos generados en formato PDF en:")
    print(" ", CARPETA_AGRUPADOS)
    print(" ", CARPETA_NO_AGRUPADOS)