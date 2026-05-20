import numpy as np
import matplotlib.pyplot as plt

# Configuración álbum
TOTAL_ESTAMPAS = 980
ESTAMPAS_POR_PAQUETE = 7
PRECIO_SOBRE = 9.50
PRECIO_CAJA = 975.0
SOBRES_POR_CAJA = 104
SIMULACIONES = 2000

# Semilla
np.random.seed(2026)

def calcular_costo(sobres):
    cajas = sobres // SOBRES_POR_CAJA # floor division
    sobres_sueltos = sobres % SOBRES_POR_CAJA
    
    # Costo comprando cajas y sobres sueltos
    costo_mixto = cajas * PRECIO_CAJA + sobres_sueltos * PRECIO_SOBRE
    # Costo comprando una caja más en lugar de sueltos (por si conviene)
    costo_solo_cajas = (cajas + 1) * PRECIO_CAJA
    
    return min(costo_mixto, costo_solo_cajas)

def simular_un_album():
    album = set()
    sobres_comprados = 0
    opciones = np.arange(TOTAL_ESTAMPAS)
    
    while len(album) < TOTAL_ESTAMPAS:
        sobre = np.random.choice(opciones, size=ESTAMPAS_POR_PAQUETE, replace=False)
        album.update(sobre)
        sobres_comprados += 1
        
    return sobres_comprados

# Correr simulación
resultados_sobres = []
for _ in range(SIMULACIONES):
    resultados_sobres.append(simular_un_album())

resultados_sobres = np.array(resultados_sobres)
resultados_costos = np.array([calcular_costo(s) for s in resultados_sobres])

# Estadísticas
promedio_sobres = np.mean(resultados_sobres)
mediana_sobres = np.median(resultados_sobres)
p90_sobres = np.percentile(resultados_sobres, 90)
min_sobres = np.min(resultados_sobres)
max_sobres = np.max(resultados_sobres)

promedio_costo = np.mean(resultados_costos)
mediana_costo = np.median(resultados_costos)
p90_costo = np.percentile(resultados_costos, 90)
min_costo = np.min(resultados_costos)
max_costo = np.max(resultados_costos)

print(f"Sobres = Promedio: {promedio_sobres:.2f}, Mediana: {mediana_sobres}, P90: {p90_sobres}, Min: {min_sobres}, Max: {max_sobres}")
print(f"Costos = Promedio: Q{promedio_costo:.2f}, Mediana: Q{mediana_costo:.2f}, P90: Q{p90_costo:.2f}, Min: Q{min_costo:.2f}, Max: Q{max_costo:.2f}")

#---------------------

#ETAPA 1
# --- PARÁMETROS ---
N = 100          # Número total de estampas diferentes
S = 7            # Estampas por sobre (sin repetir dentro del sobre)
R = 10000        # Número de simulaciones a realizar
np.random.seed(2026)  # Semilla para reproducibilidad del generador

# Resultados de las simulaciones
resultados_sobres = np.zeros(R)
resultados_repetidas = np.zeros(R)

# Combinaciones de Estampas posibles (0 a 99)
opciones_estampas = np.arange(N)

# --- SIMULACIÓN ---
for i in range(R):
    # Arreglo booleano
    album = np.zeros(N, dtype=bool)
    
    # Iniciar contadores
    sobres_comprados = 0
    repetidas_totales = 0
    
    # Repetir hasta que se hayan obtenido las 100 estampas
    while album.sum() < N:
        # Sobre con 7 estampas distintas
        sobre = np.random.choice(opciones_estampas, size=S, replace=False)
        
        # Evaluar estampas ya obtenidas
        repetidas_en_sobre = album[sobre].sum()
        repetidas_totales += repetidas_en_sobre
        
        # Registrar las estampas
        album[sobre] = True
        sobres_comprados += 1
        
    # Almacenar los resultados finales
    resultados_sobres[i] = sobres_comprados
    resultados_repetidas[i] = repetidas_totales

# --- CÁLCULOS ESTADÍSTICOS ---
media_sobres = np.mean(resultados_sobres)
desviacion_sobres = np.std(resultados_sobres, ddof=1)

media_repetidas = np.mean(resultados_repetidas)
desviacion_repetidas = np.std(resultados_repetidas, ddof=1)

# Probabilidad de necesitar más de 30 sobres
probabilidad_mas_30 = np.mean(resultados_sobres > 30)

# Mínimo teórico de sobres necesarios: N / S (redondeado hacia arriba)
minimo_teorico = np.ceil(N / S)

