class TemperatureController:

    def __init__(self, current_temperature, mode, Input, time2wait):
        self.current_temperature = current_temperature
        self.mode = mode
        self.Input = Input
        self.time2wait = time2wait

    def controller_send_realtime_temperature(self, temp_request,
                                             refer_temperature):  # establish connection between Sensor and Heater
        if temp_request == 1:
            room_realtime_temperature = sensor_send_realtime_temperature(temp_request, refer_temperature)
            return room_realtime_temperature
        else:
            print("Wrong temperature request!")

    def control_system(self):
        if self.mode == "auto":  # Auto Mode #
            ### This is cooling process in Auto Mode ####
            if self.current_temperature > 26:
                # If the current temperature is above the default setting
                cooler_activation_flag = 1
                # assign the value of cooler flag to 1
                cooler_instance.input_temperature(self.current_temperature)
                # assign the self.current_temperature to cooler
                cooler_instance.set_temperature(26)
                # In auto mode, the default setting is 26°C
                cooler_instance.cooler_activate(cooler_activation_flag)
                # activate cooler module with activation_flag
                self.current_temperature = cooler_instance.measured_room_temperature
                # receive the current temperature (the cooled temperature) from cooler #since this project is based on simulation!
                sensor_refer_temperature = self.current_temperature
                # assign the current temperature to sensor
                calibrated_current_temperature = env.current_temperature(sensor_refer_temperature)
                # receive the calibrated temperature from sensor
                self.temperature = calibrated_current_temperature
                # assign the calibrated temperature to current temperature
                cooler_activation_flag = 0
                # assign the value of cooler flag to 0
                cooler_instance.cooler_activate(cooler_activation_flag)
                # deactivate cooler module with activation_flag
                ### Auto Cooling Mode ends ###

                ### This is heating process in Auto Mode ####
            elif self.current_temperature < 26:
                # If the current temperature is below the default setting
                heater_activation_flag = 1
                # assign the value of heater flag to 1
                target_temperature = 26
                # The desired temperature in auto mode is 26°C
                current_temperature = self.current_temperature
                # Assign The current temperature to current temperature variable
                room_heater.temperature_adjust = 0
                # heater adjust temperature ==0
                room_heater.measured_room_temperature = self.current_temperature
                # assign the current tmperature to the measured temperature of hearter # since this project is based on simulation!
                room_heater.target_room_temperature = 26
                # The desired temperature in auto mode is 26°C
                self.time2wait = room_heater.heater_active_time()
                # calcuate time to get the desired temperature for Cooler
                heating_result = room_heater.heater_activate(heater_activation_flag, target_temperature,
                                                             current_temperature)
                # call heater's method and begin to heat
                self.current_temperature = heating_result
                # receive the heated temperature (in theory)
                sensor_refer_temperature = self.current_temperature
                # assign the current temperature to sensor
                calibrated_current_temperature = env.current_temperature(sensor_refer_temperature)
                # receive the calibrated temperature from sensor
                self.temperature = calibrated_current_temperature
                # assign the calibrated temperature to current temperature
                heater_activation_flag = 0
                # # assign the value of heater flag to 0
                ### Auto Heating Mode ends ###

            elif self.current_temperature == 26:
                print('the current temperature satisfies the auto setting')

        elif self.mode == "manual":
            ### This is cooling process in Manual Mode ####
            if self.current_temperature > self.Input:
                # If the current temperature is above the manual setting
                cooler_activation_flag = 1
                # assign the value of cooler flag to 1
                cooler_instance.input_temperature(self.current_temperature)
                # assign the self.current_temperature to cooler
                cooler_instance.set_temperature(self.Input)
                # assign the desired_temperature to cooler (user input)
                cooler_instance.cooler_activate(cooler_activation_flag)
                # assign the self.current_temperature to cooler
                self.current_temperature = cooler_instance.current_temperature
                # receive the current temperature (the cooled temperature) from cooler #since this project is based on simulation!
                sensor_refer_temperature = self.current_temperature
                # assign the current temperature to sensor
                calibrated_current_temperature = env.current_temperature(sensor_refer_temperature)
                # receive the calibrated temperature from sensor
                self.current_temperature = calibrated_current_temperature
                # assign the calibrated temperature to current temperature
                cooler_activation_flag = 0
                # assign the value of cooler flag to 0
                cooler_instance.cooler_activate(cooler_activation_flag)
                # deactivate cooler module with activation_flag
                ### Manual Cooling Mode ends ###

                ### This is heating process in Manual Mode ####
            if self.Input > self.current_temperature:
                # If the current temperature is below the default setting
                heater_activation_flag = 1
                # assign the value of heater flag to 1
                target_temperature = self.Input
                # The desired temperature in manual mode is the user inputted value
                current_temperature = self.current_temperature
                # Assign The current temperature to current temperature variable
                room_heater.temperature_adjust = 0
                # heater adjust temperature ==0
                room_heater.measured_room_temperature = self.current_temperature
                # assign the current tmperature to the measured temperature of hearter # since this project is based on simulation!
                room_heater.target_room_temperature = self.Input
                # The desired temperature in auto mode is the user inputted value
                self.time2wait = room_heater.heater_active_time()
                # calcuate time to reach the desired temperature for Heater
                heating_result = room_heater.heater_activate(heater_activation_flag, target_temperature,
                                                             current_temperature)
                # call heater's method and begin to heat
                self.current_temperature = heating_result
                # receive the heated temperature (in theory)
                sensor_refer_temperature = self.current_temperature
                # assign the current temperature to sensor
                calibrated_current_temperature = env.current_temperature(sensor_refer_temperature)
                # receive the calibrated temperature from sensor
                self.current_temperature = calibrated_current_temperature
                # assign the calibrated temperature to current temperature
                heater_activation_flag = 0
                # assign the value of cooler flag to 0


            elif self.Input == self.current_temperature:

                print('the current temperature satisfies the manual setting')
