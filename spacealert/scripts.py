mission1 = """
3:45 - 7:30 - 10:00
AL 0:10 T+2 ST White
UA 0:55 T+3 IT
AL 1:50 T+4 T Blue
ID 2:20
CD 2:50 - 3:00
DT 3:05
ID 3:55
AL 4:00 T+5 IT
DT 4:25
AL 4:50 T+6 T Blue
CD 5:20 - 5:35
AL 5:50 T+7 ST Red
DT 6:35
CD 7:50 - 8:10
DT 8:20
CD 9:15 - 9:25
"""

mission2 = """
4:00 - 07:45 - 10:20
UA 0:10 T+1 T Red
AL 0:35 T+2 IT
AL 1:30 T+3 T White
DT 2:00
AL 2:35 T+4 T Red
ID 3:10
ID 4:05
AL 4:15 T+5 T White
AL 4:50 T+6 SIT
CD 5:20 - 5:40
DT 5:45
AL 6:15 T+8 T Blue
ID 7:05
DT 8:00
CD 8:20 - 8:50
DT 9:25
"""

mission3 = """
3:50 - 7:30 - 10:00
AL 0:10 T+2 IT
ID 0:50
AL 1:15 T+3 T Blue
CD 1:50 - 2:00
AL 2:15 T+4 IT
DT 3:05
AL 4:00 T+6 ST White
CD 4:30 - 4:50
AL 4:55 T+7 ST White
DT 5:20
ID 5:40
UA 5:55 T+8 T Red
DT 6:50
CD 7:40 - 8:00
DT 8:05
CD 8:15 - 8:25
"""

mission4 = """
3:45 - 7:20 - 9:40
AL 0:10 T+1 T Red
UA 1:00 T+3 T White
ID 1:30
AL 1:55 T+4 ST Red
DT 2:25
DT 3:55
AL 4:10 T+5 SIT
ID 4:35
AL 5:00 T+6 ST Blue
CD 5:45 - 5:55
ID 6:25
CD 6:35 - 6:45
DT 7:35
CD 8:00 - 8:20
CD 8:55 - 9:10
"""

mission5 = """
3:50 - 7:30 - 10:00
CD 0:10 - 0:15
AL 0:20 T+2 ST Blue
ID 1:05
AL 1:30 T+3 SIT
DT 2:20
AL 2:55 T+4 T Red
CD 4:00 - 4:25
AL 4:30 T+6 T Red
UA 5:05 T+7 IT
AL 6:00 T+8 T White
DT 6:35
DT 6:50
ID 7:45
DT 8:00
CD 8:20 - 8:40
"""

mission6 = """
3:55 - 7:45 - 10:20
ID 0:10
AL 0:20 T+1 T Blue
AL 0:45 T+2 IT
AL 1:10 T+3 ST White
CD 1:30 - 1:40
ID 2:10
ID 3:00
AL 3:55 T+5 T Blue
DT 4:25
AL 4:45 T+6 IT
UA 5:20 T+7 T White
DT 6:05
AL 6:50 T+8 T Red
CD 8:00 - 8:30
CD 8:40 - 8:45
DT 9:40
"""

mission7 = """
3:40 - 7:30 - 10:00
UA 0:10 T+1 T Blue
AL 0:35 T+3 ST Red
ID 1:10
AL 1:45 T+4 SIT
DT 2:15
CD 2:55 - 3:05
AL 3:45 T+5 T White
ID 4:05
AL 4:25 T+7 T Red
DT 4:50
AL 5:20 T+8 T White
DT 6:00
ID 7:35
CD 7:55 - 8:00
CD 8:05 - 8:15
CD 8:20 - 8:45
"""

mission8 = """
3:25 - 7:15 - 9:40
AL 0:10 T+3 IT
CD 0:40 - 0:50
AL 1:10 T+4 ST Blue
CD 1:30 - 1:45
ID 2:30
ID 2:40
AL 3:30 T+5 ST White
CD 4:00 - 4:10
DT 4:35
AL 4:55 T+7 ST Red
DT 5:20
UA 6:20 T+8 T Blue
CD 7:30 - 7:40
DT 8:10
CD 8:50 - 9:10
"""

