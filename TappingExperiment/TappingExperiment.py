# imports the necessary modules
import pygame
from pygame.locals import *
import os, sys
import math
import random
import time
import threading
from threading import Thread
import xlrd
from xlrd import open_workbook
import xlutils
import xlwt


#Initiate the pygame display (necessary)
pygame.display.init()

# Define colors incase you want them (optional)
BLACK = (0,0,0)
WHITE = (255,255,255)
LIGHTGRAY = (210,210,210)
RED = (255,0,0)

# Initialize screen parameters - this changes the size of the screen and the font
board_x = 1440
board_y = 900
text_height = 22

# Init the necessary settings for pygame.
pygame.init()
screen = pygame.display.set_mode((board_x, board_y))
pygame.mouse.set_visible(0)
font = pygame.font.SysFont('times', text_height)
pygame.font.init()


#Make the appropriate functions for the experiment

#Quit function (may not work... sorry). Just use force quit for now
def quit():
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:sys.exit()

#Funtion to write text to the screen - much easier than calling it every time
def blit_text(message, line, column=490, color=WHITE):
          # render the message
          the_text  = font.render(message, True, color, (0, 0, 0))
          # set it's location
          global text_rect
          text_rect = [column,line * text_height+1,board_x,text_height]
          # blit it to the screen
          screen.blit(the_text, text_rect)
          
#Function to take key presses in case we want to.
#Currently this is listening for an "A" or an "L" press.
def get_keypress():
    #Clear the event cue
    pygame.event.clear()
    #Listen for specific key presses - wait until they're returned
    all_done = False
    while all_done == False:
        event_list = pygame.event.get()                                                
        for event in event_list:
            #If a key is pressed down, and that key is an "A" or an "L" stop listening
            if event.type == KEYDOWN:
                if event.key == K_a:
                    return 'a'
                    all_done = True
                elif event.key == K_l:
                    return 'l'
                    all_done = True
                    
                    
#Function to collect mouse clicks and append the time of the click to a data list
def take_mouse_click(trial_number):
    #Start listening for events
    event_list = pygame.event.get()
    #If a mousebutton is pressed, log the time in ms
    for event in event_list:
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = pygame.time.get_ticks()
            #Append all needed data to data lists
            clicks.append(click)
            click_trial.append(trial_number)
            pre_post.append("pre")
            
#Function to start collecting clicks in the background using the threading module
#Threading is necessary because it will let you play a sound and listen for a click
#at the same time.
#Note, this is not the function to collect mouse clicks - only to start the thread.
def mouse_thread(trial_number):
    #Make the thread
    mouse_thread_go = threading.Thread(take_mouse_click(trial_number))
    #Start the thread
    mouse_thread_go.start()
            
#Function to collect clicks when no sound is playing
#This doesn't require threading, so it can just listen for mouse clicks
def collect_no_sound(needed, trial_number):
    #Collect sound clicks for the current trial just to keep track of how many have
    #been collected.
    #This is done here so that one master data list of clicks can be kept, and written
    #to a data file later (a bit messy, but it works - sorry)
    post_sound_clicks = []
    #While the participant has made fewer clicks than needed for the trial, keep
    #collecting clicks
    while len(post_sound_clicks) < needed:
        #listen to the event cue
        event_list = pygame.event.get()                                                #Specifically wait for either an a or an l to be pressed
        for event in event_list:
            #if an event is a mouse click, check the time
            if event.type == pygame.MOUSEBUTTONDOWN:
                post_sound_click = pygame.time.get_ticks()
                #Collect all the relevant data for the data lists
                post_sound_clicks.append(post_sound_click)
                clicks.append(post_sound_click)
                click_trial.append(trial_number)
                pre_post.append("post")

