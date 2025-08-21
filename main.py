import cv2
from modules.utils import load_config
from modules.face_analysis import load_known_faces
from modules.db_operations import load_camera_data
from modules.video_processing import process_video_dynamic_skipping

# Constants
CONTINUOUS_RECOGNITION_TIME = 2  # seconds
EXIT_THRESHOLD_TIME = 120  # 2 minutes in seconds

# Load configuration and camera data
config = load_config('config/config.yaml')
employees = config['employees']

# Load known faces
known_face_embeddings, known_names, employee_id_mapping = load_known_faces(employees)

# Load camera data
camera_data = load_camera_data()

for camera_id, data in camera_data.items():
    rois = data['rois']
    video_capture = cv2.VideoCapture(data['stream_link'])
    recognized_faces = {}

    process_video_dynamic_skipping(video_capture, known_face_embeddings, known_names, employee_id_mapping, rois, recognized_faces, CONTINUOUS_RECOGNITION_TIME, EXIT_THRESHOLD_TIME)
