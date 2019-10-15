# Object detection based DuckieTown agent on INTEL Movidius Neural Compute Stick
## Objektum felismerést megvalósító DuckieTown ágens INTEL Movidius eszközön

### Introduction:
The aim of this project is to improve an existing solution of object detection, based on the excercise of the official Duckietown project documentation: [Unit B-5](https://docs.duckietown.org/DT19/exercises/out/exercise_object_detector.html).

We expect to enhance the performance of the network by using Intel Movidius Accelerator stick and a modified network architecture.

For training we are using the datasets given in the baseline with minor modifications in the separation of the three main sets for training, validation and testing.

### Creating a dataset:

The used data originates from the [darknet](https://github.com/marquezo/darknet) github repository. The dataset contains 420 labeled images where the labeling is attached in a separate text file. In order to enlarge the dataset, we use [Augmentor](https://github.com/mdbloice/Augmentor) for generating images with slightly different properties. The tool is able to generate the images on the fly, implementing a keras generator, so storing the generated images is not neccessary. For example import, see the proper example directory.

### Preparing the dataset:

TODO: rethink after cleaning is done

### Prepare config files:

TODO: NEED TO BE DISCUSSED - URGENTLY

### Training:

TODO: COLAB! Introduce usage for everyone! - URGENTLY

### Testing:

TODO : https://github.com/duckietown/docs-exercises/blob/master/book/exercises/100_exercise_train_object_detector.md

### Documentation

We used the attached template LaTeX file. The docs can be found under the __docs__ folder. The compilation can be made using the following method.

```bash
cd docs
docker run -v `pwd`:/home -it tianon/latex
cd /home
pdflatex DuckTales_assignment.tex
```
