I'll first be building the storage simulation. Here are it's features:
    - It will take an take an array of the power generated.
    - It will take an array of the power demand.
    - We can manaually set the frequency of the power input/demand (eg: 0.5 days between each value)
    - It will take in the efficiency of the power storage (0 through 1)
    - It will takae in the effieciency of the power generation (0 through 1)

The system will divert power to the storage facility if the power generated exceeds the demand. But if the power demand exceeds the power generated, the system will divert power from the storage facility to the demand. 


##
I'm assuming that the rawdata that gives us the energy produced by each energy source will not be
at the same frequency. This means that tidal could be monthly, solar could be daily, and wind could be hourly.
This will create some problems regarding the energy storage model. If we need to get live changes in the energy storage model,
we'll need to have a way to interpolate the data to the same frequency.
To do this, I'll have to adapt each energy source to be DAILY. 
After calculating all the energy produced by day, THEN I'll move on to energy storage. 