import os
import subprocess

def getMetadata(image):

    cmd = "magick identify \"{0}\"".format(image)
    return subprocess.check_output(cmd,shell=True)

def getResolution(image):
    
    return getMetadata(image)

def getWidth(image):
    
    return re.findall(" \d*x\d* ",getMetadata(image))[0].replace(" ","").split("x")[0]

def resize_as(i,o,resizeTo):

    cmd = "magick \"{0}\" -resize {1} \"{2}\"".format(i,resizeTo,o)
    return os.system(cmd)

def concatenate_image(input_file_a,input_file_b,output_file,direction="+",resizeTo = ""):

    if resizeTo:
        cmd = "magick convert \"{1}\" -resize {2}! \"{0}\" +swap -background none {3}append \"{4}\"".format(input_file_a,input_file_b,resizeTo,direction,output_file)
    else:
        cmd = "magick convert \"{0}\" \"{1}\" -background none {2}append \"{3}\"".format(input_file_a,input_file_b,direction,output_file)
        
    return os.system(cmd)

def concatenate_images(files,output_file,direction="+",resizeTo= ""):

    width = len(files)
    if width > 1:

        a = resize_as(files[0],output_file,resizeTo=resizeTo) if resizeTo else files[0]
        for i in range(1,width):
            concatenate_image(a,files[i],output_file,direction=direction,resizeTo=resizeTo)
            a = output_file

    return output_file

def addTextToImage(image,text):

    width = int(getWidth(image))
    pointsize = 150*width/7000
    cmd = "magick convert \"{0}\" -gravity South -pointsize {2} -annotate +0+100 \"{1}\" \"{0}\"".format(image,text,pointsize)
    return os.system(cmd)

def crop_image(input_file,output_file):

    cmd = "magick convert {0} -trim +repage {1}".format(input_file,output_file)
    return os.system(cmd)

def crop_images(images):

    crops = []
    for image in images:

        crop_name = image.replace("final-","crop-")
        if os.path.exists(crop_name):
            os.remove(crop_name)
        crops.append(crop_name)
        crop_image(image,crops[-1])

    return crops