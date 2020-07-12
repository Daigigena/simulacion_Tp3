import numpy as np
import matplotlib.pyplot as plt
import statistics
# Variables globales
cant_tipo_evento = 2# Defimos número de tipos de eventos (usamos 2: arribos y llegadas)
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
    arreglo_prox_event[1] = time + np.random.exponential(1 / tiempo_medio_llegada)
    arreglo_prox_event[2] = 1e30 
    area_server_status = 0.0
    return None
def timing():
    global time,arreglo_prox_event, tipo_prox_evento, tiempo_prox_evento, cant_tipo_evento
    tiempo_prox_evento = 1e29
    tipo_prox_evento = 0
    for i in range(1, cant_tipo_evento + 1):
        if arreglo_prox_event[i] <tiempo_prox_evento:
            tiempo_prox_evento = arreglo_prox_event[i]
            tipo_prox_evento = i
    if tipo_prox_evento >0:
        time = tiempo_prox_evento
        return 0
    else:
        print('Lista de eventos vacias. Fin de la simulacion')
        return 1
def arribo():
    global estado,tiempo_total_demoras,num_clientes,arreglo_tiempos_arribo,arreglo_prox_event, tiempo_ultimo_evento, tiempo_servicio_acumulado, ancc, ncc 
    arreglo_prox_event[1] = time + np.random.exponential(1 / tiempo_medio_llegada)
    if estado == 1:
        ancc += ncc * (time - tiempo_ultimo_evento)
        tiempo_ultimo_evento = time
        ncc += 1
        if ncc <= total_clientes:
            arreglo_tiempos_arribo[ncc] = time
        else:
            print('Se alcanzó el limite de clientes a observar')
    else:
        DEMORA = 0.0
        estado = 1
        tiempo_total_demoras += DEMORA
        num_clientes += 1
        arreglo_prox_event[2] = time + np.random.exponential(1 / tiempo_medio_servicio)
        tiempo_servicio_acumulado += (arreglo_prox_event[2] - time)
def partida():
    global ncc, estado, ancc, time, tiempo_ultimo_evento, arreglo_tiempos_arribo, tiempo_total_demoras,arreglo_prox_event, DEMORA, num_clientes, tiempo_medio_servicio,tiempo_servicio_acumulado
    if ncc >0:
        ancc += ncc * (time - tiempo_ultimo_evento)
        tiempo_ultimo_evento = time
        ncc -= 1
        DEMORA = time - arreglo_tiempos_arribo[1]
        tiempo_total_demoras += DEMORA
        num_clientes += 1
        arreglo_prox_event[2] = time + np.random.exponential(1 / tiempo_medio_servicio)
        tiempo_servicio_acumulado += (arreglo_prox_event[2] - time)
    if ncc != 0:
        for i in range(1, ncc + 1):
            j = i + 1
            arreglo_tiempos_arribo[i]=arreglo_tiempos_arribo[j]
    else:
        estado = 0
        arreglo_prox_event[2] = 10.0 ** 30 
    return None
def report():
    global tiempo_medio_llegada, tiempo_medio_servicio, total_clientes, num_clientes, ancc, tiempo_total_demoras, time, tiempo_servicio_acumulado
    prom_clientes_sistema_calc = num_clientes / time 
    prom_clientes_cola_calc = ancc / time
    prom_demora_sistema_calc=tiempo_total_demoras / total_clientes 
    prom_demora_cola_calc = tiempo_total_demoras / num_clientes 
    prom_ut_serv_calc = tiempo_servicio_acumulado / time 
    print('Sistema de cola simple')
    print("Numero promedio de clientes en el sistema: " , prom_clientes_sistema_calc)
    print('Numero promedio de clientes en cola', round(prom_clientes_cola_calc, 2))
    print("Demora promedio en el sistema: " + str(tiempo_total_demoras / total_clientes))
    print('Demora promedio en cola:', round(prom_demora_cola_calc, 2), 'minutos.')
    print('Utilización promedio del servidor:', "{:.2%}".format(prom_ut_serv_calc))
    return [prom_clientes_sistema_calc, prom_clientes_cola_calc, prom_demora_sistema_calc, prom_demora_cola_calc, prom_ut_serv_calc]
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
print('Promedio clientes en cola', promedio_clientes_cola)
print('Promedio clientes en sistema', promedio_clientes_sistema)
print('Promedio demora en cola', promedio_demora_cola)
print('Promedio utilización del sistema', promedio_utilizacion_servidor)
print('=====================================================')
util_corridas, demora_cola_corridas, clientes_cola_corridas, time_corridas, demora_sistema_corridas, clientes_sistema_corridas, contNCC, probNCC = [], [], [], [], [], [], [0] * 50, []
for i in range(10):
    time_acum, server_acum, niq_acum=[], [], []
    reporte = ()
    inicializar()
    while num_clientes <= total_clientes:
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
            if tipo_prox_evento == 1:
                arribo()
            else:
                contNCC[ncc] +=1  #si hay 0 clientes en cola suma 1 a su contador, si hay 1 suma 1 y así
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


