import numpy as np
import matplotlib.pyplot as plt

# Semilla
np.random.seed(2026)

#ETAPA 1
# --- PARÁMETROS ---
N = 100          # Número total de estampas diferentes
S = 7            # Estampas por sobre (sin repetir dentro del sobre)
R = 10000        # Número de simulaciones a realizar

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
