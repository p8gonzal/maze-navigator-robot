
# This program demonstrates how to control an ultrasound distance sensor

# Import the relevant libraries
import RPi.GPIO as GPIO
import time
import random

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BOARD)
 
# set GPIO Pins
TriggerPin  = 12
EchoPin     = 18
TriggerPin2 = 16
EchoPin2    = 22
TriggerPin3 = 13
EchoPin3    = 29

 
# set GPIO direction (IN / OUT)
GPIO.setup(TriggerPin, GPIO.OUT)
GPIO.setup(EchoPin, GPIO.IN)
GPIO.setup(TriggerPin2, GPIO.OUT)
GPIO.setup(EchoPin2, GPIO.IN)
GPIO.setup(TriggerPin3, GPIO.OUT)
GPIO.setup(EchoPin3, GPIO.IN)

# Wait for sensor to settle
GPIO.output(TriggerPin, False)
print("Waiting for sensor to settle")
time.sleep(2)
print("Start sensing")
def set_duty_cycle(angle):
    return ((duty_max - duty_min) * float(angle) / 180.0 + duty_min)
GPIO.output(TriggerPin2, False)
print("Waiting for sensor to settle")
time.sleep(2)
print("Start sensing")
def set_duty_cycle(angle):
    return ((duty_max - duty_min) * float(angle) / 180.0 + duty_min)
GPIO.output(TriggerPin3, False)
print("Waiting for sensor to settle")
time.sleep(2)
print("Start sensing")
def set_duty_cycle(angle):
    return ((duty_max - duty_min) * float(angle) / 180.0 + duty_min)


GPIO.setmode(GPIO.BOARD)
                                      
                   
pwm_frequency = 50
duty_min = 2.5 * float(pwm_frequency) / 50.0
duty_max = 12.5 * float(pwm_frequency) / 50.0

#servo 1
ServoPin = 3
GPIO.setup(ServoPin, GPIO.OUT)
pwm_servo = GPIO.PWM(ServoPin, (pwm_frequency*2))

#Servo 2
ServoPin2 = 31
GPIO.setup(ServoPin2, GPIO.OUT)
pwm_servo2 = GPIO.PWM(ServoPin2, (pwm_frequency/2.2))







global state
state = 0 
def foward(pwm_servo):

        try:
        
            while True:                       
                angle = 360
                pwm_servo.start(set_duty_cycle(angle))
                print ("Moving ")
                
                if(distance(TriggerPin, EchoPin)<=25):
                    return 
                print("Measured distance: ",distance(TriggerPin, EchoPin))
                foward2(pwm_servo2)
            
        except KeyboardInterrupt:
            print("Program stopped by User")
            GPIO.cleanup()
def backward(pwm_servo, pwm_servo2,x):
    t=time.clock()
    angle1=0
    while (time.clock()-t < (.5*x)):
        pwm_servo.start(set_duty_cycle(angle1))
        pwm_servo2.start(set_duty_cycle(angle1))
    pwm_servo.start(0)
    pwm_servo2.start(0)
    
def foward2(pwm_servo):

        try:
        
            while True:                       
                angle = 360
                pwm_servo.start(set_duty_cycle(angle))
                print ("Moving ")
                
                if(distance(TriggerPin, EchoPin)<=25):
                    return 
                print("Measured distance: ",distance(TriggerPin, EchoPin))
            
        except KeyboardInterrupt:
            print("Program stopped by User")
            GPIO.cleanup()

def stop(pwm_servo):
    pwm_servo.start(0)
    print("Servo has stopped.")

def RightTurn(x):
    st=time.clock()
    while(time.clock()-st < (.233*x)):
        print(time.clock()-st )
        angle = 360
        pwm_servo2.start(set_duty_cycle(angle))
        pwm_servo.start(set_duty_cycle(0))
    stop(pwm_servo2)
    stop(pwm_servo)

def LeftTurn(x):
    st=time.clock()
    while(time.clock()-st < (.2*x)):
        print(time.clock()-st )
        angle = 360
        pwm_servo.start(set_duty_cycle(angle))
        pwm_servo2.start(set_duty_cycle(0))
    stop(pwm_servo)
    stop(pwm_servo2)
    
    
    
# Helper function to get the distance from the ultrasound sensor.

def distance(TriggerPin, EchoPin):
    
    # Create a pulse on the trigger pin
    # This activates the sensor and tells it to send out an ultrasound signal
    GPIO.output(TriggerPin, True)
    time.sleep(0.00001)
    GPIO.output(TriggerPin, False)

    # Wait for a pulse to start on the echo pin
    # The response is not valid if it takes too long, and we should break the loop
    valid = True
    RefTime = time.time()
    StartTime = RefTime
    while (GPIO.input(EchoPin) == 0) and (StartTime-RefTime < 0.1):
        StartTime = time.time()
    if (StartTime-RefTime >= 0.1):
        valid = False
        
    # Wait for a pulse to end on the echo pin
    # The response is not valid if it takes too long, and we should break the loop
    if (valid):
        RefTime = time.time()
        StopTime = time.time()
        while (GPIO.input(EchoPin) == 1) and (StopTime-RefTime < 0.1):
            StopTime = time.time()
        if (StopTime-RefTime >= 0.1):
            valid = False
        
    # If we received a complete pulse on the echo pin (i.e., valid == True)
    # Calculate the distance based on the length of the echo pulse and
    # the speed of sound (34300 cm/s)
    if (valid):
        EchoPulseLength = StopTime - StartTime
        return (EchoPulseLength * 34300) / 2        # Divide by 2 because we are calculating based on a reflection, so the travel time there and back
    else:
        return -1
        
# --- End of the ultrasound sensor helper function ---
#def foward():
    
 
# Main program 
if __name__ == '__main__':
    try:
        
       
        while True:
            dist  = distance(TriggerPin, EchoPin)
            dist2 = distance(TriggerPin2, EchoPin2)
            dist3 = distance(TriggerPin3, EchoPin3)
            print("foward ",dist)
            print("Left ",dist2)
            print("Right ",dist3)

            if state == 0:
                if(dist > 10):
                    foward(pwm_servo)
                    next_state = 0
                elif(dist < 10):
                    stop(pwm_servo)
                    stop(pwm_servo2)
                    next_state = 1
            if state == 1:
                if (dist2 < 10 and (dist3 > 10 or dist3 == -1)):
                    backward(pwm_servo,pwm_servo2,1)
                    RightTurn(1)
                    next_state = 0
                elif ((dist2 > 10 or dist2 == -1) and dist3 < 10):
                    backward(pwm_servo, pwm_servo2, 1)
                    LeftTurn(1)
                    next_state = 0
                elif ((dist2 > 10 or dist2 == -1) and (dist3 >10 or dist3 == -1)):
                    backward(pwm_servo, pwm_servo2, 1)
                    s=random.randint(1,2)
                    if(s == 1):
                        LeftTurn(1)
                    else:
                        RightTurn(1)
                    next_state= 0
                elif(dist2 < 10 and dist3 < 10):
                    backward(pwm_servo, pwm_servo2, 3)
                    RightTurn(1)
                    LeftTurn(1)
                    next_state= 0
                    
            state = next_state
                    
                    
                    
                    
                    
                    
            

            
           
         





    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup() 