firstTestRun = """
4:10 - 7:00
AL 0:15 T+1 T Blue
AL 1:00 T+2 T White
DT 1:30
AL 2:15 T+3 T Red
DT 3:20
ID 4:40
DT 5:10
"""

secondTestRun = """
3:40 - 7:00
AL 0:10 T+1 T White
ID 0:50
AL 1:20 T+2 T Red
DT 2:15
AL 3:45 T+4 T Blue
DT 4:50
ID 5:30
"""

simulation1 = """
3:40 - 7:30 - 10:00
AL 0:10 T+2 T Red
ID 1:10
AL 1:30 T+3 ST White
DT 2:00
DT 2:50
UA 3:50 T+5 T Red
AL 4:50 T+6 ST Blue
DT 5:40
CD 6:00 - 6:15
ID 6:45
CD 7:50 - 8:00
DT 8:25
"""

simulation2 = """
3:40 - 7:30 - 10:00
ID 0:10
AL 0:20 T+2 ST Blue
DT 1:10
AL 1:40 T+4 T White
DT 3:00
CD 3:50 - 4:00
AL 4:10 T+6 ST Red
ID 4:45
CD 5:00 - 5:10
UA 5:30 T+7 T White
DT 6:00
DT 8:00
CD 8:40 - 8:50
"""

simulation3 = """
4:00 - 7:30 - 10:00
AL 0:10 T+1 T Blue
AL 1:05 T+3 T Red
ID 1:40
CD 2:00 - 2:10
DT 2:30
UA 3:05 T+4 T Blue
AL 4:10 T+5 ST White
DT 4:40
ID 5:00
AL 5:20 T+7 T Red
DT 5:55
CD 6:40 - 6:50
CD 7:50 - 8:05
DT 8:10
CD 8:25 - 8:30
"""
advancedSimulation1 = """
4:00 - 7:30 - 10:00
AL 0:10 T+2 IT
AL 1:00 T+3 T White
DT 1:50
UA 2:20 T+4 T Red
ID 3:10
AL 4:10 T+5 IT
ID 4:50
AL 5:20 T+7 ST Blue
DT 5:40
CD 6:00 - 6:10
DT 6:40
CD 7:50 - 8:10
DT 8:20
CD 9:10 - 9:20
"""
advancedSimulation2 = """
4:10 - 7:30 - 10:00
ID 0:10
AL 0:20 T+2 ST White
UA 1:15 T+3 T Blue
CD 2:00 - 2:15
AL 2:35 T+4 SIT
DT 3:20
ID 4:20
DT 4:30
AL 4:45 T+7 T Red
CD 5:20 - 5:50
DT 7:35
DT 8:00
CD 8:30 - 8:40
"""
advancedSimulation3 = """
4:10 - 7:40 - 10:00
AL 0:10 T+1 T Red
ID 1:10
AL 1:40 T+3 SIT
DT 2:30
AL 3:20 T+4 T Blue
UA 4:20 T+5 T White
ID 5:00
AL 5:20 T+6 IT
CD 5:45 - 5:55
DT 6:05
CD 6:45 - 7:00
CD 7:50 - 8:00
CD 8:05 - 8:15
DT 9:05
"""

# ---------------------------------------------------------------------------
# Double-action missions (Space Alert: The New Frontier).
#
# Transcribed from nibuen/SpaceAlertMissionGenerator (MIT licensed), function
# ConstructedMissions.java. Phase times carry a +5s offset relative to that
# source, matching the convention used by the missions above; this was derived
# by diffing that project's realmission1-8 against mission1-8 here.
# ---------------------------------------------------------------------------

