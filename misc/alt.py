'''
This programme will take in the current power generation and demands of the city and will 
calculate the flow of power in and out of the storage facility
'''
#Test data for energy generation
powerDemand = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
powerGeneration = [200, 300, 200, 100, 600, 300, 900, 100, 300, 6000]
frequency = 3600 #in seconds
#storage facility data
storageFacility = {
    'waterDensity': 1,
    'topWaterBody' : {
        'waterVolume': 10000,
        'height': 400,
    },
    'bottomWaterBody' : {
        'waterVolume': 5000,
        'height': 300,
    },
    'turbine' : {
        'efficiency': 0.8,
        'maxFlowRate': 0.2,  
    }
}
storageFacilityData = []
grossPowerDemand = []
netPowerDemand = []
powerLoss = []

def main(powerDemand, powerGeneration, storageFacility):
    #Calculate the flow of energy in and out of the storage facility
    for hour in range(len(powerDemand)):
        storageFacilityData.append(storageFacility)
        #the current net power demand at this hour
        print('==================================')
        print('Top water body volume: ' + str(storageFacility['topWaterBody']['waterVolume']))
        print('Bottom water body volume: ' + str(storageFacility['bottomWaterBody']['waterVolume']))
        netPowerDemand = powerDemand[hour] - powerGeneration[hour]
        print('Net power demand: ' + str(netPowerDemand))
        #the max power generation/consumption of the turbine
        maxTurbinePower = storageFacility['turbine']['maxFlowRate'] * storageFacility['waterDensity'] * 9.81 * (storageFacility['topWaterBody']['height'] - storageFacility['bottomWaterBody']['height']) * storageFacility['turbine']['efficiency']
        #turbine power
        currentTurbinePower = maxTurbinePower
        # get absolute value of net power demand
        print('Current Net Demand and Maximum Possible Power: ' + str(abs(netPowerDemand))+',' +str(maxTurbinePower))
        if abs(netPowerDemand)<maxTurbinePower:
            print('Enough flow rate to meet demand')
            currentTurbinePower = netPowerDemand
        # final net power demand init
        finalNetPowerDemand = abs(netPowerDemand) - abs(currentTurbinePower)
        print('Final Net Power Flows: ' + str(finalNetPowerDemand)) 
        #the amount of water must down
        waterVolumeChange = abs(currentTurbinePower*frequency / (storageFacility['waterDensity'] * 9.81 * (storageFacility['topWaterBody']['height'] - storageFacility['bottomWaterBody']['height']) * storageFacility['turbine']['efficiency']))
        if netPowerDemand>0:
            print('Moving water down')
            storageFacility['topWaterBody']['waterVolume'] -= waterVolumeChange
            storageFacility['bottomWaterBody']['waterVolume'] += waterVolumeChange
        elif netPowerDemand<0:
            print('Moving water up')
            storageFacility['topWaterBody']['waterVolume'] += waterVolumeChange
            storageFacility['bottomWaterBody']['waterVolume'] -= waterVolumeChange
    storageFacilityData.append(storageFacility)



main(powerDemand, powerGeneration, storageFacility)