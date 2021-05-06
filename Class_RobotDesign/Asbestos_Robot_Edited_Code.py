"""

WS 2018-19 Robotics
Final Project 
4355255 Ka Hei Pinky, Chow

Asbestos, a toxic material of high public health concern, is widely used as
building material in plentiful developing countries. Every year, over 107,000
people die in the world from exposure to this chemical substance. Our robot
design thereby aims for testing Asbestos level effectively in the indoor
environment. It is mobile with the aid of wheels. Equipped with an on-site
Asbestos sensor, three LED lights and a buzzer, the robot will move in a
straight line and stop for Asbestos testing every 5 metres. The lights and
buzzer will turn on according to the level of Asbestos. The robot is also
capable to  sense temporary obstacle and will move in reverse direction back
to the starting point when it faces some permanent obstacle like a wall.
When it is powered off, the recorded results will be save in a csv file for
further examination. 

Components:     
ultrasonic sensor x1, motor x1, Asbestos sensor x1, LEDs x3, switch x1, 
buzzer x1, rotary input (measuring distance) x1

"""

import pigpio
import time
import os

pi = pigpio.pi()

#Define GPIOs
LED_var1 = 2   #LED_Red
LED_var2 = 0   #LED_Yellow
LED_var3 = 7   #LED_Green

motor_output1 = 16
motor_output2 = 21 #Two directional movement

sensor_trig_output = 12 #Ultrasonic sensor
sensor_echo_input = 20

asbestos_input = 5 #Asbestos sensor

buzzer_output = 18 #Buzzer

power_ON = 22 #Switch

rotary_input = 24 #Optical rotary encoder

accumulated_rotary_counter = 0

Asbestos_Low_Level = 0
Asbestos_Middle_Level = 0
Asbestos_High_Level = 0

#Setting active components
pi.set_mode(LED_var1, pigpio.OUTPUT)
pi.set_mode(LED_var2, pigpio.OUTPUT)
pi.set_mode(LED_var3, pigpio.OUTPUT)

pi.set_mode(motor_output1, pigpio.OUTPUT) 
pi.set_mode(motor_output2, pigpio.OUTPUT)

pi.set_mode(sensor_trig_output, pigpio.OUTPUT)
pi.set_mode(sensor_echo_input, pigpio.INPUT)

pi.set_mode(rotary_input, pigpio.INPUT)

pi.set_mode(asbestos_input, pigpio.INPUT)

pi.set_mode(power_ON, pigpio.INPUT) 

pi.set_mode(buzzer_output, pigpio.OUTPUT)


"""
Defined Functions

"""

#The robot stops and samples Asbestos level every 5 metres

ROTARY_LIMIT = 10 #Sampling distance = 10 * 0.5m (circumference of wheel) = 5m

def process_sampling():
    pi.write(motor_output1, 1)
    pi.write(motor_output2, 0)

    rotary_counter = 0
        
    #robot stops after 5m movement and conduct sampling        
    while rotary_counter < ROTARY_LIMIT:  
        while pi.read(rotary_input) == 0:
            temporary_stop()
        rotary_counter += 1
        accumulated_rotary_counter += 1
        
    pi.write(motor_output1, 0)
    pi.write(motor_output2, 0) 
    
    #read asbestos value        
    process_asbestos_sensor()


#The robot tests Asbestos level and indicate the results
def process_asbestos_sensor():
    # We assume to have a function to read an analog value via Analog to
    # Digital converter
    
    asbestos_state = pi.read_adc(asbestos_input)
    
    #The permissible asbestos exposure limit (PEL) (f/cc) is 
    #setted by The Occupational Safety and Health Commission (OSHA)
    
    if asbestos_state >= 1: #High level (unit = f/cc)
        pi.write(LED_var1, 1)
        pi.write(buzzer_output, 1)
        time.sleep(2)
            
        pi.write(buzzer_output, 0)
        time.sleep(3)  
        pi.write(LED_var1, 0)
        
        Asbestos_High_Level += 1 
            
        pi.write(motor_output1, 1)
        pi.write(motor_output2, 0)
    
    elif asbestos_state < 1 and asbestos_state >= 0.04: #Medium level
        pi.write(LED_var2, 1)
        time.sleep(2)
            
        pi.write(LED_var2, 0)
        
        Asbestos_Middle_Level += 1
        
        pi.write(motor_output1, 1)
        pi.write(motor_output2, 0)
        
    elif asbestos_state < 0.04: #Low level
        pi.write(LED_var3, 1)
        time.sleep(2)

        pi.write(LED_var3, 0)
        
        Asbestos_Low_Level += 1
            
        pi.write(motor_output1, 1)
        pi.write(motor_output2, 0)
   
