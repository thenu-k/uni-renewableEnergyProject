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

solarData = Data.retrieveSolarData(
    error=error,
    interpolate=True,
    valuesRequired=numDataPoints,
    currentDataSpacing=30,
)

# Instantiating the component facilities
tidalInstance =  TidalEnergyModel(
    tidalData=Data.generateTidalData(
        error=error,
        valuesRequired=numDataPoints,
    ), 
    unitCount = 120,
    efficiency = 0.87,
    bladeDiameter = 40,
    mediumDensity = 997.77,
    accelerationDueToGravity=9.81,
    headHeight=10,
    isCrossFlow=False,
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
    efficiency=0.3,
    bladeDiameter=174,
    mediumDensity=1.225,
    customDailyGenerationFunction=None,
)
solarInstance = SolarEnergyModel(
    solarData=solarData,
    efficiency=0.25,
    customPower=None,
    unitCount=1e6,
    areaPerUnit=1
)
storageInstance = EnergyStorageModel(
    liquidDensity=1000,
    accelerationDueToGravity=9.81,
    maxFlowRate=100,
    efficiency=1,
    maxTopVolume=7e6,
    currentTopVolume=5e6,
    maxBottomValue=7e6,
    currentBottomValue=5e6,
    heightDifference=250,
    turbinePower=440e6,
    minimumWaterLevel=0,
    dataValues=numDataPoints
)
# Connecting the facilities together
energyDemandData = Data.generateEnergyDemandData(
        error=error,
        interpolate=True,
        valuesRequired=numDataPoints,
        currentDataSpacing=30
)
renewableInstance = RenewableEnergyModel(
    TidalEnergyModel=tidalInstance,
    WindEnergyModel=windInstance,
    SolarEnergyModel=solarInstance,
    EnergyStorageModel=storageInstance,
    dataValues=numDataPoints,
    energyDemand=energyDemandData
)
tidalEnergyGeneration = renewableInstance.TidalEnergyModel.getDailyEnergyProduction()
windEnergyGeneration = renewableInstance.WindEnergyModel.getDailyEnergyProduction()
solarEnergyGeneration = renewableInstance.SolarEnergyModel.getDailyEnergyProduction()
totalEnergyGeneration = renewableInstance.getDailyTotalEnergyProduction()
netEnergyDemand = renewableInstance.getNetDailyEnergyDemand()
[excessEnergy, energyMovementValues] = renewableInstance.accountForEnergyStorage()

print(formatter(sum(energyDemandData)))

# for count in range(12):
#     print(formatter(sum(solarEnergyGeneration[count*30:(count+1)*30])))

compareProd(
    graphs=[
        tidalEnergyGeneration,
        windEnergyGeneration,
        totalEnergyGeneration,
        energyDemandData,
        # solarEnergyGeneration
        # netEnergyDemand,
        excessEnergy,
        solarEnergyGeneration
    
    ]
)