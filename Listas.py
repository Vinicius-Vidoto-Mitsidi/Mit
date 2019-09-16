import math

sistemas = ['Aquecimento_direto', 'Aquecimento_Agua', 'Calor_processo', 'Carga_de_Tomadas', 'Ar_Condicionado',
            'Eletroquimica', 'Força_Motriz', 'Iluminação', 'Refrigeração']
subsistemas = ['teste_1', 'teste_2', 'teste_3']

titulo = [''] + sistemas

var_rel_sis_sub = [titulo,
         [subsistemas[0], 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [subsistemas[1], 0, 0, 0, 0, 0, 0, 0, 1, 0],
         [subsistemas[2], 0, 0, 0, 0, 0, 0, 1, 0, 0], ]

print('{}'.format(var_rel_sis_sub))

for x in range(len(sistemas)+1):
    for y in range(len(subsistemas)+1):
        g = var_rel_sis_sub[y][x]

        if g == 1:

            if var_rel_sis_sub[0][x] == 'Força_Motriz':
                tempoUso = float(input('Qual tempo de uso deste equipamento de {} em horas?'.format(var_rel_sis_sub[0][x])))
                gasto = 12*tempoUso+math.log(tempoUso)/3
                print('o valor gasto com {} é de {:.3f}'.format(var_rel_sis_sub[0][x], gasto))

            if var_rel_sis_sub[0][x] == 'Iluminação':
                tempoUso = float(input('Qual tempo de uso deste equipamento de {} em horas?'.format(var_rel_sis_sub[0][x])))
                gasto = 10 * tempoUso + 5*math.log(tempoUso)
                print('o valor gasto com {} é de {:.3f}'.format(var_rel_sis_sub[0][x], gasto))

            if var_rel_sis_sub[0][x] == 'Refrigeração':
                tempoUso = float(input('Qual tempo de uso deste equipamento de {} em horas?'.format(var_rel_sis_sub[0][x])))
                gasto = 15 * tempoUso + math.log(tempoUso)/12
                print('o valor gasto com {} é de {:.3f}'.format(var_rel_sis_sub[0][x], gasto))