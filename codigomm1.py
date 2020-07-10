import numpy as np
import matplotlib.pyplot as plt
import statistics
# Variables globales
cant_tipo_evento = 2# Defimos número de tipos de eventos (usamos 2: arribos y llegadas)
# Criterio de estabilidad MM1: la tasa de servicio debe ser mayor que la tasa de llegada
# tiempo medio de servicio   MU
total_clientes = 200# número total de clientes cuyas demoras serán observadas
time = 0.0# Reloj de simulación
estado = 0 # 0: si el servidor está ocioso - 1: si el servidor está ocupado
ancc=0.0 # área debajo de la función número de clientes en cola
ncc=0 # número de clientes en cola
tiempo_ultimo_evento=0.0 # tiempo del último evento que cambió el número en cola
num_clientes = 0 # número de clientes que completaron sus demoras
arreglo_prox_event = np.zeros([cant_tipo_evento + 1]) # arreglo que contiene el tiempo del próximo evento I en la posición ARREGLO_PROX_EV[I]
tiempo_total_demoras=0.0 # tiempo total de los clientes que completaron sus demoras
tiempo_prox_evento = 0.0 # tiempo de ocurrencia del próximo evento a ocurrir
tipo_prox_evento = 0 # tipo de evento (1: ARRIBOS o 2: PARTIDAS) del próximo evento que va a ocurrir
arreglo_tiempos_arribo = np.zeros([total_clientes + 1]) # tiempo de arribo del cliente I que está esperando en cola
tiempo_servicio_acumulado = 0.0
area_server_status = 0.0
# Subrutina init
def inicializar():
    global time, estado, ncc, tiempo_ultimo_evento, num_clientes, area_server_status, tiempo_total_demoras, ancc, arreglo_prox_event, tiempo_prox_evento, tipo_prox_evento, arreglo_tiempos_arribo,tiempo_servicio_acumulado
    # inicializamos.0 el reloj de simulación
    time = 0.0
    # inicializamos variables de estado
    estado = 0 # 0: si el servidor está ocioso - 1: si el servidor está ocupado
    ncc=0 # número de clientes en cola
    tiempo_ultimo_evento=0.0 # tiempo del último evento que cambió el número en cola
    # inicializamos contadores estadísticos
    num_clientes = 0 # número de clientes que completaron sus demoras
    tiempo_total_demoras=0.0 # tiempo total de los clientes que completaron sus demoras
    ancc=0.0 # área debajo de la función número de clientes en cola
    arreglo_prox_event = np.zeros([cant_tipo_evento + 1]) # arreglo que contiene el tiempo del próximo evento I en la posición ARREGLO_PROX_EV[I]
    tiempo_prox_evento = 0.0 # tiempo de ocurrencia del próximo evento a ocurrir
    tipo_prox_evento = 0 # tipo de evento (1: ARRIBOS o 2: PARTIDAS) del próximo evento que va a ocurrir
    arreglo_tiempos_arribo = np.zeros([total_clientes + 1]) # tiempo de arribo del cliente I que está esperando en cola
    tiempo_servicio_acumulado = 0.0
    # inicializamos lista de eventos. Como no hay clientes en cola, se define el tiempo de la próxima salida en infinito.
    arreglo_prox_event[1] = time + np.random.exponential(1 / tiempo_medio_llegada)# stats.expon(TIEMPO_# tiempo actual + valor generado exponencialmente con lambda = tiempo medio de llegada
    arreglo_prox_event[2] = 1e30 # Lo seteamos en infinito
    area_server_status = 0.0
    return None
# Subrutina timing
def timing():
    global time,arreglo_prox_event, tipo_prox_evento, tiempo_prox_evento, cant_tipo_evento
    tiempo_prox_evento = 1e29 # tiempo de ocurrencia del próximo evento a ocurrir
    tipo_prox_evento = 0
    # determinamos el tipo de evento del próximo evento que va a ocurrir
    for i in range(1, cant_tipo_evento + 1):
        if arreglo_prox_event[i] <tiempo_prox_evento:
            tiempo_prox_evento = arreglo_prox_event[i]
            tipo_prox_evento = i
            # veo que la lista de eventos no esté vacia
    if tipo_prox_evento >0:
        time = tiempo_prox_evento
        return 0
        # si la lista de eventos está vacía, fin de simulación
    else:
        print('Lista de eventos vacias. Fin de la simulacion')
        return 1
