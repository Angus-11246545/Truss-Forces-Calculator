from bridges import Bridge


bridge = Bridge()

A = bridge.add_joint('A', (0, 0), support_reactions=1)
B = bridge.add_joint('B', (3, 0))
C = bridge.add_joint('C', (6, 0))
D = bridge.add_joint('D', (9, 0), support_reactions=2)
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

C.forces.append((0, -10000))
bridge.determine_support_reactions()
bridge.determine_member_truss_forces()

bridge.output_forces_info()
bridge.output_structure()
