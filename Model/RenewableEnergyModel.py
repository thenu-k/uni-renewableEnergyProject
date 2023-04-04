from .helperFunctions import normalizeDataSet
from math import pi
from .ComponentModels.TidalEnergyModel import TidalEnergyModel
from .ComponentModels.WindEnergyModel import WindEnergyModel
from .ComponentModels.SolarEnergyModel import SolarEnergyModel
from .ComponentModels.EnergyStorageModel import EnergyStorageModel

class RenewableEnergyModel:
    def __init__(self, TidalEnergyModel: type[TidalEnergyModel], WindEnergyModel: type[WindEnergyModel], SolarEnergyModel: type[SolarEnergyModel], EnergyStorageModel: type[EnergyStorageModel], energyDemand: type[list]):
        if not TidalEnergyModel and not WindEnergyModel and not SolarEnergyModel:
            raise Exception("No energy model was provided")
        self.TidalEnergyModel = TidalEnergyModel
        self.WindEnergyModel = WindEnergyModel
        self.SolarEnergyModel = SolarEnergyModel
        self.EnergyStorageModel = EnergyStorageModel
        self.dataValues = len(self.TidalEnergyModel.tidalData)
        self.totalDailyEnergyProduction = None
        self.energyDemand = energyDemand
        self.netDailyEnergyDemand = None
    def getDailyTotalEnergyProduction(self):
        if self.TidalEnergyModel:
            dailyTidalEnergyProduction = self.TidalEnergyModel.getDailyEnergyProduction()
        else:
            dailyTidalEnergyProduction = [0]*self.dataValues
        if self.SolarEnergyModel:
            dailySolarEnergyProduction = self.SolarEnergyModel.getDailyEnergyProduction()
        else:
            dailySolarEnergyProduction = [0]*self.dataValues
        if self.WindEnergyModel:
            dailyWindEnergyProduction = self.WindEnergyModel.getDailyEnergyProduction()
        else:
            dailyWindEnergyProduction = [0]*self.dataValues
        totalDailyEnergyProduction = [0]*self.dataValues
        for count in range(self.dataValues):
            totalDailyEnergyProduction[count] = dailyTidalEnergyProduction[count] + dailyWindEnergyProduction[count] + dailySolarEnergyProduction[count]
        self.totalDailyEnergyProduction = totalDailyEnergyProduction
        return totalDailyEnergyProduction
    def getNetDailyEnergyDemand(self, frequencyOfData):
        netDailyEnergyDemand = [0]*self.dataValues
        for count in range(self.dataValues):
            netDailyEnergyDemand[count] = self.energyDemand[count] - self.totalDailyEnergyProduction[count]
        return netDailyEnergyDemand
    def accountForEnergyStorage(self):
        return None
