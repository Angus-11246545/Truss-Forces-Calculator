import math
from operator import xor
from fractions import Fraction

class Bridge:
    def __init__(self):
        self.joints = []
        self.members = []

    class Joint:
        def __init__(self, name, position, applied_force=(0, 0), has_support=False):
            self.name = name
            self.position = position
            self.has_support = has_support
            self.forces = []

    class Member:
        def __init__(self, joint1, joint2):
            self.joint1 = joint1
            self.joint2 = joint2
            # self.angle is the anti-clockwise angle from the positive x-axis. First parameter is y, 2nd is x
            self.angle = math.atan2(joint2.position[1] - joint1.position[1], joint2.position[0] - joint1.position[0])
            # self.direction measures where joint2 is in relation to joint1.
            # E.g. (1, 0) means joint2 is directly to the right of joint1, (-1, 1) means to the left and up.
            self.direction = [joint2.position[0] - joint1.position[0], joint2.position[1] - joint1.position[1]]
            for i, value in enumerate(self.direction):
                value = int(value)
                if value != 0:
                    value //= abs(value)
                self.direction[i] = value

            self.force = 0
            self.is_compressed = True  # If false then must be in tension

        def change_force(self, magnitude, is_compressed):
            self.is_compressed = is_compressed
            self.force = abs(magnitude)

            if self.is_compressed:
                new_force = (round(-self.force * math.cos(self.angle), 5), round(-self.force * math.sin(self.angle), 5))
            else:
                new_force = (round(self.force * math.cos(self.angle), 5), round(self.force * math.sin(self.angle), 5))
            self.joint1.forces.append(new_force)
            self.joint2.forces.append(tuple(-component for component in new_force))
            pass

    def add_joint(self, name, position, applied_force=(0, 0), has_support=False):
        self.joints.append(self.Joint(name, position, applied_force, has_support))
        return self.joints[-1]

    def add_member(self, joint1, joint2):
        self.members.append(self.Member(joint1, joint2))
        return self.members[0]

    def find_joint(self, name):
        for joint in self.joints:
            if joint.name == name:
                return joint

    def return_connected_members(self, joint):
        connected_members = []
        for member in self.members:
            if joint in [member.joint1, member.joint2]:
                connected_members.append(member)
        return connected_members

    def determine_support_reactions(self, affected_joint, force_strength):  # Down is negative
        supported_joints = []
        for joint in self.joints:
            if joint.has_support:
                supported_joints.append(joint)

        affected_joint.forces.append((0, force_strength))

        reaction_force_1 = -force_strength * math.dist(affected_joint.position,
                                                       supported_joints[1].position) / math.dist(
            supported_joints[0].position, supported_joints[1].position)
        reaction_force_2 = -force_strength - reaction_force_1
        supported_joints[0].forces.append((0, round(reaction_force_1, 5)))
        supported_joints[1].forces.append((0, round(reaction_force_2, 5)))

    def determine_member_truss_forces(self):
        force_sums = []
        while force_sums != [(0, 0)] * len(self.joints):
            force_sums = [(round(sum([force[0] for force in joint.forces]), 5),
                           round(sum([force[1] for force in joint.forces]), 5)) for joint in self.joints]
            for joint_index, unequal_sum in [isum for isum in enumerate(force_sums) if isum[1] != (0, 0)]:
                unequal_joint = self.joints[joint_index]
                if unequal_sum[0] != 0:
                    connected_members = [member for member in self.return_connected_members(unequal_joint) if
                                         abs(member.angle) != math.pi / 2 and member.force == 0]
                    if len(connected_members) == 1:
                        connected_member = connected_members[0]
                        if sum([force[0] for force in unequal_joint.forces]) != 0:
                            connected_member.change_force(abs(unequal_sum[0]) / math.cos(connected_member.angle),
                                                          xor(unequal_sum[0] * connected_member.direction[0] > 0,
                                                              unequal_joint == connected_member.joint2))
                elif unequal_sum[1] != 0:
                    connected_members = [member for member in self.return_connected_members(unequal_joint) if
                                         member.angle % math.pi != 0 and member.force == 0]
                    if len(connected_members) == 1:
                        connected_member = connected_members[0]
                        if sum([force[1] for force in unequal_joint.forces]) != 0:
                            connected_member.change_force(abs(unequal_sum[1]) / math.sin(connected_member.angle),
                                                          xor(unequal_sum[1] * connected_member.direction[1] > 0,
                                                              unequal_joint == connected_member.joint2))


bridge = Bridge()

A = bridge.add_joint('A', (0, 0), has_support=True)
B = bridge.add_joint('B', (3, 0))
C = bridge.add_joint('C', (6, 0))
D = bridge.add_joint('D', (9, 0), has_support=True)
E = bridge.add_joint('E', (6, 4))
F = bridge.add_joint('F', (3, 4))

bridge.add_member(A, B)
bridge.add_member(A, F)
bridge.add_member(B, C)
bridge.add_member(B, E)
bridge.add_member(B, F)
bridge.add_member(C, D)
bridge.add_member(C, E)
bridge.add_member(D, E)
bridge.add_member(E, F)

bridge.determine_support_reactions(C, -10000)
bridge.determine_member_truss_forces()

print('--- SUM OF FORCES ON EACH JOINT ---')
for joint in bridge.joints:
    print(joint.name, joint.forces, (sum([i[0] for i in joint.forces]), sum([i[1] for i in joint.forces])))

print('\n--- FORCES ON EACH MEMBER ---')
for member in bridge.members:
    print(member.joint1.name, member.joint2.name, member.is_compressed, member.force)