import random

class TemperatureSensor:
    def __init__(self):
        self.outdoor_temp = None
        self.indoor_temp = None
        self.outside_air_pressure = 101325  # Default outside air pressure

    def generate_initial_outdoor_temp(self):
        # Temperature data for each month: high, low
        temperature_data = {
            "January": (-3, -10),
            "February": (-2, -10),
            "March": (4, -4),
            "April": (12, 2),
            "May": (19, 7),
            "June": (24, 12),
            "July": (27, 15),
            "August": (26, 14),
            "September": (21, 10),
            "October": (14, 4),
            "November": (7, 0),
            "December": (0, -6)
        }

        def generate_random_datetime():
            # Generate a random date and time
            year = random.randint(2023, 2024)
            month = random.choice(list(temperature_data.keys()))
            day = random.randint(1, 28)  # Assuming 28 days for simplicity
            hour = random.randint(0, 23)
            minute = random.randint(0, 59)
            return year, month, day, hour, minute

        def generate_random_temperature(month, hour):
            # Retrieve temperature data for the selected month
            temp_range = temperature_data[month]

            if temp_range:
                # Generate a temperature within the high and low range for the month
                high_temp, low_temp = temp_range
                if hour <= 2 or hour > 14:  # After 2 PM, before 2 AM
                    hour_factor = abs(hour - 2) / 12  # Scale from 2 AM to 2 PM
                else:  # Between 2 AM and 2 PM
                    hour_factor = abs(hour - 14) / 12  # Scale from 2 PM to 2 AM

                temperature = low_temp + (high_temp - low_temp) * hour_factor + random.uniform(-2, 2)
                return temperature
            else:
                return None

        # Generate a random date and time
        year, month, day, hour, minute = generate_random_datetime()
        self.outdoor_temp = generate_random_temperature(month, hour)

        return self.outdoor_temp

    def indoor_temperature(self):
      self.indoor_temp=0.7*self.outdoor_temp+10
      return self.indoor_temp

    def get_initial_environment(self):
      return self.indoor_temp, self.outdoor_temp, self.outside_air_pressure

class Environment:
    def __init__(self, theoretical_temp):
        self.theoretical_temp = theoretical_temp
        self.temp_sensor = TemperatureSensor()


    ##### Read theoretical temperature from control, obtained from cooler or heater
    def theoretical_temperature(self,sensor_temp_request,sensor_refer_temperature = 5):#sensor_refer_temperture will be read from controller
    # temperatue request flag 1
      if sensor_temp_request == 1:
      # simulate the real temperature after heating using random function
        temp = sensor_refer_temperature - random.uniform(0.3,0.6)
        return temp
      else:
        print("Wrong temperature request!")
        return None
    def random_incident(self):
      incident = random.choices(
        ["door_open", "window_open", "no_incident"],
        weights=[0.2, 0.2, 0.6],
        k=1
    )[0]
    # Random incident will happen to bring the temperature up or down by +/- 0.5 degree
    # If no incident, temperature remains the same
      return incident

    def current_temperature(self,sensor_refer_temperature):
      current_temp = self.theoretical_temperature(1,sensor_refer_temperature)
      sensor_outdoor_temp = self.temp_sensor.generate_initial_outdoor_temp()
      if current_temp is not None:
          incident = self.random_incident()

          if incident == "door_open" and sensor_outdoor_temp >= current_temp:
                current_temp += 0.5
          elif incident == "window_open" and sensor_outdoor_temp >= current_temp:
                current_temp += 0.5
          elif incident == "door_open" and sensor_outdoor_temp < current_temp:
                current_temp -= 0.5
          elif incident == "window_open" and sensor_outdoor_temp < current_temp:
                current_temp -= 0.5

      # Return current temperature even if there's no incident
      return current_temp if current_temp is not None else None

import time
import random

# add this function as a sensor class function
## sensor_send_realtime_temperature
# sensor send temperature to controller when request
def sensor_send_realtime_temperature(sensor_temp_request, sensor_refer_temperature=5):
    # temperature request flag 1
    if sensor_temp_request == 1:
        # simulate the real temperature after heating using random function
        room_realtime_temperature = sensor_refer_temperature - random.uniform(0.3, 0.6)
        return room_realtime_temperature
    else:
        print("Wrong temperature request!")



