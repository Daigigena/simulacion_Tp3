import matplotlib.pyplot as plt
import numpy as np
import statistics as st


#variables globales
cant_tipo_evento=2 #numero de eventos
tiempo_medio_llegada=2.0 #lambda
tiempo_medio_servicio=3.0 # mu
total_clientes=100 #clientes cuyas demoras seran observadas
time=0.0 #reloj de la simulacion
estado=0 # 0: si el servidor está ocioso - 1: si el servidor está ocupado
ancc=0.0 #área debajo de la función número de clientes en cola
ncc=0 #numero de clientes en cola
tiempo_ult_evento=0.0 # tiempo del último evento que cambió el número en cola
num_clientes=0 #número de clientes que completaron sus demoras
arreglo_proximo_evento=np.zeros([cant_tipo_evento+1]) #contiene el tiempo del proximo evento I en la posicion lista_proximo_evento[I]
tiempo_total_demoras=0.0 # tiempo total de los clientes que completaron sus demoras
tiempo_prox_evento=0.0 #tiempo de ocurrencia del próximo evento a ocurrir
tipo_prox_evento=0 #tipo de evento (1: ARRIBOS o 2: PARTIDAS) del próximo evento que va a ocurrir
arreglo_tiempo_arribos=np.zeros([total_clientes+1])
tiempo_ser_acum=0.0

def inicializar():
    global time, estado, ncc, tiempo_ult_evento, num_clientes, tiempo_total_demoras, ancc, arreglo_proximo_evento
    global tiempo_prox_evento, tipo_prox_evento, arreglo_tiempo_arribos, tiempo_ser_acum
    time=0.0 #inicializamos el reloj de la simulacion
    estado=0
    ncc=0
    tiempo_ult_evento=0.0
    num_clientes=0
    tiempo_total_demoras=0.0
    ancc=0.0
    arreglo_proximo_evento = np.zeros([cant_tipo_evento + 1])
    tipo_prox_evento=0
    arreglo_tiempo_arribos=np.zeros([total_clientes+1])
    tiempo_ser_acum=0.0
    arreglo_proximo_evento[1]=time+np.random.exponential(1/tiempo_medio_llegada)
    arreglo_proximo_evento[2]=10.0**30
    tiempo_ser_acum=0.0


def timing():
    global time, arreglo_proximo_evento, tipo_prox_evento, tiempo_prox_evento, cant_tipo_evento
    tiempo_prox_evento=10.0**30
    tipo_prox_evento=0
    for i in range(1, cant_tipo_evento+1):
        if (arreglo_proximo_evento[i] < tiempo_prox_evento):
            tiempo_prox_evento=arreglo_proximo_evento[i]
            tipo_prox_evento=i
    if (tipo_prox_evento > 0):
        time=arreglo_proximo_evento[tipo_prox_evento]
    else:
        print(' Lista de eventos vacía. Fin de la simulación')


def arribos():
    global estado, tiempo_total_demoras, num_clientes, arreglo_tiempo_arribos, arreglo_proximo_evento
    global ncc, ancc, tiempo_ser_acum
    arreglo_proximo_evento[1]=time+np.random.exponential(1/tiempo_medio_llegada)
    if (estado==1):
        ncc+=1
        tiempo_ult_evento = time
        ancc+=ncc*(time-tiempo_ult_evento)
        if (ncc <= total_clientes):
            arreglo_tiempo_arribos[ncc]=time
        else:
            print('Se alcanzó el límite de clientes a observar')
    else:
        demora =0.0
        estado =1
        tiempo_total_demoras += demora
        num_clientes +=1
        arreglo_proximo_evento[2]=time+np.random.exponential(1/tiempo_medio_servicio)
        tiempo_ser_acum += (arreglo_proximo_evento[2]-time)


def partida():
    global ncc, estado, ancc, time, tiempo_ult_evento, arreglo_tiempo_arribos, tiempo_total_demoras,arreglo_proximo_evento
    global demora, num_clientes, tiempo_medio_servicio, tiempo_ser_acum
    if (ncc>0):
        ancc+= ncc*(time-tiempo_ult_evento)
        tiempo_ult_evento=time
        ncc-=1
        demora=time-arreglo_tiempo_arribos[1] #aca no se si es 1 o ncc
        tiempo_total_demoras += demora
        num_clientes += 1
        arreglo_proximo_evento[2]=time+np.random.exponential(1/tiempo_medio_servicio)
        tiempo_ser_acum += (arreglo_proximo_evento[2]-time)
    if (ncc != 0):
        for i in range(1, ncc+1):
            j=i+1
            arreglo_tiempo_arribos[i]=arreglo_tiempo_arribos[j]
    else:
        estado=0
        arreglo_proximo_evento[2]=10.0**30


def reporte():
    global tiempo_medio_llegada, tiempo_medio_servicio, total_clientes, num_clientes, ancc, tiempo_total_demoras
    global time, tiempo_ser_acum
    print('Sistema de cola simple')
    print('======================')
    print('Tiempo medio entre arribos:' ,tiempo_medio_llegada,'minutos')
    print('Tiempo medio servicio',tiempo_medio_servicio,'minutos')
    print('Numero maximo de clientes', total_clientes)
    avgncc=ancc/time
    print('Numero de promedio de clientes en cola', round(avgncc,2))
    avgdel=tiempo_total_demoras/num_clientes
    print('Demora promedio en cola:',round(avgdel,2), 'minutos.')
    avgustserv=tiempo_ser_acum/time
    print('Utilización promedio del servidor:' ,"{:.2%}".format(avgustserv))
    return avgncc, avgdel,avgustserv


def programa_principal(m,l):
    global num_clientes, total_clientes, tipo_prox_evento, tiempo_prox_evento, tiempo_medio_llegada
    global tiempo_medio_servicio
    tiempo_medio_llegada= m
    tiempo_medio_servicio= l
    inicializar()
    while (num_clientes <= total_clientes):
        timing()
        if tipo_prox_evento ==1:
            arribos()
        else:
            partida()
    else:
       reporte()
    return reporte


tiempo_medio_llegada= float(input("Ingrese tiempo medio de arribos (minutos): "))
tiempo_medio_servicio= float(input("Ingrese tiempo medio de servicio (minutos): "))
print('=====================================================')
for i in range(10):
    programa_principal(tiempo_medio_llegada,tiempo_medio_servicio)
    print('=====================================================')
