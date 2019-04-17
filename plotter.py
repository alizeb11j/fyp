import matplotlib.pyplot as plt
import matplotlib.animation as animation
import csv
import glob
import numpy as np
import pandas as pd
import time


begin = 0
file_no = 0

fig=plt.figure()
ax1=fig.add_subplot(1,1,1)

# def merge1():
# 	all_files = glob.glob("C:\\Users\\Ali Zeb\\Downloads\\Compressed\\diyECG-1opAmp-master\\diyECG-1opAmp-master\\software\\*.csv")     
# 	df_from_each_file = (pd.read_csv(f,header = [0]) for f in all_files)
# 	concatenated_df   = pd.concat(df_from_each_file, ignore_index=True,axis=0, join='inner')
# 	concatenated_df.to_csv("output1.csv",index=None)

all_files=glob.glob('count*.csv')
	
def load_sig(i):
				
	with open('count'+str(i)+'.csv','r') as f_pred:
		reader_pred = csv.reader(f_pred)
		qrs_peaks_indices=[]
		predictions=[]
		
		for row in reader_pred:
			qrs_peaks_indices.append(int(row[0]))
			predictions.append(int(row[1]))
	with open('raw_sig'+str(i)+'.csv','r') as f_sig:
		reader_pred = csv.reader(f_sig)
		ecg_signal = []
		for row in reader_pred:
			ecg_signal.append(row[0])

	return ecg_signal,qrs_peaks_indices,predictions	

"""
Show plots with signal data, r-peaks and predictions

N       Green
SVEB    Red
VEB     Pink
F       Yellow
Q       Blue

When the samples are not associated to a beat are displayed in black.
"""
def show_signal_and_predictions(ecg_signal,qrs_peaks_indices,predictions):
    begin = 0    
    # Add beats and its predictions represented by different colours
    colors = ["green", "red", "pink", "yellow", "blue"]
    # print len(qrs_peaks_indices)
    for r in range(0, len(qrs_peaks_indices)):
        # Original ECG RAW
        R_peak = int(qrs_peaks_indices[r])
        y = ecg_signal[begin:R_peak]
        x = range(begin,R_peak)
        
        ax1.set_title('Classified Beats', fontsize=16)
  
        ax1.axvline(x = R_peak, color = 'k', linestyle='--')
        ax1.plot(x,y, color=colors[predictions[r]], linewidth=1.0, linestyle="-")
    	# print begin,R_peak
        begin =  R_peak
    #Finding Heart Beat
    d = (qrs_peaks_indices[len(qrs_peaks_indices)-1]-qrs_peaks_indices[0])/len(qrs_peaks_indices)
    heart_rate = 60*360/d
    print ('Beats per min:',heart_rate)

        	

def animate(a):

	global begin, file_no
	colors = ["green", "red", "pink", "yellow", "blue"]
	if file_no>=len(all_files):
		file_no=0
	begin=0
	ax1.clear()
	ecg_signal,qrs_peaks_indices,predictions=load_sig(file_no)
	show_signal_and_predictions(ecg_signal,qrs_peaks_indices,predictions)  
	file_no+=1
	
# merge1()
anim=animation.FuncAnimation(fig,animate,interval=900)

plt.show()









