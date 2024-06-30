import matplotlib.pyplot as plt
import numpy as np
from character import DATA

def get_data(DATA, labels, name):
    data = []
    character = DATA[name]
    for label in labels:
        data.append(character[label])
    return data

def get_figure(DATA, name):

    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)

    try:
        labels = ['AD', 'AP', 'True', 'Defence', 'Range', 'Speed']
        data = get_data(DATA, labels, name)
    except Exception as e:
        print(e)
        return False

    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)
    data = np.concatenate((data, [data[0]]))
    angles = np.concatenate((angles, [angles[0]]))

    ax.plot(angles, data, 'o-', linewidth=2)
    ax.fill(angles, data, alpha=0.25)

    ax.set_thetagrids(angles[:-1] * 180/np.pi, labels)
    ax.set_theta_zero_location('N')
    ax.set_title('status')
    plt.savefig('fig.png')

    return True