#Function to play a sound and collect clicks througout. This involves threading
#a mouse click listening function with a sound playing function.
def play_sound(num_times, trial_number):
    current_number = 0
    #While the number of trials where a sound has been played is fewer than the
    #desired number, listen for clicks and then play the sound.
    while current_number < num_times:
        #start the data collection thread
        mouse_thread(trial_number)
        #initialize pygame's sound mixer (necessary)
        pygame.mixer.init()
        #tell pygame what the sound file is that needs to be played
        sound = pygame.mixer.Sound('beep.wav')
        #check the clock for when the sound is about to be played
        play_time = pygame.time.get_ticks()
        #play the sound
        sound.play()
        #wait a specified amount of time
        pygame.time.wait(500)
        current_number += 1
        #quit the mixer (note, not doing this will result in greater variation in
        #times between sound beeps so just do it)
        pygame.mixer.quit()
        #Log the necessary data to the data lists
        play_times.append(play_time)
        sound_trial.append(trial_number)

#Function to run a trial
def trial(number_of_sounds, number_of_no_sound_clicks, trial_number):
    #Fill the screen black so the participant isn't just looking at a desktop
    screen.fill(BLACK)
    #Refresh the screen so it actually shows the black screen (necessary)
    pygame.display.flip()
    #Execute the function to collect clicks while a sound plays
    play_sound(number_of_sounds, trial_number)
    #Execute the function to collect clicks after the sound stops playing
    collect_no_sound(number_of_no_sound_clicks, trial_number)

#Function to show text to the screen and let participants choose when to start again    
def give_break():
    break_done = False
    while break_done == False:
        #Show text to the screen
        blit_text("You're doing great!", 13)
        blit_text("Take a moment and rest", 15)
        blit_text("Then press the A key when you're ready to continue", 16.25)
        pygame.display.update()
        #Listen for a key press to move on
        key_press = get_keypress()
        if key_press == 'a':
           break_done = True
        else:
            break_done = True

#Write data file. This uses the xlwt and xutils module
def write_data_file():
    #Make a workbook
    book = xlwt.Workbook()
    
    #Make sheet one show the sound times and sheet 2 show the tapping times
    sheet1 = book.add_sheet("SoundTimes")
    sheet2 = book.add_sheet("TappingTimes")
    
    
    sheet1.write(0,0, "Trial")
    sheet1.write(0,1, "SoundTime")
    sheet2.write(0,0, "Trial")
    sheet2.write(0,1, "ClickTime")
    sheet2.write(0,2, "Pre/post")
    

    #Go through the data lists and write them to each line of the data file
    
    #Start with the beep times on sheet 1
    line_counter = 1
    for i in sound_trial:
        sheet1.write(line_counter, 0, i)
        sheet1.write(line_counter, 1, i)
        line_counter=line_counter+1
    
    #Then write the participant click data on sheet 2
    line_counter = 1
    for i in click_trial:
        sheet2.write(line_counter, 0, i)
        sheet2.write(line_counter, 1, i)
        sheet2.write(line_counter, 2, i)
        line_counter=line_counter+1
  
    #Save the data file - NOTE YOU WILL NEED TO CHANGE THE NAME OF THE FILE BETWEEN
    #PARTICIPANTS OR IT WILL WRITE OVER THE PREVIOUS PARTICIPANT'S DATA FILE!!!
    book.save("TappingExperimentData.xls")
  
###############################
########## MAIN ###############
###############################
#Initiate the data lists. This will be used to collect data throughout the experiment
#and ultimately write the data file
sound_trial = []
play_times = []
click_trial = []
pre_post = []
clicks = []


#Show the introduction text. Wait for a key press indicating that the participant
#is ready to start
intro_done = False
while intro_done == False:
    blit_text("Welcome to our lab!", 13)
    blit_text("In a moment you will hear a beep", 15)
    blit_text("That sound will repeate - tap the keypad in time with it", 16.25)
    blit_text("When the sound stops, keep tapping in that time", 17.50)
    blit_text("- we'll tell you when to stop.", 18.75)
    blit_text("Press any key to continue", 20)

    pygame.display.update()
   
    key_press = get_keypress()
    if key_press == 'a':
        intro_done = True
    else:
        intro_done = True

#Run the short trials.
short_trial_counter = 0  #This value will change how many short trials you want!
while short_trial_counter < 10: #Right now it's set to 3 trials!
    trial(10, 50, short_trial_counter)
    give_break()
    short_trial_counter += 1


write_data_file()

