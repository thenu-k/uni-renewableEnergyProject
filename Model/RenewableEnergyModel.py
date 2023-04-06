from .helperFunctions import normalizeDataSet
from math import pi
from .ComponentModels.TidalEnergyModel import TidalEnergyModel
from .ComponentModels.WindEnergyModel import WindEnergyModel
from .ComponentModels.SolarEnergyModel import SolarEnergyModel
from .ComponentModels.EnergyStorageModel import EnergyStorageModel

class RenewableEnergyModel:
    def __init__(self, TidalEnergyModel: type[TidalEnergyModel], WindEnergyModel: type[WindEnergyModel], SolarEnergyModel: type[SolarEnergyModel], EnergyStorageModel: type[EnergyStorageModel], energyDemand: type[list], dataValues:type[int]):
        if not TidalEnergyModel and not WindEnergyModel and not SolarEnergyModel:
            raise Exception("No energy model was provided")
        self.TidalEnergyModel = TidalEnergyModel
        self.WindEnergyModel = WindEnergyModel
        self.SolarEnergyModel = SolarEnergyModel
        self.EnergyStorageModel = EnergyStorageModel
        self.dataValues = dataValues
        self.totalDailyEnergyProduction = None
        self.energyDemand = energyDemand
        self.netDailyEnergyDemand = None
        self.finalEnergyDemand = None
    def getDailyTotalEnergyProduction(self):
        if not self.TidalEnergyModel==None:
            dailyTidalEnergyProduction = self.TidalEnergyModel.getDailyEnergyProduction()
        else:
            dailyTidalEnergyProduction = [0]*self.dataValues
        if not self.SolarEnergyModel==None:
            dailySolarEnergyProduction = self.SolarEnergyModel.getDailyEnergyProduction()
        else:
            dailySolarEnergyProduction = [0]*self.dataValues
        if not self.WindEnergyModel==None:
            dailyWindEnergyProduction = self.WindEnergyModel.getDailyEnergyProduction()
        else:
            dailyWindEnergyProduction = [0]*self.dataValues
        totalDailyEnergyProduction = [0]*self.dataValues
        for count in range(self.dataValues):
            totalDailyEnergyProduction[count] = dailyTidalEnergyProduction[count] + dailyWindEnergyProduction[count] + dailySolarEnergyProduction[count]
        self.totalDailyEnergyProduction = totalDailyEnergyProduction
        return totalDailyEnergyProduction
    def getNetDailyEnergyDemand(self):
        netDailyEnergyDemand = [0]*self.dataValues
        for count in range(self.dataValues):
            netDailyEnergyDemand[count] = self.energyDemand[count] - self.totalDailyEnergyProduction[count]
        self.netDailyEnergyDemand = netDailyEnergyDemand
        return netDailyEnergyDemand
    def runSimulations(self, simulationCount:type[int]):
        workingRuns = 0
        for count in range(simulationCount):
            pass
        return None
    def accountForEnergyStorage(self):
        energyMovementValues = self.EnergyStorageModel.simulate(self.netDailyEnergyDemand, False)
        excessEnergy = []
        count = 0
        for value in energyMovementValues:
            excessEnergy.append(self.netDailyEnergyDemand[count] - value['energyGenerated'])
            count += 1
        return [excessEnergy, energyMovementValues]
