from __future__ import division
'''
A class holding a set of points, which can then be manipulated in various ways.
The points are stored such that they remain sorted by x value.
@version 02/19/2016
'''
__author__ = "S. R. Moorhead"

#imports
from DataPoint import DataPoint
import bisect

class Curve(object):

    '''
    To instantiate a Curve object, you must pass either a single DataPoint object or a list of DataPoint objects.
    @throws TypeError if an array contains a non-DataPoint object
    @throws TypeError if data is not a DataPoint or list
    '''
    def __init__(self, data = None):
        if data is None:
            self.point_list = []
        elif type(data) is list:

            # check that every element is a DataPoint
            for index, point in enumerate(data):

                # if check fails
                if type(point) is not DataPoint:
                    raise TypeError("All of the elements in data must be DataPoint objects for a "
                                    "Curve to be correctly built.\nIndex " + str(index) + " is not a DataPoint"
                                                                                               " object.")
            # if check is successful
            self.point_list = data
        elif type(data) is DataPoint:
            self.point_list = [data]
        else:
            raise TypeError("You can only build a Curve out of DataPoint objects.")


    def __sizeof__(self):
        return len(self.point_list)

    def __str__(self):
        string = ""
        for point in self.point_list:
            string += DataPoint.clean_str(point) + "\n"
        return string

    # points are added using the bisect method to maintain the sorted list
    def add_point(self, point):
        if type(point) is DataPoint:
            i = bisect.bisect_left(self.get_x_list(), point.get_x())
            self.point_list.insert(i, point)

    def add_set(self, list_of_points):
        if type(list_of_points) is list:
            for point in list_of_points:
                if type(point) is not DataPoint:
                    raise TypeError("You can only add DataPoint objects to the Curve!")
        self.point_list += list_of_points
        self.point_list.sort(key = lambda datapt: datapt.get_x())

    def __repr__(self):
        return "Curve:  Size = %s, Start = %s, End = %s" % (len(self.point_list), str(self.point_list[0]),
                                                      str(self.point_list[-1]))

    def get_x_list(self):
        output = []
        for point in self.point_list:
            output.append(point.get_x())
        return output

    def get_y_list(self):
        output = []
        for point in self.point_list:
            output.append(point.get_y())
        return output

    def get_z_list(self):
        output = []
        for point in self.point_list:
            output.append(point.get_z())
        return output

    # returns a Curve object including all DataPoints between xStart and xEnd
    def subset(self, xStart, xEnd):
        stI = 0
        while self.point_list[stI].get_x() < xStart:
            stI += 1

        enI = stI
        while self.point_list[enI].get_x() < xEnd:
            enI += 1

        return Curve(self.point_list[stI : enI + 1])

    # combine two Curve objects, maintaining all points
    def combine(self, other):
        self.point_list += other.point_list
        self.point_list.sort(key = lambda datapt: datapt.get_x())

    def __getitem__(self, index):
        return self.point_list[index]

    def avg_y(self):
        sum = 0.0
        count = 0.0
        for point in self.point_list:
            sum += point.y
            count += 1
        return sum / count

    def avg_x(self):
        sum = 0.0
        count = 0.0
        for point in self.point_list:
            sum += point.x
            count += 1
        return sum / count

    def avg_z(self):
        sum = 0.0
        count = 0.0
        for point in self.point_list:
            sum += point.z
            count += 1
        return sum / count

    def toFile(self, fileString):
        with open(fileString, 'w') as f:
            f.write(str(self))

    def deep_copy(self):
        return Curve(self.point_list)
