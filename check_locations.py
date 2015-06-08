#File Goal: This file will look at all the participant data and reorganize it by
#image. It will then output a compiled data file, that can be read, coded, and then
#used for statistical analysis.

#General Outline: It will create an object for every trial of interest (some were
#simply fillers), and then collect the data from each participant for each of those
#trials. It will also determine which stimulus object was looked at first when
#the trial began. First fixation is one variable needed for analysis later.

import csv
import math
import os
import xlwt
import get_participant_data


#Define a image class that will hold all the data for each key stimulus. This will
#be the data that used for analysis, so it will include (in order) the stimulus name,
#each participant number, each participant's typed answers, and the item
#of interest fixated on first.

class image_stimulus(object):
    def __init__(self, image):
        self.image = image
        self.participant_numbers = []
        self.answers = []
        self.first_look = []
        
    #Function to collect every participant's data for the given stimulus.
    
    def organize_data(self):
        #Extract participant data from participant objects. This includes
        #the response file.
        for participant in participants:
            self.participant_numbers.append(participant.response_file)
            #If a question has an image code, then append that question and it's
            #first look as well.
            #Note, this is important because the images and participant data
            #are not in the same order.
            for idx, question in enumerate(participant.questions):
                if question[:-4] == self.image:
                    self.answers.append(participant.answers[idx])
                    self.first_look.append(participant.fixation_objects[0])
                    del participant.fixation_objects[0]

#Function to determine which object was looked first. Note, not all objects in
#each stimulus are of interest -- only the "actor" and "patient" are. This
#function will take each fixation in order and compare its x/y coordinates to the
#coordinates of those objects. If a fixation falls within them, then no more
#fixations will be considered. If not, it will consider the next fixation,
#until it finds a match. This data will be stored with the participant's other
#data (in the participant object)

def evaluate_fixations(image, participant_fixation, idx):
    
    #Declare variables for the subsequent comparison.
    #These are the x/y coordinates for the actor/patient in the image codes
    #They return as strings, and so must be cast as floats.
    actor_xmin = float(image[1])
    actor_xmax = float(image[2])
    actor_ymin = float(image[3])
    actor_ymax = float(image[4])
    patient_xmin = float(image[5])
    patient_xmax = float(image[6])
    patient_ymin = float(image[7])
    patient_ymax = float(image[8])
    
    
    #Look through an image's fixations for the first item that is the actor or patient
    fixation_counter = 0
    found_fixation = False
    
    while found_fixation == False:
        fixation_x = float(participant.fixations[idx][fixation_counter][5])
        fixation_y = float(participant.fixations[idx][fixation_counter][6])

        #If the fixation x location is beteween the image code's actor min and max x
        #coordinates, and the fixation's y location is between the code's min
        #max y coordinates, append "actor".
        if ((actor_xmin < fixation_x < actor_xmax) and (actor_ymin < fixation_y < actor_ymax)):
            participant.fixation_objects.append("actor")
            found_fixation = True
            
        #If the fixation x location is beteween the image code's patient's min and max x
        #coordinates, and the fixation's y location is between the code's min
        #max y coordinates, append "patient".
        elif ((patient_xmin < fixation_x < patient_xmax) and (patient_ymin < fixation_y < patient_ymax)):
            participant.fixation_objects.append("patient")
            found_fixation = True
        
        #Keep looping, as long as there are more fixations to check. If not, stop
        #and append "neither"
        else:
            if fixation_counter < len(participant.fixations[idx])-1:
                fixation_counter += 1
            else:
                participant.fixation_objects.append("neither")
                found_fixation = True

#Function that finds key trials, then runs the "evaluate fixations" function,
#for those trials only. 

def find_fixation(fixation_number, image_codes):
    #Consider every participant. Eenumerate participant.qusetions so we can
    #know where in other lists we need to look for corresponding data.
    for idx, question in enumerate(participant.questions):
        #Consider every image_code, but look for the one that matches the current
        #stimulus of interst.
        for image in image_codes:
            if question[:-4] == image[0]:                                       
                evaluate_fixations(image, participant.fixations, idx)           

                
##This is the main body of the script##

#Run the "get_participants_data" script to scrub the fixations out of the
#source files, and organize that data by participant.
participants = get_participant_data.find_participant_data()

#Open the "image coding.csv" file, which holds the names of the stimuli of
#interest. This involves a deep copy because each line must be it's own list
#for easier iteration later. So, "Image codes" will be image names plus
#their specified locations.
raw_image_codes = csv.reader(open('image coding.csv', "rU"))
image_codes = map(lambda image: image, raw_image_codes)                    


#First, find the first fixations for key trials for every participant.
[find_fixation(0, image_codes) for participant in participants]


#Then, create an image_stimulus object for each stimulus listed in the "image coding"
#file.
image_stimuli = [image_stimulus(image_code[0]) for image_code in image_codes]


#Then, organize participant data by stimulus for every key stimulus.
[image.organize_data() for image in image_stimuli]

#Data, organized by image, then participant, will then be written to an Excel
#file for further analysis. This Excel file will be called "FirstLooks.xls",
#and the sheet within it will be called "Master".
data_file = xlwt.Workbook()
sheet = data_file.add_sheet("Master")

#Go through all image_stimulus objects and write the object attributes to the Excel file,
#organized by stimulus.
row_counter=0
for image in image_stimuli:
    for row, participant in enumerate(image.participant_numbers):
        sheet.write(row+row_counter, 0, image.image)
        sheet.write(row+row_counter, 1, image.participant_numbers[row])
        sheet.write(row+row_counter, 2, image.answers[row])
        sheet.write(row+row_counter, 4, image.first_look[row])
    row_counter += len(image.participant_numbers)    
        
#Save the data file.
data_file.save("FirstLooksCopy.xls")
