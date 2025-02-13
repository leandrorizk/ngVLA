# Extract Data from ngVLA_RX_cascade_analysis_summary_2021-07-15.pdf
# Plots and/or prints data file of any of the listed parameters, vs frequency

# User input is not case sensitive and can recognise underscores or no, eg. T_sys or Tsys

# import modules
import numpy as np
import matplotlib.pyplot as plt
import argparse
import sys

# Parse Command line Arguments
parser = argparse.ArgumentParser()
parser.add_argument('-',type=str, dest='input',help='Choose the parameter. Options: Sensitivity [A_eff/T_sys], T_sys [System Temperature], Eff [Aperture Efficiency], Gain, P_out [Power output per GHz ], T_rx [Reciever Temperature], T_sky [Sky Temperature], T_spill [Spillover Temperature], A_eff [Effective Area]. Default = Sensitivity',default='Sensitivity')
parser.add_argument('-plot', type=str, dest='plot', help='Choose to plot data vs Frequeancy or not. Default=yes',default="yes")
parser.add_argument('-file', type=str, dest='file', help='Choose to output to textfile with frequency or not. Default=yes', default="yes")
parser.add_argument('-array',type=str, dest='array', help='Choose how much of the array to use. Options: core, main, full, SBA, LBA. Default = full', default='full')
parser.add_argument('-scale',type=str, dest='scale',help="Choose log or linear scale for graph. Default = log", default='log')
args = parser.parse_args()

# Set values from command line inputs
parameter = str.lower(args.input)
parameter = parameter.replace("_","")
plot = str.lower(args.plot)
txtfile = str.lower(args.file)
array = str.lower(args.array)
scale = str.lower(args.scale)

# Process input files to produce lists of values
def process(parameter):
    ### Takes given parameter, reads data from file, and returns list of data and list of corresponding freqencies

    if parameter == "sensitivity":
        file = open('data_2021/Aeff-Tsys.txt','r')  # Effective Area over System Temperature (m^2/K) for 1 18m dish
    elif parameter == "tsys":
        file = open('data_2021/Tsys.txt','r')   # System Temperature (K)
    elif parameter == "eff":
        file = open('data_2021/eff.txt','r')  # Aperture Effieciency
    elif parameter == "gain":
        file = open('data_2021/gain.txt','r') # Gain (dB)
    elif parameter == "pout":
        file = open('data_2021/Pout.txt','r') # Power output per GHz (dBm/GHz)
    elif parameter == "trx":
        file = open('data_2021/Trx.txt','r') # Reciever Temperature (K)
    elif parameter == "tsky":
        file = open('data_2021/Tsky.txt','r')   # Sky Temperature (K)
    elif parameter == "tspill":
        file = open('data_2021/Tspill.txt','r')   # Spillover Temperature (K)
    else:
        file = 0

    if file != 0:
        
        freq = open('data_2021/freq.txt','r') # Frequency (GHz)

        f1 = freq.readlines()
        f = []
        for i in f1:
            f.append(float(i.strip()))

        data1 = file.readlines()
        data = []
        for i in data1:
            data.append(float(i.strip()))

        return f, data

    else:
        print("Please choose from options: Sensitivity [A_eff/T_sys], T_sys [System Temperature], Eff [Aperture Efficiency], Gain, P_out [Power output per GHz ], T_rx [Reciever Temperature], T_sky [Sky Temperature], tspill [Spillover Temperature].")
        return 0,0


# Case: A_eff/T_sys and A_eff depend on how much of array in use
def get_sens(array,x="sens"):
    ### Takes A_eff/T_sys for 18 dish and calculates A_eff and A_eff/T_sys for each sub array

    f, A_T = process("sensitivity") # get list of A_eff/T_sys values
    f, T = process("tsys") # get list of T_sys values

    A_18 = [] # list of A_eff values for 1 18m dish
    for i in range(66):
        A_18.append(A_T[i]*T[i])

    A_6 = [] # list of A_eff values for 1 6m dish
    for i in A_18:
        A_6.append(i/9)
    
    # N_dishes for each sub array      
    n_6 = 0
    if array == "full":
        n_18 = 244
        n_6 = 19
        get_sens.array_name = "Full Array (263 dishes)"
    elif array == "main":
        n_18 = 214
        get_sens.array_name = "Main Array (214 dishes)"
    elif array == "core":
        n_18 = 94
        get_sens.array_name = "Core (94 dishes)"
    elif array == "sba":
        n_18 = 0
        n_6 = 19
        get_sens.array_name = "SBA (19 6m dishes)"
    elif array == "lba":
        n_18 = 30
        get_sens.array_name = "LBA (30 dishes)"

    # get effective area
    A_eff = []
    for i in range(66):
        A_eff.append(n_18*A_18[i] + n_6*A_6[i])
    
    # get sensitivity
    sens = []
    for i in range(66):
        sens.append(A_eff[i]/T[i])

    if x == "sens":
        return f, sens
    elif x == "aeff":
        return f, A_eff
       

