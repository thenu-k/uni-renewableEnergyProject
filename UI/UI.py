import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

def plotData(tidalEnergyGeneration, windEnergyGeneration, solarEnergyGeneration, totalEnergyGeneration):
    days = np.arange(1, len(tidalEnergyGeneration)+1)
    energy1 = tidalEnergyGeneration
    energy2 = windEnergyGeneration
    energy3 = solarEnergyGeneration
    energy4 = totalEnergyGeneration
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
    ani.save('EnergyProduction.gif')
    plt.show()