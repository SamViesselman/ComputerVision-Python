__author__ = 'Sam'



from SimpleCV import Image, Color

eye = Image('eye.tif')

(empty, eye_green, emptier) = eye.splitChannels(False)

eye_green = eye_green * 2.5
eye_gray = eye_green.grayscale()

eye_gray = eye_gray.smooth()


#Canny edge detection algorithm. t1 specifies the threshold value to begin an edge. t2 specifies the strength required
#build an edge off of a point found by T2.
eye_edges = eye_gray.edges(t1 = 70, t2=35)


edge_test = eye_gray + eye_edges


eye_final = eye_edges

#Perform closing to find individual objects
eye_final = eye_final.dilate(2)
eye_final = eye_final.erode()

eye_final = eye_final.dilate(4)
eye_final = eye_final.erode(3)

big_blobs = eye_final.findBlobs(minsize=500)

 #create a blank image to mask
masked_image = Image(eye.size())

for b in big_blobs:

     #set mask
   b.image = masked_image

     #draw the blob on your mask
   b.draw(color = Color.WHITE)



eye_final = eye_final - masked_image.applyLayers()
eye_final = eye_final.erode()

#eye_final.save("testthis.png")


if eye_final.findBlobs(maxsize=10):

    small_blobs = eye_final.findBlobs(maxsize=10)

    #create a blank image to mask
    masked_small_image = Image(eye.size())
    for b in small_blobs:

        #set mask
       b.image = masked_small_image

       #draw the blob on your mask
       b.draw(color = Color.WHITE)


    eye_final = eye_final - masked_small_image.applyLayers()


final_blobs = eye_final.findBlobs()

#Filter through objects to find only potential microaneurysms
masked_circle_image = Image(eye.size())
for b in final_blobs:
    blob_height = b.height()
    blob_width = b.width()
    width_height_diff = abs(blob_height-blob_width)
    if (width_height_diff > .2 * blob_height) | (width_height_diff > .2 *blob_width):
            b.image = masked_circle_image
            b.draw(color = Color.WHITE)


    if (b.area() < .45 *blob_height * blob_width):

            b.image = masked_circle_image
            b.draw(color = Color.WHITE)

    #remove large pointless blobs
    if (b.area() > 1500):
            b.image = masked_circle_image
            b.draw(color=Color.WHITE)


#Save different objects
eye_final.save("Output1.png")
masked_circle_image.applyLayers().save("Output2.png")

eye_final = eye_final - masked_circle_image.applyLayers()
eye_example = eye_final + eye

eye_example.save('example.png')
eye_final.save('FinalImage.png')