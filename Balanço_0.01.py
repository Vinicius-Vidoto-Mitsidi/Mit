# Neste modulo vamos fazer uma modelagem baseada na abordagem Colling Load Temperature Diference (CLTD).
# Esta abordagem tem ua vantagem de se basear em tabelas já bem conhecidas e de facil computação
# Num geral, usarem um calculo de carga termica para entendermos a necessidade do cliente e com esse resultado,
# divideremos-o por um fatro detendente do tipo de equipamento para sabermos a Potencia do nosso compressor.
# Com a(s) Potencia(s) poderemos estimar o custo com energia do sistema.

import math # biblioteca de funções matematicas
import datetime # Aqui, importaremos a biblioteca "datetime" que nos permite lidar com tempo mais facilmente
#----------------------------------------------------------------------------------
# Listas e dados:

# Lista dos possiveis involtorios, no futuro deverá vir de uma banco de dados. Fonte: http://projeteee.mma.gov.br/componentes-construtivos/#vidros
# Estruturados itens: [Nome, U[ (m^2 * K)/ W ], Cp[ J/ (m^2 * K)], Tipo CLTD]
Lista_parede = [["Argamassa interna 2.5 cm | Bloco cerâmico 14x19x29 cm | Argamassa Externa 2.5 cm", 0.55, 161000, 'B'],
                 ["Gesso interno fino 0.2 cm | Bloco concreto 9x19x39 cm | Argamassa Externa 2.5 cm", 0.34, 1330,'D'],
                 ["Argamassa interna 2.5 cm | Bloco cerâmico 9x19x19 cm | Argamassa externa 2.5 cm", 0.42, 1510,'C'],
                 ["Placa de gesso 1.25 cm | Lã de rocha 7.5 cm | Placa cimentícia 1 cm", 1.89, 32000,'A' ]]

# estruturados itens: [Nome, U[ (m^2 * K)/ W ], Cp[ J/ (m^2 * K)]]
Lista_Tetos = [["Forro gesso 3 cm | Câmara de ar (> 5,0 cm) | Telha cerâmica 1 cm", 0.52, 37000, 'B'],
                ["Laje maciça 10 cm | Câmara de ar (> 5,0 cm) | Telha cerâmica 1 cm", 0.49, 238000, 'B'],
                ["Forro gesso 3 cm | Câmara de ar (> 5.0 cm) | Telha fibrocimento 0.8 cm", 0.51, 32000, 'B'],
                ["Telhado vegetado extensivo: Laje pré-moldada 12 cm | Terra argilosa seca 10 cm | Vegetação", 0.54, 310000, 'B' ],
                ["Laje protendida alveolar sem preenchimento ou capa 15 cm | Contrapiso 5 cm | Piso cerâmico 0.75 cm", 0.36, 369000,'D']]

# estruturados itens: [Nome, Fator Solar[Admensional]]
Lista_Vidros = [["Vidro simples incolor 6 mm", 0.87],
                 ["Vidro monolítico 6mm | CEBRACE COOL-LITE ST 120", 0.322],
                 ["Vidro laminado incolor 8 mm (4+4)", 0.43]]

# valores de Cooling Load Temperature Difference para cada horario - ficticio, valores reais por calculos e tabelas.
# Valores para os tipo de materias "A"
#          01:00  02:00 03:00 04:00 05:00 06:00 07:00 08:00 09:00 10:00 11:00 12:00 13:00 14:00 15:00 16:00 17:00 18:00 19:00 20:00 21:00 22:00 23:00 24:00
CLTD_A = [[  2,     2,    2,    2,    2,    2,    3,    4,    5,    7,   10,   11,   12,   13,   14,   15,   14,   13,   10,    7,    5,    4,    3,    2,],
          [  2,     2,    2,    2,    2,    3,    5,    7,   10,   11,   12,   13,   12,   11,   10,    7,    4,    3,    2,    2,    2,    2,    2,    2,],
          [  2,     2,    2,    2,    2,    2,   2.5,   3,   3.5,  4.5,  5.3,   6,   6.5,   7,   7.5,   8,   7.5,   7,    5,   3.4,  2.5,   2,    2,    2,],
          [  2,     2,    2,    2,    2,    2,    2,    2,    2,    2,    2,    3,    5,    8,   12,   13,   14,   15,   13,   11,    9,    6,    4,    3,],]

