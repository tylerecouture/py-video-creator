import os

resolution = "1920:1080"

output_file = "out.mp4"
images_directory = "images"
seconds_per_image = 3
fade_duration = 1
color_space = "yuv420p"


#  https://superuser.com/questions/833232/create-video-with-5-images-with-fadein-out-effect-in-ffmpeg/834035#834035
image_files = os.listdir(images_directory)
num_images = len(image_files)

fade_out = f"fade=t=out:st={seconds_per_image - fade_duration}"
fade_in = f"fade=t=in:st=0:d={fade_duration}"
fade_in_and_out = f'{fade_in},{fade_out}'

# fade_in_cross = 'fade=d=1:t=in:alpha=1'

frame_settings = f'scale={resolution}:force_original_aspect_ratio=decrease,pad={resolution}:(ow-iw)/2:(oh-ih)/2,setsar=1'

image_inputs = ''
for image in image_files:
    # '-loop 1 -t 5 -i images/input0.png' 
    image_inputs += f'-loop 1 -t {seconds_per_image} -i {images_directory}{os.path.sep}{image} '

# Create transition filter
filter_complex = '-filter_complex "'
for i, image in enumerate(image_files):
    # first image only fades out
    if i is 0:
        fade = fade_out
    else:
        fade = fade_in_and_out
    
    #Fade to black:
    filter_complex += f'[{i}:v]{frame_settings},{fade}:d=1[v{i}]; '
    #Crossfade:
    #filter_complex += f'[{i}:v]{frame_settings},[{i}]format=yuva444p,{fade}:d=1[v{i}]; '
    

for i in range(num_images):
    filter_complex += f'[v{i}]'  # [v0][v1][v2][v3][v4]concat=n=5

filter_complex += f'concat=n={num_images}:v=1:a=0,format={color_space}[v]" -map "[v]" '

cmd = f'ffmpeg {image_inputs} {filter_complex} {output_file}'

os.system(cmd)
