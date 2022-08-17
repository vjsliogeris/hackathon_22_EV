import open3d as o3d
import laspy as lp
import numpy as np
import webbrowser
from threading import Thread
import time
import sys

FILE_PATH = sys.argv[1]
DEPTH = sys.argv[2]

def draw():
    o3d.visualization.webrtc_server.enable_webrtc()

    las = lp.read(str(FILE_PATH))
    las_points = np.vstack((las.x, las.y, las.z)).transpose()
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(las_points)
    octree = o3d.geometry.Octree(max_depth=int(DEPTH))
    octree.convert_from_point_cloud(pcd, size_expand=0.01)
    o3d.visualization.draw(octree)

def open_browser():
    url = 'http://localhost:8888'
    webbrowser.open(url)

def main():
    t1 = Thread(target=draw)
    t2 = Thread(target=open_browser)

    t1.start()
    time.sleep(1)
    t2.start()
    t1.join()
    t2.join()

if __name__ == "__main__":
    main()
