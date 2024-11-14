import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt



# Télécharger les données
data = yf.download("AAPL", start="2023-01-01", end="2024-01-01")

# Garder uniquement la colonne 'Close'
data = data[['Close']]



# Calculer la moyenne mobile simple sur 10 jours
data['SMA_10'] = data['Close'].rolling(window=10).mean()


# Supprimer les lignes avec des NaN dans SMA_10
data = data[data['SMA_10'].notnull()]

# Vérifier si un MultiIndex est utilisé
if isinstance(data.columns, pd.MultiIndex):
    # Aplatir le MultiIndex
    data.columns = ['_'.join(filter(None, col)) for col in data.columns]
    
data.to_csv('stockDataApple.csv')

#création datafram avec date en indice et 2 colonnes pr close et SAM_10
data=pd.read_csv('stockDataApple.csv', index_col='Date', parse_dates=True)

#création colonne signal:
data['Signal']=(data['Close_AAPL']>data['SMA_10']).astype(int)

#création colonne rendements =(close_t - close_(t-1))/close_(t-1)
data['Daily_Returns'] = data['Close_AAPL'].pct_change()

#rendement de la stratégie : si signal =1 on se positionne dc rendement= signal*daily_return
data['Strategy_Returns']=data['Daily_Returns']*data['Signal'].shift(1) #shift(1) car c'est le signal du jour précédent qu'on utilise,car on ne peut se positionner sur le meme jour

#cumule des rendements de la stratégie = (1+Strategy_Returnes).cumprod()
data['Cumulative_Strategy_Returns']=(1+data['Strategy_Returns']).cumprod()
data['Cumulative_Market_Returns'] = (1 + data['Daily_Returns']).cumprod() 
# perf totale du marché = rendement si on avait acheté et gardé l'action


#affichage graph du prix du close et de la moy mobile

plt.figure (figsize=(12,8))

plt.subplot(2,1,1)
data['Close_AAPL'].plot(label='Close', linewidth =2)
data['SMA_10'].plot(label='MoyGlissante', linewidth =2)

#affichage des points lorsqu'on achète = qu'on prend position = signal=1

# Jours d'achat (indices où Signal = 1)
buy_signals = data[data['Signal'] == 1]
plt.scatter(buy_signals.index, buy_signals['Close_AAPL'], color='green', label='Achat', marker='^', s=20)


plt.title('Comparaison prix close et moy glissante')
plt.xlabel('Date')
plt.legend()
plt.grid()

#affichage graphe des rendements cumulés
plt.subplot(2,1,2)
data['Cumulative_Strategy_Returns'].plot(label='Rendements Stratégie', linestyle='--', linewidth=2)
data['Cumulative_Market_Returns'].plot(label='Rendements Marché', linestyle='-', linewidth=2)
plt.title('Performance de la stratégie vs Marché')
plt.xlabel('Date')
plt.ylabel('Rendements Cumulés')
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()

data.to_csv('stockDataApple.csv')
print(data.head())
print(data.columns)
