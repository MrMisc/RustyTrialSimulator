import cv2
import json
from matplotlib import rc
from matplotlib.font_manager import FontProperties
from scipy.stats import ks_2samp
import scipy.stats as stats  
import os
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import subprocess
data, tapdata, money, data2, tapdata2, money2 = ([] for _ in range(6))
while True:
    try:
        # The last set of DAT, is actually index information about the simulation parameters
        # Removing and storing that valueset from these lists would be ideal
        #The index format for the last element in DAT is method number (ends up inside the data lists) - max number of runs per attempt(tapdata lists) - falsecap(money lists)
        DAT= input().split(" ")
        data.append(int(DAT[0]))
        tapdata.append(int(DAT[1]))
        money.append(float(DAT[2]))
        data2.append(int(DAT[3]))
        tapdata2.append(int(DAT[4]))
        money2.append(float(DAT[5]))
    except EOFError as e:
        break


#Resorting the data
method1 = data[-1]
attempts1 = tapdata[-1]
falsecap1 = money[-1]
method2 = data2[-1]
attempts2 = tapdata2[-1]
falsecap2 = money2[-1]

#remove last element/index from each list
data = data[:-1]
tapdata = tapdata[:-1]
money = money[:-1]
data2 = data2[:-1]
tapdata2 = tapdata2[:-1]
money2 = money2[:-1]

print(f"Length of data files appear to be : {len( data)}, {len(data2)}") #True length of the data is len(data)-1 because the last entry is index only 

print("For example, let us consider entry 66...")

print(f"For attempt 66, there appears to be {tapdata[65]} rolls applied at the cost of {money[65]}, for simulation 1")
print(f"This is as opposed to, {tapdata2[65]} rolls, at the cost of {money2[65]} for simulation 2")


#Data plotting
plt.clf()
fig = plt.figure()
plt.style.use('fivethirtyeight') 
plt.figure(figsize=(20,10))
alphaamt = max(max(data), max(data2))
# print(type(alphaamt))
bins = np.linspace(0, alphaamt, int(alphaamt**.7))
rc('font',**{'family':'Yu Gothic', 'size': 16})
try:
    fit_alpha, fit_loc, fit_beta=stats.gamma.fit(data)
    fit_alpha2, fit_loc2, fit_beta2=stats.gamma.fit(data2)
    plt.text(int(0.5*max(max(data),max(data2))),10,"KS sample comparison: \n"+(str(ks_2samp(data, data2)).split('(')[1].replace(")","").replace(",","\n"))+ "\n\n"+ f"Simulation 1 Gamma Fit for {fit_alpha} shape and {fit_beta} rate \n"+" " + (str(stats.kstest(data, 'gamma', args=(fit_alpha,fit_loc, fit_beta)))) + "\n\n"+ f"Simulation 2 Gamma Fit for {fit_alpha2} shape and {fit_beta2} rate \n"+" " + (str(stats.kstest(data2, 'gamma', args=(fit_alpha2,fit_loc2, fit_beta2)))), style = "italic", bbox={'facecolor': 'black', 'alpha': 0.1, 'pad': 10})
except:pass
plt.hist([data, data2], bins, alpha=0.5, label=[f'First simulation for {str(attempts1)} attempts per session [{str(method1)}]', f'Second simulation for {str(attempts2)} attempts per session [{str(method2)}]']) 
plt.xlabel("Number of attempts taken to success", color = 'black')
plt.ylabel("Frequency", color = 'black')
plt.title("Number of successes every couple of sessions of rolls/Bernoulli trials per simulation", color = 'black')
plt.legend(loc='upper right')
plt.savefig(fname='plot2')

#Tapdata plotting 

