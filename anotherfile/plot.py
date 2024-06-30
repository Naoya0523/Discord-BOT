import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from character import DATA

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

#draw the base line
ax.plot([-1, 1], [0,0], [0,0], 'black', ls=":", linewidth=0.5) #x
ax.plot([0,0], [-1, 1], [0,0], 'black', ls=":", linewidth=0.5) #y
ax.plot([0,0], [0,0], [-1, 1], 'black', ls=":", linewidth=0.5) #z

character = DATA['test']
ax.plot([0, character['AD']+0.2], [0,0], [0,0],  'orange', linewidth=3) #AD
ax.plot([0, -character['AP']-0.2], [0,0], [0,0], 'blue', linewidth=3) #AP
ax.plot([0,0], [-character['True']-0.2, 0], [0,0], 'white', linewidth=3) #True
ax.plot([0,0], [character['range']+0.2, 0], [0,0], 'green', linewidth=3) #range
ax.plot([0,0], [0,0], [character['tank']+0.2, 0], 'maroon', linewidth=3) #tank
ax.plot([0,0], [0,0], [-character['assassin']-0.2, 0], 'aqua', linewidth=3) #assassin
ax.plot([0,0], [0,0], [0,0], 'k.')

ax.text(1,0,0, 'AD', color='orange', bbox=dict(boxstyle='round', facecolor='black', alpha=0.5))
ax.text(-1,0,0, 'AP', color='deepskyblue', bbox=dict(boxstyle='round', facecolor='black', alpha=0.5))
ax.text(0,-1,0, 'True', color='white', bbox=dict(boxstyle='round', facecolor='black', alpha=0.5))
ax.text(0,1,0, 'range', color='green', bbox=dict(boxstyle='round', facecolor='black', alpha=0.5))
ax.text(0,0,1, 'tank', color='lightcoral', bbox=dict(boxstyle='round', facecolor='black', alpha=0.5))
ax.text(0,0,-1, 'assassin', color='aqua', bbox=dict(boxstyle='round', facecolor='black', alpha=0.5))

ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.set_zlim(-1, 1)
ax.set_facecolor('black')
ax.tick_params(labelbottom=False, labelleft=False, labelright=False)
plt.show()