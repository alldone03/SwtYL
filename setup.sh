

mkdir venv && python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
unzip model.zip -d model
cd ..
git clone https://github.com/ultralytics/yolov5.git 


