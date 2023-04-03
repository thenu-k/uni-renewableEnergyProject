from ..helperFunctions import normalizeDataSet

class SolarEnergyModel:
    def __init__(self, solarData):
        self.solarData = solarData
    def getDailyEnergyProduction(self):
        dailyTotalEnergy = [0]*len(self.solarData)
        count = 0
        for value in self.solarData:
            dailyTotalEnergy[count] += value * 5
            count += 1
        return dailyTotalEnergy