# Subrutina arribos
def arribo():
    global estado,tiempo_total_demoras,num_clientes,arreglo_tiempos_arribo,arreglo_prox_event, tiempo_ultimo_evento, tiempo_servicio_acumulado, ancc, ncc #programamos el próximo arribo
    arreglo_prox_event[1] = time + np.random.exponential(1 / tiempo_medio_llegada)# stats.expon(TIEMPO_# tiempo actual + valor generado exponencialmente con lambda = tiempo medio de llegada
    # Vemos el estado del servidor, si está vacío (=0) comienza el servicio el cliente que arribó
    if estado == 1: # servidor ocupado, actualizamos área debajo de la función número de clientes en cola
        ancc += ncc * (time - tiempo_ultimo_evento)
        tiempo_ultimo_evento = time
        # agregamos uno al número de clientes en cola
        ncc += 1
        # verificamos condición de máximos clientes en cola TOTAL_CLIENTES
        if ncc <= total_clientes:
            # ARREGLO_TIEMPOS_ARRIBO: tiempo de arribo del cliente I que está esperando en cola
            arreglo_tiempos_arribo[ncc] = time
        else:
            print('SE alcanxo el limite de clientes a observar')
    else:
        # servidor ocioso, cliente tiene demora nula
        DEMORA = 0.0
        # cambiamos estado del servidor a ocupado
        estado = 1
        tiempo_total_demoras += DEMORA
        # agregamos uno al número de clientes que completaron su demora
        num_clientes += 1
        # generamos la salida
        arreglo_prox_event[2] = time + np.random.exponential(1 / tiempo_medio_servicio)# stats.expon(TIEMPO_# tiempo actual + valor generado exponencialmente con lambda = tiempo medio de servicio
        tiempo_servicio_acumulado += (arreglo_prox_event[2] - time)
# Subrutina partidas
def partida():
    global ncc, estado, ancc, time, tiempo_ultimo_evento, arreglo_tiempos_arribo, tiempo_total_demoras,arreglo_prox_event, DEMORA, num_clientes, tiempo_medio_servicio,tiempo_servicio_acumulado
    # si la cola está vacía, cambiamos el estado del servidor a ocioso
    # y seteamos el tiempo del próximo evento de partida en infinito
    if ncc >0:
        # la cola no está vacía
        # actualizamos el área debajo de la función de números de clientes en cola
        ancc += ncc * (time - tiempo_ultimo_evento)
        tiempo_ultimo_evento = time
        # restamos uno del número de clientes en cola
        ncc -= 1# NCC
        # calculamos la demora del cliente que está comenzando el servicio
        DEMORA = time - arreglo_tiempos_arribo[1]# Para mi esto está mal, en lugar de 1 debería ser NCC
        tiempo_total_demoras += DEMORA
        #agregamos uno al número de clientes que completaron su demora
        num_clientes += 1
        # calculamos la partida
        arreglo_prox_event[2] = time + np.random.exponential(1 / tiempo_medio_servicio)# stats.expon(TIEMPO_# tiempo actual + valor generado exponencialmente con lambda = tiempo medio de servicio
        tiempo_servicio_acumulado += (arreglo_prox_event[2] - time)
        # si la cola no está vacía, mover cada cliente de la cola en una posición
    if ncc != 0:
        for i in range(1, ncc + 1):
            j = i + 1
            arreglo_tiempos_arribo[i]=arreglo_tiempos_arribo[j]
    else:
    # marcamos el servidor como libre
        estado = 0
        arreglo_prox_event[2] = 10.0 ** 30 # Lo seteamos en infinito
    return None
# Subrutina reportes
def report():
    global tiempo_medio_llegada, tiempo_medio_servicio, total_clientes, num_clientes, ancc, tiempo_total_demoras, time, tiempo_servicio_acumulado
    # mostramos encabezado y parámetros de entrada
    # print("Sistema de cola simple")
    # print("Tiempo medio entre arribos:", TIEMPO_MEDIO_LLEGADA,’ minutos’)# , ’. Tasa de llegadas:’, 1/TIEMPO_MEDIO_LLEGADA)
    # print("Tiempo medio de servicio:", TIEMPO_MEDIO_SERVICIO,’ minutos’)# , ’. Tasa de servicio:’, 1/TIEMPO_MEDIO_SERVICIO)
    # print("Número máximo de clientes:", TOTAL_CLIENTES)
    prom_clientes_sistema_calc = num_clientes / time # promedio de clientes en el sistema
    prom_clientes_cola_calc = ancc / time# print("Número promedio de clientes en cola", AVGNCC)
    prom_demora_sistema_calc=tiempo_total_demoras / total_clientes #demora promedio en el sistema
    prom_demora_cola_calc = tiempo_total_demoras / num_clientes # print("Demora promedio en cola:",AVGDEL,’ minutos’)
    prom_ut_serv_calc = tiempo_servicio_acumulado / time # print(Ütilización promedio del servidor:",AVGUTSERV)
    print("Numero promedio de clientes en el sistema: " , prom_clientes_sistema_calc)
    print('Numero promedio de clientes en cola', round(prom_clientes_cola_calc, 2))
    print("Demora promedio en el sistema: " + str(tiempo_total_demoras / total_clientes))
    print('Demora promedio en cola:', round(prom_demora_cola_calc, 2), 'minutos.')
    print('Utilización promedio del servidor:', "{:.2%}".format(prom_ut_serv_calc))
    return [prom_clientes_sistema_calc, prom_clientes_cola_calc, prom_demora_sistema_calc, prom_demora_cola_calc, prom_ut_serv_calc]