# parent class define a room class as a parent class stands for the target room to be heated
class room:
    def __init__(
        self,
        room_volume,
        room_area,
        hold_room_temperature,
        outside_room_pressure,
        outside_room_temperature,
        room_thermal_resistance,
    ):
        # room_volume represents air hold in the room, used to calculate air_weight
        self.room_volume = room_volume
        # room_area includes areas of walls ceiling, floors used to calculate heat loss rate
        self.room_area = room_area
        # hold_room_temperature, temperature inside room, normally same as target temperature, used to calculate heat loss
        self.hold_room_temperature = hold_room_temperature
        # outside_room_pressure, air pressure outside room, used to calculate air_density, the air weight
        self.outside_room_pressure = outside_room_pressure
        # outside_room_temperature, air temperature outside room, used to calculate heat loss
        self.outside_room_temperature = outside_room_temperature
        # room_thermal_resistance, represents the heat dissipation speed in the room, used to calculate heat loss
        self.room_thermal_resistance = room_thermal_resistance

    ### air_weight method
    # calculate air_weight inside room by following
    # air_density = air_pressure/((air_constant *(hold_room_temperature +273.15))
    # air_weight = air_density * room_volume
    ## input:
    # room_volume  m³
    # outside_room_pressure pascals
    # hold_room_temperature °C
    ## output:air_weight kg inside the room
    def air_weight(self):
        air_constant = 287.05  # J/(kg·Kelvin)
        air_density = (
            self.outside_room_pressure
            / (air_constant * (self.hold_room_temperature + 273.15))  # kg/m³
        )
        air_weight_inside_room = air_density * self.room_volume
        return air_weight_inside_room  # kg

    ### heat_loss_rate method
    # calculate heat_loss_rate of the room by
    # (3600/1000) * room_area *(hold_room_temperature - outside_room_temperature) / (room_thermal_resistance)
    ## input:
    # room_area  m²
    # hold_room_temperature °C
    # outside_room_temperature °C
    # room_thermal_resistance m²*Kelvin/W
    ## output:heat_loss_rate_room KJ/hour
    def heat_loss_rate(self):
        heat_loss_rate_room = (
            (3600 / 1000)
            * self.room_area
            * (self.hold_room_temperature - self.outside_room_temperature)
            / (self.room_thermal_resistance)
        )
        return heat_loss_rate_room  # KJ/hour

