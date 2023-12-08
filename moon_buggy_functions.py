#Detony White-Snipes
#12/5/2023
#Functions that make the monn buggy game run

import numpy as np
import matplotlib.pyplot as plt
import random as rd

#########Generate_Crater Function#####
# This function will generate random values for crater parameters
def generate_crater(crdia_min, crdia_max, crht_min, crht_max, crslope_min, crslope_max):
    crdia = np.random.uniform(crdia_min, crdia_max)
    crht = np.random.uniform(crht_min, crht_max)
    crslope = np.random.uniform(crslope_min, crslope_max)

    crbasedia =(crht/(np.tan(np.radians(crslope))) + crdia)
    crdepth = crht / 2

    return crdia, crht, crslope, crbasedia, crdepth
#########End of Generate_Crater Function#####

######Buggy_Parameters Function#######
def buggy_parameters():
    print("1 = Moonstar One, 2 = Planetexpress Truck, 3 = Metor Machine")
    print('Moonstar One: \n'
          'Max torque: 135 N-m \n'
          'Buggy mass: 150 kg \n'
          'Wheel diameter: 1.0 m')
    print()
    print('Planetexpress Truck: \n'
          'Max torque: 275 N-m \n'
          'Buggy mass: 300 kg \n'
          'Wheel diameter: 1.5 m')
    print()
    print('Metor Machine: \n'
          'Max torque: 400 N-m \n'
          'Buggy mass: 180 kg \n'
          'Wheel diameter: 1.3 m')
    print()

    is_valid_buggy=False
    while is_valid_buggy==False:
        buggy_choice = (input('Pick out a Buggy cadet 1, 2, or 3,?!'))
        if (buggy_choice=='1') or (buggy_choice=='2') or (buggy_choice=='3'):
            is_valid_buggy=True
        else:
            print('Do you have clutter in your ears cadet! I said 1, 2, or 3!')

    if buggy_choice == '1':
        buggy_choice = 'Moonstar One'
        torque = 135
        buggy_mass = 150
        wheel_dia = 1.0

    elif buggy_choice == '2':
        buggy_choice = 'Planet express Buggy'
        torque = 275
        buggy_mass = 300
        wheel_dia = 1.5

    elif buggy_choice == '3':
        buggy_choice ='Batmobile'
        torque = 400
        buggy_mass = 180
        wheel_dia = 1.3

    print(f'Alright, bring the {buggy_choice} around.')
    return buggy_choice, torque, buggy_mass, wheel_dia,
##########End of Buggy parameters Function######

#####Function Throttle percent#######3
def get_percent_throttle():
    while True:
        try:
            throttle_pct = int(input('Enter the throttle percentage (1-100): '))
            if 1 <= throttle_pct <= 100:
                return throttle_pct
            else:
                print('Invalid input. Throttle percentage must be between 1 and 100.')
        except ValueError:
            print('Invalid input. Please enter a valid integer.')
    return throttle_pct
###########End of Throttle Percent#######

#######Determine Throttle Percent#######
def determine_bugdir(wheelforce, weightforce, rolling_res):
    if (abs(weightforce) > (wheelforce + rolling_res)):
        bugdir = 'downhill'
    elif (wheelforce < (abs(weightforce) + rolling_res)):
        bugdir = 'stuck'
    else:
        bugdir = 'uphill'  # Buggy goes forward
    return bugdir
########End of  Function determine_bugdir ###########

############Calculate Flank Path##########
def calculate_flank_path(wheelforce, weightforce,rolling_res, crslope, time_step, buggy_mass,crht):
    accel = (wheelforce + weightforce + rolling_res) / buggy_mass
    xval = 0.0  # Starts at x=0
    yval = 0.0  # y never changes
    zval = 0.0  # starts at z=0
    speed = 0.0  # inital speed = 0
    t = 0.0
    pathdata = np.zeros([1, 5])
    arow = np.zeros([1, 5])
    arow[0, :] = [t, xval, yval, zval, speed]
    rownum = 0

    while (zval <= crht):
        rownum = rownum + 1
        t = t + time_step
        dist = 0.5 + accel * t ** 2  # 1D motion starting at d=0
        xval += dist * np.cos(crslope * (np.pi / 180))
        zval += dist * np.sin(crslope * (np.pi / 180))
        speed = accel * t
        arow[0, :] = [t, xval, yval, zval, speed]
        pathdata = np.vstack([pathdata, arow])
    [numrows, numcols] = pathdata.shape
    return pathdata, numrows



##############End of Calculate Flank Path######

