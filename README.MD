README 

Audio Frequency Analyzer

By Manfred Chan, mchan21@binghamton.edu

A python shell tool to determine the fundamental frequency of a musical note using pyaudio, numpy and scipy. 
Last updated in 2012.

---

To run:

apu=APU() 		#create an apu object
apu.getMicrophoneList() #find the correct microphone on your system
apu.setMicrophone(int)  #select microphone
apu.start()		#open audio resources
apu.test()		#continuously prints the frequency, terminate with a keyboard interrupt
apu.stop()		#disconnects from microphone
apu.implode()		#disconnects from microphone and shuts down pyaudio server

---

Full method list, with return type

//directly accessing pyaudio or the streams
pyaudio.PyAudio getPyAudio();
stream.Stream getStream();

//microphones
dict getMicrophoneList();               //pyaudio returns I/O device data in dicts
null setMicrophone(int mic_index);      //pyaudio uses ints as I/O device indices

//usage
float calcFrequency();                  //Accesses microphone, calculates frequency, and returns it.
float getFrequency();			//returns last calculated frequency
null test();				//repeatedly prints calcFrequency(); must be killed by a keyboard interrupt or similar event

//starting/restarting/stopping
null start();                           //stream params are immutable; use this to restart streams after setting changes
null stop();				//Disconnects from microphone
null implode();                         //Disconnects from microphone and shuts down the pyaudio server

//Tweaking these is experimental.
float getSampleSize();
int getSamplingRate();                  //Even though the standard is 44100.0, pyaudio complains if it's not an int.
null setSampleSize(int size);
null setSamplingRate(int rate);
null setHighPass(int freq);
null setLowPass(int freq);