# Gerando os valores para os tipo de materias "B" por for pq estou com preguiça, deve-se fazer o preenchimento de uma tabela na database
CLTD_B = [[],[],[],[],]
for i in range(4):
    for u in range(24):
        CLTD_B[i].append(CLTD_A[i][u]+1)

# Gerando os valores para os tipo de materias "C" por for pq estou com preguiça, deve-se fazer o preenchimento de uma tabela na database
CLTD_C = [[],[],[],[],]
for i in range(4):
    for u in range(24):
        CLTD_C[i].append(CLTD_A[i][u]+2)

# Gerando os valores para os tipo de materias "D" por for pq estou com preguiça, deve-se fazer o preenchimento de uma tabela na database
CLTD_D = [[],[],[],[],]
for i in range(4):
    for u in range(24):
        CLTD_D[i].append(CLTD_A[i][u]+4)

# Iniciamente devos ter a localização da estrutura analizada. Com a localização deveremos obter o historico climatico
# do local e com isso a temperatura do local.

# DUVIDA: Seria necessaria a Umudade Relativa? Sim!!!!!!!! para calculo de Qar e hentalpia relativa a umidade relativa

Local_estrutura = int(input("""Onde você mora?
Escolha entre: 1- São Paulo; 
               2- São José do Rio Preto;
               3- Curitiba.\nResposta: """))

if Local_estrutura == 1:
    Lista_temperatura = [20.3, 28.2, 25.4]

elif Local_estrutura == 2:
    Lista_temperatura = [25.3, 32.2, 27.4]

elif Local_estrutura == 3:
    Lista_temperatura = [14.3, 21.2, 16.4]

else:
    print("Por favor insira uma das localizades pre-designadas")
    exit()


# Agora precisamos entender qual a temperatura do set-point do sistema, ou seja, qual temperatura que deixam
# o ar-condicionado

Temp_setpoint = float(input("\nQual a  temperatura que o Ar-Condicionado costuma ficar? [°C]\nResposta: "))
print("\n")


# Agora, as dimensões do local.

Dimensoes_local = [0,0,0,0,0]
Dimensoes_local[0] = float(input("Qual ára da face Norte da estrutura? [m^2]\nResposta: "))

Dimensoes_local[1] = float(input("Qual ára da face Oeste da estrutura? [m^2]\nResposta: "))

Dimensoes_local[2] = float(input("Qual ára da face Sul da estrutura? [m^2]\nResposta: "))

Dimensoes_local[3] = float(input("Qual ára da face Leste da estrutura? [m^2]\nResposta: "))

Dimensoes_local[4] = float(input("Qual ára do teto da estrutura? [m^2]\nResposta: "))

print("\n")
# Então, vamos definir qual a extrutura do envoltorio. Esse é um ponto critico pois pode ser dificil os clientes
# saberem os dados necessarios.

Escolha_Parede = [0,0,0,0]
print("Dada a lista a seguir;\n        1- {}\n        2- {}\n        3- {}\n        4- {}\nEscolha,".format(Lista_parede[0][0],Lista_parede[1][0],Lista_parede[2][0],Lista_parede[3][0],))

Escolha_Parede[0] = int(input("Material da parede norte: "))
Escolha_Parede[1] = int(input("Material da parede oestee: "))
Escolha_Parede[2] = int(input("Material da parede sul: "))
Escolha_Parede[3] = int(input("Material da parede leste: "))
print("\n")

for x in range(len(Escolha_Parede)):
    Escolha_Parede[x]-=1

#---------------------------------------------------------------------------------------

Escolha_Teto = [0]
print("Dada a lista a seguir;\n        1- {}\n        2- {}\n        3- {}\n        4- {}\n        5- {}\nEscolha,".format(Lista_Tetos[0][0],Lista_Tetos[1][0],Lista_Tetos[2][0],Lista_Tetos[3][0],Lista_Tetos[4][0],))

Escolha_Teto[0] = int(input("Material do teto: "))
Escolha_Teto[0] -= 1
print("\n")

#---------------------------------------------------------------------------------------

Dimensoes_vidro = [0,0,0,0,0]
Dimensoes_vidro[0] = float(input("Qual ára de vidro na face Norte da estrutura? [m^2]\nResposta: "))

Dimensoes_vidro[1] = float(input("Qual ára de vidro na face Oeste da estrutura? [m^2]\nResposta: "))

