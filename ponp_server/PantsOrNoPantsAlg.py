class PantsOrNoPantsAlg:
  """
  establish default parameters:
  PCI - determined by daily weather conditions
  PCIthreshold - determined by personal factors

  """
  PCI = 5
  PCIthreshold = 5
  standardDis = [None]*50


  """
  Hometown; height; weight; sex; geo-location;

  hometown: gather weather information about particular area
  - generally warm -> inclined towards NP
  - generally cold -> inclined towards P
  """

  def masterFunction(self, height, weightP, sex, age, temp_inclination,
                   curr_high, curr_low, curr_wind_speed, curr_humidity):
    
    # Sex
    if sex == "male":
      self.PCIthreshold +=  0.15
    elif sex == "female":
      self.PCIthreshold -=  0.15
    
    
    # BMI: weight in kilograms divided by the square of height in meters
    weightKg = weightP*0.453592
    
    #input height is assumed to be in inches
    heightM = height / 36
      
    bmi = weightKg / (heightM*heightM)
    


    # BMI influence, relative to age
    if age >= 20:
      avgBMI = 21.7
      self.bmiAdjust(avgBMI, bmi)

    elif 17 <= age < 20:
      avgBMI = 21    
      self.bmiAdjust(avgBMI, bmi)

    elif age < 17:
      avgBMI = 20.5
      self.bmiAdjust(avgBMI, bmi)


    # Temperature Inclination Adjustments
    if temp_inclination == "cooler":
      self.PCIthreshold -= 0.25
    elif temp_inclination == "warmer":
      self.PCIthreshold += 0.25


    #create data distribution
    self.generateStatiticalDist()

    # Current Location Adjustments
    self.setPCI(curr_high, curr_low, curr_wind_speed, curr_humidity)

    if self.PCI >= self.PCIthreshold:
      return True

    elif self.PCI < self.PCIthreshold:
      return False




  def bmiAdjust(self, avgBMI, bmi):
      difBMI = avgBMI - bmi

      #larger tf warmer
      if difBMI < 0:
        if difBMI < 3.2:
          self.PCIthreshold += abs(difBMI)*.1875
        elif difBMI < 7:
          self.PCIthreshold += abs(difBMI)*.13
        else:
          self.PCIthreshold += abs(difBMI)*.09


      #thinner tf colder
      elif 0 < difBMI:
        if difBMI < 3.2:
          self.PCIthreshold -= abs(difBMI)*.1875
        elif difBMI < 7:
          self.PCIthreshold -= abs(difBMI)*.13
        else:
          self.PCIthreshold -= abs(difBMI)*.09

      return 



  def setPCI(self, curr_high, curr_low, curr_wind_speed, curr_humidity):
    dif = 70 - curr_high


    # set accoring to high temp
    if dif < 0:
      PCI = 10*((100 - self.standardDis[abs(round(dif))])/100)
    elif dif >= 0:
      PCI = 10*(self.standardDis[round(dif)]/100)


    # heat index
    T = curr_high
    R = curr_humidity / 100

    # check R: integer or decimal percentage value?
    heat_index = (-42.379) + (2.04901523*T) + (10.14333127*R) - (0.22475541*T*R) - (0.00683783*T*T) - (0.05481717*R*R) 
    + (0.00122874*T*T*R) + (0.00085282*T*R*R) - (0.00000199*T*T*R*R)

    print("Heat Index: ", heat_index)

    if heat_index < 60:
      self.PCI += 0.5

    elif 70 < heat_index < 80:
      self.PCI -= 0.6

    elif heat_index < 90:
      self.PCI -= 1

    elif heat_index < 105:
      self.PCI -= 1.5

    elif heat_index < 130:
      self.PCI -= 2


    # #high
    # if 70 <= curr_high < 75:
    #   self.PCI -= 0.5

    # elif 75 <= curr_high < 80:
    #   self.PCI -= 1.2

    # elif 80 <= curr_high < 85:
    #   self.PCI -= 1.5

    # elif 85 <= curr_high < 90:
    #   self.PCI -= 2.2

    # elif 90 <= curr_high < 100:
    #   self.PCI -= 2.9

    # else:
    #   self.PCI -= 3


    #low
    if 60 <= curr_low < 65:
      self.PCI += 0.2

    elif 55 <= curr_low < 60:
      self.PCI += 0.4

    elif 50 <= curr_low < 55:
      self.PCI += 0.6

    elif 45 <= curr_low < 50:
      self.PCI += 0.8

    elif 40 <= curr_low < 45:
      self.PCI += 1

    elif 35 <= curr_low < 40:
      self.PCI += 1.2

    elif 30 <= curr_low < 35:
      self.PCI += 1.4

    elif 25 <= curr_low < 30:
      self.PCI += 1.6

    elif curr_low < 25:
      self.PCI += 1.8


    # wind
    if 3 < curr_wind_speed < 7.4:
      self.PCI += 0.1

    elif curr_wind_speed < 17.9:
      self.PCI += 0.3

    elif curr_wind_speed < 31:
      self.PCI += 0.5    

    elif curr_wind_speed < 46.3:
      self.PCI += 1.1

    else:
      self.PCI += 2


  def generateStatiticalDist(self):

    exp_constant = 1.07
    startDifferential = .5
    startingProb = 50

    for count in range(0, 49):
      self.standardDis[count] = startingProb
      startingProb = startingProb + startDifferential
      startDifferential = startDifferential*exp_constant
      count = count + 1
    






# Testing------

# Reference: height, weightP, sex, age, temp_inclination, hometownAvgS, hometownAvgW, curr_high, curr_low, curr_wind_speed, curr_humidity

# testUser = PantsOrNoPants()
# print(testUser.masterFunction(80, 100, "male", 20.5, "neutral", 75, 63, 14, 85))
# print("PCI: ", testUser.PCI)
# print("Threshold: ", testUser.PCIthreshold)
# print(testUser.masterFunction(63, 150, "female", 18, "colder", 54, 33, 0, 19))
# print("PCI: ", testUser.PCI)
# print("Threshold: ", testUser.PCIthreshold)
# print(testUser.masterFunction(70, 94, "male", 25, "neutral", 99, 75, 3, 0))
# print("PCI: ", testUser.PCI)
# print("Threshold: ", testUser.PCIthreshold)
# print(testUser.masterFunction(70, 100, "female", 22, "warmer", 83, 50, 47, 89))
# print("PCI: ", testUser.PCI)
# print("Threshold: ", testUser.PCIthreshold)
# print(testUser.masterFunction(67, 250, "male", 20.5, "neutral", 75, 63, 14, 0))
# print("PCI: ", testUser.PCI)
# print("Threshold: ", testUser.PCIthreshold)







