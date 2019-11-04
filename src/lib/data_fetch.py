import Augmentor
import argparse
import sys, os, re
import xml.etree.ElementTree as ET
from xml.dom import minidom
from PIL import Image

def _get_generator(images_dir, output_dir):
  """Returns default Augmentor which enlarges dataset on-the-fly
  It changes the colors, saturation, contrast,... of the pictures

  Parameters:
  images_dir (string): Path to the pictures directory

  Returns:
  Keras generator: Returns a keras generator

  """

  output_dir = os.path.relpath(output_dir, images_dir)

  p = Augmentor.Pipeline(images_dir, output_directory=output_dir)

  p.set_seed(42)
  p.random_distortion(0.3, grid_width=10, grid_height=10, magnitude=10)
  p.invert(0.05)
  p.random_brightness(0.7, min_factor=0.2, max_factor=0.9)
  p.random_color(0.7, min_factor=0.6, max_factor=1.3)
  p.random_contrast(0.7, min_factor=0.6, max_factor=1.3)
  p.skew(0.3, magnitude=0.1)

  return p

def _get_labeling(img_directory, img_filename, labels):
  im = Image.open(os.path.join(img_directory, img_filename))
  width, height = im.size
  original = f"""<annotation>
	<folder>{img_directory}</folder>
	<filename>{img_filename}</filename>
	<path>{os.path.abspath(os.path.join(img_directory, img_filename))}</path>
	<source>
		<database>Unknown</database>
	</source>
	<size>
		<width>{width}</width>
		<height>{height}</height>
		<depth>3</depth>
	</size>
	<segmented>0</segmented>
    </annotation>"""

  class_id = {
    0 : 'bot',
    1 : 'duckie',
    2 : 'greensign',
    3 : 'yellowsign'
  }

  root = ET.fromstring(original)

  for object in labels:
    o_id = int(object[0])
    o_x_center = round(float(object[1]) * width) # TODO +-?
    o_y_center = round(float(object[2]) * height)
    o_width = round(float(object[3]) * width)
    o_height = round(float(object[4]) * height)
    new_object = ET.SubElement(root, 'object')
    ET.SubElement(new_object, 'name').text = class_id[o_id]
    ET.SubElement(new_object, 'pose').text = 'Unspecified'
    ET.SubElement(new_object, 'truncated').text = '0'
    ET.SubElement(new_object, 'difficult').text = '0'
    bndbox = ET.SubElement(new_object, 'bndbox')
    ET.SubElement(bndbox, 'xmin').text = f'{o_x_center - round(o_width / 2)}'
    ET.SubElement(bndbox, 'ymin').text = f'{o_y_center - round(o_height / 2)}'
    ET.SubElement(bndbox, 'xmax').text = f'{o_x_center + round(o_width / 2)}'
    ET.SubElement(bndbox, 'ymax').text = f'{o_y_center + round(o_height / 2)}'

  raw_string = ET.tostring(root)
  # returning the pretty formatted string
  return minidom.parseString(raw_string).toprettyxml(indent="    ")

def create_voc_augmented_database(images_dir, output_dir, label_output_dir, sample_size = 10000, label_dir = None):
  """Creates the augmented database with yolov3 compatible labeling.

  Parameters:
  images_dir (string): Path to the pictures directory
  output_dir (string): Path to the output directory where the augmented pictures will be saved
  label_output_dir (string): Path to the directory where the voc labels will be saved
  sample_size (int): Number of samples to be generated.
  label_dir (string): Path to the labeling directory. Default: images_dir
  """

  if not os.path.exists(output_dir):
    os.makedirs(output_dir)

  # Creating the augmented database
  augmentor = _get_generator(images_dir, output_dir)
  augmentor.sample(sample_size)

  # Renaming the pictures to a more readable file name
  for index, file in enumerate(list(os.listdir(output_dir))):
    try:
      original_file = re.search('.*_original_(.*)\.jpg_.*', file).group(1)
      new_file = f'{original_file}_idx{index:05d}.jpg'
    except AttributeError:
      print(f'Could not find original jpg file substring in {file}') # TODO debug log
      continue
    os.rename(os.path.join(output_dir, file), os.path.join(output_dir, new_file))
  print(output_dir)
  if not os.path.exists(label_output_dir):
    os.makedirs(label_output_dir)

  if not label_dir:
    label_dir = images_dir
    
  # Creating the labeling assignment
  for file in os.listdir(output_dir):
    try:
      original_label_file = os.path.join(label_dir, f"{re.search('(.*)_idx.*', file).group(1)}.txt")
      new_label_file = os.path.join(label_output_dir, f'{os.path.splitext(file)[0]}.xml')
      with open(original_label_file) as original_label, open(new_label_file, 'w') as new_label:
        labels = (line.strip().split() for line in original_label.readlines())
        new_file_content = _get_labeling(output_dir, file, labels)
        new_label.write(new_file_content)
        new_label.close()
        original_label.close()
    except AttributeError:
      print(f'Could not find original jpg file substring in {file}') # TODO debug log
      continue

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Creating an augmented image database with VOC xml format.')
  parser.add_argument('--input_directory', '-i', nargs=1, required=True,
                      help='The directory where the images are stored. Only images are allowed here.')
  parser.add_argument('--output_directory', '-o', nargs=1, required=True,
                      help='The output directory where the augmented images will be stored')
  parser.add_argument('--voc_label_output_dir', '-v', nargs=1, required=True,
                      help='The output directory where the augmented images will be stored')
  parser.add_argument('--label_dir', '-l', nargs=1, required=False,
                      help='The directory where the labels has to be stored.')
  parser.add_argument('--nuber_of_samples', '-n', nargs=1, type=int, required=False,
                      help='Number of images to be created.')
  args = parser.parse_args(sys.argv[1:])

  if not args.label_dir:
    args.label_dir = args.input_directory

  create_voc_augmented_database(args.input_directory[0],
                                args.output_directory[0],
                                args.voc_label_output_dir[0],
                                args.nuber_of_samples[0],
                                args.label_dir[0])