Dimensoes_vidro[2] = float(input("Qual ára de vidro na face Sul da estrutura? [m^2]\nResposta: "))

Dimensoes_vidro[3] = float(input("Qual ára de vidro na face Leste da estrutura? [m^2]\nResposta: "))

Dimensoes_vidro[4] = float(input("Qual ára de vidro na teto da estrutura? [m^2]\nResposta: "))

print("\n")

#---------------------------------------------------------------------------------------

Escolha_Vidro = [0,0,0,0,0]
print("Dada a lista a seguir;\n        1- {}\n        2- {}\n        3- {}\nEscolha,".format(Lista_Vidros[0][0],Lista_Vidros[1][0],Lista_Vidros[2][0],))

Escolha_Vidro[0] = int(input("Tipo de vidro da parede norte: "))
Escolha_Vidro[1] = int(input("Tipo de vidro da parede oestee: "))
Escolha_Vidro[2] = int(input("Tipo de vidro da parede sul: "))
Escolha_Vidro[3] = int(input("Tipo de vidro da parede leste: "))
Escolha_Vidro[4] = int(input("Tipo de vidro do teto: "))

print("\n")

for x in range(len(Escolha_Vidro)):
    Escolha_Vidro[x]-=1

#-----------------------------------------------------------------------------

Num_pessoas = int(input("Quantas pessoas frequentam este local?\n"))
print("\n")

#----------------------------------------------------------------------


# Aqui usamos o metodo "srtptime" para conseguirmos avaliar as horas inputadas e sempre devemos informar qual formato estamos trabalhando, no caso HH:MM
Hora_inicio = datetime.datetime.strptime(input("Digite a hora em que a primeira pessoa enta no predio no dia no formato HH:MM :\n"), "%H:%M").time()
Hora_Fim = datetime.datetime.strptime(input("Digite a hora em que a ultima pessoa sai no predio no dia no formato HH:MM :\n"), "%H:%M").time()
print("\n")

# Para podermos subtrair um horario do outro, devemos atribuir uma data a ele, pois variaveis datetime.time não podem ser subtraidas, apenas variaveis datetime.datetime
# E para isso, devemos usar a função ".combine(DATA, HORA)" e para data usaremos a função "datetime.date.today()"
Data_complementar1 = datetime.datetime.combine(datetime.date.today(), Hora_Fim)
Data_complementar2 = datetime.datetime.combine(datetime.date.today(), Hora_inicio)

# Agora com o objeto datetime.dateteima, podemos realizar a diferença
Delta_tempo = Data_complementar1 - Data_complementar2

# Agora, podemos ver a diferença em horas ao usarmos a função ".total_seconds" e dividir por 3600 (total de segundo em uma hora)
Delta_tempo_horas = Delta_tempo.total_seconds()/3600

#--------------------------- LAMPADAS -------------------------------------------

print("Agora vamos cadastrar os dados das lampadas.\nPara isso, precisamos que você \"separe-as\" em grupos  de potencia e diga quantas há desta determinada potencia.\nVamos começar:")
ver = 'Y'
Lampadas =[]
while ver == 'Y' or ver == 'y':
    # nova entrada onde a estrutura é [potencai em watts, numero de lampadas desta potencia, tempo de uso em horas]
    nova_entrada_lampadas = [0,0,0]
    nova_entrada_lampadas[0] = float(input("Qual a potencia das lampadas?[W]\n"))
    nova_entrada_lampadas[1] = int(input("Quantas lampadas há no local desta potencia?\n"))
    nova_entrada_lampadas[2] = float(input("Quantas horas por dia elas ficam ligadas, em média?[Horas]\n"))

    Lampadas.append(nova_entrada_lampadas)
    ver = str(input("Deseja continuar? (Y/N)\n"))

    while ver != 'Y' and ver != 'y' and ver != 'N' and ver != 'n':
        ver = input("Por favor, digite um comando que seja aceito: (Y/N)\n")

    if ver == 'N' or ver == 'n':
        Energia_lampadas = []
        for x in range(len(Lampadas)): Energia_lampadas.append(Lampadas[x][0]*Lampadas[x][1]*(Lampadas[x][2]/24))
        Tot_E_Lamp = sum(Energia_lampadas)

#------------------------------Equipamentos----------------------------------------

