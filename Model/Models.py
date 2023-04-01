from .helperFunctions import normalizeDataSet

class RenewableEnergyModel:
    def __init__(self, TidalEnergyModel, WindEnergyModel, SolarEnergyModel, EnergyStorage):
        self.TidalEnergyModel = TidalEnergyModel
        self.WindEnergyModel = WindEnergyModel
        self.SolarEnergyModel = SolarEnergyModel
        self.dataValues = len(self.TidalEnergyModel.normalizedTidalData)
        self.totalEnergy = None
        self.energyDemand = None
        self.netEnergyDemand = None
    def getPowerGeneration(self):
        tidalEnergyGeneration = self.TidalEnergyModel.getTidalEnergyGeneration()
        windEnergyGeneration = self.WindEnergyModel.getWindGeneration()
        solarEnergyGeneration = self.SolarEnergyModel.getSolarGeneration()
        totalEnergy = [0]*self.dataValues
        for count in range(self.dataValues):
            totalEnergy[count] = tidalEnergyGeneration[count] + windEnergyGeneration[count] + solarEnergyGeneration[count]
        self.totalEnergy = totalEnergy
        return totalEnergy
    def getNetEnergyDemand(self, energyDemand, frequencyOfData):
        self.energyDemand = normalizeDataSet(energyDemand, frequencyOfData)
        netEnergyDemand = [0]*self.dataValues
        for count in range(self.dataValues):
            netEnergyDemand[count] = self.energyDemand[count] - self.totalEnergy[count]
        self.netEnergyDemand = netEnergyDemand
        return self.netEnergyDemand

class TidalEnergyModel:
    def __init__(self, tidalData,isCSV, frequencyOfData):
        self.tidalData = tidalData
        self.frequencyOfData = frequencyOfData
        self.normalizedTidalData = normalizeDataSet(self.tidalData, self.frequencyOfData)
    def getTidalEnergyGeneration(self):
        totalEnergy = [0]*len(self.normalizedTidalData)
        count = 0
        for value in self.normalizedTidalData:
            totalEnergy[count] += value * 3
            count += 1
        return totalEnergy
    
class WindEnergyModel:
    def __init__(self, windData, frequencyOfData, isCSV):
        self.windData = windData
        self.frequencyOfData = frequencyOfData
        self.normalizedWindData = normalizeDataSet(self.windData, self.frequencyOfData)
    def getWindGeneration(self):
        totalEnergy = [0]*len(self.normalizedWindData)
        count = 0
        for value in self.normalizedWindData:
            totalEnergy[count] += value * 4
            count += 1
        return totalEnergy
    
class SolarEnergyModel:
    def __init__(self, solarData, frequencyOfData, isCSV):
        self.solarData = solarData
        self.frequencyOfData = frequencyOfData
        self.normalizedSolarData = normalizeDataSet(self.solarData, self.frequencyOfData)
    def getSolarGeneration(self):
        totalEnergy = [0]*len(self.normalizedSolarData)
        count = 0
        for value in self.normalizedSolarData:
            totalEnergy[count] += value * 5
            count += 1
        return totalEnergy
    
class EnergyStorage:
    def __init__(self, liquidDensity, accelerationDueToGravity, maxFlowRate, efficiency, maxTopVolume, maxBottomValue, turbinePower):
        self.liquidDensity = liquidDensity
        self.accelerationDueToGravity = accelerationDueToGravity
        self.maxFlowRate = maxFlowRate
        self.efficiency = efficiency
        self.maxTopVolume = maxTopVolume
        self.maxBottomValue = maxBottomValue
        self.turbinePower = turbinePower
    def getStorageFacility():
        return None