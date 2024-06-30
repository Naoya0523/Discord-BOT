import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from character import DATA

def get_3dfigure(DATA, name):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    #draw the base line
    ax.plot([-1, 1], [0,0], [0,0], 'black', ls=":", linewidth=0.5) #x
    ax.plot([0,0], [-1, 1], [0,0], 'black', ls=":", linewidth=0.5) #y
    ax.plot([0,0], [0,0], [-1, 1], 'black', ls=":", linewidth=0.5) #z

    #reference table
    try:
        character = DATA[name]
    except Exception as e:
        print(e)
        return False

    ax.plot([0, character['AD']+0.2], [0,0], [0,0],  'orange', linewidth=3) #AD
    ax.plot([0, -character['AP']-0.2], [0,0], [0,0], 'blue', linewidth=3) #AP
    ax.plot([0,0], [-character['True']-0.2, 0], [0,0], 'white', linewidth=3) #True
    ax.plot([0,0], [character['Range']+0.2, 0], [0,0], 'green', linewidth=3) #range
    ax.plot([0,0], [0,0], [character['Defence']+0.2, 0], 'maroon', linewidth=3) #tank
    ax.plot([0,0], [0,0], [-character['Speed']-0.2, 0], 'aqua', linewidth=3) #assassin
    ax.plot([0,0], [0,0], [0,0], 'k.')

    ax.text(1,0,0, 'AD', color='orange', bbox=dict(boxstyle='round', facecolor='black', alpha=0.5))
    ax.text(-1,0,0, 'AP', color='deepskyblue', bbox=dict(boxstyle='round', facecolor='black', alpha=0.5))
    ax.text(0,-1,0, 'True', color='white', bbox=dict(boxstyle='round', facecolor='black', alpha=0.5))
    ax.text(0,1,0, 'Range', color='green', bbox=dict(boxstyle='round', facecolor='black', alpha=0.5))
    ax.text(0,0,1, 'Defence', color='lightcoral', bbox=dict(boxstyle='round', facecolor='black', alpha=0.5))
    ax.text(0,0,-1, 'Speed', color='aqua', bbox=dict(boxstyle='round', facecolor='black', alpha=0.5))

    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-1, 1)
    ax.set_facecolor('black')
    ax.tick_params(labelbottom=False, labelleft=False, labelright=False)

    plt.savefig('fig.png')

    return True