x = np.linspace(1,len(data),len(data))
plt.clf()
fig = plt.figure()
plt.style.use('fivethirtyeight') 
plt.figure(figsize=(20,10))
alphaamt = max(tapdata) 
alphaamt = max(alphaamt,max(tapdata2))
maxatt = max(int(attempts1), int(attempts2))
minatt = min(int(attempts1), int(attempts2))
if alphaamt>60:bins = np.linspace(0, alphaamt,int(alphaamt/maxatt)) #first wrt to the smaller attempt pool
else:bins = np.linspace(0, alphaamt,int(alphaamt/5))
bins = np.array(bins)
plt.hist([tapdata, tapdata2], bins, alpha=0.5, label=[f'First simulation for {str(attempts1) } attempts per session : Method [{str(method1)}]', f'Second simulation for {str(attempts2) } attempts per session: Method [{str(method2)}]']) 
rc('font',**{'family':'Yu Gothic', 'size': 16})
fit_alpha, fit_loc, fit_beta=stats.gamma.fit(tapdata)
fit_alpha2, fit_loc2, fit_beta2=stats.gamma.fit(tapdata2)
print(f"Kolmogorov Smirnov test result for tapdata : {ks_2samp(tapdata, tapdata2)}")
plt.text(1,1," "+(str(ks_2samp(tapdata, tapdata2)).split('(')[1].replace(")","").replace(",","\n"))+ "\n\n"+ f"Simulation 1 Gamma Fit for {fit_alpha} shape and {fit_beta} rate \n"+" " + (str(stats.kstest(tapdata, 'gamma', args=(fit_alpha,fit_loc, fit_beta)))) + "\n\n"+ f"Simulation 2 Gamma Fit for {fit_alpha2} shape and {fit_beta2} rate \n"+" " + (str(stats.kstest(tapdata2, 'gamma', args=(fit_alpha2,fit_loc2, fit_beta2)))), style = "italic", bbox={'facecolor': 'black', 'alpha': 0.1, 'pad': 10})
plt.xlabel("Number of Bernoulli trials taken to success" , color = 'black')
plt.ylabel("Frequency", color = 'black')
plt.gca().set_xscale("log")
plt.title(f"Number of successes every {maxatt} rolls/Bernoulli trials", color = 'black')
plt.legend(loc='upper right')
plt.savefig(fname='tapdataplot')
# plt.show()




#money plot

plt.clf()
rc('font',**{'family':'Yu Gothic', 'size': 16})
fig = plt.figure()
plt.style.use('fivethirtyeight') 
plt.figure(figsize=(20,10))
ax = sns.kdeplot(money , bw_adjust = 0.5 , fill = True, cut = 0, label = "Simulation 1 ")
sns.kdeplot(money2 , bw_adjust = 0.5 , fill = True, cut = 0, label = "Simulation 2 ")
plt.xlabel("Money (units)", color = 'black')
plt.ylabel("Frequency", color = 'black')
fit_alpha, fit_loc, fit_beta=stats.gamma.fit(money)
fit_alpha2, fit_loc2, fit_beta2=stats.gamma.fit(money2)
plt.text(0.5*max(max(money),max(money2)),0.0," "+(str(ks_2samp(money, money2)).split('(')[1].replace(")","").replace(",","\n")) + "\n\n"+ f"Simulation 1 Gamma Fit for {fit_alpha} shape and {fit_beta} rate \n"+" " + (str(stats.kstest(money, 'gamma', args=(fit_alpha,fit_loc, fit_beta)))) + "\n\n"+ f"Simulation 2 Gamma Fit for {fit_alpha2} shape and {fit_beta2} rate \n"+" " + (str(stats.kstest(money2, 'gamma', args=(fit_alpha2,fit_loc2, fit_beta2)))), style = "italic", bbox={'facecolor': 'black', 'alpha': 0.1, 'pad': 10})
# plt.text(0.1,0.0003,  , bbox={'facecolor': 'black', 'alpha': 0.1, 'pad': 10})
# plt.gca().set_xscale("log")
plt.title(f"Cost distribution of 2 simulations", color = 'black')
ax.legend(loc='upper right')
plt.savefig(fname='moneyplot.png')  

# os._exit(0)
# subprocess.Popen("py DataEntryPoint.py", shell=True) 



f = open('duration.json')
data = json.load(f)
print("Execution took "+(lambda strset: (str(float(strset)/60.0)+"min") if float(strset)>600.0 else strset + "s")(str(data["Time"])+"."+str(data["Extended Time Details"]*10**-9).split(".")[1]))



plt.close('all')
figurine = plt.figure(figsize=(10,9))

# setting values to rows and column variables
rows = 2
columns = 1
  
# reading images
Image1 = cv2.imread('tapdataplot.png')
Image2 = cv2.imread('moneyplot.png')

figurine.add_subplot(rows, columns, 1)
  
# showing image
plt.imshow(Image1)
plt.axis('off')
# plt.title("Successes logged by each trial")
  
# Adds a subplot at the 2nd position
figurine.add_subplot(rows, columns, 2)
  
# showing image
plt.imshow(Image2)
plt.axis('off')
# plt.title("Money distribution")

plt.show()