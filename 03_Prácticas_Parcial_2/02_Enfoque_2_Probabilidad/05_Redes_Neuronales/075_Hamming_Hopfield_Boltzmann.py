import random
import math
import numpy as np # Necesario para Boltzmann

# ============================================================================
# 38. HAMMING, HOPFIELD, HEBB, BOLTZMANN
# ============================================================================

# --- Red de Hamming ---
class RedHamming:
    """
    Red de Hamming para reconocimiento de patrones binarios/bipolares
    Encuentra el patrón memorizado más cercano (menor distancia Hamming).
    """
    def __init__(self, patrones):
        if not patrones:
             raise ValueError("Se necesita al menos un patrón.")
        self.patrones = [list(p) for p in patrones]
        self.num_patrones = len(patrones)
        self.dim = len(patrones[0])

    def _distancia_hamming(self, p1, p2):
        return sum(a != b for a, b in zip(p1, p2))

    def reconocer(self, entrada):
        if len(entrada) != self.dim:
             raise ValueError(f"La entrada debe tener dimensión {self.dim}")
        min_dist = float('inf')
        mejor_patron = None
        for idx, patron in enumerate(self.patrones):
            dist = self._distancia_hamming(entrada, patron)
            if dist < min_dist:
                min_dist = dist
                mejor_patron = patron
        return mejor_patron


# --- Red de Hopfield ---
class RedHopfield:
    """
    Red de Hopfield para memoria asociativa (patrones bipolares -1, 1)
    """
    def __init__(self, num_neuronas):
        self.n = num_neuronas
        self.pesos = [[0.0 for _ in range(num_neuronas)]
                       for _ in range(num_neuronas)]

    def entrenar_hebb(self, patrones):
        if not patrones: return
        if any(len(p) != self.n for p in patrones):
             raise ValueError(f"Todos los patrones deben tener longitud {self.n}")
        self.pesos = [[0.0 for _ in range(self.n)] for _ in range(self.n)]
        num_patrones = len(patrones)
        for patron in patrones:
            for i in range(self.n):
                for j in range(self.n):
                    if i != j:
                        self.pesos[i][j] += patron[i] * patron[j]
        for i in range(self.n):
            for j in range(self.n):
                # Normalizar por N (número de neuronas) es más común que por P (número de patrones)
                # para la estabilidad, aunque ambas se usan.
                self.pesos[i][j] /= self.n

    def _activacion_sign(self, x):
        return 1 if x >= 0 else -1

    def actualizar_asincrono(self, estado_actual):
        nuevo_estado = list(estado_actual)
        i = random.randrange(self.n)
        suma_ponderada = sum(self.pesos[i][j] * nuevo_estado[j] for j in range(self.n))
        nuevo_estado[i] = self._activacion_sign(suma_ponderada)
        return nuevo_estado

    # --- MÉTODO DESCOMENTADO ---
    # Actualización síncrona (todas a la vez)
    def actualizar_sincrono(self, estado_actual):
        nuevo_estado = [0] * self.n
        for i in range(self.n):
            suma_ponderada = sum(self.pesos[i][j] * estado_actual[j] for j in range(self.n))
            nuevo_estado[i] = self._activacion_sign(suma_ponderada)
        return nuevo_estado
    # --- FIN MÉTODO DESCOMENTADO ---

    def recuperar(self, patron_ruidoso, max_iter=100, modo='asincrono'):
        if len(patron_ruidoso) != self.n:
             raise ValueError(f"El patrón debe tener longitud {self.n}")
        estado = list(patron_ruidoso)
        for iter_num in range(max_iter):
            estado_previo = list(estado) # Guardar estado antes de actualizar
            if modo == 'asincrono':
                # Iterar N veces para dar oportunidad a todas las neuronas
                for _ in range(self.n):
                    estado = self.actualizar_asincrono(estado)
                # Verificar convergencia después de un ciclo completo
                if estado == estado_previo:
                    #print(f"Hopfield convergió (asíncrono) en iteración {iter_num+1}")
                    break
            else: # Síncrono
                 estado = self.actualizar_sincrono(estado) # Llamada ahora funciona
                 # Verificar convergencia
                 if estado == estado_previo:
                     #print(f"Hopfield convergió (síncrono) en iteración {iter_num+1}")
                     break
        # else: # Se ejecutó si el bucle for terminó sin break
        #     print(f"Hopfield no convergió después de {max_iter} iteraciones.")

        return estado


