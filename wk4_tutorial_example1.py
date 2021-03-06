from bridges import Bridge


bridge = Bridge()

A = bridge.add_joint('A', (0, 0), support_reactions=1)
B = bridge.add_joint('B', (2, 0))
C = bridge.add_joint('C', (4, 0))
D = bridge.add_joint('D', (6, 0))
E = bridge.add_joint('E', (8, 0))
F = bridge.add_joint('F', (10, 0))
G = bridge.add_joint('G', (12, 0))
H = bridge.add_joint('H', (14, 0))
I = bridge.add_joint('I', (16, 0), support_reactions=2)
J = bridge.add_joint('J', (14, 2))
K = bridge.add_joint('K', (12, 4))
L = bridge.add_joint('L', (8, 4))
M = bridge.add_joint('M', (4, 4))
N = bridge.add_joint('N', (2, 2))
O = bridge.add_joint('O', (6, 2))
P = bridge.add_joint('P', (10, 2))

bridge.add_member(A, B)
bridge.add_member(A, N)
bridge.add_member(B, C)
bridge.add_member(B, N)
bridge.add_member(C, D)
bridge.add_member(C, M)
bridge.add_member(C, N)
bridge.add_member(C, O)
bridge.add_member(D, E)
bridge.add_member(D, O)
bridge.add_member(E, F)
bridge.add_member(E, L)
bridge.add_member(E, O)
bridge.add_member(E, P)
bridge.add_member(F, G)
bridge.add_member(F, P)
bridge.add_member(G, H)
bridge.add_member(G, J)
bridge.add_member(G, K)
bridge.add_member(G, P)
bridge.add_member(H, I)
bridge.add_member(H, J)
bridge.add_member(I, J)
bridge.add_member(J, K)
bridge.add_member(K, L)
bridge.add_member(K, P)
bridge.add_member(L, M)
bridge.add_member(M, N)
bridge.add_member(M, O)


C.forces.append((0, -2000))
E.forces.append((0, -5000))
F.forces.append((0, -3000))
G.forces.append((0, -2000))
bridge.determine_support_reactions()
bridge.determine_forceless_members()
bridge.determine_member_truss_forces()
bridge.output_forces_info()
bridge.output_structure()
