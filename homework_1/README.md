# Instructions on how to run the solution

There are three demos that can be run. Python 3 should be installed as well as `numpy` and `tqdm` libraries. To run the demos, enter one of the commands below in terminal/cmd that is positioned in this directory (in which this README is).

## Demo 1

The used research papers can be found and inspected here: `datasets/literature-original`. This original pdf's were converted to text using online tools and the resulting dataset is located here: `datasets/literature-text`.

`python -m demos.research_papers_demo datasets/literature-text`

## Demo 2

This is a fast version of the songs demo that uses a much smaller dataset of only 89 songs that are all from the same author. The dataset can be found here: `datasets/scraped_songs_2.csv`.

`python -m demos.songs_demo datasets/scraped_songs_2.csv`

## Demo 3

This demo took about 40 minutes on our machine. It loads a dataset of 58636 songs. The dataset is here: `datasets/scraped_songs.csv`.

`python -m demos.songs_demo datasets/scraped_songs.csv`