doubleActionEasy1 = """
4:50 - 9:00 - 12:30
AL 0:10 T+2 ST White
UA 0:45 T+3 T Red
AL 1:30 T+3 SIT
DT 1:55
ID 2:20
CD 2:50 - 3:00
AL 3:20 T+4 T Blue
ID 3:55
DT 4:05
CD 5:20 - 5:40
AL 5:55 T+6 T Blue
ID 6:15
DT 6:25
AL 6:45 T+7 T White
AL 7:15 T+8 ST Red
CD 7:35 - 8:00
DT 8:20
CD 9:15 - 9:35
DT 9:50
DT 10:30
"""

doubleActionEasy2 = """
4:50 - 9:00 - 13:00
AL 0:10 T+1 T Red
AL 1:00 T+2 IT
ID 1:35
DT 2:00
AL 2:30 T+3 T White
DT 3:30
AL 3:55 T+4 T Red
AL 5:00 T+5 T White
CD 5:20 - 5:40
DT 5:45
UA 6:05 T+7 ST Red
AL 6:40 T+7 IT
ID 7:05
AL 7:25 T+8 T Blue
DT 8:10
CD 9:10 - 9:20
DT 9:55
CD 10:35 - 11:05
DT 12:10
"""

doubleActionEasy3 = """
4:40 - 8:50 - 12:30
AL 0:10 T+1 T Blue
AL 0:45 T+3 T White
DT 1:15
AL 1:40 T+3 SIT
CD 2:10 - 2:30
DT 2:45
AL 3:20 T+4 T Blue
ID 3:55
ID 4:55
UA 5:10 T+5 ST White
DT 5:35
CD 6:00 - 6:15
AL 6:20 T+6 IT
DT 6:55
AL 7:15 T+7 ST Red
CD 8:00 - 8:15
CD 9:25 - 9:45
DT 9:55
CD 10:35 - 11:00
DT 11:35
"""

doubleActionEasy4 = """
4:50 - 9:10 - 13:00
AL 0:15 T+1 T Red
ID 0:50
AL 1:10 T+2 IT
AL 1:55 T+3 ST Blue
DT 2:20
UA 3:00 T+4 T Red
DT 3:55
AL 5:10 T+5 IT
ID 5:30
CD 5:50 - 6:05
AL 6:10 T+6 ST White
DT 6:45
AL 7:10 T+7 T Red
ID 7:45
UA 8:15 T+8 T Blue
CD 9:25 - 9:45
DT 9:50
CD 10:05 - 10:25
DT 10:55
"""

doubleActionEasy5 = """
5:00 - 9:30 - 13:30
AL 0:10 T+1 T White
AL 0:40 T+2 T Red
ID 1:10
UA 1:30 T+2 IT
DT 2:10
DT 2:25
AL 2:45 T+3 T Blue
CD 3:10 - 3:25
ID 4:10
AL 5:05 T+5 T Red
DT 5:30
AL 5:50 T+5 SIT
UA 6:40 T+6 T Blue
AL 7:10 T+7 T White
CD 7:35 - 8:00
DT 8:05
UA 8:35 T+8 IT
DT 10:00
CD 10:30 - 10:55
DT 11:20
CD 12:40 - 12:50
"""

doubleActionEasy6 = """
4:50 - 9:10 - 13:00
ID 0:15
ID 0:25
AL 0:40 T+3 ST Blue
AL 1:05 T+3 SIT
CD 1:25 - 1:50
DT 2:15
DT 3:00
AL 4:05 T+4 T Red
CD 4:55 - 5:10
AL 5:20 T+6 T White
ID 5:45
DT 6:00
AL 6:20 T+7 IT
UA 6:55 T+7 ST White
AL 7:35 T+8 T Red
DT 8:15
CD 8:30 - 8:40
DT 9:55
CD 10:25 - 10:35
CD 10:40 - 10:50
CD 10:55 - 11:05
DT 12:05
"""

doubleAction1 = """
4:50 - 9:00 - 13:30
AL 0:15 T+2 ST White
AL 1:00 T+2 IT
ID 1:30
AL 1:55 T+3 T Blue
CD 2:30 - 2:40
AL 3:05 T+4 IT
DT 4:00
AL 5:00 T+5 T Red
UA 5:20 T+6 ST White
CD 6:00 - 6:10
AL 6:30 T+7 ST Blue
DT 6:55
ID 7:15
AL 7:30 T+8 ST Red
DT 8:10
CD 9:15 - 9:30
DT 10:00
CD 11:00 - 11:10
"""

