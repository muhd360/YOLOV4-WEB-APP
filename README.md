## Full Stack Webb APP Development


#### View DEMO or Prototype via link:

["Web APP Object Detection"](https://youtu.be/DPW319gWQbU)


#### Project Root data structure

```shell
root@dd167f326b80:/tensorfl_vision/Web_Dev_AI# tree -d
.
├── Images
├── __pycache__
├── models
├── static
│   ├── images
│   ├── js
│   └── uploads
│       └── bear
└── templates

10 directories
```

```
Templates folder contains all html files
js folder contains all jaavascript files
static folder contains images on which background images and icons are held
static folder contains uploads on whioch output of inference will be visualized.
models folder contains classes.txt and prebuild models
```

### please install requirements first
```shell
$ pip install -r requirements.txt
```
#### To run the code you need to run the command:

```shell
$ python3 server_dev_db.py
```

### Note:
Please first insert all images or icons to static/images folder , before running application. Please, also add pretrained models to models folders, before running an application!


