from Model.RenewableEnergyModel import RenewableEnergyModel
from Model.ComponentModels.EnergyStorageModel import EnergyStorageModel
from Model.ComponentModels.TidalEnergyModel import TidalEnergyModel
from Model.ComponentModels.WindEnergyModel import WindEnergyModel
from Model.ComponentModels.SolarEnergyModel import SolarEnergyModel
from UI.UI import *
from Data.Data import *
from Data.helperFunctions import *
import matplotlib as mpl
formatter = mpl.ticker.EngFormatter()

# Instantiating the component facilities
tidalInstance =  TidalEnergyModel(
    tidalData=tidalData, 
    unitCount = 1,
    efficiency = 0.87,
    bladeDiameter = 0.4,
    mediumDensity = 997.77,
    accelerationDueToGravity=9.81,
    headHeight=40,
    isCrossFlow=True,
    customPower=None,
)
windInstance = WindEnergyModel(
    windData=None,
    customDailyGenerationFunction=generateWindSpeedData,
)
solarInstance = SolarEnergyModel(
    solarData=solarData, 
)
storageInstance = EnergyStorageModel(
    liquidDensity=1000,
    accelerationDueToGravity=9.81,
    maxFlowRate=100,
    efficiency=0.5,
    maxTopVolume=100,
    maxBottomValue=100,
    turbinePower=100000,
    dataValues=len(tidalData)
)
# Connecting the facilities together
renewableInstance = RenewableEnergyModel(tidalInstance, windInstance, solarInstance, storageInstance)
# tidalEnergyGeneration = renewableInstance.TidalEnergyModel.getDailyEnergyProduction()
# windEnergyGeneration = renewableInstance.WindEnergyModel.getDailyEnergyProduction()
# solarEnergyGeneration = renewableInstance.SolarEnergyModel.getDailyEnergyProduction()
# totalEnergyGeneration = renewableInstance.getDailyTotalEnergyProduction()
# netEnergyDemand = renewableInstance.getNetDailyEnergyDemand(
#     energyDemand=energyDemandData, frequencyOfData=1,
# )

waterMovement = renewableInstance.EnergyStorageModel.accountForStorage(netEnergyDemand, assumeUnlimitedWater=True)
# print(waterMovement)

# print(renewableInstance.TidalEnergyModel.testSingleUnitEnergyProduction(velocity=1.15, isDaily=False, isYearly=True))
# print(sum(renewableInstance.dailyEnergyDemand))
# totalTest  = [windEnergyGeneration[count] + tidalEnergyGeneration[count] for count in range(336)]
#convert number to engineering notation
# print(formatter(sum(tidalEnergyGeneration)))
print(formatter(renewableInstance.TidalEnergyModel.getIdealPowerPerUnit((1.15+0.6)/2)*336*24*0.87))

# compareProd(
#     energyProd=tidalEnergyGeneration,
#     energyProd2 = windEnergyGeneration,
#     energyDefecit = netEnergyDemand,
#     energyTotal=totalTest,
#     energyDemand=energyDemandData,
# )