print("Agora vamos cadastrar os dados dos Equipamentos.\nPara isso, precisamos que você \"separe-os\" em grupos  de potencia e diga quantas há desta determinada potencia.\nVamos começar:")
ver = 'Y'
Equipamentos = []
while ver == 'Y' or ver == 'y':
    # nova entrada onde a estrutura é [potencia em watts, numero de equipamentos desta potencia,tempo de uso em horas]
    nova_entrada_equipamentos = [0,0,0]
    nova_entrada_equipamentos[0] = float(input("Qual a potencia destes equipamentos?[W]\n"))
    nova_entrada_equipamentos[1] = int(input("Quantos equipamentos com esta potencia há no local?\n"))
    nova_entrada_equipamentos[2] = float(input("Quantas horas por dia eles ficam ligados em média?[Horas]\n"))

    Equipamentos.append(nova_entrada_equipamentos)
    ver = str(input("Deseja continuar? (Y/N)\n"))

    while ver != 'Y' and ver != 'y' and ver != 'N' and ver != 'n':
        ver = input("Por favor, digite um comando que seja aceito: (Y/N)\n")

    if ver == 'N' or ver == 'n':
        Energia_Equipamentos = []
        for x in range(len(Equipamentos)): Energia_Equipamentos.append(Equipamentos[x][0]*Equipamentos[x][1]*(Equipamentos[x][2]/24))
        Tot_E_Equip = sum(Energia_Equipamentos)

#----------------------------Dados de banco de dados------------------------------------------

irradiacao = float(5.12) # W/m^2 (Depende do local, coloquei a de Salvador (de outra fonte) e abaixei um pouco. Possivel fonte: http://www.cresesb.cepel.br/
#ar_renova = 4.8*Delta_tempo_horas*Num_pessoas*3.6*1.1839 # Fonte: Tabelas da USP no dropbox.
ar_renova = 4.8*Num_pessoas*0.001*1.1839 # em kg/s // Fonte: Tabelas da USP no dropbox.

#----------------------------Calculos------------------------------------------

#------------ Calculo de Calor por condução direta -----------

# Para cada temperatura da base de dados, calcular o calor para cada parede e para o teto.
# Adicionar na lista se o valor for positivo.

Q_conducao_direta_list = []

for t in range(len(Lista_temperatura)):
    for i in range(len(Escolha_Parede)):
        Q_cd = Dimensoes_local[i] * Lista_parede[Escolha_Parede[i]][1] * ((Lista_temperatura[t] + 273.15) - (Temp_setpoint + 273.15))
        Q_conducao_direta_list.append(Q_cd)


    Q_cd = Dimensoes_local[-1] * Lista_Tetos[Escolha_Teto[0]][1] * ((Lista_temperatura[t] + 273.15) - (Temp_setpoint + 273.15))
    Q_conducao_direta_list.append(Q_cd)

#Calcular por trapezio a integral de calor. Dividir por 5 para saber a "média" por ponto
for s in range(1, len(Q_conducao_direta_list)): Q_conducao_direta = ((Q_conducao_direta_list[s]+Q_conducao_direta_list[s-1])*1/2)/5 # em Watts

#-------------------------------------------------------------



Q_radiacao_supTransparente_lista = []
for i in range(5): Q_radiacao_supTransparente_lista.append(Dimensoes_vidro[i]*Lista_Vidros[Escolha_Vidro[i]][1]*irradiacao)
Q_radiacao_supTransparente = sum(Q_radiacao_supTransparente_lista) # em Watts



Q_radiacao_supOpaca_lista = []

Data_aux = datetime.datetime.combine(datetime.date.today(), datetime.datetime.strptime("00:00", "%H:%M").time())
h = int(math.floor((Data_complementar2 - Data_aux).total_seconds()/3600))

for t in range(h-1,h+int(math.ceil(Delta_tempo_horas))):
    for i in range(4):
        if Lista_parede[Escolha_Parede[0]][3] == 'A': CLTD_Mat = CLTD_A
        if Lista_parede[Escolha_Parede[0]][3] == 'B': CLTD_Mat = CLTD_B
        if Lista_parede[Escolha_Parede[0]][3] == 'C': CLTD_Mat = CLTD_C
        if Lista_parede[Escolha_Parede[0]][3] == 'D': CLTD_Mat = CLTD_D
        Q_radiacao_supOpaca_lista.append(Dimensoes_local[i]*Lista_parede[Escolha_Parede[i]][1]*CLTD_Mat[i][t])
    Q_radiacao_supOpaca_lista.append(Dimensoes_local[4] * Lista_Tetos[Escolha_Teto[0]][1] * CLTD_Mat[3][t])
