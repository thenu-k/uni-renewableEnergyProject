from .helperFunctions import normalizeDataSet
from math import pi
from .ComponentModels.TidalEnergyModel import TidalEnergyModel
from .ComponentModels.WindEnergyModel import WindEnergyModel
from .ComponentModels.SolarEnergyModel import SolarEnergyModel
from .ComponentModels.EnergyStorageModel import EnergyStorageModel

class RenewableEnergyModel:
    def __init__(self, TidalEnergyModel: type[TidalEnergyModel], WindEnergyModel: type[WindEnergyModel], SolarEnergyModel: type[SolarEnergyModel], EnergyStorageModel: type[EnergyStorageModel], energyDemand: type[list], dataValues:type[int], hoursPerUnit:type[int]):
        if not TidalEnergyModel and not WindEnergyModel and not SolarEnergyModel:
            raise Exception("No energy model was provided")
        self.TidalEnergyModel = TidalEnergyModel
        self.WindEnergyModel = WindEnergyModel
        self.SolarEnergyModel = SolarEnergyModel
        self.EnergyStorageModel = EnergyStorageModel
        self.dataValues = dataValues
        self.totalUnitlyEnergyProduction = None
        self.energyDemand = energyDemand
        self.netUnitlyEnergyDemand = None
        self.finalEnergyDemand = None
        self.hoursPerUnit = hoursPerUnit
    def getUnitlyTotalEnergyProduction(self):
        if not self.TidalEnergyModel==None:
            unitlyTidalEnergyProduction = self.TidalEnergyModel.getUnitlyEnergyProduction(unitCount=self.dataValues)
        else:
            unitlyTidalEnergyProduction = [0]*self.dataValues
        if not self.SolarEnergyModel==None:
            unitlySolarEnergyProduction = self.SolarEnergyModel.getUnitlyEnergyProduction()
        else:
            unitlySolarEnergyProduction = [0]*self.dataValues
        if not self.WindEnergyModel==None:
            unitlyWindEnergyProduction = self.WindEnergyModel.getUnitlyEnergyProduction(hoursPerUnit=self.hoursPerUnit)
        else:
            unitlyWindEnergyProduction = [0]*self.dataValues
        totalUnitlyEnergyProduction = [0]*self.dataValues
        for count in range(self.dataValues):
            totalUnitlyEnergyProduction[count] = unitlyTidalEnergyProduction[count] + unitlyWindEnergyProduction[count] + unitlySolarEnergyProduction[count]
        self.totalUnitlyEnergyProduction = totalUnitlyEnergyProduction
        return [totalUnitlyEnergyProduction, unitlyTidalEnergyProduction, unitlyWindEnergyProduction, unitlySolarEnergyProduction]
    def getNetUnitlyEnergyDemand(self):
        netUnitlyEnergyDemand = [0]*self.dataValues
        for count in range(self.dataValues):
            netUnitlyEnergyDemand[count] = self.energyDemand[count] - self.totalUnitlyEnergyProduction[count]
        self.netUnitlyEnergyDemand = netUnitlyEnergyDemand
        return netUnitlyEnergyDemand
    def runSimulations(self, simulationCount:type[int]):
        workingRuns = 0
        for count in range(simulationCount):
            pass
        return None
    def accountForEnergyStorage(self):
        energyMovementValues = self.EnergyStorageModel.simulate(self.netUnitlyEnergyDemand, False)
        excessEnergy = []
        count = 0
        for value in energyMovementValues:
            excessEnergy.append(self.netUnitlyEnergyDemand[count] - value['energyGenerated'])
            count += 1
        return [excessEnergy, energyMovementValues]
