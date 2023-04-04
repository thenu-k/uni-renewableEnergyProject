class EnergyStorageModel:
    def __init__(self, liquidDensity:type[float], accelerationDueToGravity:type[float], maxFlowRate:type[float], efficiency:type[float], maxTopVolume:type[float], maxBottomValue:type[float], turbinePower:type[float], dataValues):
        self.liquidDensity = liquidDensity
        self.accelerationDueToGravity = accelerationDueToGravity
        self.maxFlowRate = maxFlowRate
        self.efficiency = efficiency
        self.maxTopVolume = maxTopVolume
        self.currentTopVolume = None
        self.maxBottomValue = maxBottomValue
        self.currentBottomValue = None
        self.turbinePower = turbinePower
        self.dailyMaximumEnergyPossible = self.turbinePower * 24 
    def updateTopVolume(self, newVolume):
        self.currentTopVolume = newVolume
    def updateBottomVolume(self, newVolume):
        self.currentBottomValue = newVolume
    def calculateWaterMovement(self, currentNetEnergyDemand):
        moveWaterUp = True if currentNetEnergyDemand>0 else False
        if abs(currentNetEnergyDemand)>self.dailyMaximumEnergyPossible:
            energyMovement = self.dailyMaximumEnergyPossible
            energyLost = abs(currentNetEnergyDemand) - self.dailyMaximumEnergyPossible
        else:
            energyMovement = abs(currentNetEnergyDemand)
            energyLost = 0
        waterMovement = energyMovement / (self.liquidDensity * self.accelerationDueToGravity)
        return [moveWaterUp, waterMovement, energyLost]
    def accountForStorage(self, netEnergyDemand, assumeUnlimitedWater):
        energyMovementValues = []
        count = 0
        for value in netEnergyDemand:
            [moveWaterUp, waterMovement, energyLost] = self.calculateWaterMovement(value)
            if assumeUnlimitedWater:
                energyMovementValues.append({
                    "moveWaterUp": moveWaterUp,
                    "waterMovement": waterMovement,
                    "energyLost": energyLost,
                    "day": count,
                })
            else: 
                if moveWaterUp :
                    if self.currentTopVolume + waterMovement > self.maxTopVolume:
                        waterMovement = self.maxTopVolume - self.currentTopVolume
                        energyLost = (waterMovement * self.liquidDensity * self.accelerationDueToGravity) - energyLost
                    self.updateTopVolume(self.currentTopVolume + waterMovement)
                pass
            count += 1
        return energyMovementValues
    
    '''
    Notes:
        If the currentNetEnergyDemand is positive, then energy is required -> water moves down
        If the currentNetEnergyDemand is negative, then energy is produced -> water moves up
    '''