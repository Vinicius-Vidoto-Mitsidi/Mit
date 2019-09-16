import pypyodbc, pandas
from matplotlib import pyplot


#pypyodbc.win_connect_mdb('C:/Users/viniv/Dropbox (Mitsidi Projetos)/05_TEC/TEC_Pastas-Individuais/Vinicius Vidoto/Banco de dados/Teste de mudança de formato/bd_atlas_solarimetrico.mdb')

series = pandas.read_csv('Tab1.csv',sep=',')

print(series.head())
series.plot()
pyplot.show()


series = pandas.read_csv('Tab1.csv',index_col='-3')
pandas.plotting.lag_plot(series)
pyplot.show()