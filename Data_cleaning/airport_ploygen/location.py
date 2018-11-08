#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Introductions
Mainly used to detect if a point is in a ploygon/multiploygon
CLass Ploygon Sample Code:
>>>runway = Ploygon()
>>>runway.readOSM('./runway.osm')
>>>coordinate = [latitude, longtitude]
>>>runway.is_in(coordinate)
True/False

Class Location Sample Code:
>>>loc = Location(apron, runway, aerodrome)
>>>loc.loc_array(coordinate)
[0,1,0]/[0,0,0]
'''

import xml.etree.ElementTree as ET
import matplotlib.path as mplpath

class Ploygon(object):
    def __init__(self):
        self.ploygons = {}

    def is_valid(self):
        num_nodes = len(self.tree.findall('node'))
        num_ways = len(self.tree.findall('way'))
        if num_nodes and num_ways:
            return True
        else:
            return False

    def getallnodes(self):
        nodespool = {}
        try:
            for node in self.tree.iter('node'):
                id = node.attrib['id']
                lat = float(node.attrib['lat'])
                lon = float(node.attrib['lon'])
                nodespool[id] = [lat, lon]
        except NameError as e:
            print('[!] Should run readOSM() first.')
            raise
        return nodespool

    def extract_ploygons(self):
        nodespool = self.getallnodes()
        for way in self.tree.iter('way'):
            elements = way.findall('nd')
            nodes = []
            for element in elements:
                try:
                    nodes.append(nodespool[element.attrib['ref']])
                except KeyError as e:
                    print('[!] Failed to find the node information: node_id=%s, way_id=%s' % (
                    element.attrib['ref'], way.attrib['id']))
            self.ploygons[way.attrib['id']] = nodes

    def readOSM(self, path):
        self.tree = ET.ElementTree(file=path)
        if self.is_valid():
            self.extract_ploygons()
        else:
            print('[!] Failed to find valid nodes or ways.')
            raise ValueError

    def is_in(self, coordinate):
        if not isinstance(coordinate, (list, tuple)):
            print('[!] Failed to parse the coordinate. Coordinate should be a list or tuple.')
            raise TypeError
        for id, vertexs in self.ploygons.items():
            ploygon = mplpath.Path(vertexs)
            if ploygon.contains_point(coordinate):
                # print('[*] The point is within the closedway:%s' % id)
                return True
        return False

class Location(object):
    def __init__(self, *ploygons):
        if len(ploygons) <=1:
            print('[!] At least two ploygons are expected.')
            raise ValueError
        for ploygon in ploygons:
            if not isinstance(ploygon, Ploygon):
                print('[!] Ploygon is expected.')
                raise ValueError
        self.ploygons = ploygons
        self.is_covered()

    def is_covered(self):
        cover = self.ploygons[-1]
        for i in range(len(self.ploygons)-1):
            allnodes = self.ploygons[i].getallnodes()
            for id, coordinate in allnodes.items():
                if not cover.is_in(coordinate):
                    print('[!] The No.%s ploygon/multiploygon has a node that is not covered by the last ploygon/multiploygon: '
                          'Node id=%s' % (i+1, id))
                    raise ValueError
        return True

    def loc_array(self, coordinate):
        if not isinstance(coordinate, (list, tuple)):
            print('[!] Failed to parse the coordinate. Coordinate should be a list or tuple.')
            raise TypeError
        if len(coordinate) != 2:
            print('[!] Coordinate should have 2 arguments: latitude and longitude.')
            raise ValueError
        res = [0,] * len(self.ploygons)
        for i in range(len(self.ploygons)):
            if self.ploygons[i].is_in(coordinate):
                res[i] = 1
                return res
        return res
