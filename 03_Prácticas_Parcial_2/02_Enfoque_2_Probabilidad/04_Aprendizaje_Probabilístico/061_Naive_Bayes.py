import math
from collections import defaultdict

# ============================================================================
# 24. NAÏVE BAYES
# ============================================================================

class NaiveBayes:
    """
    Clasificador Naïve Bayes (para features categóricas)
    """
    def __init__(self, alpha=1.0): # alpha para suavizado de Laplace
        self.clases = []
        self.prior = {}             # P(clase)
        self.verosimilitud = {}     # P(feature=valor|clase)
        self.alpha = alpha          # Parámetro de suavizado
        self.vocabulario_features = defaultdict(set) # Para suavizado
        self.y_train = []           # Guardar etiquetas para suavizado en predecir
        self.conteo_clases = {}     # Guardar conteos para suavizado en predecir

    def entrenar(self, X, y):
        """
        Entrena el clasificador
        Args:
            X: lista de ejemplos (cada ejemplo es lista de features)
            y: lista de etiquetas de clase
        """
        self.y_train = y # Guardar etiquetas
        n_samples = len(y)
        if n_samples == 0: return
        n_features = len(X[0])

        # Contar clases y calcular prior P(clase)
        self.clases = list(set(y))
        self.conteo_clases = {c: y.count(c) for c in self.clases}
        self.prior = {c: count/n_samples for c, count in self.conteo_clases.items()}

        # Calcular verosimilitud P(feature=valor|clase)
        self.verosimilitud = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
        conteos_features = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

        # Llenar vocabulario y conteos iniciales
        for f_idx in range(n_features):
             for sample in X:
                 self.vocabulario_features[f_idx].add(sample[f_idx])

        # Contar ocurrencias de feature=valor para cada clase
        for i in range(n_samples):
            label = y[i]
            sample = X[i]
            for f_idx in range(n_features):
                valor = sample[f_idx]
                conteos_features[label][f_idx][valor] += 1

        # Calcular probabilidades con suavizado de Laplace
        for clase in self.clases:
            for f_idx in range(n_features):
                vocab_size = len(self.vocabulario_features[f_idx])
                denominador = self.conteo_clases[clase] + self.alpha * vocab_size
                if denominador == 0: continue # Evitar división por cero si la clase no tiene ejemplos

                for valor in self.vocabulario_features[f_idx]:
                    numerador = conteos_features[clase][f_idx][valor] + self.alpha
                    self.verosimilitud[clase][f_idx][valor] = numerador / denominador

    def predecir(self, ejemplo):
        """
        Predice la clase de un ejemplo
        Args:
            ejemplo: lista de features
        Returns:
            clase predicha
        """
        mejor_clase = None
        mejor_log_prob = float('-inf')

        for clase in self.clases:
            # log P(clase|ejemplo) ∝ log P(clase) + Σ log P(feature|clase)
            log_prob_clase = math.log(self.prior[clase])

            for f_idx, valor in enumerate(ejemplo):
                # Obtener verosimilitud P(valor | clase)
                prob = self.verosimilitud[clase][f_idx].get(valor)

                # Si el valor no se vio durante el entrenamiento para esta clase/feature,
                # calcular la probabilidad suavizada
                if prob is None:
                    vocab_size = len(self.vocabulario_features[f_idx])
                    denominador = self.conteo_clases[clase] + self.alpha * vocab_size
                    if denominador == 0:
                        prob = 1e-9 # Evitar log(0), asignar probabilidad muy baja
                    else:
                        prob = self.alpha / denominador
                elif prob == 0: # Si la probabilidad calculada fue 0 (raro con suavizado)
                    prob = 1e-9

                log_prob_clase += math.log(prob)

            if log_prob_clase > mejor_log_prob:
                mejor_log_prob = log_prob_clase
                mejor_clase = clase

        return mejor_clase

# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 24. Naïve Bayes ===\n")

    # Clasificar si jugar tenis según clima
    X_train = [
        ['soleado', 'caliente', 'alta', 'debil'],
        ['soleado', 'caliente', 'alta', 'fuerte'],
        ['nublado', 'caliente', 'alta', 'debil'],
        ['lluvioso', 'templado', 'alta', 'debil'],
        ['lluvioso', 'frio', 'normal', 'debil'],
        ['nublado', 'frio', 'normal', 'fuerte'],
        ['soleado', 'templado', 'normal', 'debil'],
        ['lluvioso', 'templado', 'normal', 'fuerte'],
    ]
    y_train = ['no', 'no', 'si', 'si', 'si', 'no', 'si', 'no'] # si=4, no=4

    nb = NaiveBayes(alpha=1.0)
    nb.entrenar(X_train, y_train)

    ejemplo_test = ['soleado', 'templado', 'alta', 'debil']
    prediccion = nb.predecir(ejemplo_test)
    print(f"   Datos de entrenamiento (jugar tenis):")
    #for x, y in zip(X_train, y_train): print(f"      {x} -> {y}")
    print(f"   Ejemplo a clasificar: {ejemplo_test}")
    print(f"   Predicción: Jugar = '{prediccion}'\n")

    # Debug: Ver probabilidades
    # print("Prior:", nb.prior)
    # print("Verosimilitud (ejemplo): P(soleado|si) =", nb.verosimilitud['si'][0].get('soleado'))
    # print("Verosimilitud (ejemplo): P(soleado|no) =", nb.verosimilitud['no'][0].get('soleado'))