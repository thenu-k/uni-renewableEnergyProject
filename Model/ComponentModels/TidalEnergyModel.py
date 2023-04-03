from ..helperFunctions import normalizeDataSet
from math import pi

class TidalEnergyModel:
    def __init__(self, tidalData:type[list[float]], unitCount:type[int], efficiency:type[float], bladeDiameter:type[float], mediumDensity:type[float], headHeight:type[float], accelerationDueToGravity:type[float]):
        if efficiency > 1:
            raise ValueError("Efficiency cannot be greater than 1")
        self.tidalData = tidalData
        self.unitCount = unitCount
        self.efficiency = efficiency
        self.bladeDiameter = bladeDiameter
        self.bladeSweepArea = pi * (self.bladeDiameter/2)**2
        self.mediumDensity = mediumDensity
        self.accelerationDueToGravity = accelerationDueToGravity
        self.headHeight = headHeight
    def getIdealPowerPerUnit(self, velocity):
        return self.mediumDensity * self.bladeSweepArea * velocity * self.accelerationDueToGravity * self.headHeight
    def getDailyEnergyProduction(self):
        dailyTotalEnergy = [0]*len(self.tidalData)
        count = 0
        for currentSpeedValue in self.tidalData:
            dailyTotalEnergy[count] += 24 * self.unitCount * self.getIdealPowerPerUnit(currentSpeedValue) * self.efficiency 
            count += 1
        return dailyTotalEnergy
    def testSingleUnitEnergyProduction(self, velocity, isDaily, isYearly):
        if isDaily:
            return 24 * self.unitCount * self.efficiency * self.idealPowerPerUnit(velocity)
        elif isYearly:
            return 365 * 24 * self.unitCount * self.efficiency * self.idealPowerPerUnit(velocity)