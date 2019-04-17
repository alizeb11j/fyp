
from __future__ import print_function
from QRS_detector import QRSDetectorOffline
from QRS_classifier import QRSClassifier
import sys
import matplotlib.pyplot as plt
import csv
import glob
import time

def write_signal(count,low,high, ecg_signal):
    print('running',count)
    # raw_input()
    with open("testing\\count" + str(count) + ".csv","wb") as f:
            writer = csv.writer(f)

            qrs_detector = QRSDetectorOffline(ecg_data_raw = ecg_signal[low:high], fs = fs,\
                                      verbose=False, plot_data=False,    \
                                      show_plot=False)
            qrs_classifier = QRSClassifier(svm_models_path = '..\\svm_models', \
                    ecg_data = qrs_detector.ecg_data, \
                    qrs_peaks_indices = qrs_detector.qrs_peaks_indices, \
                    min_A = -1024, max_A = 1024, verbose=False)
            
            

            for j in range(len(qrs_detector.qrs_peaks_indices)):
                    writer.writerow([qrs_detector.qrs_peaks_indices[j]] + [qrs_classifier.predictions[j]])
            #Finding Heart Beat
            d = (qrs_detector.qrs_peaks_indices[len(qrs_detector.qrs_peaks_indices)-1]-qrs_detector.qrs_peaks_indices[0])/len(qrs_detector.qrs_peaks_indices)
            heart_rate = 60*360/d
            print ('Beats per min:',heart_rate)
    with open("testing\\raw_sig" + str(count) + ".csv","wb") as f:
        writer = csv.writer(f)
        for j in range(low,high):
            writer.writerow([ecg_signal[j]])                
                    
         
"""
Read signal from text file
"""
def load_signal( filename ):
    # Read data from file .csv 
    ecg_signal = list()
    with open(filename,"r") as f:
        reader = csv.reader(f)
        for row in reader:
            ecg_signal.append(float(row[0]))

    fs = ecg_signal[0]
    min_A = ecg_signal[1]
    max_A = ecg_signal[2]
    n_bits = ecg_signal[3]
    ecg_signal = ecg_signal[4:]   
    
    return ecg_signal, fs, min_A, max_A, n_bits


def show_signal_and_predictions(qrs_detector, qrs_classifier,count,low,high):
    # Show data
    begin = 0
    begin_360 = 0
    colors = ["green", "red", "pink", "yellow", "blue"]

    predictions = qrs_classifier.predictions

    # Data at original frequency sampling 

    fig, axarr = plt.subplots(2, sharex=True)
    # print len(qrs_detector.ecg_data_raw)
    # Add beats and its predictions represented by different colours
    for r in range(0, len(qrs_detector.qrs_peaks_indices)):
        # Original ECG RAW
        R_peak = int(qrs_detector.qrs_peaks_indices_fs[r])
        x = range(begin, R_peak)
        y = qrs_detector.ecg_data_raw[begin:R_peak]
        # print 'x',len(x),'y',len(y)
        

        axarr[0].set_title('ECG RAW', fontsize=16)
        #axarr[0].grid(which='both', axis='both', linestyle='--')
        axarr[0].axvline(x = R_peak, color = 'k', linestyle='--')
        axarr[0].plot(x, y, color=colors[predictions[r]], linewidth=2.5, linestyle="-")
        begin =  R_peak

        # Preprocesed ECG data sampled at 360Hz
        R_peak_360 = int(qrs_detector.qrs_peaks_indices[r])
        x = range(begin_360, R_peak_360)
        y = qrs_detector.ecg_data[begin_360:R_peak_360]
        print ('R peak: ', R_peak, ' predicted class : ', predictions[r])

        axarr[1].set_title('Filtered and normalized ECG 360Hz', fontsize=16)
        #axarr[0].grid(which='both', axis='both', linestyle='--')
        axarr[1].axvline(x = R_peak_360, color = 'k', linestyle='--')
        axarr[1].plot(x, y, color=colors[predictions[r]], linewidth=2.5, linestyle="-")
        begin_360 =  R_peak_360

            
          
    # Add from last detected peak to the final signal in black
    last_point = len(qrs_detector.ecg_data_raw)
    x = range(begin, last_point)
    y = qrs_detector.ecg_data_raw[begin:last_point]

    axarr[0].set_title('ECG RAW', fontsize=16)
    axarr[0].axvline(x = last_point, color = 'k', linestyle='--')
    axarr[0].plot(x, y, color="black", linewidth=2.5, linestyle="-")

    # Preprocesed ECG data sampled at 360Hz
    last_point = len(qrs_detector.ecg_data)
    x = range(begin_360, last_point)
    y = qrs_detector.ecg_data[begin_360:last_point]

    axarr[1].set_title('Filtered and normalized ECG 360Hz', fontsize=16)
    axarr[1].axvline(x = last_point, color = 'k', linestyle='--')
    axarr[1].plot(x, y, color="black", linewidth=2.5, linestyle="-")


    plt.show()

