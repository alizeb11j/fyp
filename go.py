"""
diyECG GUI for monitoring live ECG through sound card input (by Scott Harden).
If you haven't built the circuit, test this software by playing demo_ecg.wav
while you run this software. If you don't use a virtual audio cable to connect
the output (speaker jack) to the input (default microphone jack), consider
running an actual cable to connect these two.
"""

from PyQt4 import QtGui,QtCore
import sys
import ui_main
import numpy as np
import pyqtgraph
import swhear
import time
import pyqtgraph.exporters
import webbrowser
import csv
import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import matplotlib.animation as animation

COUNTER=0
count=0
begin = 0
file_no = 0
fig=plt.figure()
ax1=fig.add_subplot(1,1,1)
# 	#Finding Heart Beat
# 	d = (qrs_peaks_indices[len(qrs_peaks_indices)-1]-qrs_peaks_indices[0])/len(qrs_peaks_indices)
# 	heart_rate = 60*360/d
# 	print ('Beats per min:',heart_rate)	
class ExampleApp(QtGui.QMainWindow, ui_main.Ui_MainWindow):
    def __init__(self, parent=None):
        pyqtgraph.setConfigOption('background', 'w') #before loading widget
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)
        self.grECG.plotItem.showGrid(True, True, 0.7)
        # self.grECG1.plotItem.showGrid(True, True, 0.7)
        self.btnSave.clicked.connect(self.saveFig)
        self.btnSite.clicked.connect(self.website)
        stamp="ECG Output"
        self.stamp = pyqtgraph.TextItem(stamp,anchor=(-.01,1),color=(150,150,150),
                                        fill=pyqtgraph.mkBrush('w'))
        self.ear = swhear.Ear(chunk=int(1000)) # determines refresh rate
        # optionally you can manually set the audio input device to use like this:
        self.ear = swhear.Ear(chunk=int(100), device=0) # use audio input device 5
        if len(self.ear.valid_input_devices()):
            self.ear.stream_start()
            self.lblDevice.setText(self.ear.msg)
            self.update()
    


    def closeEvent(self, event):
        self.ear.close()
        event.accept()

  #   def load_sig(self,i,rangee):
				
		# with open('testing\\count'+str(i)+'.csv','rb') as f_pred:
		# 	reader_pred = csv.reader(f_pred)
		# 	qrs_peaks_indices=[]
		# 	predictions=[]
			
		# 	for row in reader_pred:
		# 		qrs_peaks_indices.append(int(row[0]))
		# 		predictions.append(int(row[1]))
		# with open('testing\\raw_sig'+str(i)+'.csv','rb') as f_sig:
		# 	reader_pred = csv.reader(f_sig)
		# 	ecg_signal = []
		# 	for row in reader_pred:
		# 		ecg_signal.append(row[0])
		# begin = 0
		# # Add beats and its predictions represented by different colours
		# colors = ["g", "r", "m", "y", "b"]
		# # print len(qrs_peaks_indices)
		# for r in range(0, len(qrs_peaks_indices)):
		#     # Original ECG RAW
		#     R_peak = int(qrs_peaks_indices[r])
		#     y = ecg_signal[begin:R_peak]
		#     x = range(begin,R_peak)
		#     self.grECG1.plotItem.setRange(xRange=[0,self.ear.maxMemorySec],
  #                           yRange=[-rangee,rangee],padding=0)
		#     self.grECG1.plot(x,y,clear=True,pen=pyqtgraph.mkPen(color=colors[predictions[r]], width=2),antialias=True)
		#     self.grECG1.plotItem.setTitle(self.lineTitle.text(),color=(0,0,0))
		#     self.stamp1.setPos(0,-rangee)
		#     self.grECG1.plotItem.addItem(self.stamp)
		
	        # ax1.set_title('Classified Beats', fontsize=16)
	  
	        # ax1.axvline(x = R_peak, color = 'k', linestyle='--')
	        # ax1.plot(x,y, color=colors[predictions[r]], linewidth=2.5, linestyle="-")
	        # begin =  R_peak



		    # # self.grECG.plotItem.setRange(xRange=[0,self.ear.maxMemorySec],
                            # yRange=[-self.Yscale,self.Yscale],padding=0)
            
		    # ax1.set_title('ECG RAW', fontsize=16)

		    # ax1.axvline(x = R_peak, color = 'k', linestyle='--')
		    # ax1.plot(x,y, color=colors[predictions[r]], linewidth=2.5, linestyle="-")
			# print begin,R_peak
		    




    def saveFig(self):
        global count
        fname="ECG_%d.csv"%count
        exp = pyqtgraph.exporters.CSVExporter(self.grECG.plotItem)       
        exp.export(fname)
        print("saved",fname)
        # Take out the Column With values of voltage
        df = pd.read_csv(fname, usecols = [1])
        df.to_csv('test'+str(count)+'.csv',index=None,header=['8000'])
        count+=1

                       
    def update(self):
    	global count,begin, file_no,COUNTER
    	all_files=glob.glob('testing\\count*.csv')
        t1,timeTook=time.time(),0
        
        if len(self.ear.data) and not self.btnPause.isChecked():
            freqHighCutoff=0
            if self.spinLowpass.value()>0:
                freqHighCutoff=self.spinLowpass.value()
            data=self.ear.getFiltered(freqHighCutoff)
            if self.chkInvert.isChecked():
                data=np.negative(data)
            if self.chkAutoscale.isChecked():
                self.Yscale=np.max(np.abs(data))*1.1

            self.grECG.plotItem.setRange(xRange=[0,self.ear.maxMemorySec],
                            yRange=[-self.Yscale,self.Yscale],padding=0)
            self.grECG.plot(np.arange(len(data))/float(self.ear.rate),data,clear=True,
                            pen=pyqtgraph.mkPen(color='g', width=2),antialias=True)
          
            # self.grECG.plotItem.setTitle(self.lineTitle.text(),color=(0,0,0))
            # self.stamp.setPos(0,-self.Yscale)
            # self.grECG.plotItem.addItem(self.stamp)

            # self.grECG1.plotItem.setRange(xRange=[0,self.ear.maxMemorySec],
            #                 yRange=[-self.Yscale,self.Yscale],padding=0)
            # self.grECG1.plot(np.arange(len(data))/float(self.ear.rate),data,clear=True,
            #                 pen=pyqtgraph.mkPen(color='g', width=2),antialias=True)
          
            # self.grECG1.plotItem.setTitle(self.lineTitle.text(),color=(0,0,0))
            # self.grECG1.plotItem.addItem(self.stamp)
           
            # COUNTER+=1
            # while COUNTER>=100:
	           #  fname="..\\TEMP\\ECG_%d.csv"%count
	           #  exp = pyqtgraph.exporters.CSVExporter(self.grECG.plotItem)
	           #  exp.export(fname)
	           #  # Take out the Column With values of voltage
	           #  df = pd.read_csv(fname, usecols = [1])
	           #  df.to_csv('test'+str(count)+'.csv',index=None,header=[str(self.ear.rate)])
	           #  os.system("python example_org.py"+" "+"test"+str(count)+".csv")
	           #  count+=1
	           #  ax1.clear()
	           #  self.load_sig(file_no,self.Yscale)
	            # self.show_signal_and_predictions(ecg_signal,qrs_peaks_indices,predictions)  
	           
	            # os.system("python plotter.py")

	           #  self.grECG1.plotItem.setRange(xRange=[0,self.ear.maxMemorySec],
	           #                  yRange=[-self.Yscale,self.Yscale],padding=0)
	           #  self.grECG1.plot(np.arange(len(data))/float(self.ear.rate),data,clear=True,
	           #                  pen=pyqtgraph.mkPen(color='g', width=2),antialias=True)
	          
	           #  self.grECG1.plotItem.setTitle(self.lineTitle.text(),color=(0,0,0))
	           #  self.stamp1.setPos(0,-self.Yscale)
	           #  self.grECG1.plotItem.addItem(self.stamp)
				
	            # COUNTER-=10
	            
				# if file_no>=len(all_files):
				# 	file_no=0
				# ecg_signal,qrs_peaks_indices,predictions=load_sig(file_no)
				# show_signal_and_predictions(ecg_signal,qrs_peaks_indices,predictions)
				# file_no+=1

		        
            timeTook=(time.time()-t1)*1000
            print("plotting took %.02f ms"%(timeTook))

        msTillUpdate=int(self.ear.chunk/self.ear.rate*1000)-timeTook
        QtCore.QTimer.singleShot(max(0,msTillUpdate), self.update)

    def website(self):
        webbrowser.open("http://www.SWHarden.com")

if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    app.exec_()
