import csv
import glob
import time
import urllib

def load_irregular(i):
				
	with open('count'+str(i)+'.csv','rb') as f_pred:
		reader_pred = csv.reader(f_pred)
		qrs_peaks_indices=[]
		# predictions=[]
		
		for row in reader_pred:
			qrs_peaks_indices.append(int(row[0]))
			# predictions.append(int(row[1]))
	with open('raw_sig'+str(i)+'.csv','rb') as f_sig:
		reader_pred = csv.reader(f_sig)
		ecg_signal = []
		for row in reader_pred:
			ecg_signal.append(row[0])

	print(qrs_peaks_indices[0])

	return ecg_signal,qrs_peaks_indices


def R_rate():

	with open('R_rate'+'.csv','rb') as f_pred:
		reader_pred = csv.reader(f_pred)
		r_rate=[]
		# predictions=[]
		
		for row in reader_pred:
			r_rate.append(int(row[0]))


		return r_rate

def UPLOAD():
	with open("upload.txt",'r') as FILE_NO:
			a=FILE_NO.read()
			# print(a)
	ecg_signal,qrs_peaks_indices=load_irregular(int(a)-1)
	rr=R_rate()
	print(ecg_signal[0])
	for i in range(len(ecg_signal)):
		dd=urllib.urlopen("https://api.thingspeak.com/update?api_key=ALWF3S2P31EZCW34&field1="+str(ecg_signal[i]))
		print(dd)

	for j in range(len(rr)):
		data=urllib.urlopen("https://api.thingspeak.com/update?api_key=ALWF3S2P31EZCW34&field2="+str(rr[j]))
		print(data)
	



if __name__=="__main__":
	UPLOAD()