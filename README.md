<img align="center" src=logo.png/>

***

# iSight
Prototype personal smartphone skin lesion detection

The repository containing our iSight project developed during the implementAI2020 hackathon hosted by MAIS.
The project is divided into 3 main components, the deep learning algorithm, the backend, the app (android).
All these element work together, making use of REST APIs, to efficiently communicate results.

__Java 1.8 and Android APK 29__ were used for the Android application. __Python 3.6__ was used for the flask backend and deep learning components.

## Installation
The project can be installed from source for development or personal usage.<br>
```
git clone https://github.com/EricZimmermann/iSight.git
cd android 
./gradlew assemble
cd ../
conda create -n isight python=3.6 pip
conda activate isight
pip install -r Flask\ Backend/requirements.txt
pip install -r dl/requirements.txt
```
