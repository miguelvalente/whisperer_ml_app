# whisperer_ml_app

This the repo for developing a user friendly frontend for the [whisperer_ML](https://github.com/miguelvalente/whisperer).

Built with [Streamlit](https://streamlit.io/).

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/)

### Installing

1. Download the repo

```
git clone https://github.com/miguelvalente/whisperer_ml_app

```

2. Build the image. It migth take a while because you just entered dependency hell. Xzibit style. And not the cool MTV version you're thinking about.
```
docker build -t whisperer_ml_app .
```
### Running

1. Make the following folder structure

```
│── /data
│   ├── archives
│   ├── converted_files
│   ├── datasets
│   └── raw_files
```

2. Run docker
```
docker run  -v data:/home/data -p 8501:8501 whisperer_ml_app
```
The ```-v data:/home/data``` mounts the ```data``` directory you just made into the specified path inside the Docker container. This type of volume mounting is called __host volume__.

3. You're done and you can access the app at ```localhost:8501```.
