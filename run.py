from aligner import *
from iris_tracker import *
from os import listdir, remove, path
from os import rename as osrename
from colorama import init, Fore
import click

class loading_bar:
    def __init__(self, total):
        self.total=total
    def update(self, progress):
        progress+=1
        percent=100*(progress/self.total)
        bar='█'*round(percent)+' '*round(100-percent)
        print(f'\r[{bar}] {percent:.2f}%',end='\r')

IAP=click.Group()
init()
click.echo(Fore.CYAN)

@click.command()
@click.option('-source_folder','-sf', prompt='Source folder', help='Folder to rename files in', required=True, type=click.Path(exists=True))
@click.option('-newname','-n', '-prefix', prompt='Prefix', help='Prefix of renamed files', required=True, type=click.STRING)
@click.option('-start_n','-sn', '-from', prompt='Start number', help='Start numbering from this number', required=True, type=click.STRING)
def rename(source_folder, newname, start_n):
    click.echo('Renaming')
    l=loading_bar(len(listdir(source_folder)))
    for count, filename in enumerate(listdir(source_folder)):
        dst = f"{newname}{str(count + int(start_n)).zfill(5)}.jpg"
        src =f"{source_folder}/{filename}"
        dst =f"{source_folder}/{dst}"
        osrename(src, dst)
        l.update(count)
    click.echo('\n')

@click.command()
@click.option('-source_folder','-sf', prompt='Source folder', help='Folder to align images in', required=True, type=click.Path(exists=True))
@click.option('-destination_folder','-df', prompt='Destination folder', help='Folder to output aligned images in', required=True, type=click.Path(exists=True))
def align(source_folder, destination_folder):
    click.echo('Getting iris positions')
    l=loading_bar(len(listdir(source_folder)))
    detector=Iris_Detector()
    dict_cords={}
    for count, file in enumerate(listdir(source_folder)):
        img=cv2.imread(f'{source_folder}/{file}')
        res=detector.get_iris_info(img)
        left_eye=detector.get_average([res[474],res[475],res[476],res[477]])
        right_eye=detector.get_average([res[469],res[470],res[471],res[472]])
        dict_cords[count]=(left_eye,right_eye)

        # cv2.circle(img,dict_cords[count][0],5,(240,240,240),5)
        # cv2.circle(img,dict_cords[count][1],5,(240,240,240),5)
        # while True:
        #     img=cv2.resize(img,(500,500))
        #     cv2.imshow('',img)
        #     if cv2.waitKey(1) & 0xFF == ord("q"):
        #         break
        l.update(count)
    click.echo('\n')

    click.echo('Aligning')
    l=loading_bar(len(listdir(source_folder)))
    for count, file in enumerate(listdir(source_folder)):
        image=Image.open(f'{source_folder}/{file}')
        new_image=CropFace(image, eye_left=dict_cords[count][0], eye_right=dict_cords[count][1], offset_pct=(0.45,0.45), dest_sz=image.size)
        new_image.save(f'{destination_folder}/{file}')
        l.update(count)
    click.echo('\n')

@click.command()
@click.option('-folder','-f', prompt='Folder', help='Folder to empty [Not ran during "all"]', required=True, type=click.Path(exists=True))
def empty_folder(folder):
    click.echo(Fore.RED+'Deleting folder contents')
    l=loading_bar(len(listdir(folder)))
    for count,filename in enumerate(listdir(folder)):
        file_path = path.join(folder, filename)
        remove(file_path)
        l.update(count)
    click.echo(Fore.CYAN)

@click.command()
@click.option('-source_folder','-sf', prompt='Source folder', help='Folder to loop images in', required=True, type=click.Path(exists=True))
@click.option('-destination_file','-exporting_file','-ef', prompt='Destination file', help='File to output gif in', required=True, type=click.Path(exists=True))
@click.option('-duration','-d', default=175, help='duration of one frame/speed', type=click.INT)
def export_gif(source_folder, destination_file, duration):
    click.echo('Exporting gif')
    l=loading_bar(len(listdir(source_folder))+1)
    imgs=[]
    for count, file in enumerate(sorted(listdir(source_folder))):
        imgs.append(Image.open(f'{source_folder}/{file}'))
        l.update(count)
    img = imgs[0]
    img.save(fp=destination_file, format='GIF', append_images=imgs, save_all=True, duration=duration)
    l.update(len(listdir(source_folder)))
    click.echo('\n')

@click.command()
@click.option('-source_folder','-sf', default='images', help='Folder to rename files in', type=click.Path(exists=True))
@click.option('-newname','-n', '-prefix', default='IMG-', help='Prefix of renamed files', type=click.STRING)
@click.option('-destination_folder','-df', default='processed', help='Folder to output aligned images in', type=click.Path(exists=True))
@click.option('-destination_file', '-exporting_file','-ef', default='exported.gif', help='File to output gif in', type=click.Path(exists=True))
@click.option('-duration','-d', default=175, help='duration of one frame/speed', type=click.INT)
@click.pass_context
def all(ctx, source_folder, newname, destination_folder, destination_file, duration):
    ctx.invoke(rename,source_folder=source_folder,newname=newname, start_n=0)
    ctx.invoke(align,source_folder=source_folder,destination_folder=destination_folder)
    ctx.invoke(export_gif,source_folder=destination_folder,destination_file=destination_file)

IAP.add_command(all)
IAP.add_command(align)
IAP.add_command(rename)
IAP.add_command(empty_folder)
IAP.add_command(export_gif)
if __name__=='__main__':
    IAP()