doubleAction2 = """
4:50 - 9:40 - 13:30
AL 0:15 T+1 T Red
ID 0:40
AL 1:05 T+2 ST Blue
UA 2:00 T+3 T White
DT 2:35
CD 3:00 - 3:10
DT 3:25
AL 3:55 T+4 SIT
AL 5:05 T+5 T Blue
DT 5:30
AL 5:45 T+6 ST Red
ID 6:10
CD 6:25 - 6:40
AL 6:50 T+7 IT
AL 7:20 T+7 T White
DT 7:45
UA 8:05 T+8 T Blue
CD 8:55 - 9:10
CD 10:05 - 10:35
DT 10:50
DT 12:35
"""

doubleAction3 = """
4:55 - 9:20 - 13:00
AL 0:15 T+2 IT
AL 0:40 T+2 ST Red
ID 1:05
CD 1:30 - 1:50
DT 2:15
AL 2:35 T+3 ST White
DT 3:25
AL 4:00 T+4 T Red
UA 5:05 T+5 SIT
ID 5:35
AL 6:00 T+6 ST Blue
DT 6:35
DT 6:50
CD 7:10 - 7:20
AL 7:30 T+7 IT
AL 8:25 T+8 T White
DT 9:30
CD 10:30 - 10:55
DT 11:00
CD 12:05 - 12:20
"""

doubleAction4 = """
5:10 - 10:00 - 14:00
UA 0:10 T+1 T Red
AL 0:40 T+2 IT
AL 1:30 T+3 ST White
ID 1:55
ID 2:10
AL 2:30 T+4 T Blue
DT 3:00
AL 3:25 T+4 IT
CD 3:45 - 3:50
DT 4:20
AL 5:25 T+5 T Red
AL 5:50 T+6 ST White
DT 6:20
AL 6:50 T+7 T Blue
UA 7:10 T+7 IT
CD 7:45 - 8:00
AL 8:15 T+8 T Red
DT 8:40
CD 9:05 - 9:15
CD 10:10 - 10:20
CD 10:30 - 10:40
CD 10:50 - 11:10
DT 11:40
DT 12:20
"""

doubleAction5 = """
4:50 - 9:10 - 13:00
AL 0:10 T+1 T Blue
CD 0:45 - 1:00
AL 1:15 T+2 ST White
DT 1:50
ID 2:15
AL 2:35 T+4 SIT
DT 3:20
AL 4:05 T+4 T Blue
ID 5:00
AL 5:10 T+5 ST Red
DT 5:45
AL 6:10 T+6 T White
CD 6:35 - 7:00
UA 7:05 T+7 SIT
DT 7:35
AL 8:15 T+8 T Red
CD 9:25 - 9:40
DT 10:00
CD 11:15 - 11:30
DT 12:20
"""

doubleAction6 = """
5:00 - 9:30 - 13:30
UA 0:10 T+1 T Blue
AL 0:40 T+2 T Red
CD 1:15 - 1:30
ID 1:40
DT 2:00
AL 2:25 T+3 SIT
AL 2:50 T+3 T Blue
DT 3:35
AL 4:05 T+4 ST Red
CD 5:10 - 5:20
UA 5:25 T+5 T White
AL 6:25 T+6 IT
ID 6:55
DT 7:05
AL 7:20 T+6 ST White
AL 8:00 T+7 T Red
ID 8:40
DT 9:40
CD 10:00 - 10:30
CD 10:35 - 10:50
DT 11:55
"""

