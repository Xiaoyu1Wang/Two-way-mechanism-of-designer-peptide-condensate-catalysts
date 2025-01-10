import os, sys
import MDAnalysis, MDAnalysis.analysis.distances
import numpy, csv

name = sys.argv[1]
#name = "annealing_cubic_WGR2H@3_WGE2H@3_ION@15_box8_1"
trjpath = f"../../{name}/wrap"
outpath = f"data/{name}.csv"
trjfiles = sorted([os.path.join(trjpath, file) for file in os.listdir(trjpath) if file.endswith(".trr")])

distance_matrix = []

# 获取迭代器,continous 会自动处理 trr 中的重复帧
trajectory = MDAnalysis.Universe(os.path.join(trjpath ,"wrap.pdb"),trjfiles, continous = True)
atom_selection = "name CA and resname HIE HID HSD HSE HIS"
atoms = trajectory.select_atoms(atom_selection)
# foreach timestep
for ts in trajectory.trajectory:
    # box = ts.dimensions 用于指定考虑 PBC
    distance = MDAnalysis.analysis.distances.distance_array(atoms.positions, atoms.positions, box = ts.dimensions)
    # 计算结果是一个对称的矩阵，故只需要不包括对角线的上（下）三角部分
    upper_triangle_indices = numpy.triu_indices(distance.shape[0], k=1)
    distance_str = ["{:5.1f}".format(value) for value in distance[upper_triangle_indices]]
    filename, _ = os.path.splitext(os.path.basename(trajectory.trajectory.filename))
    line = [ts.frame, filename] + distance_str
    distance_matrix.append(line)

with open(outpath, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerows(distance_matrix)
