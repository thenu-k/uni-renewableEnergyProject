from ..helperFunctions import normalizeDataSet
from math import pi
import random

class TidalEnergyModel:
    def __init__(self, topTidalCurrentSpeed, bottomTidalCurrentSpeed, unitCount:type[int], efficiency:type[float], bladeDiameter:type[float], mediumDensity:type[float], headHeight:type[float], accelerationDueToGravity:type[float], isCrossFlow:type[bool], customPower: type[float], isDaily:type[bool], error:type[float]):
        if efficiency > 1:
            raise ValueError("Efficiency cannot be greater than 1")
        self.unitCount = unitCount
        self.efficiency = efficiency
        self.bladeDiameter = bladeDiameter
        self.bladeSweepArea = pi * (self.bladeDiameter/2)**2
        self.mediumDensity = mediumDensity
        self.accelerationDueToGravity = accelerationDueToGravity
        self.isCrossFlow = isCrossFlow
        self.topTidalCurrentSpeed = topTidalCurrentSpeed
        self.bottomTidalCurrentSpeed = bottomTidalCurrentSpeed
        self.isDaily = isDaily
        self.error = error
        if isCrossFlow:
            self.headHeight = headHeight
        else:
            self.headHeight = None
        if customPower:
            self.customPower = customPower
        else:
            self.customPower = None
    def getIdealPowerPerUnit(self, velocity):
        # add random error from uniform distribution
        velocity = velocity + random.uniform(-velocity*self.error, velocity*self.error)
        if self.customPower:
            raise ValueError("Custom power cannot be used with this function")
        if self.isCrossFlow:
            return self.mediumDensity * self.bladeSweepArea * velocity * self.accelerationDueToGravity * self.headHeight
        else:
            return self.mediumDensity * self.bladeSweepArea * velocity**3 * 0.5
    def getDailyEnergyProduction(self, days):
        dailyEnergyProduction = [0]*days
        altWeek = False
        for count in range(days):
            dailyEnergyProduction[count] += 24 * self.unitCount * self.getIdealPowerPerUnit(self.topTidalCurrentSpeed if not altWeek else self.bottomTidalCurrentSpeed) * self.efficiency 
            altWeek = not altWeek if (count+1) % 7==0 else altWeek
        return dailyEnergyProduction
    def getMonthlyEnergyProduction(self, months):
        dailyEnergyProduction = self.getDailyEnergyProduction(months*30)
        monthlyEnergyProduction = [0]*months
        for count in range(months):
            monthlyEnergyProduction[count] = sum(dailyEnergyProduction[count*30:(count+1)*30])
        return monthlyEnergyProduction
    def getUnitlyEnergyProduction(self, unitCount):
        if self.isDaily:
            return self.getDailyEnergyProduction(unitCount)
        else:
            return self.getMonthlyEnergyProduction(unitCount)