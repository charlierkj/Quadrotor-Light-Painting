#!/usr/bin/env python


import sys
import yaml
import rospy
import numpy as np
import time
import threading
import math
from std_srvs.srv import Empty
from crazyflie_driver.srv import *
from crazyflie_driver.msg import TrajectoryPolynomialPiece
from tf import TransformListener
import modify_durations as md

def arrayToGeometryPoint(a):
    return geometry_msgs.msg.Point(a[0], a[1], a[2])

class TimeHelper:
    def __init__(self):
        rospy.wait_for_service("/next_phase")
        self.nextPhase = rospy.ServiceProxy("/next_phase", Empty)

    def time(self):
        return time.time()

    def sleep(self, duration):
        time.sleep(duration)

    def nextPhase(self):
        self.nextPhase()


class Crazyflie:
    def __init__(self, id, initialPosition, tf):
        self.id = id
        self.prefix = "/cf" + str(id)
        self.initialPosition = np.array(initialPosition)
        self.record = []

        self.tf = tf

        rospy.wait_for_service(self.prefix + "/set_group_mask")
        self.setGroupMaskService = rospy.ServiceProxy(self.prefix + "/set_group_mask", SetGroupMask)
        rospy.wait_for_service(self.prefix + "/takeoff")
        self.takeoffService = rospy.ServiceProxy(self.prefix + "/takeoff", Takeoff)
        rospy.wait_for_service(self.prefix + "/land")
        self.landService = rospy.ServiceProxy(self.prefix + "/land", Land)
        # rospy.wait_for_service(self.prefix + "/stop")
        # self.stopService = rospy.ServiceProxy(self.prefix + "/stop", Stop)
        rospy.wait_for_service(self.prefix + "/go_to")
        self.goToService = rospy.ServiceProxy(self.prefix + "/go_to", GoTo)
        rospy.wait_for_service(self.prefix + "/upload_trajectory")
        self.uploadTrajectoryService = rospy.ServiceProxy(self.prefix + "/upload_trajectory", UploadTrajectory)
        # rospy.wait_for_service(self.prefix + "/start_trajectory")
        # self.startTrajectoryService = rospy.ServiceProxy(self.prefix + "/start_trajectory", StartTrajectory)
        rospy.wait_for_service(self.prefix + "/update_params")
        self.updateParamsService = rospy.ServiceProxy(self.prefix + "/update_params", UpdateParams)

    def setGroupMask(self, groupMask):
        self.setGroupMaskService(groupMask)

    def takeoff(self, targetHeight, duration, groupMask = 0):
        self.takeoffService(groupMask, targetHeight, rospy.Duration.from_sec(duration))

    def land(self, targetHeight, duration, groupMask = 0):
        self.landService(groupMask, targetHeight, rospy.Duration.from_sec(duration))

    def stop(self, groupMask = 0):
        self.stopService(groupMask)

    def goTo(self, goal, yaw, duration, relative = False, groupMask = 0):
        gp = arrayToGeometryPoint(goal)
        self.goToService(groupMask, relative, gp, yaw, rospy.Duration.from_sec(duration))

    def uploadTrajectory(self, trajectoryId, pieceOffset, trajectory):
        pieces = []
        for poly in trajectory.polynomials:
            piece = TrajectoryPolynomialPiece()
            piece.duration = rospy.Duration.from_sec(poly.duration)
            piece.poly_x   = poly.px.p
            piece.poly_y   = poly.py.p
            piece.poly_z   = poly.pz.p
            piece.poly_yaw = poly.pyaw.p
            pieces.append(piece)
        self.uploadTrajectoryService(trajectoryId, pieceOffset, pieces)

    def startTrajectory(self, trajectoryId, timescale = 1.0, reverse = False, relative = True, groupMask = 0):
        self.startTrajectoryService(groupMask, trajectoryId, timescale, reverse, relative)

    def position(self):
        self.tf.waitForTransform("/world", "/cf" + str(self.id), rospy.Time(0), rospy.Duration(10))
        position, quaternion = self.tf.lookupTransform("/world", "/cf" + str(self.id), rospy.Time(0))
        return np.array(position)

    def getParam(self, name):
        return rospy.get_param(self.prefix + "/" + name)

    def setParam(self, name, value):
        rospy.set_param(self.prefix + "/" + name, value)
        self.updateParamsService([name])

    def setParams(self, params):
        for name, value in params.iteritems():
            rospy.set_param(self.prefix + "/" + name, value)
        self.updateParamsService(params.keys())

    def addRecord(self, t):
        rcd = []
        rcd.append(t)
        rcd.append(self.position()[0])
        rcd.append(self.position()[1])
        rcd.append(self.position()[2])
        rcd.append(self.getParam('ring/solidRed'))
        rcd.append(self.getParam('ring/solidGreen'))
        rcd.append(self.getParam('ring/solidBlue'))
        self.record.append(rcd)