# --- Máquina de Boltzmann (Simplificada - RBM) ---
class MaquinaBoltzmann:
    """
    Máquina de Boltzmann Restringida (RBM) - Conceptual
    Conexiones solo entre capa visible y oculta. Usa Numpy.
    """
    def __init__(self, num_visibles, num_ocultas, temperatura=1.0, lr=0.1):
        self.nv = num_visibles
        self.nh = num_ocultas
        self.T = temperatura # Usado en muestreo Gibbs, no tanto en RBM estándar
        self.lr = lr
        self.pesos = np.random.randn(num_visibles, num_ocultas) * 0.1
        self.bias_v = np.zeros(num_visibles)
        self.bias_h = np.zeros(num_ocultas)

    def _sig(self, x):
        return 1.0 / (1.0 + np.exp(-x / self.T)) # Incluir Temperatura si es BM completa

    def prob_h_dado_v(self, v):
        activacion = v @ self.pesos + self.bias_h
        return self._sig(activacion)

    def prob_v_dado_h(self, h):
        activacion = h @ self.pesos.T + self.bias_v
        return self._sig(activacion)

    def muestrear_h_dado_v(self, v):
        probs_h = self.prob_h_dado_v(np.array(v)) # Asegurar numpy array
        return (np.random.rand(self.nh) < probs_h).astype(int)

    def muestrear_v_dado_h(self, h):
        probs_v = self.prob_v_dado_h(np.array(h)) # Asegurar numpy array
        return (np.random.rand(self.nv) < probs_v).astype(int)
    # Entrenamiento (ej. Contrastive Divergence) omitido.

# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 38. Hamming, Hopfield, Boltzmann ===\n")

    # --- Red de Hamming ---
    print("Red de Hamming:")
    patrones_hamming = [[1, 0, 1, 0], [0, 1, 0, 1], [1, 1, 1, 1]]
    hamming_net = RedHamming(patrones_hamming)
    entrada_hamming = [1, 0, 0, 0]
    reconocido = hamming_net.reconocer(entrada_hamming)
    print(f"   Patrones memorizados: {patrones_hamming}")
    print(f"   Entrada: {entrada_hamming}")
    print(f"   Patrón reconocido: {reconocido}\n")

    # --- Red de Hopfield ---
    print("Red de Hopfield:")
    patron1_hop = [ 1,  1, -1, -1]
    patron2_hop = [-1, -1,  1,  1]
    hopfield_net = RedHopfield(num_neuronas=4)
    hopfield_net.entrenar_hebb([patron1_hop, patron2_hop])
    ruidoso_hop = [ 1, -1, -1, -1]
    recuperado_hop = hopfield_net.recuperar(ruidoso_hop, max_iter=20, modo='asincrono')
    print(f"   Patrones memorizados: {patron1_hop}, {patron2_hop}")
    print(f"   Patrón ruidoso: {ruidoso_hop}")
    print(f"   Patrón recuperado (asíncrono): {recuperado_hop}")
    # Prueba síncrona (si se descomentó y corrigió recuperar)
    # recuperado_sync = hopfield_net.recuperar(ruidoso_hop, max_iter=20, modo='sincrono')
    # print(f"   Patrón recuperado (síncrono): {recuperado_sync}\n")


    # --- Máquina de Boltzmann (RBM - Conceptual) ---
    print("\nMáquina de Boltzmann (RBM - Conceptual):")
    rbm = MaquinaBoltzmann(num_visibles=4, num_ocultas=2)
    v_entrada = np.array([1, 0, 1, 0])
    prob_h = rbm.prob_h_dado_v(v_entrada)
    muestra_h = rbm.muestrear_h_dado_v(v_entrada)
    prob_v_rec = rbm.prob_v_dado_h(muestra_h)
    muestra_v_rec = rbm.muestrear_v_dado_h(muestra_h)
    print(f"   RBM creada ({rbm.nv} visibles, {rbm.nh} ocultas)")
    print(f"   Entrada visible: {v_entrada}")
    print(f"   Prob. activación ocultas P(h=1|v): {[f'{p:.2f}' for p in prob_h]}")
    print(f"   Muestra oculta h: {muestra_h}")
    print(f"   Prob. reconstrucción visibles P(v=1|h): {[f'{p:.2f}' for p in prob_v_rec]}")
    print(f"   Muestra reconstruida v': {muestra_v_rec}")