# child class room_with_heater inherited from room class stands for the room with heater
class room_with_heater(room):
    def __init__(
        self,
        air_heat_capacity,
        heat_generation_rate,
        temperature_accuracy,
        target_room_temperature,
        initial_room_temperature,
        measured_room_temperature,
        estimated_time_to_target_temperature,
        temperature_adjust,
        theoretical_room_temperature,
        room_volume,
        room_area,
        hold_room_temperature,
        outside_room_pressure,
        outside_room_temperature,
        room_thermal_resistance,
    ):
        super().__init__(
            room_volume,
            room_area,
            hold_room_temperature,
            outside_room_pressure,
            outside_room_temperature,
            room_thermal_resistance,
        )
        # air_heat_capacity represents heat 1kg air up 1 kelvin how much energy needed, used for heat balance related calculation
        self.air_heat_capacity = air_heat_capacity  # 1.006 KJ/(kg*kelvin)
        # heat_generation_rate represents how much energy per hour will be produced for heater to heat the air
        self.heat_generation_rate = heat_generation_rate  # 73853.4KJ/hour
        # temperature_accuracy represents the tolerance of the target temperature
        self.temperature_accuracy = temperature_accuracy  # 0.5 °C
        # target_room_temperature stands for the expected temperature need to reach
        self.target_room_temperature = target_room_temperature  # °C
        # initial_room_temperature the starting temperature of the control process
        self.initial_room_temperature = initial_room_temperature  # °C
        # measured_room_temperature represents the current temperature during the control process, used for heater working time calculation
        self.measured_room_temperature = measured_room_temperature  # °C
        # estimated_time_to_target_temperature represents for time needed to heat room from initial to target temperature
        self.estimated_time_to_target_temperature = estimated_time_to_target_temperature  # minutes
        # temperature_adjust is a variable to optimize the heating algorithm
        self.temperature_adjust = temperature_adjust
        # after each heat round calculate theoretical temperature to be reached
        self.theoretical_room_temperature = theoretical_room_temperature  # °C

    ### heater_active_time
    # calculate the heater working time for heating room from current temperature to target temperature
    # the key is heat balance equation: energy produced equals to energy used to increase temperature plus energy lost
    # 1, calculate the total heat requirement KJ for heating given room air to target temperature from measured temperature
    # 2, calculate net heat rate kj/h which equals heat_generation_rate minus heat_loss_rate
    # 3, active time = total heat divide net heat rate
    ## input:
    # air_weight kg
    # air_heat_capacity  KJ/(kg*kelvin)
    # target_room_temperature °C
    # measured_room_temperature °C
    # temperature_adjust °C
    # heat_generation_rate KJ/h
    # heat_loss_rate KJ/h
    ## output:active_time minutes
    def heater_active_time(self): #get time2wait
            heat_requirement_for_room = self.air_weight() * self.air_heat_capacity * (self.target_room_temperature - self.measured_room_temperature + self.temperature_adjust) # KJ
            print("heat_requirement_for_room KJ",heat_requirement_for_room)
            net_heat_rate_for_room = self.heat_generation_rate - self.heat_loss_rate()  # KJ/hour
            print("net_heat_rate_for_room KJ/h",net_heat_rate_for_room)
            active_time =  60 * heat_requirement_for_room / net_heat_rate_for_room  # minutes
            return active_time
    ### heat_control_linear
    # activate heater to linear control mode heat room to 3°C below target temperature
    # the key is heat balance equation: energy produced equals to energy used to increase temperature plus energy lost
    # 1, set temperature_adjust = -3 °C, call heater_active_time to get the heater working time
    # 2, simulate heating
    # 3, calculate the theoretical_temperature after linear heating
    ## input:
    # air_weight kg
    # air_heat_capacity  KJ/(kg*kelvin)
    # target_room_temperature °C
    # measured_room_temperature °C
    # temperature_adjust °C
    # heat_generation_rate KJ/h
    # heat_loss_rate KJ/h
    ## output: theoretical_temperature °C
    def heat_control_linear(self):
        # set linear heat to 3°C below target temperature to avoid overshooting
        bisection_method_temperature = 3.0
        self.temperature_adjust = -bisection_method_temperature
        active_time_temp = self.heater_active_time()

        print("Linear heat active time(minutes):", active_time_temp)

        # simulate the heating process
        time.sleep(2)

        # calculate theoretical_temperature after linear heating finishes
        net_heat_added = (
            (self.heat_generation_rate - self.heat_loss_rate())
            * (active_time_temp / 60)
        )
        theoretical_temperature = (
            net_heat_added / (self.air_weight() * self.air_heat_capacity)
            + self.measured_room_temperature
        )
        print(
            "theoretical_room_temperature after Linear control °C:",
            theoretical_temperature,
        )
        return theoretical_temperature

    ### get_realtime_temperatue
    # get_realtime_temperatue from controller to calculate heating time
    def get_realtime_temperature(self, temp_request):
        return temperature_controller.controller_send_realtime_temperature(temp_request, self.theoretical_room_temperature)


    ### heat_control_bisection
    # activate heater to bisection control mode heat remaining 3°C
    # 1, bisection algorithm: calculate new active time, but only set heater to work half of active time, till reach target temperature to avoid over-heating
    # 2, simulate heating
    # 3, calculate the theoretical_temperature after bisection heating
    ## input:
    # air_weight kg
    # air_heat_capacity  KJ/(kg*kelvin)
    # target_room_temperature °C
    # measured_room_temperature °C
    # temperature_adjust °C
    # heat_generation_rate KJ/h
    # heat_loss_rate KJ/h
    ## output: theoretical_temperature °C
    def heat_control_bisection(self):
        # set temperature_adjust to adjust the algorithm
        self.temperature_adjust = 2 * self.temperature_accuracy
        active_time_temp = self.heater_active_time()
        half_active_time = (1 / 2) * active_time_temp
        print("Bisection heat active time(minutes):", half_active_time)

        # simulate the heating process
        time.sleep(1)

        # calculate theoretical_temperature after each bisection heating round
        net_heat_added = (
            (self.heat_generation_rate - self.heat_loss_rate())
            * (half_active_time / 60)
        )
        theoretical_temperature = (
            net_heat_added / (self.air_weight() * self.air_heat_capacity)
            + self.measured_room_temperature
        )
        print(
            "theoretical_room_temperature after bisection control °C:",
            theoretical_temperature,
        )
        return theoretical_temperature

    ### heater_activate function
    # center control module call this function to activate heater to heat the room to target temperature
    # 1 step activate heat_control_linear method to heat room to 3°C below the target temperature
    # 2 step use heat_control_bisection to fine heat room to target temperature
    ## input: heater_activation_flag, target_temperature, current_temperature
    ## output: final_temperature
    def heater_activate(self, heater_activation_flag, target_temperature, current_temperature):
        bisection_method_temperature = 3.0
        bisection_round = 0

        # target temperature needs to be smaller than 49°C, real-time temperature no less than -29 °C
        if (
            heater_activation_flag == 1
            and self.target_room_temperature > self.measured_room_temperature
            and self.measured_room_temperature > -29
            and self.target_room_temperature < 49
            and target_temperature - current_temperature > self.temperature_accuracy
        ):

            self.target_room_temperature = target_temperature #
            self.measured_room_temperature = current_temperature#
            print("Room info:")
            print("Volume m³:", self.room_volume, ", Area m²:", self.room_area, ", Heat loss rate KJ/h:", self.heat_loss_rate())
            print("\n")
            print("Heater info:")
            print(
                "heat_generation_rate KJ/h:",
                self.heat_generation_rate,
                ", net_heat_rate KJ/h:",
                self.heat_generation_rate - self.heat_loss_rate(),
            )
            print("Temperature °C:")
            print(
                "Target:",
                self.target_room_temperature,
                ", Initial:",
                self.measured_room_temperature,
                ", Tolerance:",
                self.temperature_accuracy,
            )
            print("\n")

            self.estimated_time_to_target_temperature = self.heater_active_time()
            print("Estimated Heating time minutes:", self.estimated_time_to_target_temperature)
            print("\n")

            # active linear heating to 3°C below the target temperature
            if (self.target_room_temperature - self.measured_room_temperature) >= bisection_method_temperature:
                print("Linear Heating is ongoing...")
                self.theoretical_room_temperature = self.heat_control_linear()
                # simulate heating process
                time.sleep(8)

                # get real temperature from controller measured_room_temperature
                self.measured_room_temperature = self.get_realtime_temperature(temp_request=1)

                print("Target temperature", self.target_room_temperature)
                print("Measured temperature", self.measured_room_temperature)

            # active bisection heating to remaining 3°C to the target temperature
            # for loop round N_bisection, will be turned by real application
            N_bisection = 15
            for n in range(1, N_bisection):
                if (
                    self.target_room_temperature > self.measured_room_temperature
                    and self.target_room_temperature - self.measured_room_temperature > self.temperature_accuracy
                ):
                    print("\n")
                    print("Bisection Heating Round ", n, "is ongoing...")
                    self.theoretical_room_temperature = self.heat_control_bisection()

                    # simulate heating process
                    time.sleep(4)

                    # get real temperature from controller measured_room_temperature
                    self.measured_room_temperature = self.get_realtime_temperature(temp_request=1)
                    print("Target temperature", self.target_room_temperature)
                    print("Measured temperature", self.measured_room_temperature)

                    if (self.target_room_temperature - self.measured_room_temperature) < self.temperature_accuracy:
                        print("\n")
                        print("Temperature reached, Heater turned off!")
                        break

            if self.target_room_temperature - self.measured_room_temperature <= self.temperature_accuracy:
                return self.measured_room_temperature
            else:
                print("Not reach heating target!")
                return False

        else:
            print("System error:Please Check temperature input!")
            return False


