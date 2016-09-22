# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 16:37:41 2016
plot polar chart
@author: liang.kuang
"""
from pylab import *
from matplotlib import cm

colormaps()  # get all colormap names
set_cmap('jet')
cm.jet(0)  # return (0,0,0.5,1)

r = amp_df.values  #.flatten()
theta = np.deg2rad(phase_df.values)  #.flatten())

area = 20
colors = theta
fig1 = plt.figure(num=1,figsize=[8,8], dpi=150)
plt.clf()
ax = fig1.add_axes([0.12,0.12,0.8,0.8],polar=True)
ax.set_theta_zero_location("N")
ax.set_theta_direction(-1) #clockwise
#ax.set_theta_offset(pi)

#ax = subplot(111,polar=True)
for n in np.arange(r.shape[0]):  # per constituents
  
    #c = scatter(theta,r,hold = True, c = (0,1,0,1))
    c = scatter(theta[n,], r[n,], color = cm.jet(int(np.floor(n*256/r.shape[0]))), s = area,cmap = cm.hsv,hold=True,label=amp_df.index[n])

c.set_alpha(0.75)
leg=legend(loc='best',fontsize=6)
leg.draggable(True)
show()
title("Amplititude and Phase difference")
# by station
colors = theta
fig2 = plt.figure(num=2,figsize=[8,8], dpi=150)
plt.clf()
ax2 = fig2.add_axes([0.12,0.12,0.8,0.8],polar=True)
ax2.set_theta_zero_location("N")
ax2.set_theta_direction(-1) #clockwise
#ax.set_theta_offset(pi)

#ax = subplot(111,polar=True)
for n in np.arange(r.shape[1]):  # per constituents
  
    #c = scatter(theta,r,hold = True, c = (0,1,0,1))
    print(int(np.floor(n*256/r.shape[0])))
    c = scatter(theta[:,n], r[:,n], color = cm.jet(int(np.floor(n*256/r.shape[1]))), s = area,cmap = cm.hsv,hold=True,label=amp_df.columns[n])

c.set_alpha(0.75)
leg=legend(loc='best',fontsize=6, markerscale=1)
leg.draggable()
show()
title("Amplititude and Phase difference",fontsize=10)



#observation vs. model
 

fig3 = plt.figure(num=3,figsize=[8,8],dpi=150)
plt.clf()
ax3 = fig3.add_axes([0.12,0.12,0.8,0.8],polar=True)
ax3.set_theta_zero_location("N")
ax3.set_theta_direction(-1) #clockwise
scatter(np.deg2rad(phase_data),amp_data,marker="s",c=amp_data,s=area,hold=True,label='Data',cmap=cm.Paired)
scatter(np.deg2rad(phase_model),amp_model,c=amp_data,s=area,hold=True,label='Model',cmap=cm.Paired)
leg=legend(loc='best')
leg.draggable()
show()
title("Model vs. Data",fontsize=10)




