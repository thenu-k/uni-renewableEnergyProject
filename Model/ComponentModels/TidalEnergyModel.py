from ..helperFunctions import normalizeDataSet
from math import pi

class TidalEnergyModel:
    def __init__(self, tidalData:type[list[float]], unitCount:type[int], efficiency:type[float], bladeDiameter:type[float], mediumDensity:type[float], headHeight:type[float], accelerationDueToGravity:type[float], isCrossFlow:type[bool], customPower: type[float]):
        if efficiency > 1:
            raise ValueError("Efficiency cannot be greater than 1")
        self.tidalData = tidalData
        self.unitCount = unitCount
        self.efficiency = efficiency
        self.bladeDiameter = bladeDiameter
        self.bladeSweepArea = pi * (self.bladeDiameter/2)**2
        self.mediumDensity = mediumDensity
        self.accelerationDueToGravity = accelerationDueToGravity
        self.isCrossFlow = isCrossFlow
        if isCrossFlow:
            self.headHeight = headHeight
        else:
            self.headHeight = None
        if customPower:
            self.customPower = customPower
        else:
            self.customPower = None
    def getIdealPowerPerUnit(self, velocity):
        if self.customPower:
            raise ValueError("Custom power cannot be used with this function")
        if self.isCrossFlow:
            print('using cross flow')
            return self.mediumDensity * self.bladeSweepArea * velocity * self.accelerationDueToGravity * self.headHeight
        else:
            return self.mediumDensity * self.bladeSweepArea * velocity**3 * 0.5
    def getDailyEnergyProduction(self):
        dailyTotalEnergy = [0]*len(self.tidalData)
        count = 0
        for currentSpeedValue in self.tidalData:
            if self.customPower:
                dailyTotalEnergy[count] += 24 * self.unitCount * self.customPower
            else:   
                dailyTotalEnergy[count] += 24 * self.unitCount * self.getIdealPowerPerUnit(currentSpeedValue) * self.efficiency 
            count += 1
        return dailyTotalEnergy
    def testSingleUnitEnergyProduction(self, velocity, isDaily, isYearly):
        if isDaily:
            return 24 * self.unitCount * self.efficiency * self.getIdealPowerPerUnit(velocity)
        elif isYearly:
            return 336 * 24 * self.unitCount * self.efficiency * self.getIdealPowerPerUnit(velocity)