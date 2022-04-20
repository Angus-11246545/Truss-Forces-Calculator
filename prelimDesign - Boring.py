from bridges import Bridge


bridge = Bridge()

A = bridge.add_joint('A', (0, 0), support_reactions=2)
B = bridge.add_joint('B', (0.1, 0), support_reactions=1)
C = bridge.add_joint('C', (0.2, 0))
D = bridge.add_joint('D', (0.3, 0))
E = bridge.add_joint('E', (0.4, 0))
F = bridge.add_joint('F', (0.5, 0))
G = bridge.add_joint('G', (0.1, 0.17))
H = bridge.add_joint('H', (0.2, 0.17))
I = bridge.add_joint('I', (0.3, 0.17))
J = bridge.add_joint('J', (0.4, 0.17))
# K = bridge.add_joint('K', (0.5, 0.17))

bridge.add_member(A, B)
bridge.add_member(A, G)
bridge.add_member(B, C)
bridge.add_member(B, G)
bridge.add_member(C, D)
bridge.add_member(C, G)
bridge.add_member(C, H)
bridge.add_member(D, E)
bridge.add_member(D, H)
bridge.add_member(D, I)
bridge.add_member(E, F)
bridge.add_member(E, I)
bridge.add_member(E, J)
bridge.add_member(F, J)
# bridge.add_member(F, K)
bridge.add_member(G, H)
bridge.add_member(H, I)
bridge.add_member(I, J)
# bridge.add_member(J, K)

print(bridge.find_truss_determinacy())

bridge.output_structure()

F.forces.append((0, -10000))
bridge.determine_support_reactions()
bridge.determine_member_truss_forces()

bridge.output_forces_info()
bridge.output_structure()
