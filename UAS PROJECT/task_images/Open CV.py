import cv2 as cv
import numpy as np

image = cv.imread("task_images/graph.jpeg")

#Reading an Image
# if image is not None:
#     cv.imshow("First Image", image)
#     cv.waitKey(0)
#     cv.destroyAllWindows()
# else:
#     print("Image not found")


#Writing/Saving an Image
# success=cv.imwrite("task_images/try.png", image)
# if success:
#     print("Image saved succesfully")


#Dimensions of Image 
# h,w,c = image.shape
# print(h,w,c)

# gray = cv.cvtColor(image,cv.COLOR_BGR2GRAY)

# cv.imshow("Gray Image", gray)
# cv.waitKey(0)
# cv.destroyAllWindows()


#Croping Image using Slicing in OpenCV


# cropped  = image[0:500,0:500] #First width, then height
# cv.imshow("Real Image", image)
# cv.imshow("Cropped Image", cropped)
# cv.waitKey(0)
# cv.destroyAllWindows()


# M = cv.getRotationMatrix2D((h//2,w//2),120,1)
# rotated_image = cv.warpAffine((image), M, (w,h))
# flip = cv.flip(image,0)
#0 Vertical Flip 
#1 Horizontal Flip 
#-1 both 

# cv.imshow("Flipped Image", flip)
# #cv.imshow("Image", rotated_image)
# cv.waitKey(0)
# cv.destroyAllWindows()

pt1 = (0,0)
#Right and Down
pt2 = (100,100)
color = (255,0,0)
thickness = 4
cv.line(image,pt1,pt2,color,thickness)

cv.rectangle(image,(50,50), (250,200), (255,0,0), thickness)
cv.circle(image,(50,50), 50, (0,0,255), -1)

#put text 

cv.putText(image, "Hello Python Programmers", (50,300), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

cv.imshow("Text", image)
cv.waitKey(0)
cv.destroyAllWindows()

