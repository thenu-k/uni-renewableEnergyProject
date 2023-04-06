from Model.RenewableEnergyModel import RenewableEnergyModel
from Model.ComponentModels.EnergyStorageModel import EnergyStorageModel
from Model.ComponentModels.TidalEnergyModel import TidalEnergyModel
from Model.ComponentModels.WindEnergyModel import WindEnergyModel
from Model.ComponentModels.SolarEnergyModel import SolarEnergyModel
from UI.UI import *
from Data.Data import Data
import matplotlib as mpl
formatter = mpl.ticker.EngFormatter()

#Data
numDataPoints = 365
error = 0
spacing = 30
solarData = Data.retrieveSolarData(
    error=error,
    interpolate=True,
    valuesRequired=numDataPoints,
    currentDataSpacing=spacing,
)
windData = Data.generateWindSpeedData(
    error=error,
    interpolate=True,
    valuesRequired=numDataPoints,
    currentDataSpacing=spacing,
)
energyDemandData = Data.generateEnergyDemandData(
    error=error,
    interpolate=True,
    valuesRequired=numDataPoints,
    currentDataSpacing=spacing,
)
tidalData = Data.generateTidalData(
    error=error,
    valuesRequired=numDataPoints*30,
)

#initialise models
solarModel = SolarEnergyModel(
    solarData=solarData,
    unitCount=7e5,
    areaPerUnit=1,
    efficiency=0.25,
    customPower=None,
    scalingFactor=1,
)
windModel = WindEnergyModel(
    windData=windData,
    unitCount=6,
    customDailyGenerationFunction=None,
    efficiency=0.4,
    bladeDiameter=174,
    mediumDensity=1.225
)
tidalModel = TidalEnergyModel(
    topTidalCurrentSpeed=1.15,
    bottomTidalCurrentSpeed=0.6,
    unitCount=80,
    isCrossFlow=False,
    bladeDiameter=40,
    efficiency=0.87,
    mediumDensity=999.7,
    headHeight=None,
    accelerationDueToGravity=9.81,
    customPower=None,
    isDaily=True
)
secondTidalModel = TidalEnergyModel(
    topTidalCurrentSpeed=1.15,
    bottomTidalCurrentSpeed=0.6,
    unitCount=40,
    isCrossFlow=True,
    bladeDiameter=0.8,
    efficiency=0.87,
    mediumDensity=999.7,
    headHeight=40,
    accelerationDueToGravity=9.81,
    customPower=None,
    isDaily=True
)


# print(formatter(sum(energyDemandData)))

#Connect the models
renewableInstance = RenewableEnergyModel(
    SolarEnergyModel=solarModel,
    WindEnergyModel=windModel,
    TidalEnergyModels=[tidalModel, secondTidalModel],
    EnergyStorageModel=None,
    dataValues=numDataPoints,
    hoursPerUnit=24,
    energyDemand=energyDemandData,
)
#Wind production -> correct
#Solar production -> 
[totalUnitlyEnergyProduction, unitlyTidalEnergyProduction, unitlyWindEnergyProduction, unitlySolarEnergyProduction]= renewableInstance.getUnitlyTotalEnergyProduction()

flag = False
for count in range(numDataPoints):
    if totalUnitlyEnergyProduction[count] < energyDemandData[count]:#
        flag=True
print(flag)

compareProd([
    energyDemandData,
    totalUnitlyEnergyProduction,
    # unitlyTidalEnergyProduction,
    # unitlyWindEnergyProduction,
    # unitlySolarEnergyProduction,
])
