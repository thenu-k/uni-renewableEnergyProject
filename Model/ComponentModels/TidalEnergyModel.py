from ..helperFunctions import normalizeDataSet
from math import pi

class TidalEnergyModel:
    def __init__(self, tidalData,isCSV, frequencyOfData, unitCount, efficiency, bladeDiameter, mediumDensity, headHeight, accelerationDueToGravity):
        self.tidalData = tidalData
        self.frequencyOfData = frequencyOfData
        self.normalizedTidalData = normalizeDataSet(self.tidalData, self.frequencyOfData)
        self.unitCount = unitCount
        self.efficiency = efficiency
        self.bladeDiameter = bladeDiameter
        self.bladeSweepArea = pi * (self.bladeDiameter/2)**2
        self.mediumDensity = mediumDensity
        self.accelerationDueToGravity = accelerationDueToGravity
        self.headHeight = headHeight
        self.idealPowerPerUnit  = lambda currVelocity:  self.mediumDensity * self.bladeSweepArea * currVelocity * self.accelerationDueToGravity * self.headHeight
    def getDailyEnergyProduction(self):
        dailyTotalEnergy = [0]*len(self.normalizedTidalData)
        count = 0
        for currentSpeedValue in self.normalizedTidalData:
            dailyTotalEnergy[count] += 24 * self.unitCount * self.idealPowerPerUnit(currentSpeedValue) * self.efficiency 
            count += 1
        print(sum(dailyTotalEnergy))
        return dailyTotalEnergy
    def testSingleUnitEnergyProduction(self, velocity, isDaily, isYearly):
        if isDaily:
            return 24 * self.unitCount * self.efficiency * self.idealPowerPerUnit(velocity)
        elif isYearly:
            return 365 * 24 * self.unitCount * self.efficiency * self.idealPowerPerUnit(velocity)