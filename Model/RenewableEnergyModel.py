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