# Programa principal
# l:lambda; mu:mu
tiempo_medio_llegada= float(input("Ingrese tiempo medio de arribos (minutos): "))
tiempo_medio_servicio= float(input("Ingrese tiempo medio de servicio (minutos): "))
print('=====================================================')
# Valores teóricos
promedio_utilizacion_servidor = tiempo_medio_llegada / tiempo_medio_servicio
promedio_clientes_cola = promedio_utilizacion_servidor ** 2 / (1 - promedio_utilizacion_servidor)
promedio_demora_cola = promedio_clientes_cola / tiempo_medio_llegada
promedio_demora_sistema = promedio_demora_cola + 1 / tiempo_medio_servicio
promedio_clientes_sistema = tiempo_medio_llegada * promedio_demora_sistema
print('Valores teoricos')
print('promedio clientes en cola', promedio_clientes_cola)
print('promedio clientes en sistema', promedio_clientes_sistema)
print('promedio demora en cola', promedio_demora_cola)
print('promedio utilixacion del sistema', promedio_utilizacion_servidor)
print('=====================================================')
util_corridas, demora_cola_corridas, clientes_cola_corridas, time_corridas, demora_sistema_corridas, clientes_sistema_corridas = [], [], [], [], [], []
for i in range(10):
    time_acum, server_acum, niq_acum=[], [], []
    reporte = ()
    # iniciamos la simulación, llamamos subrutina init
    inicializar()
    # si la simulación terminó, llamamos la rutina de reportes y fin de la simulación
    while num_clientes <= total_clientes:# no terminó simulación
    # determinamos próximo evento, llamamos subrutina timing
        timing()
        if timing() == 0:
            # update_time_avg_stats()
            time_since_last_event = time - tiempo_ultimo_evento
            tiempo_ultimo_evento = time
            time_acum.append(time)
            server_acum.append(estado)
            niq_acum.append(ncc)
            ancc = ancc + (ncc * time_since_last_event)
            area_server_status = area_server_status + (estado * time_since_last_event)
    # vemos qué tipo de evento es el próximo
            if tipo_prox_evento == 1:
            # llamamos la rutina de arribos de eventos
                arribo()
            else:
                # llamamos la rutina de partidas
                partida()
        elif timing() == 1:
            break# terminó simulación
            # llamamos a la subrutina de reporte
    print("Corrida nº: ", i+1 ,"=====")
    report()
    clientes_sistema_corridas.append(tiempo_medio_llegada * ((tiempo_total_demoras / num_clientes) + (1 / tiempo_medio_servicio)))
    demora_sistema_corridas.append((tiempo_total_demoras / num_clientes) + (1 / tiempo_medio_servicio))
    util_corridas.append(area_server_status / time)
    demora_cola_corridas.append(tiempo_total_demoras / num_clientes)
    clientes_cola_corridas.append(ancc / time)
    time_corridas.append(time)


def graficar(proms, prom_esp, tit, ylbl):
    plt.title(tit)
    plt.xlabel('Corrida')
    plt.ylabel(ylbl)
    plt.bar([x for x in range(len(proms))], [prom_esp for i in range(len(proms))], label = "{} Esperada".format(ylbl), color = "g", width = 0.25)
    plt.bar([x+0.25 for x in range(len(proms))], proms, label = "{} Observada".format(ylbl), color = "violet", width = 0.25)
    plt.xticks([x+0.15 for x in range(len(proms))], [x for x in range(len(proms))])
    plt.legend(loc='lower right', prop={'size': 7})
    plt.show()


print("\nPromedios de las corridas: ====")
print("Promedio de la utilizacion del servidor: ", np.mean(util_corridas))
print("Promedio de tiempo promedio en cola:", np.mean(demora_cola_corridas))
print("Promedio de numero de clientes promedio en cola:", np.mean(clientes_cola_corridas))
print("Promedio de tiempo promedio en el sistema:", np.mean(demora_sistema_corridas))
print("Promedio de numero de clientes promedio en el sistema:", np.mean(clientes_sistema_corridas))
graficar(util_corridas, promedio_utilizacion_servidor, 'Utilización del servidor', 'B(t)') 
graficar(demora_cola_corridas, promedio_demora_cola, 'Demora promedio en cola', 'Dq(n)')   
graficar(clientes_cola_corridas, promedio_clientes_cola, 'Clientes promedio en cola', 'Q(t)')    
graficar(demora_sistema_corridas, promedio_demora_sistema, 'Demora promedio en el sistema', 'Ds(n)')    
graficar(clientes_sistema_corridas, promedio_clientes_sistema, 'Clientes promedio en el sistema', 'S(t)')   
