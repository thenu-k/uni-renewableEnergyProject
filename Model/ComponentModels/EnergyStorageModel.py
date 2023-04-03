class EnergyStorage:
    def __init__(self, liquidDensity, accelerationDueToGravity, maxFlowRate, efficiency, maxTopVolume, maxBottomValue, turbinePower, dataValues):
        self.liquidDensity = liquidDensity
        self.accelerationDueToGravity = accelerationDueToGravity
        self.maxFlowRate = maxFlowRate
        self.efficiency = efficiency
        self.maxTopVolume = maxTopVolume
        self.currentTopVolume = None
        self.maxBottomValue = maxBottomValue
        self.currentBottomValue = None
        self.turbinePower = turbinePower
        self.dailyMaximumEnergyPossible = self.turbinePower * 24 * 60 * 60
        self.dailyStorageEnergyUsage = [0]*dataValues
    def updateTopVolume(self, newVolume):
        self.currentTopVolume = newVolume
    def updateBottomVolume(self, newVolume):
        self.currentBottomValue = newVolume
    def calculateWaterMovement(self, currentNetEnergyDemand):
        energyRequired = True if currentNetEnergyDemand>0 else False
        if currentNetEnergyDemand>self.dailyMaximumEnergyPossible:
            energyMovement = self.dailyMaximumEnergyPossible
        else:
            energyMovement = currentNetEnergyDemand
        waterMovement = energyMovement / (self.liquidDensity * self.accelerationDueToGravity)
        return None