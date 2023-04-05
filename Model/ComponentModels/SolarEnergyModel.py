from ..helperFunctions import normalizeDataSet

class SolarEnergyModel:
    def __init__(self, solarData, customPower, unitCount):
        self.solarData = solarData
        self.customPower = customPower
        self.unitCount = unitCount
    def getIdealPowerPerUnit(self):
        if self.customPower is not None:
            return self.customPower
        return 0
    def getDailyEnergyProduction(self):
        dailyTotalEnergy = [0]*len(self.solarData)
        count = 0
        for value in self.solarData:
            dailyTotalEnergy[count] += self.getIdealPowerPerUnit() * self.unitCount * 24
            count += 1
        return dailyTotalEnergy