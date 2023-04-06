from ..helperFunctions import normalizeDataSet
from math import pi

class WindEnergyModel:
    # create a type of a function that returns a list of integers: type[function: list[int]]
    def __init__(self, windData: type[list[float]],unitCount:type[int], customDailyGenerationFunction, efficiency:type[float], bladeDiameter:type[float], mediumDensity:type[float]):
        self.windData = windData
        if not customDailyGenerationFunction:
            self.customDailyGenerationFunction = None
            self.unitCount = unitCount
            self.efficiency = efficiency
            self.bladeDiameter = bladeDiameter
            self.mediumDensity = mediumDensity
            self.areaSwept = (self.bladeDiameter/2)**2 * pi
        else:
            self.customDailyGenerationFunction = customDailyGenerationFunction
    def getIdealPowerProductionPerUnit(self, velocity:type[float]):
        return 0.5 * self.mediumDensity * (velocity ** 3) * self.areaSwept
    def getUnitlyEnergyProduction(self, hoursPerUnit:type[int]):
        if not self.customDailyGenerationFunction:
            unitlyTotalEnergy = [0]*len(self.windData)
            count = 0
            for velocity in self.windData:
                unitlyTotalEnergy[count] = self.getIdealPowerProductionPerUnit(velocity) * self.unitCount * self.efficiency * hoursPerUnit
                count += 1
            return unitlyTotalEnergy
        else:
            return self.customDailyGenerationFunction()