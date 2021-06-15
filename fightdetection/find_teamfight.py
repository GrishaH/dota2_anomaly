import json
import os
import math
import csv
# import datetime

base_dir = '7_27'
HERO = [None]*10  # var 0 = HERO0, and the value is their UID
HEROID = {}  # UID : Hero name dict.
HERODEATHS = {}  # UID : Hero death times
HERODEATHSCOUNT = {}
HERODEATHStemp = 0
participantCount = {}
deathCount = [False]*10
downTime = 15  # How many seconds of no damage being dealt is required to count it as a finished fight
desiredCount = 3  # How many heroes have to be on each side in a fight for it to count as a "team" fight
tempCountRadiant = 0  # How many are currently involved in a local exchange
tempCountDire = 0
tempHeroList = []
startFrame = 0  # Starting time of the fight
recentFrame = 0  # Most recent time of the fight
teamFights = {}  # Final output of teamfight times start:end
trigger = False  # teamfight trigger
fightAreaStart = 2000  # Units of area to keep track of, start = must be in this range for it to count as a fight
fightAreaContinue = 3500  # continue = how close to original point it must be to continue as a fight blink dagger = 1200
tfXPOS = None  # coords of the fight's start
tfYPOS = None


def findHEROIDs(frames, HEROID):
    # Get all heroes IDs, names, and UIDs.
    for i in range(0, 10):
        for frame in frames:
            for entity in frame["Entities"]:
                if frame["Entities"][entity]["ID"] == "HERO" + str(i) and HERO[i] is None:
                    # print(frame["Entities"][entity])
                    # HEROID[i] = [frame["Entities"][entity]["UID"],
                    #           frame["Entities"][entity]["NAME"]]
                    HEROID[frame["Entities"][entity]["UID"]] = frame["Entities"][entity]["NAME"]
                    HERO[i] = frame["Entities"][entity]["UID"]
                    

def heroesInRange(val, XPOS, YPOS, desiredCount):
    # at least 3v3 heroes in range of the attacker
    direRange = 0
    radiantRange = 0
    for char in HERO:
        try:
            tempX = val["Entities"]["0"+str(char)]["XPOS"]
            tempY = val["Entities"]["0"+str(char)]["YPOS"]
            if math.hypot(XPOS - tempX, YPOS - tempY) <= fightAreaStart:
                #  if HERO.index(val["Entities"]["0"+str(char)]["UID"]) <= 4:
                if int(val["Entities"]["0"+str(char)]["ID"][4:]) <= 4:
                    radiantRange += 1
                else:
                    direRange += 1
        except KeyError:
            #  print("No pos found for hero, skipping...")
            pass

    if radiantRange >= desiredCount and direRange >= desiredCount:
        return True
    else:
        return False

    
