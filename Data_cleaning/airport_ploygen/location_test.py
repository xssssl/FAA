#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from location import Ploygon
from location import Location

class TestPloygon(unittest.TestCase):
    def setUp(self):
        self.apron = Ploygon()
        self.apron.readOSM('./data/Apron.osm')
        self.runway = Ploygon()
        self.runway.readOSM('./data/Runway_ploygons.osm')
        self.aerodrome = Ploygon()
        self.aerodrome.readOSM('./data/Aerodrome.osm')

    def test_is_in(self):
        # apron
        self.assertTrue(self.apron.is_in([33.9472, -118.4033]))
        self.assertTrue(self.apron.is_in([33.93965, -118.40654]))
        self.assertFalse(self.apron.is_in([33.9354, -118.4093]))
        self.assertFalse(self.apron.is_in([33.9357, -118.4109]))
        # runway
        self.assertTrue(self.runway.is_in([33.950754, -118.415205]))         # 06L/24R
        self.assertTrue(self.runway.is_in([33.947934, -118.423889]))         # 06R/24L
        self.assertTrue(self.runway.is_in([33.937190, -118.406135]))         # 07L/25R
        self.assertTrue(self.runway.is_in([33.936926, -118.387134]))         # 07R/25L
        # aerodrome
        self.assertTrue(self.aerodrome.is_in([33.9338, -118.4221]))
        self.assertTrue(self.aerodrome.is_in([33.935, -118.3827]))
        self.assertFalse(self.aerodrome.is_in([33.9482, -118.3837]))
        self.assertFalse(self.aerodrome.is_in([33.9326, -118.4315]))

class TestLocation(unittest.TestCase):
    def setUp(self):
        self.apron = Ploygon()
        self.apron.readOSM('./data/Apron.osm')
        self.runway = Ploygon()
        self.runway.readOSM('./data/Runway_ploygons.osm')
        self.aerodrome = Ploygon()
        self.aerodrome.readOSM('./data/Aerodrome.osm')

    def test_is_covered(self):
        with self.assertRaises(ValueError):
            Location(self.apron, self.runway)
        with self.assertRaises(ValueError):
            Location(self.apron, self.aerodrome, self.runway)

    def test_loc_array(self):
        sampleloc = Location(self.apron, self.runway, self.aerodrome)
        self.assertEqual(sampleloc.loc_array([33.93965, -118.40654]), [1, 0, 0])
        self.assertEqual(sampleloc.loc_array([33.937190, -118.406135]), [0, 1, 0])
        self.assertEqual(sampleloc.loc_array([33.9338, -118.4221]), [0, 0, 1])
        self.assertEqual(sampleloc.loc_array([33.9326, -118.4315]), [0, 0, 0])


if __name__ == '__main__':
    unittest.main()

'''
from location import Ploygon
from location import Location
apron = Ploygon()
apron.readOSM('./data/Apron.osm')
runway = Ploygon()
runway.readOSM('./data/Runway_ploygons.osm')
aerodrome = Ploygon()
aerodrome.readOSM('./data/Aerodrome.osm')
sampleloc = Location(apron, runway, aerodrome)
'''