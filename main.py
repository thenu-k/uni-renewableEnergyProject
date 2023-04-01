from Model.Models import RenewableEnergyModel, TidalEnergyModel, WindEnergyModel, SolarEnergyModel, EnergyStorage

tidalInstance =  TidalEnergyModel([])
windInstance = WindEnergyModel([])
solarInstance = SolarEnergyModel([])
storageInstance = EnergyStorage([])
renewableInstance = RenewableEnergyModel(tidalInstance, windInstance, solarInstance, storageInstance)