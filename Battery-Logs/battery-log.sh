#!/bin/bash

log_date=$(date '+%d_%m_%Y-%H_%M')

upower -i /org/freedesktop/UPower/devices/battery_BAT1 > ~/.battery-logs/$log_date
