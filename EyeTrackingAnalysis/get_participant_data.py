#File Goal: This file will find meaningful fixations in eye-tracking data and pair
#them with typed answers.
#
#General Outline: It will iterate through a folder of participant data and
#perform all tasks for participants. It will look in each file, and find fixations
#that belong to each trial. Note that the trial order was randomized
#for each participant, so the order is not uniform. Participants also provided
#typed answers, which were stored in a separate file. This file will also iterate
#through those files and pair typed answers with fixations by trial.

import csv
import math
import os


#This file will mostly be called from another file, so it will be written as a
#main function.

def find_participant_data():
    
    
    #Define a participant class that can store all the relevant data for a given
    #participant. It will also hold functions that allow that data to be scrubbed from
    #the source files (both typed response files and the tracking data files).
    #It's attributes will include (in order) those files, the lines in the
    #tracking data file that denote the start and stop of each trial, the
    #specific stimulus (question) shown, the typed answer given, the participant's 
    #fixations, and the objects that were fixated upon (note, this final field
    #will be filled in by the "checklocations.py" file).
    
    class participant(object):
        def __init__(self, response_file, tracking_file):
    
            self.response_file = response_file
            self.tracking_file = tracking_file
            self.lines_to_start_at = []
            self.lines_to_stop_at = []
            self.questions = ["training.jpg"]
            self.answers = ["training.jpg"]
            self.fixations = []
            self.fixation_objects = []
            
        #Function to open the typed response file and tracking data file
        #Returns those files as variables.
        def open_files(self):
            self.response_data = csv.reader(open(self.response_file, "rU"))
            self.tracking_data = csv.reader(open(self.tracking_file, "rU"))
    
            return [self.response_data, self.tracking_data]
        
        #Function to open the response filesand attach the contents to the
        #object fields above.
        
        def response_data_qandas(self):
            participant.open_files()
            map(lambda line: self.questions.append(line[0]), self.response_data) 
            participant.open_files()
            map(lambda line: self.answers.append(line[1]), self.response_data) 
        
        
        #Function to scan every line in the tracking data file for "new trail" flags.
        #These flags include the word "image", and "end" + "notice", so if these
        #are found, then it will append that line to the "lines_to_start_at" or
        #"lines_to_end_at" lists.
        
        def find_useful_lines(self, tracking_data):
            #Open the tracking and response files
            participant.open_files()
            line_counter = 1
            
            #Consider every line in the tracking data
            for line in self.tracking_data:
                #Consider every item in that line
                for item in line:
                    #Start flags include the word "image", so only log those
                    if "image" in item:
                        self.lines_to_start_at.append(line_counter)
                    #End flags include "end" and "notice", so only log those
                    elif ("end" in item) and ("NOTICE" not in line):
                        self.lines_to_stop_at.append(line_counter)      
                line_counter = line_counter + 1
        
        
        #Function to find the fixations for each stimulus trial within the tracking
        #data.It will use pairs of the "lines_to_start_at" and "lines_to_stop_at" values
        #and look for fixation line numbers that show up between them. It will
        #temporarily keep track of the fixations locally, and then append them to
        #the participant's fixations. This is done so that each image's fixations
        #are seperated within the participant's fixations (it will make querrying
        #easier later on).
        
        def find_fixations_per_image(self, tracking_data):
            #Zip the start and stop lines to have line pairs that surround each stim
            zipped_start_and_stop = zip(self.lines_to_start_at, self.lines_to_stop_at)
         
            #For each of those pairs, open the files and enumerate the tracking data
            for pair in zipped_start_and_stop:
                participant.open_files() 
                enumerated_tracking_data = enumerate(self.tracking_data) 
                image_fixations = []
                #For every line in that data, look for a line that is between the
                #stim's start and stop lines, and has "EFIX" in the second slot.
                #If found, append it to the image's fixations
                for line in enumerated_tracking_data:
                    if (pair[0] < line[0] < pair[1]) and ("EFIX" in line[1]):
                        image_fixations.append(line[1])                    
                #Append a stimulus's fixations to the participant's fixations
                self.fixations.append(image_fixations)



    ##This is functionally the body of the script.##
    
    #First, find all files in the relevant directory that hold data.
    #Since each participant has two files, an object will be initiated for each
    #participant, but not each file. Both files will be considered though, and
    #one will be the "response _file", and the other the "tracking_file".
    #Participant objects will then be appended to a list of participant objects.
    
    participants = []
    
    #Find the relative path
    for file in os.listdir(os.path.dirname(__file__)):
        #Find files that end with ans.csv
        if file.endswith("ans.csv"):
            #Files that end in "ans.csv" are the answer files
            response_file = file
            #Files that end in "track.csv" are the tracking files
            tracking_file = file[:-7] + "track.csv"
            #Create participant object for those files, and append to participant
            #list.
            new_participant = participant(response_file, tracking_file)
            participants.append(new_participant)
        
        
    #Run each of the functions specified in the participant object class. This
    #will result in the organization of most necessary participant data,
    #and the raw files will no longer need to be opened.
    
    for participant in participants:
        participant.response_data_qandas()
        participant.find_useful_lines(participant.tracking_data)
        participant.find_fixations_per_image(participant.tracking_data)

    return participants

#Run the main loop if called as a module.
if __name__ == '__main__':
    find_participant_data()


    