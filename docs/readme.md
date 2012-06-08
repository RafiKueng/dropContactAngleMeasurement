DROM C.A.M. (contact angle messurement) - README
================================================

0. Administrative Infos 
    suff thats nice to know
1. About - Introduction 
    what this program does in one (or two) sentences
2. How to use the data generated 
    how to read the tables, pictures produced
3. How to setup and use it 
    you want to analyse your own data? how you have to set up the tools (not complete!)
4. Details of Evaluation 
    all the techy details of the program
5. References



0. Administrative Infos
-----------------------
author: rafikueng
version: v2
date: 2012-06-08

data storage location: `\\dalli.physik.uzh.ch\data\ContactAngleMeasurement\Rh111BN_11`



1. About - Introduction
-----------------------
In the recorded video files, for each frame the contours are detected (using the filters [Canny86], [Matas00], [Suzuki85]) and a 5th order polynomial is fitted to the resulting contour points. The foot points result from the intersection of the base line with the polynomial, whereas the contact angle is the angle between them.

In the recorded video files, for each frame the contours are detected (using the filters [Canny86], [Matas00], [Suzuki85]) and a line is fitted to the resulting contour points near the base line. The foot points result from the intersection of the base line with the fitted line, whereas the contact angle is the angle between them.


-----
[Matas00] 
Matas, J. and Galambos, C. and Kittler, J.V., Robust Detection of Lines Using the Progressive Probabilistic Hough Transform. CVIU 78 1, pp 119-137 (2000)

[Suzuki85] 
Suzuki, S. and Abe, K., Topological Structural Analysis of Digitized Binary Images by Border Following. CVGIP 30 1, pp 32-46 (1985)

[Canny86] 
Canny. A Computational Approach to Edge Detection, IEEE Trans. on Pattern Analysis and Machine Intelligence, 8(6), pp. 679-698 (1986).



2. How to use the data generated
--------------------------------
there are 2 sorts of output:
- raw data (comma separated table, csv)
- images (jpg)

The raw data contains all the data for all the frames from a video file, whereas only a few selected images are saved (every 25th keyframe and frames with bad fits)

They can be found in the output folder (default `./outp`) and are named after the input video file. a frame number counter is added to the image files.

For example: 
- video file name: `MessurementA.avi`
- table: `MessurementA.csv`
- images: `MessurementA00000.jpg`, `MessurementA00025.jpg`, `MessurementA00027.jpg`, `MessurementA00050.jpg` ...


2.1 The CSV Table
-----------------
Here is a list of each data field in the table and a short description:

*   FrameNr  
    the number of the frame
*   ms  
    the timestamp of the frame
*   chosenAngle  
    two digits XY, that show which messurement was taken by the autmatic selection for the left (X) and the right (Y) side.
    example: 
    chosen=23 means that for the left side, the messurement 2 and for the right side, the 3rd was used.
      

the following occure multiple time with a suffix:
*   AngleL/ AngleR 
    the angle on the left / right side
*   ResL / ResR 
    the residual of the right/left hand side fit 
    `(sum_(over all pixels) of (dist(pixel^2)) ) / numPixels`
*   RootL / RootR 
    the footpoint on the left / right hand side

possible suffixes:
*   [none] 
    the automatically selected, best messurement (attention with this)
*   [Mean] 
    the average over the last X (default:5), automatically selected values
*   [Median] 
    the median over the last X (default:5), automatically selected values
*   [1] 
    results for fit of 5th degree polynomial
*   [2] 
    results for linear fit of points near baseline (best for small angles < 45deg)
*   [3] 
    results for linear fit of points near baseline with rotated coordinate system (best for big angles near 90deg)






3. How to setup and use it
--------------------------

NOT COMPLETE

you only need to setup if you want to analyse your own data...
(very basic, more to come or just write me a mail if there are questions)

3.1. setup
----------
* install python
    - install numpy
    - install scipy
    - install matplotlib
    - install pyqt
* install opencv
    - extract
    - add bin to %path%
    - add cv/build/python to %pythonpath%
* get the programm from github


3.2. how to use it
-------------------
(* edit parameters in parameters.py TODO not yet implemented)
* run it with:
	$ quick_eval.py inputvideofile.avi [outputdir=.]
* wait
* checkout the output

you can run multiple analyses in parallel straight forward if you'd like to, have a look at the "startquickeval.cmd" script for windows in the root directory.






4. Details of Evaluation
---------------------
In this section the evaluation algorythm is explained in details.

The evaluation process for one videofile (`eval_vid`) consists of 4 steps:
1. Initialisation
2. Training
3. Evaluation
4. Output


4.1 Initialisation
------------------
* setup of input and output path
* setup of parameters
* initialisation of output file


