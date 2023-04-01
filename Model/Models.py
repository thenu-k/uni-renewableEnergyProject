from .helperFunctions import normalizeDataSet

class RenewableEnergyModel:
    def __init__(self, TidalEnergyModel, WindEnergyModel, SolarEnergyModel, EnergyStorage):
        self.TidalEnergyModel = TidalEnergyModel
        self.WindEnergyModel = WindEnergyModel
        self.SolarEnergyModel = SolarEnergyModel
        self.dataValues = len(self.TidalEnergyModel.normalizedTidalData)
        self.totalDailyEnergyProduction = None
        self.dailyEnergyDemand = None
        self.netDailyEnergyDemand = None
    def getDailyTotalEnergyProduction(self):
        dailyTidalEnergyProduction = self.TidalEnergyModel.getTidalEnergyGeneration()
        dailyWindEnergyProduction = self.WindEnergyModel.getWindGeneration()
        dailySolarEnergyProduction = self.SolarEnergyModel.getSolarGeneration()
        totalDailyEnergyProduction = [0]*self.dataValues
        for count in range(self.dataValues):
            totalDailyEnergyProduction[count] = dailyTidalEnergyProduction[count] + dailyWindEnergyProduction[count] + dailySolarEnergyProduction[count]
        self.totalDailyEnergyProduction = totalDailyEnergyProduction
        return totalDailyEnergyProduction
    def getNetDailyEnergyDemand(self, energyDemand, frequencyOfData):
        self.dailyEnergyDemand = normalizeDataSet(energyDemand, frequencyOfData)
        netDailyEnergyDemand = [0]*self.dataValues
        for count in range(self.dataValues):
            netDailyEnergyDemand[count] = self.dailyEnergyDemand[count] - self.totalDailyEnergyProduction[count]
        self.netDailyEnergyDemand = netDailyEnergyDemand
        return self.netDailyEnergyDemand

class TidalEnergyModel:
    def __init__(self, tidalData,isCSV, frequencyOfData):
        self.tidalData = tidalData
        self.frequencyOfData = frequencyOfData
        self.normalizedTidalData = normalizeDataSet(self.tidalData, self.frequencyOfData)
    def getTidalEnergyGeneration(self):
        dailyTotalEnergy = [0]*len(self.normalizedTidalData)
        count = 0
        for value in self.normalizedTidalData:
            dailyTotalEnergy[count] += value * 3
            count += 1
        return dailyTotalEnergy
    
class WindEnergyModel:
    def __init__(self, windData, frequencyOfData, isCSV):
        self.windData = windData
        self.frequencyOfData = frequencyOfData
        self.normalizedWindData = normalizeDataSet(self.windData, self.frequencyOfData)
    def getWindGeneration(self):
        dailyTotalEnergy = [0]*len(self.normalizedWindData)
        count = 0
        for value in self.normalizedWindData:
            dailyTotalEnergy[count] += value * 4
            count += 1
        return dailyTotalEnergy
    
class SolarEnergyModel:
    def __init__(self, solarData, frequencyOfData, isCSV):
        self.solarData = solarData
        self.frequencyOfData = frequencyOfData
        self.normalizedSolarData = normalizeDataSet(self.solarData, self.frequencyOfData)
    def getSolarGeneration(self):
        dailyTotalEnergy = [0]*len(self.normalizedSolarData)
        count = 0
        for value in self.normalizedSolarData:
            dailyTotalEnergy[count] += value * 5
            count += 1
        return dailyTotalEnergy
    
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