####################################################################
########### Below this line is for Heater Test function ############
#######if test the heater module，need to enable last line to call test_heater_activate() function

def test_heater_activate():
    class Test_controller:
      def controller_send_realtime_temperature(self,temp_request,refer_temperature):
        # temperatue request flag 1
        if temp_request == 1:
        # call sensor to send real temperature
          room_realtime_temperature = refer_temperature - random.uniform(0.3,0.6)
          return room_realtime_temperature
        else:
          print("Wrong temperature request!")

    temperature_controller = Test_controller()


    # instantiate parameter for room_with_heater
    room_volume = 6000  # m³
    room_area = 2200   # m²
    hold_room_temperature = 20 # °C should be same as target_temperature
    outside_room_pressure = 101325  # pascals
    outside_room_temperature = 5 # °C
    room_thermal_resistance = 5.42  # m²*Kelvin/W

    air_heat_capacity =1.006 # KJ/(kg*kelvin)
    heat_generation_rate = 73853.4 # KJ/hour
    temperature_accuracy = 0.5 # °C
    target_room_temperature = 20.0 #°C
    initial_room_temperature = 5.0 #°C
    measured_room_temperature = 5.0 #°C
    estimated_time_to_target_temperature = 0.0 # minutes
    temperature_adjust = 0.0 #°C
    theoretical_room_temperature = 0.0 #°C

    # object of room_with_heater class
    room_heater = room_with_heater(room_volume=room_volume,
                                  room_area = room_area,
                                  hold_room_temperature = hold_room_temperature,
                                  outside_room_pressure = outside_room_pressure,
                                  outside_room_temperature = outside_room_temperature,
                                  room_thermal_resistance = room_thermal_resistance,
                                  air_heat_capacity = air_heat_capacity,
                                  heat_generation_rate = heat_generation_rate,
                                  temperature_accuracy = temperature_accuracy,
                                  target_room_temperature = target_room_temperature,
                                  initial_room_temperature = initial_room_temperature,
                                  measured_room_temperature = measured_room_temperature,
                                  estimated_time_to_target_temperature = estimated_time_to_target_temperature,
                                  temperature_adjust = temperature_adjust,theoretical_room_temperature = theoretical_room_temperature)

    # center control module call heater,set active heater flag ,target tuemperature,current temperature
    heater_activation_flag = 1

    # Normal heating
    target_temperature1 = 25.0
    current_temperature1 = -10.0
    heating_result1 = room_heater.heater_activate(heater_activation_flag =heater_activation_flag,target_temperature = target_temperature1,current_temperature = current_temperature1)
    assert abs(heating_result1 - room_heater.measured_room_temperature) < 0.5
    print("***************Test Result******************")
    print("******Test_heating1,result:",heating_result1)
    print("\n")

    #Wrong input: target smaller than current
    target_temperature2 = 10.0
    current_temperature2 = 20.0
    heating_result2 = room_heater.heater_activate(heater_activation_flag =heater_activation_flag,target_temperature = target_temperature2,current_temperature = current_temperature2)
    assert heating_result2==False
    print("***************Test Result******************")
    print("******Test_heating2,result:",heating_result2)
    print("\n")

    #Wrong input :target equal to current
    target_temperature3 = 20.0
    current_temperature3 = 20.0
    heating_result3 = room_heater.heater_activate(heater_activation_flag =heater_activation_flag,target_temperature = target_temperature3,current_temperature = current_temperature3)
    assert heating_result3==False
    print("***************Test Result******************")
    print("******Test_heating3,result:",heating_result3)
    print("\n")

    #Boundary correct input::target -current bigger than 0.5
    target_temperature4 = 16.51
    current_temperature4 = 16.0
    heating_result4 = room_heater.heater_activate(heater_activation_flag =heater_activation_flag,target_temperature = target_temperature4,current_temperature = current_temperature4)
    assert abs(heating_result4 - room_heater.measured_room_temperature) < 0.5
    print("***************Test Result******************")
    print("******Test_heating4,result:",heating_result4)
    print("\n")

    #Boundary error input::target -current equals to 0.5
    target_temperature5 = 16.5
    current_temperature5 = 16.0
    heating_result5 = room_heater.heater_activate(heater_activation_flag =heater_activation_flag,target_temperature = target_temperature5,current_temperature = current_temperature5)
    assert heating_result5==False
    print("***************Test Result******************")
    print("******Test_heating5,result:",heating_result5)
    print("\n")
