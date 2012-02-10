# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 17:52:14 2012

@author: rafik
"""

# def of datatypes that can be used in the datastream

Bool = 1
Int = 2
Float = 3
Complex = 4

Array = 10
Matrix = 11
List = 12
Image = 13

#image datatypes
iBW
iGray
i4b
i8b
i16b
i32b


def createDataDescriptor(name, desc, dtype, embtype):
    return (name, desc, dtype, embtype)