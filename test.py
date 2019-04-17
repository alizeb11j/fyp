from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.lang import Builder
# from kivy.garden.knob import  Knob
import csv
import glob
import time




kv = """

<CLASS_DISP>:
	GridLayout:
	    pos: root.pos
	    size: root.size
	    cols: 2
	    spacing: 100
	    padding: 50

	    Label:
			id:label1
			font_size:20
			color:1,1,1,1
			bold:True
			text: root.TEXT
			size_hint:(0.5, 0.5)
			pos_hint:(0.5, 0.5)
		


"""

Builder.load_string(kv)
all_files=glob.glob('count*.csv')
	


def load_sig(i):
				
	with open('count'+str(i)+'.csv','rb') as f_pred:
		reader_pred = csv.reader(f_pred)
		predictions=[]
		
		for row in reader_pred:
			predictions.append(int(row[1]))

	return predictions

# def load_irregular(i):
				
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



class CLASS_DISP(GridLayout):
	TEXT = StringProperty('Normal')
	TYPE=["Normal","Supraventicular","Ventricular","Fusion","Unknown Beat"]
	
	def __init__(self,**kwargs):

		super(CLASS_DISP,self).__init__(**kwargs)
		
		a=0
		with open("test.txt",'r') as FILE_NO:
			a=FILE_NO.read()
			predictions=load_sig(a)
			if int(a)>=len(all_files):
				a=int(a)
				a=0
		self.event = Clock.schedule_interval(self.DISP,0.5)
		# def on_knob(self, value):
  #           print "hi"
  #       self.knob1.bind(on_knob=on_knob)


		


	def DISP(self, *args):	
		with open("test.txt",'r') as FILE_NO:
			a=FILE_NO.read()
			# print(a)
			predictions=load_sig(int(a)-1)	
			self.TEXT=self.TYPE[max(predictions[1:])]
			# print(self.TEXT)
			if (self.TEXT!="Normal"):
				with open('upload.txt','w') as FILE_NO:
					FILE_NO.write(str(a))
				



	

class CLASS(App):
	def build(self):
		return CLASS_DISP()


if __name__ =="__main__":
	CLASS().run()
