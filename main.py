from Model.RenewableEnergyModel import RenewableEnergyModel
from Model.ComponentModels.EnergyStorageModel import EnergyStorageModel
from Model.ComponentModels.TidalEnergyModel import TidalEnergyModel
from Model.ComponentModels.WindEnergyModel import WindEnergyModel
from Model.ComponentModels.SolarEnergyModel import SolarEnergyModel
from UI.UI import *
from Data.Data import Data
import matplotlib as mpl
import csv
formatter = mpl.ticker.EngFormatter()
#

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
    unitCount=1.5e6,
    areaPerUnit=1,
    efficiency=0.25,
    customPower=None,
    scalingFactor=1,
)
windModel = WindEnergyModel(
    windData=windData,
    unitCount=10,
    customDailyGenerationFunction=None,
    efficiency=0.4,
    bladeDiameter=174,
    mediumDensity=1.225
)
tidalModel = TidalEnergyModel(
    topTidalCurrentSpeed=1.15,
    bottomTidalCurrentSpeed=0.6,
    unitCount=10,
    isCrossFlow=False,
    bladeDiameter=40,
    efficiency=0.87,
    mediumDensity=999.7,
    headHeight=None,
    accelerationDueToGravity=9.81,
    customPower=None,
    isDaily=True,
    error=error
)
secondTidalModel = TidalEnergyModel(
    topTidalCurrentSpeed=1.15,
    bottomTidalCurrentSpeed=0.6,
    unitCount=50,
    isCrossFlow=True,
    bladeDiameter=0.8,
    efficiency=0.87,
    mediumDensity=999.7,
    headHeight=40,
    accelerationDueToGravity=9.81,
    customPower=None,
    isDaily=True,
    error=error
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
deficitCount = 0
for count in range(numDataPoints):
    if totalUnitlyEnergyProduction[count] < energyDemandData[count]:
        flag=True
        deficitCount += 1

print(flag)
print(deficitCount)
print(formatter(sum(unitlyTidalEnergyProduction)), formatter(sum(unitlyWindEnergyProduction)), formatter(sum(unitlySolarEnergyProduction)))
print(formatter(sum(totalUnitlyEnergyProduction)))
compareProd([
    energyDemandData,
    totalUnitlyEnergyProduction,
    unitlyTidalEnergyProduction,
    unitlyWindEnergyProduction,
    unitlySolarEnergyProduction,
])

# create csv of energy demand data
# with open('energyDataNoErrors.csv', 'w', newline='') as file:
#     #create csv with headers: x and y
#     totalData = [totalUnitlyEnergyProduction[count]/1e9 for count in range(len(totalUnitlyEnergyProduction))]
#     windData = [unitlyWindEnergyProduction[count]/1e9 for count in range(len(unitlyWindEnergyProduction))]
#     solarData = [unitlySolarEnergyProduction[count]/1e9 for count in range(len(unitlySolarEnergyProduction))]
#     tidalData = [unitlyTidalEnergyProduction[count]/1e9 for count in range(len(unitlyTidalEnergyProduction))]
#     demandData = [energyDemandData[count]/1e9 for count in range(len(energyDemandData))]
#     writer = csv.writer(file)
#     writer.writerow(["x", "demand", "tidal", "wind", "solar", "total"])
#     for count in range(numDataPoints):
#         writer.writerow([count+1, demandData[count], tidalData[count], windData[count], solarData[count], totalData[count]])
