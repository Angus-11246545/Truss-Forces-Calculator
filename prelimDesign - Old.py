from bridges import Bridge


bridge = Bridge()

A = bridge.add_joint('A', (0, 0), support_reactions=1)
B = bridge.add_joint('B', (2, 0))
C = bridge.add_joint('C', (4, 0), support_reactions=2)
D = bridge.add_joint('D', (6, 0))
E = bridge.add_joint('E', (0.5, 2))
F = bridge.add_joint('F', (2.5, 1.5))
G = bridge.add_joint('G', (4.5, 1))

bridge.add_member(A, B)
bridge.add_member(A, E)
bridge.add_member(B, C)
bridge.add_member(B, E)
bridge.add_member(B, F)
bridge.add_member(C, D)
bridge.add_member(C, F)
bridge.add_member(C, G)
bridge.add_member(D, G)
bridge.add_member(E, F)
bridge.add_member(F, G)

print(bridge.find_truss_determinacy())

bridge.output_structure()
D.forces.append((0, -10000))
bridge.determine_support_reactions()
bridge.determine_member_truss_forces()

bridge.output_forces_info()
bridge.output_structure()
