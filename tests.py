from Model.RenewableEnergyModel import RenewableEnergyModel
from Model.ComponentModels.EnergyStorageModel import EnergyStorageModel
from Model.ComponentModels.TidalEnergyModel import TidalEnergyModel
from Model.ComponentModels.WindEnergyModel import WindEnergyModel
from Model.ComponentModels.SolarEnergyModel import SolarEnergyModel
from UI.UI import *
from Data.Data import Data
import matplotlib as mpl
formatter = mpl.ticker.EngFormatter()

numDataPoints = 365
error = 0.025

# Instantiating the component facilities
tidalInstance =  TidalEnergyModel(
    tidalData=Data.generateTidalData(
        error=error,
        valuesRequired=numDataPoints,
    ), 
    unitCount = 5,
    efficiency = 0.87,
    bladeDiameter = 8,
    mediumDensity = 997.77,
    accelerationDueToGravity=9.81,
    headHeight=20,
    isCrossFlow=True,
    customPower=None,
)
windInstance = WindEnergyModel(
    windData=Data.generateWindSpeedData(
        error=error,
        interpolate=True,
        valuesRequired = numDataPoints,
        currentDataSpacing=30,
    ),
    unitCount=12,
    efficiency=0.4,
    bladeDiameter=174,
    mediumDensity=1.225,
    customDailyGenerationFunction=None,
)
solarInstance = SolarEnergyModel(
    solarData=Data.retrieveSolarData(error=0),
)
storageInstance = EnergyStorageModel(
    liquidDensity=1000,
    accelerationDueToGravity=9.81,
    maxFlowRate=100,
    efficiency=0.5,
    maxTopVolume=1000,
    currentTopVolume=100,
    maxBottomValue=1000,
    currentBottomValue=100,
    heightDifference=250,
    turbinePower=1000,
    dataValues=numDataPoints
)
# Connecting the facilities together
renewableInstance = RenewableEnergyModel(
    TidalEnergyModel=tidalInstance,
    WindEnergyModel=windInstance,
    SolarEnergyModel=None,
    EnergyStorageModel=storageInstance,
    dataValues=numDataPoints,
    energyDemand=Data.generateEnergyDemandData(
        error=error,
        interpolate=True,
        valuesRequired=numDataPoints,
        currentDataSpacing=30
    )
)
tidalEnergyGeneration = renewableInstance.TidalEnergyModel.getDailyEnergyProduction()
windEnergyGeneration = renewableInstance.WindEnergyModel.getDailyEnergyProduction()
totalEnergyGeneration = renewableInstance.getDailyTotalEnergyProduction()
netEnergyDemand = renewableInstance.getNetDailyEnergyDemand()


totalTest  = [windEnergyGeneration[count] + tidalEnergyGeneration[count] for count in range(336)]
# print(formatter(windEnergyGeneration[359]))

# compareProd(
#     energyProd=windEnergyGeneration,
#     energyProd2 = tidalEnergyGeneration,
#     energyDefecit = tidalEnergyGeneration,
#     energyTotal=windEnergyGeneration,
#     energyDemand=renewableInstance.energyDemand,
# )

print(renewableInstance.EnergyStorageModel.accountForStorage(
    netEnergyDemand=[24000, -12000],
    assumeUnlimitedWater=False,
))