file_list = []
for file in os.listdir(base_dir):
    with open(os.path.join(base_dir, file)) as json_file: 
        data = json.load(json_file)
        findHEROIDs(data["frames"], HEROID)
        for ind, val in enumerate(data["frames"]):  # Go through each individual frame/second
            # reset progress if fight didn't update in given time
            if (tempHeroList and (val["Entities"]["0000000000"]["CLOCK_TIME"]
                                  - recentFrame >= downTime)):
                if trigger:
                    # teamFights[str(datetime.timedelta(seconds=round(startFrame)))] =
                    # str(datetime.timedelta(seconds=round(recentFrame)))
                    teamFights[startFrame] = recentFrame
                    trigger = False
                    HERODEATHSCOUNT[startFrame] = HERODEATHStemp
                    participantCount[startFrame] = len(tempHeroList)
                    #  print("TEAMFIGHT ORIGINALLY STARTED AT TIME: " + str(startFrame))
                    #  print("TEAMFIGHT WENT UP TO TIME: " + str(recentFrame))
                    #  print("TEAMFIGHT END, TIME: " + str(val["Entities"]["0000000000"]["CLOCK_TIME"]))
                    #  print("TEAMFIGHT STARTED IN POSITION X: " + str(tfXPOS) + " AND Y: " + str(tfYPOS))
                HERODEATHStemp = 0
                tempCountRadiant = 0
                tempCountDire = 0
                startFrame = 0
                tempHeroList = []
                tfXPOS = None
                tfYPOS = None
            if val["Entities"]:
                # deathCount = [x - 1 for x in deathCount if x > 0]
                for entity in val["Entities"]:
                    if val["Entities"][entity]["ENTITY_TYPE"] == "HeroEntity":
                        if "ALIVE" in val["Entities"][entity] and val["Entities"][entity]["ALIVE"] is False:
                            if ("RESPAWN_SECONDS" in val["Entities"][entity] and
                                    val["Entities"][entity]["RESPAWN_SECONDS"] > 0 and
                                    deathCount[HERO.index(val["Entities"][entity]["UID"])] is False):
                                # start of game count as 'dead' but respawner timers of -1 and 0.
                                if val["Entities"][entity]["UID"] in HERODEATHS:
                                    HERODEATHS[val["Entities"][entity]["UID"]].append(
                                        val["Entities"]["0000000000"]["CLOCK_TIME"])
                                else:
                                    HERODEATHS[val["Entities"][entity]["UID"]] = \
                                        [val["Entities"]["0000000000"]["CLOCK_TIME"]]
                                deathCount[HERO.index(val["Entities"][entity]["UID"])] = True
                                # int(val["Entities"][entity]["RESPAWN_SECONDS"])
                                if trigger:
                                    HERODEATHStemp += 1  # TEMP
                        else:
                            deathCount[HERO.index(val["Entities"][entity]["UID"])] = False
                    
            if val["Events"]:
                for event in val["Events"]:
                                    
                    if val["Events"][event]["EventType"] == "DamageDealtEvent":
                        #  print("ON FRAME: " + str(ind))
                        #  print("HERO: " + HEROID[val["Events"][event]["Source"]] +
                        #      " Attacked HERO: " + HEROID[val["Events"][event]["Target"]] +
                        #      " with: " + val["Events"][event]["DamageType"] +
                        #      " at time: " + str(val["Events"][event]["TimeInPhase"]))

                        if startFrame == 0:
                            try:
                                tfXPOS = val["Entities"]["0"+str(val["Events"][event]["Source"])]["XPOS"]
                                tfYPOS = val["Entities"]["0"+str(val["Events"][event]["Source"])]["YPOS"]
                            except KeyError:
                                # print("XPOS / YPOS not updated, ignoring...")
                                break # Go to next frame
                            if heroesInRange(val, tfXPOS, tfYPOS, desiredCount):
                                for participant in ("Source", "Target"):
                                    if val["Events"][event][participant] not in tempHeroList:
                                        tempHeroList.append(val["Events"][event][participant])
                                        if HERO.index(val["Events"][event][participant]) <= 4:
                                            tempCountRadiant += 1
                                        else:
                                            tempCountDire += 1
                                startFrame = val["Entities"]["0000000000"]["CLOCK_TIME"]
                                recentFrame = val["Entities"]["0000000000"]["CLOCK_TIME"]
                        else:
                            try:
                                tempXPOS = val["Entities"]["0"+str(val["Events"][event]["Source"])]["XPOS"]
                                tempYPOS = val["Entities"]["0"+str(val["Events"][event]["Source"])]["YPOS"]
                                if math.hypot(tfXPOS - tempXPOS, tfYPOS - tempYPOS) <= fightAreaContinue:
                                    recentFrame = val["Entities"]["0000000000"]["CLOCK_TIME"]
                                    for participant in ("Source", "Target"):
                                        if val["Events"][event][participant] not in tempHeroList:
                                            tempHeroList.append(val["Events"][event][participant])
                                            if HERO.index(val["Events"][event][participant]) <= 4:
                                                tempCountRadiant += 1
                                            else:
                                                tempCountDire += 1
                            except KeyError:
                                #  print("XPOS / YPOS not updated, ignoring...")
                                pass

                            if tempCountRadiant >= desiredCount and tempCountDire >= desiredCount:
                                # print("TEAMFIGHT TRIGGERED, TIME: " + str(recentFrame))
                                trigger = True
                                
    if trigger:
        teamFights[startFrame] = recentFrame
        #  teamFights[str(datetime.timedelta(seconds=round(startFrame)))] =
        #  str(datetime.timedelta(seconds=round(recentFrame)))
        HERODEATHSCOUNT[startFrame] = HERODEATHStemp
        participantCount[startFrame] = len(tempHeroList)
    trigger = False
    HERODEATHStemp = 0
    tempCountRadiant = 0
    tempCountDire = 0
    startFrame = 0
    tempHeroList = []
    tfXPOS = None
    tfYPOS = None

    #  print(teamFights)
    #  print("A total of " + str(len(teamFights)) + " teamfights.")
    print("Finished match ID: " + file)
    with open("7_27_test_data.csv", mode='a') as csv_file:
        #  fieldnames = ["matchID","fightStart","fightEnd"]
        writer = csv.writer(csv_file)  # fieldnames=fieldnames
        # writer.writeheader()
        for key, value in teamFights.items():
            writer.writerow([file[:-5], key, value, value-key, HERODEATHSCOUNT[key], participantCount[key]])
    # TODO - this is lazy, just find a way to continue without clearing each time?
    HERO = [None]*10
    HEROID = {}
    HERODEATHS = {}
    teamFights = {}
    