############Calculate Parabolic Path##########
def calculate_parabolic_path(pathdata, numrows, crslope, time_step, g):
    t_init = pathdata[((numrows - 1), 0)].copy()
    x_init = pathdata[((numrows - 1), 1)].copy()
    z_init = pathdata[((numrows - 1), 3)].copy()
    speed_init = pathdata[((numrows - 1 ), 4)].copy()
    rownum = numrows - 1
    t = t_init
    zval = z_init
    yval = 0 #Y value never changes
    x_speed = speed_init *np.cos(crslope * np.pi / 180)
    temprow = np.zeros([1, 5])
    print(t)
    print(f't_init = {t_init}')

    while zval >= 0.0:
        t = t + time_step
        rownum = rownum + 1
        tpar = (t - t_init)
        z_speed = g * tpar + speed_init * np.sin(crslope * np.pi / 180)
        zval = .5 * (g) * (tpar) ** 2 + z_speed * tpar + z_init
        xval = x_speed * tpar + x_init
        speed = np.sqrt(x_speed ** 2 + z_speed ** 2)
        temprow[0, :] = [t, xval, yval, zval, speed]
        print(temprow)
        pathdata = np.vstack([pathdata, temprow])
    [numrows, numcols] = np.shape(pathdata)

    print(temprow)
    return pathdata, numrows
########End of Parabolic Function##########

########Finding Landing point###########
def find_landing_point(pathdata, launchrow, crdia, crbasedia, crht, crdepth, crslope):
    [numrows, numcols] = np.shape(pathdata)

    # Extract the launch x-coordinate
    xlaunch = pathdata[launchrow, 1].copy()

    # Initialize variables
    xval = xlaunch
    zval = pathdata[launchrow, 3].copy()
    rownum = launchrow
    landed = False

    while (rownum < numrows - 1) and (xval <= xlaunch + crdia) and (not landed):
        rownum += 1
        xval = pathdata[rownum, 1].copy()
        zval = pathdata[rownum, 3].copy()

        if zval <= (crht - crdepth):  # Check if landed on the crater floor
            landingz = zval
            landingx = xval
            landing_row = rownum
            landing_cond = 'craterfloor'
            landed = True

        elif zval <= crht:  # Check if landed on the crater wall
            landingz = zval
            landingx = xval
            landing_row = rownum
            landing_cond = 'craterwall'
            landed = True

    while rownum < numrows - 1 and not landed:
        rownum += 1
        xval = pathdata[rownum, 1].copy()
        zval = pathdata[rownum, 3].copy()

    flankz = -np.tan(crslope * np.pi / 180) * (xval - ((crbasedia / 2) * crdia / 2)) + crht  # Calculate the expected z-coordinate on the flank
    print(f'current numbers equal {xval}')

    if zval <= flankz:  # Check if the buggy has landed on the flank
        landing_row = rownum
        landing_cond = 'flank'
        landed = True

    final_pathdata = pathdata[:landing_row + 1, :]
    return final_pathdata, landing_row, landing_cond

##########End of Landing#############

##########Calculate_Path#########
def calculate_path(throttlepct, torque, wheeldia, crslope, buggy_mass, g,time_step,crht,crdia, crbasedia, crdepth  ):
    wheelforce = 4 * (throttlepct / 100) * torque / (wheeldia / 2)
    weightforce = buggy_mass * (-g) * np.sin(crslope)
    rolling_res = 0.3 * buggy_mass * (g) * np.cos(crslope) #Coefficient of rolling resistance equal 0.3
    print(wheelforce)

    #Finding out which way buggy moves
    bugdir = determine_bugdir(wheelforce,weightforce, rolling_res)
    if bugdir == 'downhill':
        final_pathdata = np.ones((5, 5)) #put in dummy values for the pathdata matrix just to keepf rom crashing
        launch_row = 2
        landing_row = 3
        landing_cond = 'downhill'

    elif bugdir == 'stuck':
        final_pathdata = np.ones((5, 5 )) #more dummy values
        launch_row = 2
        landing_row = 3
        landing_cond = 'stuck'

    else: #buggy accelerates uphill
        pathdata, numrows =calculate_flank_path(wheelforce, weightforce, rolling_res, crslope, time_step, buggy_mass,crht)
        launch_row = numrows
        pathdata, numrows = calculate_parabolic_path(pathdata, numrows, crslope,time_step,g)
        final_pathdata, landing_row, landing_cond = find_landing_point(pathdata, launch_row, crdia, crbasedia, crht, crdepth, crslope)

    return final_pathdata, landing_row, launch_row, landing_cond


    #############End of function

#######Report function##########
def report_path(final_pathdata, launch_row, landing_cond, landing_row):
        launch_time = final_pathdata[launch_row, 0]
        landing_time = final_pathdata[landing_row, 0]
        flight_time = launch_time - landing_time

        print("Jump Results:")
        print("Launch Time:", launch_time)
        print("Landing Time:", landing_time)
        print("Flight Time:", flight_time)

        if "craterfloor" in landing_cond:
            print("Landing Condition: In the bottom of the crater")
        elif "craterwall" in landing_cond:
            print("Landing Condition: Against the back wall of the crater")
        elif "flank" in landing_cond:
            print("Landing Condition: On the flank of the crater")
        else:
            print("Landing Condition: No where close")
###########End of Functions######

