# Kraken

| File                                   | Description                                        |
|----------------------------------------|----------------------------------------------------|
| [frame_cap.py](frame_cap.py)           | Receive the frame stream from ipcam, turning frames into a video |
| [input_cap.py](input_cap.py)                 | Sends video to be procced using a trained model                 |
| [object_count.py](object_count.py)         | Receive video files to be procced. cant set the model to be used                              |


## Python script instructions

Run `pip install -r requirements.txt` to get the dependencies.

    usage: input_cap.py [video path]

    or using the webapp: webapp.sh
    
