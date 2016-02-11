
import pyaudio
import numpy
import scipy

class APU:
#self contained audio input and processing unit; theoretically it should be possible to have a few running in tandem, but I lack the microphones for that. 

  import pyaudio
  import numpy
  import scipy
  import scipy.signal

  MONO=1
  BUTTERWORTH_ORDER=5
  DEFAULT_SAMPLE_SIZE=1024

  __pyaud=None
  stream=None

  mic_index=None

  sample_size=0
  frequency=0.0
  sampling_rate=0

  #high cuts off bass, low cuts off treble, together they form a bandpass filter.
  high_pass=4
  low_pass=10000

  def __init__(self): #wait for the user to pick microphone and start recording before initializing everything.
    self.__pyaud=pyaudio.PyAudio()
    self.sample_size=self.DEFAULT_SAMPLE_SIZE
    #TODO: complain if there's no input device

  def getPyAudio(self):
    return(self.__pyaud)
  
  def getStream(self):
    return(self.stream)

  
  def getMicrophoneList(self):
    retval={}
    adict=None
    for devindex in range(self.getPyAudio().get_device_count()):
      adict=self.getPyAudio().get_device_info_by_index(devindex)
      #print(adict)
      if(bool(int(adict["maxInputChannels"]))):
        retval[adict["name"]]=adict["index"]
    return(retval)      
    
  def setMicrophone(self,index):
    self.mic_index=index
    if(self.stream):
      self.stop()

  def getSampleSize(self):
    return(self.sample_size)
  
  def getFrequency(self):
    return(self.frequency)
  
  def getSamplingRate(self):
    return(self.sampling_rate)  
  
  def setSampleSize(self, size):
    self.sample_size=size
    self.start()
  
  def setSamplingRate(self, rate):
    self.sampling_rate=rate  
    self.start()

  def setHighPass(self, freq):
    self.high_pass=freq
  
  def setLowPass(self, freq):
    self.low_pass=freq

  def calcFrequency(self):
    peakfreq=0.0
    if(self.stream):
      readbuf=self.stream.read(self.sample_size)

      tdarray=numpy.fromstring(readbuf, dtype=numpy.float32)

      fftarray=numpy.fft.fft(tdarray)

      nyquist=.5*self.sampling_rate

      denom,numer=scipy.signal.butter(self.BUTTERWORTH_ORDER,[self.high_pass/nyquist, self.low_pass/nyquist],btype="band")  
      ffftarray=scipy.signal.lfilter(denom,numer,fftarray)

      freqarray=numpy.fft.fftfreq(tdarray.size)

      ind=numpy.argmax(numpy.abs(ffftarray)**2)

      peakfreq=numpy.abs(freqarray[ind])*self.sampling_rate
      #print(freq*sampling_rate)
      self.frequency=peakfreq
    return peakfreq
  
  
  def start(self): 
    if(self.stream):
      self.stop()  
    if(not self.mic_index):
      self.mic_index=int(self.getPyAudio().get_default_input_device_info()["index"])
      #print(self.mic_index)
      self.setSamplingRate(int(self.getPyAudio().get_device_info_by_index(self.mic_index)["defaultSampleRate"]))
      #print(self.getSamplingRate())
    self.stream=self.getPyAudio().open(format=pyaudio.paFloat32,channels=self.MONO,input_device_index=self.mic_index,rate=self.sampling_rate,input=True, frames_per_buffer=self.sample_size)
    
  def stop(self):
    self.stream.stop_stream()
    self.stream.close() 

  def implode(self):   
    self.stop()
    self.getPyAudio().terminate()

  def toggle(self):
    if(self.stream):
      self.stop()
    else:
      self.start()

  def test(self):
    while(True):
      self.calcFrequency()
      print(self .getFrequency())
      
