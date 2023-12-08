import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np

def plot_crater(crdia,crht,crht_max,crslope,crdepth,crbasedia,plot_interval_spacing):
    centerx = crbasedia/2.0
    number_of_circles = int((crht // plot_interval_spacing)+1)   #Note floor division
    if number_of_circles < 2:
        number_of_circles = 2
    zstep = crht/(number_of_circles-1)
    xstep = zstep/np.tan(crslope*np.pi/180)

    circangs = np.arange(0,360,1)
    numangs = np.size(circangs)
    xvals = np.ones(numangs)
    yvals = np.ones(numangs)
    zvals = np.ones(numangs)

    # fig1 = plt.figure()
    ax1 = plt.axes(projection='3d')
    plt.ion()
    plt.show()

    ax1.plot3D(xvals,yvals,zvals,'green')
    ax1.set_xlabel('x axis')
    ax1.set_ylabel('y axis')
    ax1.set_zlabel('z axis')
    ax1.set_xlim(-xstep,crbasedia*1.5)
    ax1.set_ylim(-crbasedia/1.5, crbasedia/1.5)
    ax1.set_zlim(-xstep, crbasedia*1.5)
    ax1.set_title('MONSTER TRUCKS ON THE MOON!!!!')

    for i in range(0,number_of_circles):
        rad = centerx - xstep * i
        zvals = zstep * i
        for j in range(0,numangs):
            xvals[j] = centerx + rad*np.cos(circangs[j] * (np.pi/180))
            yvals[j] = rad * np.sin(circangs[j] * (np.pi / 180))

        ax1.plot3D(xvals,yvals,zvals,'blue')
        plt.draw()
        plt.pause(0.020)

    #Now plot the crater inner walls
    number_of_inner_circles = int((crdepth // plot_interval_spacing))  #Note floor division
    for i in range(0,number_of_inner_circles):
        zvals = (crht - crdepth) + zstep * i
        for j in range(0,numangs):
            xvals[j] = centerx + rad*np.cos(circangs[j] * (np.pi/180))
            yvals[j] = rad * np.sin(circangs[j] * (np.pi / 180))

        ax1.plot3D(xvals,yvals,zvals,'green')
        plt.draw()
        plt.pause(0.020)

    # Now plot the crater floor
    number_of_floor_circles = int((crdia // (plot_interval_spacing*5))+1)  # Note floor division
    floor_circle_spacing = int((crdia/2)//(number_of_floor_circles-1))
    for i in range(0, number_of_floor_circles):
        zvals = (crht - crdepth)
        rad = crdia / 2 - floor_circle_spacing*i
        for j in range(0, numangs):
            xvals[j] = centerx + rad * np.cos(circangs[j] * (np.pi / 180))
            yvals[j] = rad * np.sin(circangs[j] * (np.pi / 180))

        ax1.plot3D(xvals, yvals, zvals, 'green')
        plt.draw()
        plt.pause(0.030)

    #Now put in the starting point
    ax1.scatter3D(0,0,0, color='blue')
    plt.draw()
    plt.pause(0.030)

    return ax1

def plot_final_path(craterplot,final_pathdata,launch_row,landing_row):
    [numrows,numcols]=np.shape(final_pathdata)
    for i in range(1,launch_row):
        x = final_pathdata[i,1].copy()
        y = 0.0
        z = final_pathdata[i,3].copy()
        craterplot.scatter3D(x,y,z,color = 'magenta')
    for i in range(launch_row,numrows-2):
        x = final_pathdata[i, 1].copy()
        y = 0.0
        z = final_pathdata[i, 3].copy()
        craterplot.scatter3D(x, y, z, color='yellow')
    x = final_pathdata[numrows-1, 1].copy()
    y = 0.0
    z = final_pathdata[numrows - 1, 3].copy()
    craterplot.scatter3D(x, y, z, color='red')
    plt.draw()
    plt.pause(0.020)
    plt.show(block = True)
