from setuptools import setup

setup(name='voice_assistant',
      version='0.2.0',
      description='Python library to build a Voice Assistant',
      url='https://github.com/noviluni/voice_assistant',
      author='Marc H.',
      author_email='noviluni@gmail.com',
      license='MIT',
      packages=['voice_assistant'],
      install_requires=[
          'SpeechRecognition==3.8.1',
          'google-speech==1.1.0',
          'PyAudio==0.2.11',
      ],
      zip_safe=False)