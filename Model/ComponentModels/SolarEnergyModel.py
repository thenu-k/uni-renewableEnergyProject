from ..helperFunctions import normalizeDataSet

class SolarEnergyModel:
    def __init__(self, solarData, customPower, unitCount, areaPerUnit, efficiency, scalingFactor):
        self.solarData = solarData
        self.customPower = customPower
        self.unitCount = unitCount
        self.areaPerUnit = areaPerUnit
        self.efficiency = efficiency
        self.scalingFactor = scalingFactor
    def getUnitlyEnergyProduction(self):
        unitlyGeneration = []
        if self.customPower is None:
            for solarEnergyReading in self.solarData:
                unitlyGeneration.append(solarEnergyReading*self.unitCount*self.areaPerUnit*self.efficiency * self.scalingFactor)
            return unitlyGeneration
        else:
            return None