class CrazyflieServer:
    def __init__(self):
        rospy.init_node("CrazyflieAPI", anonymous=False)
        rospy.wait_for_service("/emergency")
        self.emergencyService = rospy.ServiceProxy("/emergency", Empty)
        rospy.wait_for_service("/takeoff")
        self.takeoffService = rospy.ServiceProxy("/takeoff", Takeoff)
        rospy.wait_for_service("/land")
        self.landService = rospy.ServiceProxy("/land", Land)
        # rospy.wait_for_service("/stop")
        # self.stopService = rospy.ServiceProxy("/stop", Stop)
        # rospy.wait_for_service("/go_to")
        # self.goToService = rospy.ServiceProxy("/go_to", GoTo)
        rospy.wait_for_service("/start_trajectory");
        self.startTrajectoryService = rospy.ServiceProxy("/start_trajectory", StartTrajectory)
        # rospy.wait_for_service("/update_params")
        # self.updateParamsService = rospy.ServiceProxy("/update_params", UpdateParams)

        with open("../launch/crazyflies.yaml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile)

        self.tf = TransformListener()

        self.crazyflies = []
        self.crazyfliesById = dict()
        for crazyflie in cfg["crazyflies"]:
            id = int(crazyflie["id"])
            initialPosition = crazyflie["initialPosition"]
            cf = Crazyflie(id, initialPosition, self.tf)
            self.crazyflies.append(cf)
            self.crazyfliesById[id] = cf

    def emergency(self):
        self.emergencyService()

    def takeoff(self, targetHeight, duration, groupMask = 0):
        self.takeoffService(groupMask, targetHeight, rospy.Duration.from_sec(duration))

    def land(self, targetHeight, duration, groupMask = 0):
        self.landService(groupMask, targetHeight, rospy.Duration.from_sec(duration))

    # def stop(self, groupMask = 0):
    #     self.stopService(groupMask)

    # def goTo(self, goal, yaw, duration, groupMask = 0):
    #     gp = arrayToGeometryPoint(goal)
    #     self.goToService(groupMask, True, gp, yaw, rospy.Duration.from_sec(duration))

    def startTrajectory(self, trajectoryId, timescale = 1.0, reverse = False, relative = True, groupMask = 0):
        self.startTrajectoryService(groupMask, trajectoryId, timescale, reverse, relative)

    # def setParam(self, name, value, group = 0):
    #     rospy.set_param("/cfgroup" + str(group) + "/" + name, value)
    #     self.updateParamsService(group, [name])

    def recordingsleep(self, duration, initialtime):
        for i in range(0, int(math.floor(duration*100))): 
            for cf in self.crazyflies:
                cf.addRecord(time.time() - initialtime)
            time.sleep(0.01)
            for cf in self.crazyflies:
                cf.addRecord(time.time() - initialtime)
        time.sleep(duration - math.floor(duration*100)/100)            

    def startColorTrajectory(self, trajectory, trajectoryId, timescale = 1.0, reverse = False, relative = True, groupMask = 0):
        durations = md.Modify_Durations(trajectory)
        print durations

        self.startTrajectoryService(groupMask, trajectoryId, timescale, reverse, relative)

        t0 = time.time()

        for i in range(0, len(trajectory.polynomials)):
            if reverse is False:
                color = trajectory.color[i]
                for cf in self.crazyflies:
                    cf.setParam('ring/solidRed', int(color[0]))
                    cf.setParam('ring/solidGreen', int(color[1]))
                    cf.setParam('ring/solidBlue', int(color[2]))
                self.recordingsleep(durations[i]*timescale, t0)
            elif reverse is True:
                color = trajectory.color[len(trajectory.polynomials)-1-i]
                for cf in self.crazyflies:
                    cf.setParam('ring/solidRed', int(color[0]))
                    cf.setParam('ring/solidGreen', int(color[1]))
                    cf.setParam('ring/solidBlue', int(color[2]))
                self.recordingsleep(durations[len(trajectory.polynomials)-1-i]*timescale, t0)

