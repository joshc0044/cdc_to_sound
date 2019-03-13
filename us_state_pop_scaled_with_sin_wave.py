import numpy as np
import matplotlib.pyplot as plt
import wave
import struct

cdcData = open('processedCDC.txt')
#data = [line.strip() for line in cdcData]
#print(data)

# get 
col_names = ['state', 'July 1999', 'April 2000', 'July 2001', 'July 2002', 'July 2003', 'July 2004']
numpyTest = np.genfromtxt(cdcData,names=col_names,dtype="S20,i8,i8,i8,i8,i8,i8")
states = numpyTest.getfield('S20')

stateTuple = [x for x in numpyTest]
stateMatrix = [[x for x in test] for test in stateTuple]

justNums = [item[1:] for item in stateMatrix]
#plt.matshow(justNums)
#plt.show()
cdcData.close()

## create some kind of sound representation
# ref: https://www.pythonforengineers.com/audio-and-digital-signal-processingdsp-in-python/
# frequency is the number of times a wave repeats a second
 
frequency = 1000
 
noisy_freq = 50
 
num_samples = 48000
 
# The sampling rate of the analog to digital convert
 
sampling_rate = 48000.0
  
amplitude = 16000
#dtype=[('state', 'S15'), ('July1999', 'i8'), ('April2000', 'i8'), ('July2001', 'i8'), ('July2002', 'i8'), ('July2003', 'i8'), ('July2004', 'i8')])

#testAudio = justNums[:,0]/abs(justNums[:,0]).max()
# from https://stackoverflow.com/questions/1735025/how-to-normalize-a-numpy-array-to-within-a-certain-range

testAudio = justNums.copy()
testAudio /= np.max(np.abs(justNums),axis=0)
#print(testAudio)

sine_wave = [np.sin(2 * np.pi * frequency * x1 / sampling_rate) for x1 in range(num_samples)]
#print(sine_wave[0:10])
print(list(zip(testAudio,sine_wave))[-3:])
wave_with_pop = list(zip(testAudio,sine_wave))
#for pair in wave_with_pop[:25]:
	#print(pair)
	#for item in pair[0]:
		#print(item*pair[1])
		


file = "cdc_pop_test.wav"


nframes=num_samples
 
comptype="NONE"
 
compname="not compressed"
 
nchannels=1
 
sampwidth=2

wav_file=wave.open(file, 'w')
 
wav_file.setparams((nchannels, sampwidth, int(sampling_rate), nframes, comptype, compname))

#for s in sine_wave:
#   wav_file.writeframes(struct.pack('h', int(s*amplitude)))
for pair in wave_with_pop:
	#print(pair)
	for item in pair[0]:
		#print(item*pair[1])
		wav_file.writeframes(struct.pack('h', int(item*pair[1]*amplitude)))
scaledPop = [[item*pair[1]*amplitude for item in pair[0]] for pair in wave_with_pop]
plt.plot(scaledPop)
plt.show()
###