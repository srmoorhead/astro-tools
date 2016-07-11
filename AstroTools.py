from __future__ import division

'''
Written specifically for determining the mean profile of events in the lightcurve of the Kepler DAV
@version 02/19/2016
'''

__author__ = "S. R. Moorhead"

# imports
from Curve import Curve
from DataPoint import DataPoint


'''
Reads in a light curve file of type:
        time flux
        time flux
        time flux
        ...

@param file_string is the file string of the light curve file (relative to the working directory)
@return a Curve object containing the data from the file

** Debugging tip:  Make sure there is no new line at the end of the file
'''
def lc_read_in(file_string):
    pt_list = []
    with open(file_string, 'r') as lcf:
        lc_list = lcf.read().splitlines()

        for line in lc_list:
            line_elements = line.split()
            point = DataPoint(float(line_elements[0]), float(line_elements[1]))
            pt_list.append(point)
    lc = Curve(pt_list)

    return lc

'''
Reads in a list of information on events of type:
        HEADER  HEADER  HEADER  HEADER
        starttime endtime peaktime weight
        starttime endtime peaktime weight
        starttime endtime peaktime weight
        ...

@param file_string is the file string of the event info file (relative to the working directory)
@return four lists:
    peaks = [peaktime, peaktime, peaktime, ...]
    starts = [starttime, starttime, starttime, ...]
    ends = [endtime, endtime, endtime, ...]
    weights = [weight, weight, weight, ...]
'''
def events_read_in(file_string):
    peaks = []
    starts = []
    ends = []
    weights = []
    with open(file_string, 'r') as evf:
        event_list = evf.read().splitlines()
        del event_list[0] # delete the header line

        for line in event_list:
            line_elements = line.split()
            peaks.append(float(line_elements[2]))
            starts.append(float(line_elements[0]))
            ends.append(float(line_elements[1]))
            weights.append(float(line_elements[3]))

    return peaks, starts, ends, weights

'''
Determines the longest event by time

@param pks is a list of the peak times of all events
@param sts is a list of the start times of all events
@param ens is a list of the end times of all events
@return half the duration of the longest event
'''
def longest_event(pks, sts, ens):
    max_t = -1
    for index, pk_val in enumerate(pks):
        if ens[index] - pk_val > max_t:
            max_t = ens[index] - pk_val
        if pk_val - sts[index] > max_t:
            max_t = pk_val - sts[index]
    return max_t

'''
Makes all events uniform length by altering the start and end times

@param pks is a list of the peak times of all events
@param sts is a list of the start times of all events
@param ens is a list of the end times of all events
@param half_t is the difference to set on either side of peak times
@return two lists:
    starts = [newstarttime, newstarttime, newstarttime, ...]
    ends = [newendtime, newendtime, newendtime, ...]
'''
def uniform_size(pks, sts, ens, half_t):
    for index, peak in enumerate(pks):
        sts[index] = peak - half_t
        ens[index] = peak + half_t
    return sts, ens

'''
Bins the points in each event by a dT (preferably the Kepler dT), and averages the bins across all events
This is the meat of the mean event profile calculation

@param lc is a Curve that holds the lightcurve with events
@param pks is a list of event peak times
@param sts is a list of event start times
@param ens is a list of event end times
@param wts is a list of weights for each event
@param w is a bool denoting whether or not there are weights
@param dT is the size of each bin in time (typically the Kepler dT)
@return a Curve object containing the mean profile of all the events
'''
def calculateMeanProfile(lc, pks, sts, ens, wts, w, dT):
    # this is the meat of the mean profile code
    # make sure everything is good before beginning:
    if type(lc) is not Curve:
        raise TypeError("Parameter lc must be of type Curve")
    if type(pks) is not list:
        raise TypeError("Parameter pks must be a list")
    if type(sts) is not list:
        raise TypeError("Parameter sts must be a list")
    if type(ens) is not list:
        raise TypeError("Parameter ens must be a list")
    if type(wts) is not list:
        raise TypeError("Parameter wts must be a list")
    if len(pks) != len(sts) != len(ens) != len(wts):
        raise IndexError("Parameters pks, sts, ens, and wts must all have the same dimensions")
    if type(w) is not bool:
        raise TypeError("Parameter w must be a Boolean")

    # okay, now that we're all settled and correctly typed/sized, begin the code:

    # stack all events on top of each other
    # bin the points by a dT
    # average each bin
    bins = []
    add = True
    print("Number of Events Processed (Total = " + str(len(pks) + 1) + "):")
    for index in range(len(pks)):
        time = sts[index]
        event = lc.subset(sts[index], ens[index])
        if w:
            weight = wts[index]
        else:
            weight = 1.0

        step = 0
        while (time + dT + 0.0000001) < ens[index]:
            # the additional small number is to ensure each bin has at least 1 point
            temp_curve = event.subset(time, time + dT + 0.0000001)
            if add:
                if w:
                    bins.append(temp_curve.avg_y() * weight)
                else:
                    bins.append(temp_curve.avg_y())
            else:
                if w:
                    bins[step] += temp_curve.avg_y() * weight
                else:
                    bins[step] += temp_curve.avg_y()
            step += 1
            time += dT
        add = False
        print(index + 1)

    # divide the weights out of each bin
    if w:
        weightSum = 0
        for wVal in wts:
            weightSum += wVal
        for i in range(len(bins)):
            bins[i] = bins[i] / weightSum

    # add each event's flux to a model event with the peak centered at zero
    result = Curve()
    time = 0.0 - (pks[0] - sts[0])
    for bin_val in bins:
        if w:
            result.add_point(DataPoint(time, bin_val)) # already divided out weights to get avg
        else:
            result.add_point(DataPoint(time, bin_val / len(pks))) # need to divide to compute avg
        time += dT


    return result
