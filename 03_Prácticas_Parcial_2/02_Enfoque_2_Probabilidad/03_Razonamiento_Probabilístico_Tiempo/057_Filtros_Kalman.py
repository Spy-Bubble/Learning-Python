import numpy as np

# ============================================================================
# 20. FILTROS DE KALMAN
# ============================================================================

class FiltroKalman:
    """
    Filtro de Kalman para sistemas lineales con ruido gaussiano
    """
    def __init__(self, F, H, Q, R, x0, P0):
        """
        Args:
            F: matriz de transición de estado
            H: matriz de observación
            Q: covarianza del ruido del proceso
            R: covarianza del ruido de medición
            x0: estado inicial (vector)
            P0: covarianza inicial (matriz)
        """
        self.F = np.array(F)  # Transición
        self.H = np.array(H)  # Observación
        self.Q = np.array(Q)  # Ruido proceso
        self.R = np.array(R)  # Ruido medición
        self.x = np.array(x0)  # Estado
        self.P = np.array(P0)  # Covarianza
    
    def predecir(self):
        """Paso de predicción"""
        # x_k = F * x_{k-1}
        self.x = self.F @ self.x
        # P_k = F * P_{k-1} * F' + Q
        self.P = self.F @ self.P @ self.F.T + self.Q
        
        return self.x, self.P
    
    def actualizar(self, z):
        """
        Paso de actualización con medición
        Args:
            z: vector de medición
        """
        z = np.array(z)
        
        # Innovación: y = z - H * x_k
        y = z - self.H @ self.x
        
        # Covarianza de la innovación: S = H * P_k * H' + R
        S = self.H @ self.P @ self.H.T + self.R
        
        # Ganancia de Kalman: K = P_k * H' * S^{-1}
        K = self.P @ self.H.T @ np.linalg.inv(S)
        
        # Actualizar estado: x_k = x_k + K * y
        self.x = self.x + K @ y
        
        # Actualizar covarianza: P_k = (I - K * H) * P_k
        I = np.eye(self.x.shape[0])
        self.P = (I - K @ self.H) @ self.P
        
        return self.x, self.P

# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == "__main__":
    print("=== 20. Filtro de Kalman ===\n")
    
    # Sistema simple: posición con velocidad constante
    # Estado: [posición, velocidad]
    # Observación: solo posición
    
    dt = 1.0 # Intervalo de tiempo
    
    # x_t = x_{t-1} + v_{t-1} * dt
    # v_t = v_{t-1}
    F = [[1, dt], [0, 1]]   # Matriz de transición
    
    # z = [1, 0] * [x, v]'
    H = [[1, 0]]            # Matriz de observación (solo vemos posición)
    
    Q = [[0.1, 0], [0, 0.1]] # Ruido del proceso (incertidumbre en modelo)
    R = [[1.0]]             # Ruido de medición (incertidumbre del sensor)
    x0 = [0, 1]             # Estado inicial: pos=0, vel=1
    P0 = [[1, 0], [0, 1]]    # Covarianza inicial (incertidumbre inicial)
    
    kf = FiltroKalman(F, H, Q, R, x0, P0)
    
    # Simular mediciones (verdad = 1, 2, 3, 4, 5)
    mediciones = [1.1, 2.05, 2.9, 4.1, 5.2]
    
    print(f"   Estado inicial: {x0}")
    for i, z in enumerate(mediciones):
        kf.predecir()
        estado, cov = kf.actualizar([z])
        print(f"   Tiempo {i+1}: medición={z:.2f}, estimado_pos={estado[0]:.2f}, estimado_vel={estado[1]:.2f}")