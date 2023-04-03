from ..helperFunctions import normalizeDataSet

class SolarEnergyModel:
    def __init__(self, solarData, frequencyOfData, isCSV):
        self.solarData = solarData
        self.frequencyOfData = frequencyOfData
        self.normalizedSolarData = normalizeDataSet(self.solarData, self.frequencyOfData)
    def getDailyEnergyProduction(self):
        dailyTotalEnergy = [0]*len(self.normalizedSolarData)
        count = 0
        for value in self.normalizedSolarData:
            dailyTotalEnergy[count] += value * 5
            count += 1
        return dailyTotalEnergy