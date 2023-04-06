class EnergyStorageModel:
    def __init__(self, liquidDensity:type[float], accelerationDueToGravity:type[float], maxFlowRate:type[float], efficiency:type[float], maxTopVolume:type[float], maxBottomValue:type[float], turbinePower:type[float], dataValues, heightDifference:type[float], currentTopVolume:type[float], currentBottomValue:type[float], minimumWaterLevel:type[float]):
        self.liquidDensity = liquidDensity
        self.accelerationDueToGravity = accelerationDueToGravity
        self.maxFlowRate = maxFlowRate
        self.efficiency = efficiency
        self.maxTopVolume = maxTopVolume
        self.currentTopVolume = currentTopVolume
        self.maxBottomValue = maxBottomValue
        self.currentBottomValue = currentBottomValue
        self.turbinePower = turbinePower
        self.dailyMaximumEnergyPossible = self.turbinePower * 24 
        self.heightDifference = heightDifference
        self.minimumWaterLevel = minimumWaterLevel
    def updateTopVolume(self, newVolume):
        self.currentTopVolume = newVolume
    def updateBottomVolume(self, newVolume):
        self.currentBottomValue = newVolume
    def calculateWaterMovement(self, currentNetEnergyDemand):
        moveWaterUp = True if currentNetEnergyDemand>0 else False
        if abs(currentNetEnergyDemand)>self.dailyMaximumEnergyPossible:
            energyMovement = self.dailyMaximumEnergyPossible
            energyLost = abs(currentNetEnergyDemand) - (self.dailyMaximumEnergyPossible)
        else:
            energyMovement = abs(currentNetEnergyDemand)
            energyLost = 0
        waterMovement = energyMovement*3600 / (self.liquidDensity * self.accelerationDueToGravity * self.heightDifference)
        return [moveWaterUp, waterMovement, energyLost]
    def simulate(self, netEnergyDemand, assumeUnlimitedWater):
        energyMovementValues = []
        topVolumeVariation = []
        bottomVolumeVariation = []
        energyLossVariation = []
        count = 0
        for value in netEnergyDemand:
            [moveWaterUp, waterMovement, energyLost] = self.calculateWaterMovement(value)
            if self.currentTopVolume > self.maxTopVolume or self.currentBottomValue > self.maxBottomValue or self.currentTopVolume < self.maxTopVolume*self.minimumWaterLevel or self.currentBottomValue < self.maxBottomValue*self.minimumWaterLevel:
                raise Exception("Water levels are not within the maximum and minimum values")
            if assumeUnlimitedWater:
                energyMovementValues.append({
                    "moveWaterUp": moveWaterUp,
                    "waterMovement": waterMovement,
                    "requiredEnergyMovement": value,
                    "energyMoved": value - energyLost,
                    "energyLost": energyLost,
                    "day": count,
                })
            else: 
                flags = []
                if moveWaterUp:
                    # First check whether the bottom tank has enough water to move
                    if self.currentBottomValue - waterMovement < self.maxBottomValue*self.minimumWaterLevel:
                        actualWaterMovement = self.currentBottomValue - self.maxBottomValue*self.minimumWaterLevel
                        actualEnergyLost= energyLost + ((waterMovement-actualWaterMovement) * self.liquidDensity * self.accelerationDueToGravity * self.heightDifference)/3600
                        flags.append("Bottom tank does not have enough water")
                    else:
                        actualWaterMovement = waterMovement
                        actualEnergyLost = energyLost
                    # Check whether the top tank has enough space to move the water
                    if actualWaterMovement + self.currentTopVolume > self.maxTopVolume:
                        actualWaterMovement = self.maxTopVolume - self.currentTopVolume
                        actualEnergyLost = actualEnergyLost + ((waterMovement-actualWaterMovement) * self.liquidDensity * self.accelerationDueToGravity * self.heightDifference)/3600
                        flags.append("Top tank does not have enough space")
                    else:
                        actualWaterMovement = actualWaterMovement
                        actualEnergyLost = actualEnergyLost
                    topVolumeVariation.append(self.currentTopVolume + actualWaterMovement)
                    bottomVolumeVariation.append(self.currentBottomValue - actualWaterMovement)
                    self.currentTopVolume = self.currentTopVolume + actualWaterMovement
                    self.currentBottomValue = self.currentBottomValue - actualWaterMovement
                else:
                    if self.currentTopVolume - waterMovement < self.maxTopVolume*self.minimumWaterLevel:
                        actualWaterMovement = self.currentTopVolume - self.maxTopVolume*self.minimumWaterLevel
                        actualEnergyLost=energyLost + ((waterMovement-actualWaterMovement) * self.liquidDensity * self.accelerationDueToGravity * self.heightDifference)/3600
                        flags.append("Top tank does not have enough water")
                    else:
                        actualWaterMovement = waterMovement
                        actualEnergyLost = energyLost
                    if actualWaterMovement + self.currentBottomValue > self.maxBottomValue:
                        actualWaterMovement = self.maxBottomValue - self.currentBottomValue
                        actualEnergyLost =  actualEnergyLost + ((waterMovement-actualWaterMovement) * self.liquidDensity * self.accelerationDueToGravity * self.heightDifference)/3600
                        flags.append("Bottom tank does not have enough space")
                    else:
                        actualWaterMovement = actualWaterMovement
                        actualEnergyLost = actualEnergyLost
                    self.currentTopVolume = self.currentTopVolume - actualWaterMovement
                    self.currentBottomValue = self.currentBottomValue + actualWaterMovement
                    topVolumeVariation.append(self.currentTopVolume - actualWaterMovement)
                    bottomVolumeVariation.append(self.currentBottomValue + actualWaterMovement)
                energyMovementValues.append({
                    "moveWaterUp": moveWaterUp,
                    "requiredWaterMovement": waterMovement,
                    "waterMovement": actualWaterMovement,
                    "requiredEnergyMovement": abs(value),
                    "energyMoved": abs(value) - actualEnergyLost,
                    "energyLost": actualEnergyLost,
                    "topVolume": self.currentTopVolume,
                    "bottomVolume": self.currentBottomValue,
                    "day": count+1,
                    "flags": flags,
                    "energyGenerated": 1*(abs(value) - actualEnergyLost) if moveWaterUp else -1*(abs(value) - actualEnergyLost)
                })
            energyLossVariation.append(energyLost)
            count += 1
        return energyMovementValues
    