print("="*60)
print("                 RESULTADOS DE LA SIMULACIÓN")
print("="*60)
print(f"Sobres necesarios  -> Media: {media_sobres:.2f} | Desv. Estándar: {desviacion_sobres:.2f}")
print(f"Estampas repetidas -> Media: {media_repetidas:.2f} | Desv. Estándar: {desviacion_repetidas:.2f}")
print(f"Probabilidad de requerir > 30 sobres: {probabilidad_mas_30 * 100:.2f}%")
print(f"Mínimo teórico de sobres: {int(minimo_teorico)}")
print("="*60)

# --- VISUALIZACIÓN ---
plt.figure(figsize=(10, 6))

# Dibujar el histograma
plt.hist(resultados_sobres, 
         bins=range(int(np.min(resultados_sobres)), int(np.max(resultados_sobres)) + 2), 
         color='skyblue', edgecolor='black', alpha=0.7)

# Trazar las líneas verticales solicitadas
plt.axvline(media_sobres, color='red', linestyle='dashed', linewidth=2, 
            label=f'Media Muestral ({media_sobres:.1f})')
plt.axvline(minimo_teorico, color='green', linestyle='solid', linewidth=2, 
            label=f'Mínimo Teórico ({int(minimo_teorico)})')

# Formatear el gráfico
plt.title('Distribución de Sobres Necesarios para Completar el Álbum\n(10,000 Simulaciones, $N=100$, $S=7$)', fontsize=14)
plt.xlabel('Número de Sobres Comprados', fontsize=12)
plt.ylabel('Frecuencia', fontsize=12)
plt.legend()
plt.grid(axis='y', alpha=0.4)
plt.tight_layout()

# Mostrar el resultado visual
plt.show()

#-------------------

# --- PARÁMETROS ---
N = 100
S = 7
R = 10000
np.random.seed(2026)

# Cantidades de sobres a evaluar
M_values = [20, 25, 30, 35, 40, 45, 50, 60, 70, 80]

probabilidades = []
print("Calculando probabilidades. Por favor, espera...")

# --- PROCEDIMIENTO ---
for M in M_values:
    albumes_completados = 0
    
    for _ in range(R):
        album = np.zeros(N, dtype=bool)
        
        # Comprar exactamente M sobres
        for _ in range(M):
            sobre = np.random.choice(N, size=S, replace=False)
            album[sobre] = True
            
        # Verificar si el álbum está 100% completo
        if album.sum() == N:
            albumes_completados += 1
            
    # Calcular la proporción: casos de éxito / total de simulaciones
    prob_estimada = albumes_completados / R
    probabilidades.append(prob_estimada)

# --- TABLA ---
print("\n" + "="*45)
print(" PROBABILIDAD DE COMPLETAR EL ÁLBUM (N=100)")
print("="*45)
print(f"{'Sobres Comprados (M)':<25} | {'Probabilidad Estimada'}")
print("-" * 45)
for m, p in zip(M_values, probabilidades):
    print(f"{m:<25} | {p:.4f}  ({p * 100:>5.2f}%)")
print("="*45)

# --- VISUALIZACIÓN ---
plt.figure(figsize=(10, 6))

# Crear el gráfico de barras (convertir M_values a string)
x_labels = [str(m) for m in M_values]
barras = plt.bar(x_labels, probabilidades, color='coral', edgecolor='black', zorder=2)

# Añadir la línea horizontal en P = 0.5
plt.axhline(y=0.5, color='darkblue', linestyle='--', linewidth=2, zorder=3, 
            label='Línea de 50% de Probabilidad (P=0.5)')

# Formatear el gráfico
plt.title('Probabilidad de Completar el Álbum Comprando "M" Sobres\n(10,000 Simulaciones por nivel, N=100, S=7)', fontsize=14)
plt.xlabel('Cantidad Exacta de Sobres Comprados (M)', fontsize=12)
plt.ylabel('Probabilidad Estimada (0 a 1)', fontsize=12)
plt.ylim(0, 1.05) # Límite Y hasta 1.05 para que no se pegue al borde
plt.grid(axis='y', linestyle='--', alpha=0.6, zorder=1)
plt.legend()

# Añadir las etiquetas de valor encima de cada barra
for barra, prob in zip(barras, probabilidades):
    altura = barra.get_height()
    if altura > 0.005:  # Solo mostrar si el valor es visible
        plt.text(barra.get_x() + barra.get_width()/2., altura + 0.02,
                 f'{prob:.2f}', ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.show()