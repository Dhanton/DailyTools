#!/bin/bash

is_charging=$(acpi | grep Charging)

# Add different prefix to log file depending if charging or not
if [[ $is_charging = "" ]]; then
	prefix=$'dis'
else
	prefix=$'char'
fi

log_date=$(date '+%d_%m_%Y-%H_%M')

# Write log file
upower -i /org/freedesktop/UPower/devices/battery_BAT1 > ~/.battery-logs/$prefix-$log_date