4.2 Training
------------
In the first part of the program, the position of the pipette and the baseline are evaluated from a series of frames and saved for the evaluation phase. (that means, they remain the same for each frame)

* a number of frames (`n_training_frames`; default:64) is read from the video file. They are selected evenly distributed from the whole video file (which has `n_frames`): 

  - for fNr from 0 to n_training_frames:
      * trainingSet[fNr] <- video.getFrameNr(n_frames / n_training_frames * fNr)


* the training frames are then analysed. the details of the training algorythm (`worker.train()`):

  - for each frame in trainingSet do:
    * edgesMap <- find edges in grayscale image (Canny(), using [Canny86] algorythm)
    + contours <- find contours in edgesMap (findContours(), using [Suzuki85] algorythm)

  - get the pipette position:
    + verticalLines <- find vertical lines in edgesMap (HoughLinesP(), using probabilistic hough transformation, as described in [Matas00])
    + pipettePosLeft, pipettePosRight  <- get min and max from verticalLines in x direction


  - split up and sort all the contour points into 2 sets:
    + contourPointsLeft <- all points in contours, where x component < pipettePosLeft
    + contourPointsRight <- all points in contours, where x component > pipettePosRight

  - to get the baseline position:
    + leftMostPoints <- all points with minimal x component from contourPointsLeft
    + leftBaselinePosition <- average over leftMostPoints, iff exists points in contourPointsLeft that have x component bigger than point and y smaller than point. else no baseline found.

    + and similar for the right side
  
  - finally do:
    + pipettePosLeftAverage <- average over all pipettePosLeft from each frame
    + pipettePosRightAverage <- average over all pipettePosRight from each frame
    
    + pipettePosLeft <- median over all pipettePosLeft that are > pipettePosLeftAverage
    + pipettePosRight <- median over all pipettePosRight that are < pipettePosRightAverage
  
  - and for the baseline:
    + BaselinePos <- average over all found LeftBaselinePosition and RightBaselinePosition





4.3. Evaluation
---------------

for each frame, the worker is called and evaluates the frame:

* preprocessing: 
  quite the same as in the training phase:
  * adjust contrast and brighnes by fixed factors (`contrast_adj`, `bright_adj`)
  * get edges using [canny86]
  * get contours using [Suzuki85]

  * leftSet, rightSet <- split points into < pipettePosLeft and > pipettePosRight
  * for all points with y component smaller BaselinePos: flip at baseline

* fitting I: Polynomial 5th deg: general case
  * for leftSet and rightSet do:
    * poly1 <- fit 5th degree polynomial to set
    * root1 <- find root of poly - baselinePos
    * angle1 <- value of poly.derrive at root1
    * res1 <- residuum of fit

* fitting II: line fit for small angles:
  * for leftSet and rightSet do:
    * subset <- from set select points with distance to baseline < threshold (fit_small_closeness) or first 10 points
    * poly2 <- fit line to subset
    * root2 <- find root of poly2 - baselinePos
    * angle2 <- arctan(slope(poly2))
    * res2 <- residuum of fit
    
* fitting III: line fit for big angles:
  * for leftSet and rightSet do:
    * subset <- from set select points with distance to baseline < threshold (fit_small_closeness) or first 10 points
    * subset <- mirror subset at y=x plane
    * invpoly3 <- fit line to subset
    * poly3 <- invert invpoly3
    * root3 <- invpoly3(baselinePos)
    * angle3 <- arctan(slope(poly3))
    * res3 <- residuum of fit
    

* selection of best fit:
  * ave_angle <- average over angle1, angle2, angle3
  * if ave_angle >75:
    * final_angle <- angle3
  * else if average_angle < 45:
    * final_angle <- angle2
  * else:
    * final_angle <- angle1


* create additional datasets:
  * mean_angle <- (running) mean over last X frames
  * median_angle <- (running) median from last X frames


4.4 Output
----------
* for each frame do:
  * if is keyframe (every 25th) or some fit parameter bad:
    * construct a picture with data drawn
    * save it
  * save data to table

  

-----
5. References
-------------
[Matas00] 
Matas, J. and Galambos, C. and Kittler, J.V., Robust Detection of Lines Using the Progressive Probabilistic Hough Transform. CVIU 78 1, pp 119-137 (2000)

[Suzuki85] 
Suzuki, S. and Abe, K., Topological Structural Analysis of Digitized Binary Images by Border Following. CVGIP 30 1, pp 32-46 (1985)

[Canny86] 
Canny. A Computational Approach to Edge Detection, IEEE Trans. on Pattern Analysis and Machine Intelligence, 8(6), pp. 679-698 (1986).

