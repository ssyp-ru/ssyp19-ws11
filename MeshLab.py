# Writes all calculated coordinates into coords.ply file
def write(point_cloud):
    f = open('coords.ply', 'w')

    # Header start
    f.write("ply\n")
    f.write("format ascii 1.0\n")
    f.write("element vertex " + str(len(point_cloud)) + '\n')
    f.write("property float32 x\n")
    f.write("property float32 y\n")
    f.write("property float32 z\n")
    f.write("end_header\n")
    # Header end

    # Coords writing
    for point in point_cloud:
        f.write("{} {} {}\n".format(point[0], point[1], point[2]))
    f.close()