doubleAction7 = """
5:10 - 9:50 - 14:00
AL 0:10 T+1 T Red
CD 0:40 - 0:50
UA 1:10 T+2 IT
AL 1:55 T+2 T White
ID 2:25
DT 2:40
ID 3:00
AL 3:30 T+3 ST Blue
AL 4:20 T+4 T White
DT 5:15
AL 5:30 T+5 SIT
DT 6:00
UA 6:25 T+6 T Red
CD 6:50 - 7:00
CD 7:05 - 7:20
AL 7:30 T+7 T White
AL 8:00 T+8 IT
DT 8:30
AL 8:55 T+8 T Blue
DT 10:05
CD 11:00 - 11:10
CD 11:15 - 11:30
CD 11:35 - 11:55
DT 13:15
"""

doubleAction8 = """
5:00 - 9:30 - 13:30
AL 0:10 T+2 IT
AL 0:35 T+2 T Blue
CD 1:00 - 1:20
ID 1:35
DT 1:45
AL 2:20 T+3 T White
ID 2:50
DT 3:00
AL 3:20 T+4 ST Red
AL 4:10 T+4 IT
AL 5:15 T+5 T Blue
ID 5:50
UA 6:15 T+6 ST White
DT 6:50
AL 7:25 T+7 IT
AL 8:05 T+8 ST Blue
DT 8:35
CD 10:05 - 10:10
CD 10:20 - 10:50
DT 11:05
CD 12:40 - 13:00
"""

doubleAction9 = """
4:50 - 9:10 - 13:00
CD 0:10 - 0:20
AL 0:25 T+1 T White
ID 0:50
AL 1:05 T+2 ST Red
DT 1:30
AL 1:55 T+2 IT
DT 2:35
UA 3:20 T+3 ST Blue
DT 4:05
CD 4:55 - 5:15
AL 5:20 T+5 IT
ID 5:40
AL 5:55 T+6 ST Red
DT 6:25
AL 6:50 T+7 T White
AL 7:45 T+8 ST Blue
ID 8:20
DT 9:35
DT 9:50
CD 10:15 - 10:25
CD 10:35 - 11:05
"""

doubleAction10 = """
5:00 - 9:30 - 13:30
DT 0:10
AL 0:25 T+2 T Red
CD 0:50 - 1:05
AL 1:15 T+3 SIT
DT 1:55
AL 2:35 T+3 T White
DT 3:00
AL 3:25 T+4 T Blue
CD 4:05 - 4:25
AL 5:05 T+5 ST White
UA 5:35 T+6 ST Red
AL 6:15 T+7 T Blue
DT 6:40
CD 7:00 - 7:25
DT 7:35
AL 8:00 T+8 IT
AL 8:40 T+8 T White
ID 9:40
DT 10:30
CD 11:05 - 11:15
DT 12:40
"""

doubleAction11 = """
5:10 - 9:50 - 14:00
ID 0:10
AL 0:20 T+1 T White
UA 1:05 T+2 T Blue
AL 2:10 T+3 IT
DT 2:30
AL 2:50 T+3 ST White
DT 3:10
CD 3:50 - 4:00
AL 4:25 T+4 T Red
AL 5:20 T+5 ST Blue
UA 6:05 T+6 T White
DT 6:40
ID 6:55
AL 7:20 T+7 IT
AL 7:45 T+7 T Red
CD 8:15 - 8:30
AL 8:55 T+8 T White
ID 9:15
DT 10:50
CD 12:20 - 12:50
CD 13:05 - 13:15
DT 13:20
"""

doubleAction12 = """
5:00 - 9:30 - 13:30
AL 0:10 T+2 T White
UA 0:40 T+2 IT
AL 1:40 T+3 T Blue
ID 2:10
ID 2:20
CD 2:30 - 2:50
DT 3:15
AL 3:35 T+4 SIT
DT 5:05
AL 5:20 T+5 T Red
AL 5:50 T+6 ST White
ID 6:15
CD 6:25 - 6:55
UA 7:10 T+7 T White
AL 7:40 T+7 SIT
DT 8:05
AL 8:45 T+8 T Blue
DT 9:40
DT 10:50
CD 11:20 - 11:40
DT 12:05
"""

scripts = {k:v for k,v in locals().items() if not k.startswith('_')}