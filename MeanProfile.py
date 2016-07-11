'''
A class used to call the supporting methods to create a mean profile of a series of events in a light curve
This requires the following files:
    DataPoint.py
    Curve.py
    AstroTools.py
    MeanProfile.py (this file)

@version 02/19/2016

Contact:  sean.moorhead@utexas.edu or smoo93@gmail.com
'''
__author__ = "S. R. Moorhead"

# imports
import AstroTools as AT

# global variables
'''
The below variables assume all time values are in the same units.
Weights MUST be provided, even if they are all the same value, even if they won't be used.

LIGHTCURVE_FILE_STRING should point to a file of type:
    time flux
    time flux
    time flux
    time flux
    ...

EVENTS_FILE_STRING should point to a file of type:
    HEADER  HEADER  HEADER  HEADER
    starttime endtime peaktime weight
    starttime endtime peaktime weight
    starttime endtime peaktime weight
    ...

W is a boolean denoting whether or not to use weights when determining the mean profile

dT is a float denoting the time difference between frames of the observing instrument
    In the case of Kepler, dT = 58.84876 seconds

OUT_FILE_STRING will write the resultant mean profile to a file, with type:
    time flux
    time flux
    time flux
    ...

'''
LIGHTCURVE_FILE_STRING = "lightcurve.dat"
EVENTS_FILE_STRING = "events.dat"
OUT_FILE_STRING = "sampleResult.dat"
W = True
dT = 58.84876



def meanProfile():
    # read in the lightcurve file
    lc = AT.lc_read_in(LIGHTCURVE_FILE_STRING)
    print("Light curve read.")

    # read in the event parameters
    peaks, starts, ends, weights = AT.events_read_in(EVENTS_FILE_STRING)
    print("Events file read.")

    # alter the event parameters so that each event is the same length
    starts, ends = AT.uniform_size(peaks, starts, ends, AT.longest_event(peaks, starts, ends))

    # do the dirty work
    result = AT.calculateMeanProfile(lc, peaks, starts, ends, weights, W, dT)
    print("Mean profile calculated.")

    # write the resultant light curve to a file for safe keeping
    result.toFile(OUT_FILE_STRING)
    print("Results written to: " + OUT_FILE_STRING)
    print("Mean Profile Complete")

meanProfile()