if __name__ == "__main__":

    if len(sys.argv) < 2:
	    print ('Error an argument is needed! \n Example of use:\n\t python example.py ..\\data\\220.csv')
	    sys.exit()
    
    ecg_signal, fs, min_A, max_A, n_bits = load_signal(sys.argv[1])
    # 
    if len(ecg_signal)>2100:
        for i in range(len(ecg_signal)//2100):
            write_signal(i,(i*2100),(i*2100)+2100,ecg_signal)
       
    else:
        write_signal(0,0,2100,ecg_signal)
    # write_signal(0,0,len(ecg_signal),ecg_signal)
        # print(len(ecg_signal))
    # write_signal(0,0,20000,ecg_signal)
    # write_signal(1,20000,39999,ecg_signal)








































    #######################################################################
    # Detect R-peak points
    # if fs != 360 ecg_data will be resampled
    # qrs_detector = QRSDetectorOffline(ecg_data_raw = ecg_signal, fs = fs,\
    #                                   verbose=False, plot_data=False,    \
    #                                   show_plot=False)

    # qrs_detector.ecg_data_raw             signal at original sampling frecuency
    # qrs_detector.ecg_data                 signal resampled at 360Hz
    # qrs_detector.qrs_peaks_indices        contains R peaks at 360 Hz sampling frequency
    # qrs_detector.qrs_peaks_indices_fs     contains R peaks at original sampling frequency



    #######################################################################
    # Classify Beats 
    # qrs_classifier = QRSClassifier(svm_models_path = '../svm_models', \
    #                 ecg_data = qrs_detector.ecg_data, \
    #                 qrs_peaks_indices = qrs_detector.qrs_peaks_indices, \
    #                 min_A = min_A, max_A = max_A, verbose=False) 

    # qrs_detector.ecg_data                 signal resampled at 360Hz and filtered
    # qrs_classifier.predictions            class prediction for beat [0-4]
    #                                       Following AAMI-Recomendations: 
    #                                       N, SVEB, VEB, F, Q



    # all_files=glob.glob('testing/count'+'*.csv')

    
    # count=0
    # for file in all_files:
    #     with open('testing/Predictions'+str(count)+'.csv', 'wb') as f_out:
    #             writer = csv.writer(f_out)
    #             if count==0:
    #                 for i in range(0,inds[count]):
    #                     writer.writerow([qrs_detector.qrs_peaks_indices[i]] + [qrs_classifier.predictions[i]])
                    
    #             else:
    #                 for i in range(inds[count-1],inds[count]):
    #                     writer.writerow([qrs_detector.qrs_peaks_indices[i]] + [qrs_classifier.predictions[i]])

    #     count+=1            
    # print inds, qrs_detector.qrs_peaks_indices                




    #######################################################################
    # Display results
    # show_signal_and_predictions(qrs_detector, qrs_classifier)    
