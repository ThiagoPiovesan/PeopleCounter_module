# People Counting with TelegramBot + WebHook integration:

People Counting in Real-Time using live video stream/IP camera in OpenCV.

> This is an improvement/modification to https://github.com/Gupu25/PeopleCounter && https://github.com/saimj7/People-Counting-in-Real-Time.git

> Refer to added [Features](#features).

- The primary aim is to use the project as a modular solution, with a business perspective, ready to scale and easy to use.
- Use case: Counting the number of people inside stores/buildings/shopping malls etc., in real-time.
- Sending an alert to and website or a Telegram Bot.
- Automating features and optimising the real-time stream for better performance (with threading).
- Version: 1.0.0

--- 

## Table of Contents
* [Simple Theory](#simple-theory)
* [Running Inference](#running-inference)
* [Features](#features)
* [References](#references)
* [Next Steps](#next-steps)

## Simple Theory
**SSD detector:**
- We are using a color subtration to identify when a different object enter in the frame. In general, it takes snapshot from every frame. After, it applies some color treatments in the image captured.
- Then it starts to track the new object until it disappears from the frame.  
- It Compares the new shot, with the last one, to compare a 'Delta' variation in the last position.
- So, in the end, an Artificial Intelligence is not needed, once we are only using a python library to image processing.
---

**Centroid tracker:**
- "Centroid tracker is one of the most reliable trackers out there". To be straightforward, the centroid tracker computes the centroid of the bounding boxes.
- That is, the bounding boxes are (x, y) co-ordinates of the objects in an image. 
- Once the co-ordinates are obtained by the histogram, the tracker computes the centroid (center) of the box. In other words, the center of an object.
- Then an unique ID is assigned to every particular object deteced, for tracking over the sequence of frames.

## Running Inference
- Install all the required Python dependencies:
```
pip install -r requirements.txt
```
- To run inference on a test video file (already added two examples videos to test =P), just run the follow command: 
```
python personCounter_module.py

```
> To run inference on an IP camera ou Webcam, just uncommed the lines inside de file on "camera_init" class:
```
# cap = cv2.VideoCapture("rtsp://user:Passwd@www.xxx.yyy.zzz/video")            # IP camera
# cap = cv.VideoCapture(0)                                                      # Webcam
```

## Features
The following is some features the are working on actual version of the module, but also some will only be implemented in new versions.

***1. Real-Time alert --> Telegram Bot:***
- If selected, we send an message alert in real-time to an telegram bot. Use case: If the total number of people (say 10 or 30) exceeded in a store/building, we simply alert the staff. 
- You can set the max. people limit in config. (``` Threshold = 10 // Telegram_sender = True ```).

- Obs.: IN PROGRESS...

***2. Real-Time alert --> Webserver:*** 
- If selected, we send an email alert in real-time. Use case: If the total number of people (say 10 or 30) exceeded in a store/building, we simply alert the staff. 
- You can set the max. people limit in config. (``` Threshold = 10 // Webserver_sender = True```).

- Obs.: IN PROGRESS...

***3. Real-Time alert --> E-mail:***
- If selected, we send an email alert in real-time. Use case: If the total number of people (say 10 or 30) exceeded in a store/building, we simply alert the staff. 
- You can set the max. people limit in config. (``` Threshold = 10 // Email_sender = True ```).

- Obs.: NOT IMPLEMENTED YET...


***4. Scheduler:***
- Automatic scheduler to start the software. Configure to run at every second, minute, day, or Monday to Friday.
- This is extremely useful in a business scenario, for instance, you can run it only at your desired time (9-5?).
- Variables and memory would be reset == less load on your machine.

```
##Runs at every day (9:00 am). You can change it.
schedule.every().day.at("9:00").do(run)
```

- Obs.: NOT IMPLEMENTED YET...

***5. Timer:***
- Configure stopping the software after a certain time, e.g., 30 min or 9 hours from now.
- All you have to do is set your desired time and run the script.

```
if Timer:
	# Automatic timer to stop the live stream. Set to 8 hours (28800s).
	t1 = time.time()
	num_seconds=(t1-t0)
	if num_seconds > 28800:
		break
```

- Obs.: NOT IMPLEMENTED YET...

***6. Simple log:***
- Logs all data at end of the day.
- Useful for footfall analysis.

- Obs.: NOT IMPLEMENTED YET...

## References
***Main:***
- SSD paper: https://arxiv.org/abs/1512.02325
- MobileNet paper: https://arxiv.org/abs/1704.04861
- Centroid tracker: https://www.pyimagesearch.com/2018/07/23/simple-object-tracking-with-opencv/
- https://towardsdatascience.com/review-ssd-single-shot-detector-object-detection-851a94607d11
- https://pypi.org/project/schedule/

## Next steps

- Evaluate the performance on multiple IP cameras.
- Create zones os passages and multiple lines.

<p>&nbsp;</p>

---

## Thanks for the read & I hope you enjoy it!

> To get started/contribute (if you want - optional) ...

- **Option 1**
    - 🍴 Fork this repo and pull request!

- **Option 2**
    - 👯 Clone this repo: 
    ```
    $ git clone https://github.com/ThiagoPiovesan/PeopleCounter_module.git
    ```

- **Enjoy it!**

---

Ass: Thiago Piovesan - 17-11-2021 -- version: 1.0.0.

