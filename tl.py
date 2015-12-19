#!/usr/bin/python

from datetime import datetime
from datetime import timedelta
import subprocess
import time
import os

from wrappers import GPhoto
from wrappers import Identify
from wrappers import NetworkInfo


MIN_INTER_SHOT_DELAY_SECONDS = timedelta(seconds=60) # minimum is 50 seconds
MIN_BRIGHTNESS = 20000
MAX_BRIGHTNESS = 30000
IMAGE_DIRECTORY = "/home/pi/timelapse/"

CONFIGS = [(47, "1/1600", 4, 200),
		(46, "1/1250", 4, 200),
	   	(45, "1/1000", 4, 200),
	   	(44, "1/800", 4, 200),
	   	(43, "1/640", 4, 200),
	   	(42, "1/500", 4, 200),
	   	(41, "1/400", 4, 200),
	   	(40, "1/320", 4, 200),
	   	(39, "1/250", 4, 200),
	   	(38, "1/200", 4, 200),
	   	(37, "1/160", 4, 200),
	   	(36, "1/125", 4, 200),
	   	(35, "1/100", 4, 200),
	   	(34, "1/80", 4, 200),
	   	(33, "1/60", 4, 200),
	   	(32, "1/50", 4, 200),
	   	(31, "1/40", 4, 200),
	   	(30, "1/30", 4, 200),
	   	(29, "1/25", 4, 200),
	   	(28, "1/20", 4, 200),
	   	(27, "1/15", 4, 200),
	   	(26, "1/13", 4, 200),
	   	(25, "1/10", 4, 200),
	   	(24, "1/8", 4, 200),
	   	(23, "1/6", 4, 200),
	   	(22, "1/5", 4, 200),
	   	(21, "1/4", 4, 200),
	   	(20, "0.3", 4, 200),
	   	(19, "0.4", 4, 200),
	   	(18, "0.5", 4, 200),
	   	(17, "0.6", 4, 200),
	   	(16, "0.8", 4, 200),
	   	(15, "1", 4, 200),
	   	(14, "1.3", 4, 200),
	   	(13, "1.6", 4, 200),
	   	(12, "2", 4, 200),
	   	(11, "2.5", 4, 200),
	   	(10, "3.2", 4, 200),
	   	( 9, "4", 4, 200),
	   	( 8, "5", 4, 200),
	   	( 7, "6", 4, 200),
	   	( 6, "8", 4, 200),
	   	( 5, "10", 4, 200),
	   	( 4, "13", 4, 200),
	   	( 3, "15", 4, 200),
	   	( 2, "20", 4, 200),
	   	( 1, "25", 4, 200),
	   	( 0, "30", 4, 200),
	   	( 0, "30", 5, 250),
	   	( 0, "30", 6, 320),
	   	( 0, "30", 7, 400),
	   	( 0, "30", 9, 640),
	   	( 0, "30", 10, 800),
	   	( 0, "30", 11, 1000),
	   	( 0, "30", 12, 1250),
	   	( 0, "30", 13, 1600)]

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
    print "Timelapse with %s second interval" % str(MIN_INTER_SHOT_DELAY_SECONDS)
    if not os.path.exists(IMAGE_DIRECTORY):
        os.makedirs(IMAGE_DIRECTORY)
    camera = GPhoto(subprocess)
    idy = Identify(subprocess)
    netinfo = NetworkInfo(subprocess)

    current_config = 17
    shot = 0
    last_acquired = None
    last_started = None

    network_status = netinfo.network_status()

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
            brightness = float(idy.mean_brightness(filename))

            print "-> %s %s" % (filename, brightness)
            os.rename(filename,IMAGE_DIRECTORY+filename)
            last_acquired = datetime.now()

            if brightness < MIN_BRIGHTNESS and current_config < len(CONFIGS) - 1:
                current_config = current_config + 1
            elif brightness > MAX_BRIGHTNESS and current_config > 0:
                current_config = current_config - 1

            if last_started and last_acquired and last_acquired - last_started < MIN_INTER_SHOT_DELAY_SECONDS:
                print "Processing complete, sleeping for %s" % str(MIN_INTER_SHOT_DELAY_SECONDS - (last_acquired - last_started))

				time.sleep((MIN_INTER_SHOT_DELAY_SECONDS - (last_acquired - last_started)).seconds)
            shot = shot + 1
    except Exception,e:
        print "Error: %s" %(str(e))


if __name__ == "__main__":
    main()