Q_radiacao_supOpaca = sum(Q_radiacao_supOpaca_lista) # em Watts

UR_fora=0.65 # Umidade Relativa // Admincional
#UR_dentro = 0.58
Delta_umidade = 0.0077*UR_fora
if Delta_umidade < 0: Delta_umidade = 0.0001
Calor_latente = ar_renova*2453500*Delta_umidade  # em Watts ; ar_renova em kg/s ; valor numerico é o calor de vaporizaçao da agua e está em J/kg
temperatura_media_externa_em_K = (sum(Lista_temperatura)+273.15*len(Lista_temperatura))/len(Lista_temperatura) # em K
Delta_temperatura = temperatura_media_externa_em_K - (Temp_setpoint+273.15) # em K
Calor_sensivel = ar_renova*(1013*(Delta_temperatura) + UR_fora*4178*(Delta_temperatura)) # Calor_sensivel em Watts ; Cp em J/kg*K ; ar_renova em kg/s ; temperaturas em K
Q_ar_entra = (Calor_sensivel + Calor_latente) # Q em Watts ; ar_renova em kg/s ; Calor em J/kg
print('Temperatura média em K: {:.3f}'.format(temperatura_media_externa_em_K))
print('delta temperatura: {:.3f}'.format(Delta_temperatura))
print('Calor sencivel: {:.3f}'.format(Calor_sensivel))
print('Calor Latente: {:.3f}'.format(Calor_latente))
print('ar que entra {:.3f}'.format(ar_renova))
print('calor de ar que entra {:.3f}'.format(Q_ar_entra))

Calor_p_sensivel = 75
Calor_p_latente = 55
Q_pessoa = Num_pessoas*(Calor_p_sensivel+Calor_p_latente) # fonte Tabela dropbox usp // em Watts

Q_iluminacao_lista = []
#Q_iluminacao = 0.25*Tot_E_Lamp # Em Watts // Estou considerando uma porcentagem, mas deve vir de banco de dados o valor da irrdiação de cada lampada, sendo esta multiplicada pela fator de uso e pela quantidade
for x in range(len(Lampadas)):
    Calor_lampada = 0.25 * Lampadas[x][0]
    Q_iluminacao_lista.append(Calor_lampada * Lampadas[x][1] * (Lampadas[x][2] / 24))
Q_iluminacao = sum(Q_iluminacao_lista)

Q_Equipamentos_lista = []
#Q_Equipamentos = 0.35*Tot_E_Equip # Em Watts //  Estou considerando uma porcentagem, mas deve vir de banco de dados o valor da irrdiação de cada equipamento, sendo esta multiplicada pela fator de uso e pela quantidade
for x in range(len(Equipamentos)):
    Calor_equipamento = 0.35 * Equipamentos[x][0]
    Q_Equipamentos_lista.append(Calor_equipamento * Equipamentos[x][1] * (Equipamentos[x][2] / 24))
Q_Equipamentos = sum(Q_Equipamentos_lista)

Q_total = Q_conducao_direta + Q_radiacao_supTransparente + Q_radiacao_supOpaca + Q_ar_entra + Q_pessoa + Q_iluminacao + Q_Equipamentos

Lista_BTUs_ar = [7500, 10000, 12000, 15000, 18000, 21000, 30000] #BTUs/h

Num_ar_BTU = []
for d in range(len(Lista_BTUs_ar)) : Num_ar_BTU.append(math.ceil(Q_total/(0.293071*Lista_BTUs_ar[d]))) # 0,293071 é o fator de conversao entre BTU/h e watt;

Potencia_compressor_comum = math.ceil(Q_total/3.49)
Potencia_compressor_inverter = math.ceil(Q_total/4.89)
Potencia_compressor_multiEstagio = math.ceil(Q_total/3.00)

#----------------------------------------------------------------------

