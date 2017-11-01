#!/bin/bash
xrandr --newmode "1600x900_60.00"  118.25  1600 1696 1856 2112  900 903 908 934 -hsync +vsync
xrandr --addmode eDP-1 1600x900_60.00

xrandr --output DP-1 --off --output HDMI-1 --off --output eDP-1 --primary --mode 1600x900_60.00 --pos 0x0 --rotate normal --output HDMI-2 --off
