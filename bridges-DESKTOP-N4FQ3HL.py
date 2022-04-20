import math
from operator import xor
from fractions import Fraction
import matplotlib.pyplot as plt


class Bridge:
    def __init__(self):
        self.joints = []
        self.members = []

    class Joint:
        def __init__(self, name, position, applied_force=(0, 0), support_reactions=0):
            self.name = name
            self.position = position
            self.support_reactions = support_reactions
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

    def add_joint(self, name, position, applied_force=(0, 0), support_reactions=0):
        self.joints.append(self.Joint(name, position, applied_force, support_reactions))
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

    def determine_support_reactions(self):  # Down is negative
        supported_joints = []
        for joint in self.joints:
            if joint.support_reactions > 0:
                supported_joints.append(joint)

        reaction_moment_1 = 0
        for joint in self.joints:
            for force in joint.forces:
                reaction_moment_1 += force[1] * abs(joint.position[0] - supported_joints[0].position[0])
        reaction_force_2 = -reaction_moment_1 / abs(supported_joints[0].position[0] - supported_joints[1].position[0])
        reaction_force_1 = -sum([sum([force[1] for force in joint.forces]) for joint in self.joints]) - reaction_force_2
        supported_joints[0].forces.append((0, round(reaction_force_1, 5)))
        supported_joints[1].forces.append((0, round(reaction_force_2, 5)))

    def find_truss_determinacy(self):
        return 2 * len(self.joints) == len(self.members) + sum([joint.support_reactions for joint in self.joints])

    def determine_forceless_members(self):
        forceless_members = []
        previous_members = []
        while previous_members != self.members:
            previous_members = list(self.members)
            for joint in self.joints:
                if len(joint.forces) == 0:
                    connected_members = [member for member in self.return_connected_members(joint)
                                         if member not in forceless_members]
                    if len(connected_members) == 3:
                        connected_member_angles = [member.angle for member in connected_members]
                        connected_member_angles = [((angle - min(connected_member_angles)) / math.pi) % 1 * 2
                                                   for angle in connected_member_angles]
                        if sum(connected_member_angles) % 1 == 0:
                            for i, angle in enumerate(connected_member_angles):
                                if connected_member_angles.count(angle) == 1:
                                    forceless_members.append(connected_members[i])
                                    # self.members.remove(connected_members[i])
                                    break
        return forceless_members





    def determine_member_truss_forces(self):
        force_sums = []
        forceless_members = self.determine_forceless_members()
        while force_sums != [(0, 0)] * len(self.joints):
            force_sums = [(round(sum([force[0] for force in joint.forces]), 5),
                           round(sum([force[1] for force in joint.forces]), 5)) for joint in self.joints]
            for joint_index, unequal_sum in [isum for isum in enumerate(force_sums) if isum[1] != (0, 0)]:
                unequal_joint = self.joints[joint_index]
                if unequal_sum[0] != 0:
                    connected_members = [member for member in self.return_connected_members(unequal_joint) if
                                         abs(member.angle) != math.pi / 2 and member.force == 0 and member not in forceless_members]
                    if len(connected_members) == 1:
                        connected_member = connected_members[0]
                        if sum([force[0] for force in unequal_joint.forces]) != 0:
                            unequal_sum = sum([force[0] for force in unequal_joint.forces])
                            connected_member.change_force(abs(unequal_sum) / math.cos(connected_member.angle),
                                                          xor(unequal_sum * connected_member.direction[0] > 0,
                                                              unequal_joint == connected_member.joint2))
                            continue
                if unequal_sum[1] != 0:
                    connected_members = [member for member in self.return_connected_members(unequal_joint) if
                                         member.angle % math.pi != 0 and member.force == 0 and member not in forceless_members]
                    if len(connected_members) == 1:
                        connected_member = connected_members[0]
                        if sum([force[1] for force in unequal_joint.forces]) != 0:
                            unequal_sum = sum([force[1] for force in unequal_joint.forces])
                            connected_member.change_force(abs(unequal_sum) / math.sin(connected_member.angle),
                                                          xor(unequal_sum * connected_member.direction[1] > 0,
                                                              unequal_joint == connected_member.joint2))

    def output_structure(self):
        for member in self.members:
            joint_positions = [member.joint1.position, member.joint2.position]
            plt.plot(*zip(*joint_positions))
        for joint in self.joints:
            plt.scatter(joint.position[0], joint.position[1])
            plt.text(joint.position[0], joint.position[1], joint.name)
        plt.show()

    def output_forces_info(self):
        print('--- SUM OF FORCES ON EACH JOINT ---')
        for joint in self.joints:
            print(joint.name, joint.forces, (sum([i[0] for i in joint.forces]), sum([i[1] for i in joint.forces])))

        print('\n--- FORCES ON EACH MEMBER ---')
        for member in self.members:
            print(member.joint1.name, member.joint2.name, member.is_compressed, member.force)
