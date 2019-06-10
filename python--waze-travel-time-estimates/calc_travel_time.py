#!/usr/bin/env python
#
# Purpose: Given a configuration from a settings file, calculate the time between
#          two locations and output the result in the following format:
#
#   - Current Date/Time
#   - Source Town
#   - Destination Town
#   - Travel Time

import WazeRouteCalculator

from_address = 'Boston, Massachusetts'
to_address = 'Cleveland, Ohio'
region = 'US'
route = WazeRouteCalculator.WazeRouteCalculator(from_address, to_address, region)
route.calc_route_info()
