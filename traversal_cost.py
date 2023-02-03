import rosbag
import rospy

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
plt.rcParams['text.usetex'] = True  # Render Matplotlib text with Tex

from scipy.fft import rfft, rfftfreq
from scipy.ndimage import uniform_filter1d

"""
tom_path_grass:
- grass: 175 - 190
- grass to path: 87 - 95
- path: 102 - 108

tom_road:
- road: 30 - 50

tom_grass_wood:
- sidewalk: 7 - 12 (0.5)
- paved way: 17 - 20
- grass mud: 90 - 100
- grass - leaves: 137 - 147 (0.5)
- leaves: 166 - 176
"""
data = np.load("grassmud_t10_v1.npy")

z_acceleration = data[:, 0]
roll_rate = data[:, 1]
pitch_rate = data[:, 2]
x_velocity = data[:, 3]

IMU_SAMPLE_RATE = 43

roll_rate_mean = uniform_filter1d(roll_rate, size=5)  # To reduce noise

hanning_window = np.hanning(len(z_acceleration))
roll_rate_windowing = roll_rate*hanning_window

roll_rate_mean_windowing = roll_rate_mean*hanning_window


# 2d time domain plots
plt.figure()

plt.subplot(221)
plt.plot(x_velocity)
plt.title("X velocitity")
plt.xlabel("Time ($s$)")
plt.ylabel("Velocity ($m/s$)")

plt.subplot(222)
plt.plot(z_acceleration)
plt.title("Z acceleration")
plt.xlabel("Time ($s$)")
plt.ylabel("Acceleration ($m/s^2$)")

plt.subplot(223)
plt.plot(roll_rate, "b", label="raw")
plt.plot(roll_rate_mean, "c", label="mean filter")
plt.plot(roll_rate_windowing, "m", label="Hanning windowing")
plt.plot(roll_rate_mean_windowing, "r", label="mean filter + Hanning windowing")
plt.title("Roll rate")
plt.xlabel("t")
plt.xlabel("Time ($s$)")
plt.ylabel("Angular rate ($rad/s$)")
plt.legend()

plt.subplot(224)
plt.plot(pitch_rate)
plt.title("Pitch rate")
plt.xlabel("Time ($s$)")
plt.ylabel("Angular rate ($rad/s$)")



z_acceleration_fourier = rfft(z_acceleration - 9.81)
roll_rate_fourier = rfft(roll_rate)
pitch_rate_fourier = rfft(pitch_rate)

roll_rate_mean_fourier = rfft(roll_rate_mean)
roll_rate_windowing_fourier = rfft(roll_rate_windowing)
roll_rate_mean_windowing_fourier = rfft(roll_rate_mean_windowing)

frequencies = rfftfreq(len(z_acceleration), 1/IMU_SAMPLE_RATE)

# 2d frequency domain plots
plt.figure()

plt.subplot(131)
plt.plot(frequencies,
         np.abs(z_acceleration_fourier))
plt.title("Z acceleration")
plt.xlabel("Frequency ($s^{-1}$)")
plt.ylabel("Amplitude ($m/s^2$)")

plt.subplot(132)
plt.plot(frequencies,
         np.abs(roll_rate_fourier), "b", label="raw")
plt.plot(frequencies,
         np.abs(roll_rate_mean_fourier), "c", label="mean filter")
plt.plot(frequencies,
         np.abs(roll_rate_windowing_fourier), "m", label="Hanning windowing")
plt.plot(frequencies,
         np.abs(roll_rate_mean_windowing_fourier), "r", label="mean filter + Hanning windowing")
plt.title("Roll rate")
plt.xlabel("Frequency ($s^{-1}$)")
plt.ylabel("Amplitude ($rad/s$)")
plt.legend()

plt.subplot(133)
plt.plot(frequencies,
         np.abs(pitch_rate_fourier))
plt.title("Pitch rate")
plt.xlabel("Frequency ($s^{-1}$)")
plt.ylabel("Amplitude ($rad/s$)")


# FILES = ["grass_t15_v1.npy",
#          "grasspath_t8_v1.npy",
#          "path_t6_v1.npy",
#          "road_t20_v1.npy",
#          "sidewalk_t5_v0.5.npy",
#          "pavedway_t3_v1.npy",
#          "grassmud_t10_v1.npy",
#          "grassleaves_t10_v0.5.npy",
#          "leaves_t10_v1.npy"]

# # 3d time domain plot and box plots
# fig = plt.figure("3D")
# ax = fig.add_subplot(projection="3d")

# fig5, ax5 = plt.subplots()
# fig6, ax6 = plt.subplots()
# fig7, ax7 = plt.subplots()

# labels = []
# z_accelerations = []
# roll_rates = []
# pitch_rates = []

# for file in FILES:
#     data = np.load(file)
    
#     z_acceleration = data[:, 0]
#     roll_rate = data[:, 1]
#     pitch_rate = data[:, 2]
#     x_velocity  = data[:, 3]
    
#     label = file.split("_")[0]

#     ax.scatter(z_acceleration, roll_rate, pitch_rate, label=label)
    
#     labels.append(label)
#     z_accelerations.append(z_acceleration[:120])
#     roll_rates.append(roll_rate[:120])
#     pitch_rates.append(pitch_rate[:120])
    
    
#     z_acceleration_fourier = rfft(z_acceleration - 9.81)
#     roll_rate_fourier = rfft(roll_rate)
#     pitch_rate_fourier = rfft(pitch_rate)

#     frequencies = rfftfreq(len(z_acceleration), 1/IMU_SAMPLE_RATE)
    
#     ax5.plot(frequencies, np.abs(z_acceleration_fourier), label=label)
#     ax6.plot(frequencies, np.abs(roll_rate_fourier), label=label)
#     ax7.plot(frequencies, np.abs(pitch_rate_fourier), label=label)




# ax.set_xlabel("Z acceleration")
# ax.set_ylabel("Roll rate")
# ax.set_zlabel("Pitch rate")
# ax.legend()

# ax5.legend()
# ax6.legend()
# ax7.legend()

# fig2, ax2 = plt.subplots()
# ax2.boxplot(z_accelerations)
# ax2.set_xticklabels(labels)
# ax2.set_title("Z acceleration")

# fig3, ax3 = plt.subplots()
# ax3.boxplot(roll_rates)
# ax3.set_xticklabels(labels)
# ax3.set_title("Roll rate")

# fig4, ax4 = plt.subplots()
# ax4.boxplot(pitch_rates)
# ax4.set_xticklabels(labels)
# ax4.set_title("Pitch rate")


plt.show()
