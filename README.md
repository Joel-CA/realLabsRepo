# REALLab Undergrad Research Coding Assignment

## Building a simulation environment for dough manipulation
**Description**: 
The goal for this task is building a minimally functioning simulation scene where a Franka robot is programmed to interact with a piece of dough, i.e. a soft, highly-deformable object that cannot be easily modeled with simple rigid body physics simulation. Create a simulation scene where the dough is either put on the floor or on a table, and a Franka robot arm mounted near the workspace. Also program the Franka arm to perform some predefined actions, for example, move the gripper near the dough, then close the gripper to squeeze it, move it around, etc. 

We strongly recommend using Genesis as the base simulation.  [https://github.com/Genesis-Embodied-AI/Genesis](https://github.com/Genesis-Embodied-AI/Genesis): it should be locally/pip installable and there’s plenty of existing examples: https://github.com/Genesis-Embodied-AI/Genesis/tree/main/examples/tutorials    
### Useful links:
🕹️ Control Your Robot -> follow this example for loading and controlling a Franka am

🐛 Soft Robots -> good reference for how to simulate a soft object in Genesis
https://dough-net.github.io/  -> further reading on why we want to work on deformable object manipulation.

### Issues encountered (and how I fixed them[ish])
- Encountoured error described in forum [here](https://github.com/Genesis-Embodied-AI/Genesis/issues/243](https://github.com/Genesis-Embodied-AI/Genesis/issues/243). Solution attempts included force installation ofgenesis-world==0.2.1 as described in the thread, but to no avail. I was able to install `genesis-world` only via Ubuntu shell (since Genisis has better support there).
- Once installed, running `genisis_test.py` resulted in an error of the type described in [https://github.com/Genesis-Embodied-AI/Genesis/issues/246]. Re-installing WSL2 resolved this error, but resulted in something like the following: [https://github.com/Genesis-Embodied-AI/Genesis/issues/143]. A [thread](https://github.com/Genesis-Embodied-AI/Genesis/issues/12) revealed that Genisis cannot render in Windows. I thought I'd try one more workaround by, rather than using a windows-linux subprocess, emulating the Ubuntu OS in VirtualBox, but this resulted in the same `OpenGL.error.Error: Attempt to retrieve context when no valid context`.

Without much time left to work on this, it was time to shift gears....

## Automating point prompting for video segmentation 
**Description**: 
Build a user interface that: 1) load this video file, 2) let the user select one specific frame in the video, 3) display that selected image frame to the user. 4) ask the user to click on any area of the image, and display that user point on the same image, e.g. a red cross overlaid with the input image. We don’t have specific constraints on how to implement this. You are welcomed to make any low-level design choices for this user interface, as long as it achieves these desired functionalities.

More context for this task: when working with SAMv2, a state-of-the-art video segmentation model, a 2D prompt point is required from the user to specify which object to segment and track across frames. Your GUI is therefore used to better automate this process: after a user clicks on the desired location, this 2D point can be then fed into the SAM model as input prompt.
Useful Links:
REU_example_input_video_SAM.mp4 use this video for input to your GUI 
SAM 2: Segment Anything in Images and Videos | Research - AI at Meta: further readings on video segmentation

### Setup
Clone this repository and run the following:
```
pip install -r requirements.txt
```
Then you are free to run the python GUI like so:
```
python video_segmentation/video_segmentation.py
```

### Functioning Interface
You can watch a video of the GUI in action [here](https://drive.google.com/file/d/1sgi5N4TY759ZvhCVwTlAG_SBTBSU0pmU/view?usp=sharing).

### Issues encountered (and how I fixed them [for real, this time])
Two features I implemented were a bit at odds for the majority of my implementing this project: the video scrubber and the marker ('x') drawer. It doesn't make sense for someone to be able to scrub to the next frame with an x atop an object it is no longer meant for due to the camera movement. To resolve this, I added a global "pause" variable that acts as a flag for when a user is and is not allowed to scrub through the video. Now, a user must select an "Annotate Frame" option and, only during that period where the frame is locked, may the user draw markers over the frame.

