import cv2

import color_tracker

# You can determine these values with the HSVColorRangeDetector()
HSV_LOWER_VALUE = [164 ,188  ,80]
HSV_UPPER_VALUE = [255, 255 ,255] 
global x,y
def getpos():
    def tracking_callback(tracker: color_tracker.ColorTracker):
        # Visualizing the original frame and the debugger frame
        cv2.imshow("debug frame", tracker.debug_frame)
        cv2.imshow("frame tracker",tracker.frame)
    
        # Stop the script when we press ESC
        key = cv2.waitKey(1)
        if key == 27:
            tracker.stop_tracking()
    
        for obj in tracker.tracked_objects:
            x,y =obj.last_point[0],obj.last_point[1];
            # print(x,',',y)
            # print("Object {0} X: {1} and Y: {2}".format(obj.id, obj.last_point[0],obj.last_point[1]))
    
    
    # Creating a kernel for the morphology operations
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    
    # Init the ColorTracker object
    tracker = color_tracker.ColorTracker(max_nb_of_objects=1, max_nb_of_points=20, debug=True)
    # Setting a callback which is called at every iteration
    tracker.set_tracking_callback(tracking_callback=tracking_callback)
    
    # Start tracking with a camera
    with color_tracker.WebCamera(video_src=0) as webcam:
        # Start the actual tracking of the object
        # color_tracker.HSVColorRangeDetector(webcam)
        tracker.track(webcam,
                      hsv_lower_value=HSV_LOWER_VALUE,
                      hsv_upper_value=HSV_UPPER_VALUE,
                      min_contour_area=2500,
                      kernel=kernel)
        # cv2.imshow("frame dd",tracker.frame)
    # return x,y
print(getpos())