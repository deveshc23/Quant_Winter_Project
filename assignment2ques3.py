import pandas as pd
import matplotlib.pyplot as plt
data=pd.read_csv('daily_data.csv')
hammer=[0]
counter=0
j=0
for i in range(0,len(data)):
  if data['close'][i]>=data['open'][i]:    if (data['open'][i]-data['low'][i])!=0 and (data['high'][i]-data['close'][i])!=0:
      if (data['close'][i]-data['open'][i])/(data['open'][i]-data['low'][i])<0.5 and (data['close'][i]-data['open'][i])/(data['high'][i]-data['close'][i])>5:
        counter+=1
        if counter==1:
          j=i
        hammer.append(data['datetime'][i])
  elif data['close'][i]<=data['open'][i]:
    if (data['close'][i]-data['low'][i])!=0 and (data['high'][i]-data['open'][i])!=0:
      if (data['open'][i]-data['close'][i])/(data['close'][i]-data['low'][i])<0.5 and (data['open'][i]-data['close'][i])/(data['high'][i]-data['open'][i])>5:
        hammer.append(data['datetime'][i])
        counter+=1
        if counter==1:
          j=i
print("The Hammer appears on the following days ",pd.DataFrame(hammer))

fig,ax = plt.subplots()


candlestick = ax.plot([0.5, 0.5], [data['low'][j],data['high'][j]], color='black', linewidth=1)
rect = plt.Rectangle((0.4, data['open'][j]), 0.2, data['close'][j] - data['open'][j], linewidth=1, edgecolor='black', facecolor='green' if data['close'][j] > data['open'][j] else 'red')
ax.add_patch(rect)


ax.set_xlim(data['datetime'][j-1],data['datetime'][j+1])
ax.set_ylim(min(data['low'][j], data['open'][j], data['close'][j]), max(data['high'][j], data['open'][j], data['close'][j]))

plt.show()