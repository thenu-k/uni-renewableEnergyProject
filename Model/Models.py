from ..helperFunctions import getNormalizedData

class RenewableEnergyModel:
    def __init__(self, TidalEnergyModel, WindEnergyModel, SolarEnergyModel, EnergyStorage):
        self.TidalEnergyModel = TidalEnergyModel
        self.WindEnergyModel = WindEnergyModel
        self.SolarEnergyModel = SolarEnergyModel
    def getPowerGeneration():
        return None

class TidalEnergyModel:
    def __init__(self, tidalData, frequencyOfData):
        self.tidalData = tidalData
        self.frequencyOfData = frequencyOfData
        self.normalizedTidalData = getNormalizedData(frequencyOfData)

class WindEnergyModel:
    def __init__(self, windData):
        self.windData = windData
    def getWindGeneration():
        return None
    
class SolarEnergyModel:
    def __init__(self, solarData):
        self.solarData = solarData
    def getSolarGeneration():
        return None
    
class EnergyStorage:
    def __init__(self, storageFacility):
        self.storageFacility = storageFacility
    def getStorageFacility():
        return None