# un comment below line to active moudle test
#test_heater_activate()
import time
import random
class Test_controller:
  def controller_send_realtime_temperature(self,temp_request,refer_temperature):
        # temperatue request flag 1
        if temp_request == 1:
        # call sensor to send real temperature
          room_realtime_temperature = refer_temperature - random.uniform(0.3,0.6)
          return room_realtime_temperature
        else:
          print("Wrong temperature request!")

temperature_controller = Test_controller()

class Room:
    def __init__(self, room_volume, room_area, hold_room_temperature,
                 outside_room_pressure, outside_room_temperature, room_thermal_resistance):
        self.room_volume = room_volume
        self.room_area = room_area
        self.hold_room_temperature = hold_room_temperature
        self.outside_room_pressure = outside_room_pressure
        self.outside_room_temperature = outside_room_temperature
        self.room_thermal_resistance = room_thermal_resistance

    def air_density(self):
        air_constant = 287.05  # J/(kg*K), specific gas constant for dry air
        air_density_value = self.outside_room_pressure / (air_constant * (self.hold_room_temperature + 273.15))
        return air_density_value

    def outdoor_temperature(self):
        return self.outside_room_temperature

class Cooler(Room):
    def __init__(
        self,
        temperature_accuracy,
        target_room_temperature,
        initial_room_temperature,
        measured_room_temperature,
        estimated_time_to_target_temperature,
        temperature_adjust,
        theoretical_room_temperature,
        room_volume,
        room_area,
        hold_room_temperature,
        outside_room_pressure,
        outside_room_temperature,
        room_thermal_resistance,
        current_temperature,
        setting_temperature
        #temperature_controller
    ):
        super().__init__(
            room_volume,
            room_area,
            hold_room_temperature,
            outside_room_pressure,
            outside_room_temperature,
            room_thermal_resistance,
        )
        #self.temperature_controller = temperature_controller

        # temperature_accuracy represents the tolerance of the target temperature
        self.temperature_accuracy = temperature_accuracy  # 0.5 °C
        # target_room_temperature stands for the expected temperature need to reach
        self.target_room_temperature = target_room_temperature  # °C
        # initial_room_temperature the starting temperature of the control process
        self.initial_room_temperature = initial_room_temperature  # °C
        # measured_room_temperature represents the current temperature during the control process, used for heater working time calculation
        self.measured_room_temperature = measured_room_temperature  # °C
        # estimated_time_to_target_temperature represents for time needed to heat room from initial to target temperature
        self.estimated_time_to_target_temperature = estimated_time_to_target_temperature  # minutes
        # temperature_adjust is a variable to optimize the heating algorithm
        self.temperature_adjust = temperature_adjust
        # after each heat round calculate theoretical temperature to be reached
        self.theoretical_room_temperature = theoretical_room_temperature

    def input_temperature(self, new_temperature):
        # Receive the temperature from an external source (e.g., sensor)
        self.current_temperature = new_temperature

    def set_temperature(self, new_setting_temperature):
        # Setting the target temperature for cooling
        if new_setting_temperature > self.current_temperature:
            print("Error: Target temperature is higher than the current room temperature.")
        else:
            self.setting_temperature = new_setting_temperature
            print(f"Setting temperature to {self.setting_temperature} degrees Celsius.")
            return self.setting_temperature



    def get_realtime_temperature(self, temp_request):
        # Simulate controller sending real-time temperature
        return temperature_controller.controller_send_realtime_temperature(temp_request, self.theoretical_room_temperature)

    def cooler_activate(self, cooler_activation_flag):
        # Activate the cooler based on the controller's flag
        if cooler_activation_flag == 1:

            # Perform the cooling
            i = 0
            while abs(self.current_temperature - self.setting_temperature) > self.temperature_accuracy :
                print("\nsetting_temperature", self.setting_temperature)
                print("current_temperature", self.current_temperature)
                i = i+1

                if self.current_temperature - self.setting_temperature  <= 3:
                    self.target_room_temperature = self.setting_temperature
                    # Factors influencing the cooling rate
                    air_density_influence = -0.9 * self.air_density()
                    outdoor_temperature_influence = 0.03 * self.outdoor_temperature()

                    # Calculate the total cooling influence
                    total_cooling_influence =   air_density_influence +  outdoor_temperature_influence

                    print("total_cooling_influence ℃:",total_cooling_influence)

                    # Decrease the temperature with consideration for total cooling influence
                    self.theoretical_room_temperature = self.current_temperature + total_cooling_influence

                    # Get real-time temperature from the controller
                    self.current_temperature  = self.get_realtime_temperature(temp_request=1)

                    print(f"Cooling round {i} in progress. Current temperature: {self.current_temperature} degrees Celsius.")

                    # simulate heating process
                    time.sleep(1)
                else:
                    # Factors influencing the cooling rate
                    air_density_influence = -1.8 * self.air_density()
                    outdoor_temperature_influence = 0.03 * self.outdoor_temperature()

                    # Calculate the total cooling influence
                    total_cooling_influence =   air_density_influence +  outdoor_temperature_influence

                    print("total_cooling_influence ℃:",total_cooling_influence)

                    # Decrease the temperature with consideration for total cooling influence
                    self.theoretical_room_temperature = self.current_temperature + total_cooling_influence

                    # Get real-time temperature from the controller
                    self.current_temperature  = self.get_realtime_temperature(temp_request=1)

                    print(f"Cooling round {i} in progress. Current temperature: {self.current_temperature} degrees Celsius.")

                    # simulate heating process
                    time.sleep(1)

            print("Target temperature", self.setting_temperature)
            print("Measured temperature", self.current_temperature)
            if (self.setting_temperature - self.current_temperature) <= self.temperature_accuracy:
              print("\n")
              print("Temperature reached, Cooler turned off!")
              return self.current_temperature
            else:
              print("Temperature not reached!")
              return self.current_temperature


