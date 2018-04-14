# A ROS service that provides sneeze recognition

## Functionality
This module creates a ROS node `roboy_local_speech_recognition` that provides a ROS service `/roboy/cognition/speech/recognition`.
Calling this service triggers the speech recognition which will record audio on the PC that runs the node and will send that audio to the (currently hardcoded) KALDI server.

It will return the recognized text as a string.