from .helperFunctions import normalizeDataSet
from math import pi

class RenewableEnergyModel:
    def __init__(self, TidalEnergyModel, WindEnergyModel, SolarEnergyModel, EnergyStorage):
        self.TidalEnergyModel = TidalEnergyModel
        self.WindEnergyModel = WindEnergyModel
        self.SolarEnergyModel = SolarEnergyModel
        self.EnergyStorage = EnergyStorage
        self.dataValues = len(self.TidalEnergyModel.normalizedTidalData)
        self.totalDailyEnergyProduction = None
        self.dailyEnergyDemand = None
        self.netDailyEnergyDemand = None
    def getDailyTotalEnergyProduction(self):
        dailyTidalEnergyProduction = self.TidalEnergyModel.getDailyEnergyProduction()
        dailyWindEnergyProduction = self.WindEnergyModel.getDailyEnergyProduction()
        dailySolarEnergyProduction = self.SolarEnergyModel.getDailyEnergyProduction()
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
    def accountForEnergyStorage(self):
        return None

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
    
class WindEnergyModel:
    def __init__(self, windData, frequencyOfData, isCSV, customDailyGenerationFunction):
        self.windData = windData
        self.frequencyOfData = frequencyOfData
        if not customDailyGenerationFunction:
            self.normalizedWindData = normalizeDataSet(self.windData, self.frequencyOfData)
        self.customDailyGenerationFunction = customDailyGenerationFunction
    def getDailyEnergyProduction(self):
        if not self.customDailyGenerationFunction:
            dailyTotalEnergy = [0]*len(self.normalizedWindData)
            count = 0
            for value in self.normalizedWindData:
                dailyTotalEnergy[count] += value * 4
                count += 1
            return dailyTotalEnergy
        else:
            return self.customDailyGenerationFunction()
    def getHourlyEnergyProduction(self):
        return None
    
class SolarEnergyModel:
    def __init__(self, solarData, frequencyOfData, isCSV):
        self.solarData = solarData
        self.frequencyOfData = frequencyOfData
        self.normalizedSolarData = normalizeDataSet(self.solarData, self.frequencyOfData)
    def getDailyEnergyProduction(self):
        dailyTotalEnergy = [0]*len(self.normalizedSolarData)
        count = 0
        for value in self.normalizedSolarData:
            dailyTotalEnergy[count] += value * 5
            count += 1
        return dailyTotalEnergy
    
class EnergyStorage:
    def __init__(self, liquidDensity, accelerationDueToGravity, maxFlowRate, efficiency, maxTopVolume, maxBottomValue, turbinePower, dataValues):
        self.liquidDensity = liquidDensity
        self.accelerationDueToGravity = accelerationDueToGravity
        self.maxFlowRate = maxFlowRate
        self.efficiency = efficiency
        self.maxTopVolume = maxTopVolume
        self.currentTopVolume = None
        self.maxBottomValue = maxBottomValue
        self.currentBottomValue = None
        self.turbinePower = turbinePower
        self.dailyMaximumEnergyPossible = self.turbinePower * 24 * 60 * 60
        self.dailyStorageEnergyUsage = [0]*dataValues
    def updateTopVolume(self, newVolume):
        self.currentTopVolume = newVolume
    def updateBottomVolume(self, newVolume):
        self.currentBottomValue = newVolume
    def calculateWaterMovement(self, currentNetEnergyDemand):
        energyRequired = True if currentNetEnergyDemand>0 else False
        if currentNetEnergyDemand>self.dailyMaximumEnergyPossible:
            energyMovement = self.dailyMaximumEnergyPossible
        else:
            energyMovement = currentNetEnergyDemand
        waterMovement = energyMovement / (self.liquidDensity * self.accelerationDueToGravity)
        return None