from ..helperFunctions import normalizeDataSet

class WindEnergyModel:
    def __init__(self, windData, frequencyOfData, isCSV, customDailyGenerationFunction):
        self.windData = windData
        self.frequencyOfData = frequencyOfData
        if not customDailyGenerationFunction:
            self.normalizedWindData = normalizeDataSet(self.windData, self.frequencyOfData)
        self.customDailyGenerationFunction = customDailyGenerationFunction
    def getDailyEnergyProduction(self):
        if not self.customDailyGenerationFunction:
            dailyTotalEnergy = [0]*len(self.normalizedWindData)
            count = 0
            for value in self.normalizedWindData:
                dailyTotalEnergy[count] += value * 4
                count += 1
            return dailyTotalEnergy
        else:
            return self.customDailyGenerationFunction()
    def getHourlyEnergyProduction(self):
        return None