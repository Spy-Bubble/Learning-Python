# ============================================================================
# 7. RED BAYESIANA
# ============================================================================

class RedBayesiana:
    """
    Representa una Red Bayesiana (grafo dirigido acíclico con probabilidades)
    """
    def __init__(self):
        self.nodos = {}  # {nombre: Nodo}
        self.estructura = {}  # {hijo: [padres]}
    
    def agregar_nodo(self, nombre, padres, tabla_prob):
        """
        Agrega un nodo a la red
        Args:
            nombre: nombre del nodo
            padres: lista de nombres de nodos padres
            tabla_prob: dict con P(nodo|padres)
        """
        self.nodos[nombre] = {
            'padres': padres,
            'tabla': tabla_prob
        }
        self.estructura[nombre] = padres
    
    def prob_dado_padres(self, nodo, valor, valores_padres):
        """
        Obtiene P(nodo=valor|padres)
        Args:
            nodo: nombre del nodo
            valor: valor del nodo
            valores_padres: dict {padre: valor}
        Returns:
            probabilidad
        """
        tabla = self.nodos[nodo]['tabla']
        padres = self.nodos[nodo]['padres']
        
        # Sin padres
        if not padres:
            return tabla.get(valor, 0)
        
        # Con padres: buscar en tabla
        # Construir la clave de la tabla (Valor, Padre1_val, Padre2_val, ...)
        clave_padres = tuple(valores_padres.get(p) for p in padres)
        clave_completa = (valor,) + clave_padres
        
        return tabla.get(clave_completa, 0)

# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 7. Red Bayesiana ===\n")
    
    # Crear una red bayesiana simple: Alarma
    # Robo → Alarma ← Terremoto
    
    print("Creando red simple (Robo -> Alarma)...")
    red = RedBayesiana()
    
    # Nodos sin padres
    red.agregar_nodo('Robo', [], {
        True: 0.001,
        False: 0.999
    })
    
    red.agregar_nodo('Terremoto', [], {
        True: 0.002,
        False: 0.998
    })
    
    # Alarma depende de Robo y Terremoto
    red.agregar_nodo('Alarma', ['Robo', 'Terremoto'], {
        # (Valor, Robo_val, Terremoto_val)
        (True, True, True): 0.95,
        (False, True, True): 0.05,
        (True, True, False): 0.94,
        (False, True, False): 0.06,
        (True, False, True): 0.29,
        (False, False, True): 0.71,
        (True, False, False): 0.001,
        (False, False, False): 0.999,
    })
    
    print("   Red creada con 3 nodos.\n")
    
    # Consultar una probabilidad
    # P(Alarma=True | Robo=True, Terremoto=False)
    prob = red.prob_dado_padres('Alarma', True, {'Robo': True, 'Terremoto': False})
    print(f"   P(Alarma=T | Robo=T, Terremoto=F) = {prob}")