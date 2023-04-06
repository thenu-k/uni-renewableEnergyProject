import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

def plotData(tidalEnergyGeneration, windEnergyGeneration, solarEnergyGeneration, totalEnergyGeneration, netEnergyDemand):
    days = np.arange(1, len(tidalEnergyGeneration)+1)
    energy1 = tidalEnergyGeneration
    energy2 = windEnergyGeneration
    energy3 = solarEnergyGeneration
    energy4 = totalEnergyGeneration
    # energy5 = netEnergyDemand
    energies = [energy1, energy2, energy3, energy4]
    fig, axs = plt.subplots(nrows=2, ncols=2)

    lines = []
    count = 0
    for ax in axs.flat:
        line, = ax.plot([], [], color='r')
        # set random color for each line
        line.set_color((np.random.rand(), np.random.rand(), np.random.rand()))
        lines.append(line)
        ax.set_xlim(0, 336)
        ax.set_ylim(0, max(energies[count]))
        count += 1

    def update(num, days, energy1, energy2, energy3, energy4, lines):
        lines[0].set_data(days[:num], energy1[:num])
        lines[1].set_data(days[:num], energy2[:num])
        lines[2].set_data(days[:num], energy3[:num])
        lines[3].set_data(days[:num], energy4[:num])
        return lines

    ani = animation.FuncAnimation(fig, update, frames=len(days), fargs=[days, energy1, energy2, energy3, energy4, lines], interval=50)
    ani.save('./Media/EnergyProduction.gif')
    plt.show()


def compareProd(graphs):
    # days = np.arange(1, len(energyProd)+1)
    # plt.plot(days, energyDemand, color='b')
    # if energyProd:
    #     plt.plot(days, energyProd, color='#AAAAAA', linestyle='dotted')
    # if energyProd2:
    #     # hex value for dark gray: #AAAAAA
    #     plt.plot(days, energyProd2, color='#AAAAAA', linestyle='dotted')
    # if energyTotal:
    #     plt.plot(days, energyTotal, color='r')
    # if energyDefecit:
    #     plt.plot(days, energyDefecit, color='g')
    # plt.xlabel("X-axis data")
    # plt.ylabel("Y-axis data")
    # plt.ylim(0)
    # plt.title('multiple plots')
    # plt.show()
    days = np.arange(1, len(graphs[0])+1)

    for i in range(len(graphs)):
        if i == 0:
            plt.plot(days, graphs[i], color='b', linewidth=2)
        else:
            plt.plot(days, graphs[i], color='r', linewidth=2)
    plt.ylim(0)
    plt.grid(True)
    #change grid thickness and axis thickness
    plt.rcParams['axes.linewidth'] = 1
    plt.rcParams['grid.linewidth'] = 1
    plt.ylabel("Energy (Wh)")
    plt.xlabel("Units")
    plt.show()