print("""\n\n\nResumo:\n[A face norte tem {} metros quadrados de {},com U de {} e Cp de {}, assim como {} metros quadros envidraçados com o vidro {} de Fs {}]
[A face oeste tem {} metros quadrados de {},com U de {} e Cp de {}, assim como {} metros quadros envidraçados com o vidro {} de Fs {}]
[A face sul tem {} metros quadrados de {},com U de {} e Cp de {}, assim como {} metros quadros envidraçados com o vidro {} de Fs {}]
[A face leste tem {} metros quadrados de {},com U de {} e Cp de {}, assim como {} metros quadros envidraçados com o vidro {} de Fs {}]
[O teto tem {} metros quadrados de {},com U de {} e Cp de {}, assim como {} metros quadros envidraçados com o vidro {} de Fs {}]"""
.format(Dimensoes_local[0], Lista_parede[Escolha_Parede[0]][0], Lista_parede[Escolha_Parede[0]][1], Lista_parede[Escolha_Parede[0]][2], Dimensoes_vidro[0], Lista_Vidros[Escolha_Vidro[0]][0],Lista_Vidros[Escolha_Vidro[0]][1],
Dimensoes_local[1], Lista_parede[Escolha_Parede[1]][0], Lista_parede[Escolha_Parede[1]][1], Lista_parede[Escolha_Parede[1]][2], Dimensoes_vidro[1], Lista_Vidros[Escolha_Vidro[1]][0],Lista_Vidros[Escolha_Vidro[1]][1],
Dimensoes_local[2], Lista_parede[Escolha_Parede[2]][0], Lista_parede[Escolha_Parede[2]][1], Lista_parede[Escolha_Parede[2]][2], Dimensoes_vidro[2], Lista_Vidros[Escolha_Vidro[2]][0],Lista_Vidros[Escolha_Vidro[2]][1],
Dimensoes_local[3], Lista_parede[Escolha_Parede[3]][0], Lista_parede[Escolha_Parede[3]][1], Lista_parede[Escolha_Parede[3]][2], Dimensoes_vidro[3], Lista_Vidros[Escolha_Vidro[3]][0],Lista_Vidros[Escolha_Vidro[3]][1],
Dimensoes_local[4], Lista_Tetos[Escolha_Teto[0]][0], Lista_Tetos[Escolha_Teto[0]][1], Lista_Tetos[Escolha_Teto[0]][2], Dimensoes_vidro[4], Lista_Vidros[Escolha_Vidro[4]][0],Lista_Vidros[Escolha_Vidro[4]][1],))

print("\n[{} ocupam o predio com a primeira entrando as {} e a ultima saida as {}, ficando um total de {} Horas]".format(Num_pessoas, Hora_inicio, Hora_Fim, Delta_tempo_horas,))

print("\nCalor por condução direta: \n{:.3f} ".format(Q_conducao_direta))
print("\nCalor por radiação por superficie transparente:: \n{:.3f} ".format(Q_radiacao_supTransparente))
print("\nCalor por radiação por superficie opaca: \n{:.3f} ".format(Q_radiacao_supOpaca))
print("\nCalor por Trocas de ar: \n{:.3f} ".format(Q_ar_entra))
print("\nCalor por iluminaçao: \n{:.3f} ".format(Q_iluminacao))
print("\nCalor por equipamento: \n{:.3f} ".format(Q_Equipamentos))
print("\nCalor por pessoa: \n{:.3f} ".format(Q_pessoa))
print("\nCarga termica total (somatorio de todos os calores): \n{:.3f} ".format(Q_total))

print("Com sua carga termica voce poderia ter:\n")
for n in range(len(Num_ar_BTU)): print("              {} ar-condicionados de {} BTUs, exigindo uma podencia de {:.3f} kW pelos seus compressores (não inverter); ".format(Num_ar_BTU[n],Lista_BTUs_ar[n],Num_ar_BTU[n]*Lista_BTUs_ar[n]*0.2929/(1000*3.49)))
print('        Ou')
for n in range(len(Num_ar_BTU)): print("              {} ar-condicionados de {} BTUs, exigindo uma podencia de {:.3f} kW pelos seus compressores (inverter); ".format(Num_ar_BTU[n],Lista_BTUs_ar[n],Num_ar_BTU[n]*Lista_BTUs_ar[n]*0.2929/(1000*4.89)))
print('        Ou')
print("(VERIFICAR!)  1 ar-condicionados central que retire uma carga termica de {:.3f} kW, exigindo uma podencia de {:.3f} kW pelos seus compressores ( media entre 3 compressores); ".format(Q_total/1000,Q_total/(1000*3.2)))

print("\n[O total de energia gasta com lampadas é de {:.3f} kW]".format(Tot_E_Lamp / 1000))
print("\n[O total de energia gasta com equipamentos é de {:.3f} kW]".format(Tot_E_Equip / 1000))