from flask import Flask, render_template, request, redirect, url_for, flash, jsonify  # assemble


##initiate sensor module
sensor = TemperatureSensor()
env = Environment(theoretical_temp=26.0)
# Generate initial outdoor temperature
initial_outdoor_temp = sensor.generate_initial_outdoor_temp()
# Calculate indoor temperature based on outdoor temperature
initial_indoor_temp = sensor.indoor_temperature()

##initiate controller module
initial_temperature = initial_indoor_temp
Input = int(initial_indoor_temp)
temperature_controller = TemperatureController(initial_temperature, 'auto', Input, 0)

##initiate heater
# instantiate parameter for room_with_heater
room_volume = 6000  # m³
room_area = 2200  # m²
hold_room_temperature = initial_temperature  # °C should be same as target_temperature
outside_room_pressure = 101325  # pascals
outside_room_temperature = 5  # °C
room_thermal_resistance = 5.42  # m²*Kelvin/W

air_heat_capacity = 1.006  # KJ/(kg*kelvin)
heat_generation_rate = 73853.4  # KJ/hour
temperature_accuracy = 0.5  # °C
target_room_temperature = initial_temperature  # °C
initial_room_temperature = initial_indoor_temp  # °C
measured_room_temperature = initial_indoor_temp  # °C
estimated_time_to_target_temperature = 0.0  # minutes
temperature_adjust = 0.0  # °C
theoretical_room_temperature = initial_indoor_temp  # °C

# object of room_with_heater class
room_heater = room_with_heater(room_volume=room_volume,
                               room_area=room_area,
                               hold_room_temperature=hold_room_temperature,
                               outside_room_pressure=outside_room_pressure,
                               outside_room_temperature=outside_room_temperature,
                               room_thermal_resistance=room_thermal_resistance,
                               air_heat_capacity=air_heat_capacity,
                               heat_generation_rate=heat_generation_rate,
                               temperature_accuracy=temperature_accuracy,
                               target_room_temperature=target_room_temperature,
                               initial_room_temperature=initial_room_temperature,
                               measured_room_temperature=measured_room_temperature,
                               estimated_time_to_target_temperature=estimated_time_to_target_temperature,
                               temperature_adjust=temperature_adjust,
                               theoretical_room_temperature=theoretical_room_temperature)

###initiate cooler
initial_room_temperature = initial_indoor_temp
initial_indoor_temp = initial_indoor_temp
temperature_accuracy = 0.5
target_room_temperature = 26.0
estimated_time_to_target_temperature = 0.0
theoretical_room_temperature = initial_temperature
room_volume = 6000
room_area = 2200
hold_room_temperature = 26
outside_room_pressure = 101325
outside_room_temperature = 5
room_thermal_resistance = 5
current_temperature = initial_indoor_temp
setting_temperature = 26.0

cooler_instance = Cooler(
    temperature_accuracy,
    target_room_temperature,
    initial_room_temperature,
    measured_room_temperature,
    estimated_time_to_target_temperature,
    temperature_adjust,
    theoretical_room_temperature,
    room_volume,
    room_area,
    hold_room_temperature,
    outside_room_pressure,
    outside_room_temperature,
    room_thermal_resistance,
    current_temperature,
    setting_temperature
)

### Flask web application##

app = Flask(__name__)

app.secret_key = '123456'