# Produce txtfiles for plotting
def output_file(parameter,f,data):
    ### Takes a parameter and outputs a space-delimited .txt file of that parameter at each frequency

    if parameter == "sensitivity":
        file = "nglva_sens.txt"
    elif parameter == "tsys":
        file = "nglva_tsys.txt"
    elif parameter == "eff":
        file = "nglva_eff.txt"
    elif parameter == "gain":
        file = "nglva_gain.txt"
    elif parameter == "pout":
        file = "ngvla_pout.txt"
    elif parameter == "trx":
        file = "ngvla_trx.txt"
    elif parameter == "tsky":
        file = "ngvla_tsky.txt"
    elif parameter == "tspill":
        file = "ngvla_tspill.txt"
    else:
        file = 0

    if file != 0:
        
        output = open(file, 'w')
        
        for i in range(len(f)):
            newline = str(f[i]) + ' ' + str(data[i]) + '\n'
            output.write(newline)


# Plot in each band
def plot_parameter(parameter,scale,f,data):
    ### Takes a parameter and plots it against frequency in each band
    
    if parameter == "sensitivity":
        plt.title("Sensitivity vs Frequency: " + str(get_sens.array_name))
        plt.ylabel("A_eff/T_sys (m^2/K)")
    elif parameter == "tsys":
        plt.title("System Temperature vs Frequency")
        plt.ylabel("System Temperature (K)")
    elif parameter == "eff":
        plt.title("Aperture Efficiency vs Frequency")
        plt.ylabel("Aperture Efficiency")
    elif parameter == "gain":
        plt.title("Gain vs Frequency")
        plt.ylabel("Gain(dB)")
    elif parameter == "pout":
        scale = "linear"
        plt.title("Power Output per GHz vs Frequency")
        plt.ylabel("Power Output per GHz(dBm/GHz)")
    elif parameter == "trx":
        plt.title("Reciever Temperature vs Frequency")
        plt.ylabel("Reciever Temperature (K)")
    elif parameter == "tsky":
        plt.title("Sky Temperature vs Frequency")
        plt.ylabel("Sky Temperature (K)")
    elif parameter == "tspill":
        plt.title("Spillover Temperature vs Frequency")
        plt.ylabel("Spillover Temperature (K)")
    elif parameter == "aeff":
        plt.title("Effective Area vs Frequency: " + str(get_sens.array_name))
        plt.ylabel("Effective Area (m^2)")
    else:
        parameter = 0

    if parameter != 0:
        
        if scale == "log":
            plt.loglog(f[0:11],data[0:11],linestyle='-', marker='o', color='r',label="Band 1")
            plt.loglog(f[11:22],data[11:22],linestyle='-', marker='o', color='g',label="Band 2")
            plt.loglog(f[22:33],data[22:33],linestyle='-', marker='o', color='b',label="Band 3")
            plt.loglog(f[33:44],data[33:44],linestyle='-', marker='o', color='c',label="Band 4")
            plt.loglog(f[44:55],data[44:55],linestyle='-', marker='o', color='m',label="Band 5")
            plt.loglog(f[55:66],data[55:66],linestyle='-', marker='o', color='y',label="Band 6")
        elif scale == "linear":
            plt.plot(f[0:11],data[0:11],linestyle='-', marker='o', color='r',label="Band 1")
            plt.plot(f[11:22],data[11:22],linestyle='-', marker='o', color='g',label="Band 2")
            plt.plot(f[22:33],data[22:33],linestyle='-', marker='o', color='b',label="Band 3")
            plt.plot(f[33:44],data[33:44],linestyle='-', marker='o', color='c',label="Band 4")
            plt.plot(f[44:55],data[44:55],linestyle='-', marker='o', color='m',label="Band 5")
            plt.plot(f[55:66],data[55:66],linestyle='-', marker='o', color='y',label="Band 6")

        plt.xlabel("Frequency (GHz)")
        plt.legend()
        plt.grid()
        plt.show()

# function to sort data & call other finctions
def main(parameter):
    if parameter == "sensitivity":
        f, data = get_sens(array)
    elif parameter == "aeff":
        f, data = get_sens(array,"aeff")
    else:
        f, data = process(parameter)

    if plot == 'yes':
        plot_parameter(parameter,scale,f,data)
    
    if txtfile == 'yes':
        output_file(parameter,f,data)

main(parameter)
