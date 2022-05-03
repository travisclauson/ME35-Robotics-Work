from cmath import phase
from lib2to3.pygram import python_grammar_no_print_statement
from buildhat import MotorPair, ColorSensor
from airtable import Airtable
import time
import stepper

baseID = 'appuhn9X6CJyPGaho'
tableName = 'control'
APIkey = 'keyKh14uewaMw11ax'

airtable = Airtable(baseID, tableName, APIkey)

wheels = MotorPair('A','B')
sensor = ColorSensor('C')

speed = 15 # power sent to motors for wheels 
num_degrees = 720
cook_time = 900 # in seconds

primaryHeight = 200
liftHeight = 250

wheels.start(0,0)
arms = stepper.Stepper(200, 18, 16)
#Hard code heights
arms.primaryHeight = 0
arms.releaseHeight = 300
arms.frostingHeight = 11850

def updateAirtable(phase, status):
    record = airtable.match("Name", phase)
    if status == 'in progress':
        fields = {'Select': 'in progress'}
    elif status == 'complete':
        fields = {'Select': 'complete'}
    airtable.update(record["id"], fields)
    print(phase + ' is ' + status)

def driveForward(targ_phase):
    run = True
    while run:
        return_phase = airtable.match('Name', targ_phase)

        if return_phase['fields']['Select'] == 'complete':

            if targ_phase == 'mixing':
                updateAirtable('loading', 'in progress')
            elif targ_phase == 'cooking':
                updateAirtable('unloading', 'in progress')
            elif targ_phase == 'unloading':
                updateAirtable('frosting position set', 'in progress')

            print('move forward')
            wheels.start(speed, -speed)
            time.sleep(2)
            sensor.wait_until_color('black')
            wheels.stop()
            time.sleep(1)
            run = False
        else:
            print('do nothing')

        time.sleep(0.2)


def driveBackwards():
    print('move backwards')
    wheels.run_for_degrees(num_degrees, -speed, speed)
    #wheels.start(-speed, speed)
    #time.sleep(2)
    #sensor.wait_until_color('red')
    wheels.stop()
    time.sleep(1)

def waitForPhase(phase):
    run_func = True
    while run_func:
        return_phase = airtable.match('Name', phase)
        if return_phase['fields']['Select'] == 'complete':
            print('previous phase is done')
            run_func = False

        time.sleep(0.2)


def cookTime():
    updateAirtable('cooking', 'in progress')
    start = time.time()
    print(time.localtime(start))
    done = False
    while done == False:
        end = time.time()
        seconds = int(end - start)

        if seconds % 5 == 0:

            timer = cook_time - seconds
            record = airtable.match("Name", 'cooking')
            fields = {'time': timer}
            print(seconds)
            airtable.update(record["id"], fields)

        if seconds > cook_time:
            done = True
        time.sleep(0.2)
    print(end - start)
    updateAirtable('cooking', 'complete')
    


waitForPhase('mixing')

#arms.moveToLocation(arms.primaryHeight) ## DO NOT NEED THIS LINE

#driveForward('mixing') # drive forward to black tape for loading once mixing done

#arms.moveToLocation(arms.releaseHeight)

#driveBackwards() # drive backwards to red tape
updateAirtable('loading', 'complete')
# arms should still be at correct height so move forward
#cookTime()
#driveForward('cooking') # drive forward to black tape for unloading once cooking is done

#arms.moveToLocation(arms.primaryHeight)

#driveBackwards() # drive backwards to black tape
updateAirtable('unloading', 'complete')

arms.moveToLocation(arms.frostingHeight)

driveForward('unloading') # drive forward to black tape for frosting once door closed
updateAirtable('frosting position set', 'complete')
waitForPhase('frosting')
driveBackwards() # drive backwards to red tape for display 

arms.moveToLocation(arms.primaryHeight)


## DONE