@app.route('/', methods=['GET', 'POST'])  # define index route
def index():
    if request.method == 'POST':  # use 'POST' method to receive values generated by the user interface (HTML)
        if 'mode' in request.form:

            temperature_controller.mode = request.form['mode']
            # check the route that the user choosed
            if temperature_controller.mode == 'auto':  # define the route for the auto button
                flash('The default auto setting is 26°C.')  # flash the auto page when the user entering auto.html
                return render_template('auto.html', current_temperature=temperature_controller.current_temperature)

            else:  # define the route for the manual button
                flash('The temperature previously set by the user was ' + str(temperature_controller.Input) + '°C.')
                return render_template('manual.html', current_temperature=temperature_controller.current_temperature)

    return render_template('index.html', current_temperature=temperature_controller.current_temperature)
    # define the end point of index.html (if the user does not click any butoon)


@app.route('/auto', methods=['GET', 'POST'])  # define auto route
def auto_mode():
    if request.method == 'POST':
        if 'action' in request.form:
            if request.form['action'] == 'start':  # receive the value of from the request form.
                temperature_controller.mode = 'auto'
                if 26 - temperature_controller.current_temperature < 0:  # if the current temperature is above 26°C
                    temperature_controller.control_system()  # call control_system() method
                    flash('It requires cooler ' + str(
                        temperature_controller.time2wait) + ' minutes to complete the cooling process')
                    return render_template('auto.html', current_temperature=temperature_controller.current_temperature)

                elif 26 - temperature_controller.current_temperature > 0:  # if the current temperature is below 26°C
                    temperature_controller.control_system()  # call control_system() method
                    flash('It requires heater ' + str(
                        temperature_controller.time2wait) + ' minutes to complete the heating process')
                    return render_template('auto.html', current_temperature=temperature_controller.current_temperature)

                else:
                    flash('The current temperature satisfy the auto setting.')
                    return render_template('auto.html', current_temperature=temperature_controller.current_temperature)

            elif request.form['action'] == 'back':  # if user click 'Home' button with 'back' value in request form
                flash('Welcome Back')
                return render_template('index.html',
                                       current_temperature=temperature_controller.current_temperature)  # redirect to main page

    return render_template('auto.html', current_temperature=temperature_controller.current_temperature)


@app.route('/manual', methods=['GET', 'POST'])  # define manual route
def manual_mode():
    if request.method == 'POST':
        if 'action' in request.form:  # receive the value of from the request form.
            temperature_controller.mode = 'manual'
            if request.form['action'] == 'cool':
                temperature_controller.Input -= 1  # The setting temperature minus 1 each time of clicking Cool button
                temperature_controller.control_system()  # call control_system() method
                flash('It requires cooler ' + str(
                    temperature_controller.time2wait) + ' minutes to complete the cooling process.')
                return render_template('manual.html', current_temperature=temperature_controller.current_temperature)

            elif request.form['action'] == 'heat':
                temperature_controller.Input += 1  # The setting temperature plus 1 each time of clicking Heat button
                temperature_controller.control_system()  # call control_system() method
                flash('It requires heater ' + str(
                    temperature_controller.time2wait) + ' minutes to complete the heating process.')
                return render_template('manual.html', current_temperature=temperature_controller.current_temperature)

        elif 'back' in request.form:
            if request.form['back'] == 'back':  # if user click 'Home' button with 'back' value in request form
                flash('Welcome Back')
                return render_template('index.html',
                                       current_temperature=temperature_controller.current_temperature)  # redirect to main page

        try:
            if 'temperature' in request.form:  #

                new_temp = int(request.form['temperature'])  # received the user inputted value

                temperature_controller.Input = new_temp

                if temperature_controller.Input - temperature_controller.current_temperature < 0:
                    # if the user inputted value is below the current temperature
                    temperature_controller.control_system()
                    flash('The temperature previously set by the user was ' + str(temperature_controller.Input) + '°C.')
                    return render_template('manual.html',
                                           current_temperature=temperature_controller.current_temperature)
                    # if the user inputted value is above the current temperature
                elif temperature_controller.Input - temperature_controller.current_temperature > 0:
                    temperature_controller.control_system()
                    flash('The temperature previously set by the user was ' + str(temperature_controller.Input) + '°C.')
                    return render_template('manual.html',
                                           current_temperature=temperature_controller.current_temperature)

                else:
                    flash('The temperature previously set by the user was ' + str(temperature_controller.Input) + '°C.')
                    return render_template('manual.html',
                                           current_temperature=temperature_controller.current_temperature)
        except ValueError:  # if it is an invalid input
            notification_message = "Invalid temperature input"
            return jsonify({'message': notification_message})

    return render_template('manual.html', current_temperature=temperature_controller.current_temperature)


@app.route('/real_time_current_temperature', methods=['GET'])  # define real_time_current_temperatue route
def real_time_current_temperature():
    current_temperature = temperature_controller.current_temperature  # establish connection between function and HTML file, which allows the current_temperature in html to be updated in real-time

    return jsonify(current_temperature=current_temperature)


@app.route('/target')
def target():
    target = temperature_controller.Input
    return jsonify(target_temperature=target)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)  # run on localhost port 8000