# The robot measures distance to any obstacle
def process_ultrasonic_sensor():
    print("Sending Ping..")
    
    distance = 0
    
    pi.write(sensor_trig_output, 0)
    time.sleep(0.1)
        
    pi.write(sensor_trig_output, 1)  
    time.sleep(0.00001)
    pi.write(sensor_trig_output, 0) 
    
    while pi.read(sensor_echo_input) == 0:
        pass
        
    start_time = time.time()
        
    while pi.read(sensor_echo_input) == 1:
        pass
        
    print("Receiving Ping..")
        
    end_time = time.time()
        
    distance = ((end_time -  start_time) * 34300) / 2 # initial distance
    
    # Measurement repeats 5 times for better accuracy
    for i in range(5): 

        pi.write(sensor_trig_output, 0)
        time.sleep(0.1)
        
        pi.write(sensor_trig_output, 1)  
        time.sleep(0.00001)
        pi.write(sensor_trig_output, 0) 
    
        while pi.read(sensor_echo_input) == 0:
            pass
        
        start_time = time.time()
        
        while pi.read(sensor_echo_input) == 1:
            pass
        
        print("Receiving Ping..")
        
        end_time = time.time()
        
        #Calculate average distance
        distance += ((end_time -  start_time) * 34300) / 2 / 2 
    
    return distance

def detect_obstacle():
        
    obstacle_distance = process_ultrasonic_sensor()
    print("Distance = ", obstacle_distance)
    time.sleep(0.5)
    
    if obstacle_distance < 50: #Obstacle exists within 0.5m
        obstacle = True
    else:
        obstacle = False
    return obstacle

def temporary_stop():
    #Stop robot when temporary obstacle detected
    obstacle = detect_obstacle()
    if obstacle == False:
        return
    
    pi.write(motor_output1, 0) 
    pi.write(motor_output2, 0)
    
    # Robot returns when obstacle lasts more than 10s
    start = time.time()
    end = time.time()
    while end - start < 10:
        if detect_obstacle() == False:
            return
        end = time.time()
               
    pi.write(motor_output1, 0)
    pi.write(motor_output2, 1)
        
    while accumulated_rotary_counter > 0:
        while pi.read(rotary_input) == 0:
            pass
        accumulated_rotary_counter -= 1
            
    pi.write(motor_output1, 0)
    pi.write(motor_output2, 0)
        
    os.exit(0)

def power_off():    
    #Turn off the robot
    pi.write(LED_var1, 0)  
    pi.write(LED_var2, 0)
    pi.write(LED_var3, 0)

    pi.write(motor_output1, 0)
    pi.write(motor_output2, 0)

    pi.write(sensor_trig_output, 0)
    pi.write(sensor_echo_input, 0)

    pi.write(asbestos_input, 0)

    pi.write(buzzer_output, 0)
    
    #According to the suggestions after presentation, a "memory function" for
    #the asbestos level is added to indicate the inspection result.
    f = open("Asbestos_Test_Results.csv", "a")
    f.write("Asbestos Test Results as below\n")
    f.write("Asbestos_Low_Level: " + Asbestos_Low_Level + '\n')
    f.write("Asbestos_Middle_Level: " + Asbestos_Middle_Level + '\n')
    f.write("Asbestos_High_Level: " + Asbestos_Low_Level + '\n')
    f.close()


"""
 Operation Process 
 
"""   
 
while True:
    power_state = pi.read(power_ON)
#power on    
    if power_state > 0:
        
#motor runs            
        process_sampling()

#power off: turn off every active component            
    if power_state == 0:  
        power_off()
 




"""         

End of code

"""       
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

