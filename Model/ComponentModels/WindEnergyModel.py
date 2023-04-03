from ..helperFunctions import normalizeDataSet

class WindEnergyModel:
    # create a type of a function that returns a list of integers: type[function: list[int]]
    def __init__(self, windData: type[list[float]], customDailyGenerationFunction):
        self.windData = windData
        self.customDailyGenerationFunction = customDailyGenerationFunction
    def getDailyEnergyProduction(self):
        if not self.customDailyGenerationFunction:
            dailyTotalEnergy = [0]*self.windData
            count = 0
            for value in self.windData:
                dailyTotalEnergy[count] += value * 4
                count += 1
            return dailyTotalEnergy
        else:
            return self.customDailyGenerationFunction()
    def getHourlyEnergyProduction(self):
        return None