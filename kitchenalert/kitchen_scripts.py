# -*- coding: utf-8 -*-
# Scripted Kitchen Alert services, made with kitchenalert.py and frozen so that every
# playtest group can play the same service. Format, one event per line after the phase ends:
#   OR <time> T+<round> <N|L> <Red|Blue>   an order (N = regular, L = large)
#   5P ...                                   the same, but only with five players
#   ID <time>                                delivery (Space Alert: incoming data)
#   DT <time>                                handover (Space Alert: data transfer)
#   CD <from> - <to>                         rush hour, no talking (Space Alert: communications down)

firstService = """
3:30 - 7:15 - 9:45
OR 0:10 T+2 N Red
5P 0:25 T+3 N Blue
OR 0:45 T+4 L Blue
DT 1:25
ID 1:55
DT 2:10
OR 3:40 T+6 N Blue
OR 4:05 T+7 N Red
OR 4:30 T+8 N Blue
CD 5:00 - 5:10
ID 5:25
DT 5:40
CD 6:40 - 6:50
CD 7:25 - 7:40
DT 8:30
CD 8:55 - 9:05
"""

service1 = """
3:55 - 7:45 - 10:25
OR 0:10 T+1 N Red
CD 0:35 - 0:40
OR 0:55 T+2 N Blue
ID 1:10
OR 1:40 T+3 N Blue
DT 2:00
5P 2:15 T+4 N Red
OR 4:05 T+5 N Red
CD 4:40 - 4:45
OR 5:10 T+6 N Blue
DT 6:05
ID 6:25
OR 7:00 T+7 L Red
ID 7:15
CD 8:00 - 8:20
CD 9:00 - 9:20
DT 9:45
"""

service2 = """
3:55 - 7:40 - 10:15
OR 0:10 T+1 N Red
ID 0:30
OR 0:35 T+2 L Blue
5P 0:50 T+3 N Red
ID 1:15
CD 1:30 - 1:35
OR 4:05 T+5 N Red
DT 4:25
DT 4:40
OR 5:10 T+6 N Blue
OR 5:35 T+7 N Red
ID 5:55
OR 6:00 T+8 N Red
CD 7:05 - 7:15
CD 7:55 - 8:15
DT 8:50
CD 9:25 - 9:45
"""

service3 = """
4:00 - 7:50 - 10:20
OR 0:10 T+2 N Blue
5P 0:25 T+3 N Red
ID 1:10
OR 1:20 T+4 L Red
ID 1:35
CD 2:30 - 2:35
OR 4:10 T+5 N Red
OR 4:35 T+6 N Blue
OR 5:00 T+7 N Red
OR 5:25 T+8 N Blue
CD 6:05 - 6:10
DT 6:35
DT 7:15
CD 8:05 - 8:25
CD 8:55 - 9:15
DT 9:30
ID 9:55
"""

busyNight = """
3:45 - 7:30 - 10:00
OR 0:10 T+1 N Red
OR 0:50 T+2 L Red
5P 1:05 T+3 N Blue
OR 1:35 T+4 N Blue
CD 1:55 - 2:00
ID 2:35
ID 3:20
OR 3:55 T+5 L Red
ID 4:40
OR 5:20 T+6 N Red
CD 5:35 - 5:45
DT 6:10
OR 6:40 T+7 N Blue
DT 6:55
DT 7:40
CD 8:10 - 8:30
CD 8:40 - 8:55
"""

# (name, label) in menu order
SERVICES = [
    ('firstService', 'First service (easy)'),
    ('service1', 'Service 1'),
    ('service2', 'Service 2'),
    ('service3', 'Service 3'),
    ('busyNight', 'Busy night (hard)'),
]

scripts = {name: globals()[name] for name, label in SERVICES}
