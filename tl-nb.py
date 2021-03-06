#!/usr/bin/python

# USAGE
# python tl.py aperture config interval


from datetime import datetime
from datetime import timedelta
import subprocess
import time
import os
import sys

from wrappers import GPhoto

SHOT_INTERVAL_SECONDS = timedelta(seconds=15) # minimum is 12 seconds
IMAGE_DIRECTORY = "/home/pi/timelapse/"

CONFIGS = [(47, "1/1600", 4, 200), # 0
		(46, "1/1250", 4, 200),    # 1
	   	(45, "1/1000", 4, 200),    # 2
	   	(44, "1/800", 4, 200),     # 3
	   	(43, "1/640", 4, 200),     # 4
	   	(42, "1/500", 4, 200),     # 5
	   	(41, "1/400", 4, 200),     # 6
	   	(40, "1/320", 4, 200),     # 7
	   	(39, "1/250", 4, 200),     # 8
	   	(38, "1/200", 4, 200),     # 9
	   	(37, "1/160", 4, 200),     # 10
	   	(36, "1/125", 4, 200),     # 11
	   	(35, "1/100", 4, 200),     # 12
	   	(34, "1/80", 4, 200),      # 13
	   	(33, "1/60", 4, 200),      # 14
	   	(32, "1/50", 4, 200),      # 15
	   	(31, "1/40", 4, 200),      # 16
	   	(30, "1/30", 4, 200),      # 17
	   	(29, "1/25", 4, 200),      # 18
	   	(28, "1/20", 4, 200),      # 19
	   	(27, "1/15", 4, 200),      # 20
	   	(26, "1/13", 4, 200),      # 21
	   	(25, "1/10", 4, 200),      # 22
	   	(24, "1/8", 4, 200),       # 23
	   	(23, "1/6", 4, 200),       # 24
	   	(22, "1/5", 4, 200),       # 25
	   	(21, "1/4", 4, 200),       # 26
	   	(20, "0.3", 4, 200),       # 27
	   	(19, "0.4", 4, 200),       # 28
	   	(18, "0.5", 4, 200),       # 29
	   	(17, "0.6", 4, 200),       # 30
	   	(16, "0.8", 4, 200),       # 31
	   	(15, "1", 4, 200),         # 32
	   	(14, "1.3", 4, 200),       # 33
	   	(13, "1.6", 4, 200),       # 34
	   	(12, "2", 4, 200),         # 35
	   	(11, "2.5", 4, 200),       # 36
	   	(10, "3.2", 4, 200),       # 37
	   	( 9, "4", 4, 200),         # 38
	   	( 8, "5", 4, 200),         # 39
	   	( 7, "6", 4, 200),         # 40
	   	( 6, "8", 4, 200),         # 41
	   	( 5, "10", 4, 200),        # 42
	   	( 4, "13", 4, 200),        # 43
	   	( 3, "15", 4, 200),        # 44
	   	( 2, "20", 4, 200),        # 45
	   	( 1, "25", 4, 200),        # 46
	   	( 0, "30", 4, 200),        # 47
	   	( 0, "30", 5, 250),        # 48
	   	( 0, "30", 6, 320),        # 49
	   	( 0, "30", 7, 400),        # 50
	   	( 0, "30", 9, 640),        # 51
	   	( 0, "30", 10, 800),       # 52
	   	( 0, "30", 11, 1000),      # 53
	   	( 0, "30", 12, 1250),      # 54
	   	( 0, "30", 13, 1600)]      # 55

def test_configs():
    camera = GPhoto(subprocess)

    for config in CONFIGS:
        print "Testing camera setting: Shutter: %s ISO %d" % (config[1], config[3])
        camera.set_shutter_speed(secs=config[1])
        camera.set_iso(iso=str(config[3]))
        time.sleep(1)

def main():
    # print "Testing Configs"
    # test_configs()
    if not os.path.exists(IMAGE_DIRECTORY):
        os.makedirs(IMAGE_DIRECTORY)
    camera = GPhoto(subprocess)
    # idy = Identify(subprocess)
    ana = Analysis(subprocess)

    # Pull Values from Command Line
    try:
      sys.argv[1]
    except NameError:
      aperture = 3
    else:
      aperture = int(sys.argv[1])

    try:
      sys.argv[2]
    except NameError:
      current_config = 20
    else:
      current_config = int(sys.argv[2])

    try:
      sys.argv[3]
    except NameError:
      shot_interval = SHOT_INTERVAL_SECONDS
    else:
      shot_interval = timedelta(seconds=int(sys.argv[3]))

    shot = 0
    last_acquired = None
    last_started = None

    print "Timelapse with %s second interval" % str((shot_interval).seconds)
    camera.set_aperture(index=aperture)

    try:
        while True:
            last_started = datetime.now()
            config = CONFIGS[current_config]
            print "Shot: %d Shutter: %s ISO: %d" % (shot, config[1], config[3])
            camera.set_shutter_speed(index=config[0])
            camera.set_iso(iso=str(config[3]))
            try:
              filename = camera.capture_image_and_download()
            except Exception, e:
              print "Error on capture." + str(e)
              print "Retrying..."
              # Occasionally, capture can fail but retries will be successful.
              continue

            os.rename(filename,IMAGE_DIRECTORY+filename)
            last_acquired = datetime.now()

            if last_started and last_acquired and last_acquired - last_started < shot_interval:
                print "Processing complete for %s, sleeping for %s" % str(filename, shot_interval - (last_acquired - last_started))

			time.sleep((shot_interval - (last_acquired - last_started)).seconds)
            shot = shot + 1
    except Exception,e:
        print "Error: %s" %(str(e))

if __name__ == "__main__":
    main()