def grafico_probNegacion_probNclientes(probabilidad1, probabilidad2):
    n_clientes_esperados, n_clientes_observados, probs2 = [], [], []
    n_clientes_esperados.append(probabilidad2)
    n_clientes_observados.append(1 - probabilidad1[0])
    for j in [0, 2, 5, 10, 50]: #probabilidad de denegacion de servicio para cola finita de tamaño 0, 2,5 ,10, 50
        n_clientes_esperados.append(1 - sum((probabilidad2) ** i * (1 - probabilidad2) for i in range(j)))
        n_clientes_observados.append(1 - sum(probabilidad1[i] for i in range(j)))

    print("Probabilidad de denegación de servicio observadas:", n_clientes_observados)
    print("Probabilidad de denegacion de servicio esperadas:", n_clientes_esperados)
    for i in range(len(probabilidad1)):
        if probabilidad1[i] > 0:
            probs2.append(probabilidad1[i])
    #grafico probabilidad de N clientes en cola
    plt.subplot(121)
    plt.title("Probabilidades de N clientes en cola")
    plt.xlabel('N clientes')
    plt.ylabel("Prob N clientes")
    plt.bar([x for x in range(len(probs2))], [(probabilidad2 ** i) * (1 - probabilidad2) for i in range(len(probs2))], label="Prob de N clientes esperada",
            color="black", width=0.25)
    plt.bar([x + 0.25 for x in range(len(probs2))], probs2, label="Prob de N clientes observada", color="red", width=0.25)
    plt.xticks([x + 0.15 for x in range(len(probs2))], [x for x in range(len(probs2))])
    plt.legend(loc='upper right')
    #grafico probabilidad de denegacion
    plt.subplot(122)
    plt.title("Probabilidades de denegación de servicio")
    plt.xlabel('N clientes')
    plt.ylabel('Prob de denegacion')
    plt.bar([x for x in range(len(n_clientes_esperados))], n_clientes_esperados, label="Prob de denegación esperada", color="black", width=0.25)
    plt.bar([x + 0.25 for x in range(len(n_clientes_esperados))], n_clientes_observados, label="Prob de denegacion observada", color="red", width=0.25)
    plt.xticks([x + 0.15 for x in range(len(n_clientes_observados))], ['0', '2', '5', '10', '50'])
    plt.legend(loc='upper right')
    plt.show()

for j in range(len(contNCC)):
    probNCC.append(contNCC[j]/sum(contNCC))
print("\nPromedios de las corridas: ====")
print("Promedio de la utilizacion del servidor: ", np.mean(util_corridas))
print("Promedio de tiempo promedio en cola:", np.mean(demora_cola_corridas))
print("Promedio de numero de clientes promedio en cola:", np.mean(clientes_cola_corridas))
print("Promedio de tiempo promedio en el sistema:", np.mean(demora_sistema_corridas))
print("Promedio de numero de clientes promedio en el sistema:", np.mean(clientes_sistema_corridas))
for j in range(len(probNCC)):
    if probNCC[j] > 0:
        print('Probabilidad de que haya {0} clientes en cola: {1}%'.format(j, probNCC[j]*100))  #Pn
print("Prob acumulada: ", sum(probNCC))

graficar(clientes_sistema_corridas, promedio_clientes_sistema, 'Clientes promedio en el sistema', 'S(t)')
graficar(clientes_cola_corridas, promedio_clientes_cola, 'Clientes promedio en cola', 'Q(t)')
graficar(demora_sistema_corridas, promedio_demora_sistema, 'Demora promedio en el sistema', 'Ds(n)')
graficar(demora_cola_corridas, promedio_demora_cola, 'Demora promedio en cola', 'Dq(n)')
graficar(util_corridas, promedio_utilizacion_servidor, 'Utilización del servidor', 'B(t)')
grafico_probNegacion_probNclientes(probNCC ,promedio_utilizacion_servidor)
