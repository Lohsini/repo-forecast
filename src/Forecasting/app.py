
from google.cloud import storage
from flask import Flask, jsonify
from nbclient import NotebookClient
from nbformat import read
import os
from dotenv import load_dotenv
load_dotenv()

# Initilize flask app
app = Flask(__name__)

# Initlize Google cloud storage client
client = storage.Client()

# Set your bucket and base URL
BUCKET_NAME = os.environ.get('BUCKET_NAME', 'Your_BUCKET_NAME')
BASE_IMAGE_PATH = os.environ.get(
    'BASE_IMAGE_PATH', 'https://storage.googleapis.com/Your_BUCKET_NAME/')

# Folders to upload from
IMAGE_FOLDERS = ['charts', 'Tensorflow_LSTM', 'Prophet', 'StatsModel']


def upload_folder_images_to_gcs(local_folder):
    urls = []
    folder_path = os.path.join(os.getcwd(), local_folder)
    if not os.path.exists(folder_path):
        return urls  # skip if folder doesn't exist

    for filename in os.listdir(folder_path):
        if filename.endswith('.png') or filename.endswith('.jpg'):
            full_path = os.path.join(folder_path, filename)
            blob = client.bucket(BUCKET_NAME).blob(
                f"{local_folder}/{filename}")
            blob.upload_from_filename(full_path)
            urls.append(BASE_IMAGE_PATH + f"{local_folder}/{filename}")
    return urls


@app.route('/run-notebook', methods=['GET'])
def run_notebook():
    notebook_path = "GitHub_Repos_Issues_Forecasting.ipynb"
    # notebook_path = "test.ipynb"
    print(f"hit run_notebook {notebook_path}")

    try:
        with open(notebook_path) as f:
            nb = read(f, as_version=4)

        client_nb = NotebookClient(nb, kernel_name="python3")
        client_nb.execute()

        print("Notebook executed successfully!")
        print("Start uploading images to GCS")

        # Upload all generated images from each folder
        all_uploaded_images = {}
        for folder in IMAGE_FOLDERS:
            print(f"Uploading images from {folder} folder")
            urls = upload_folder_images_to_gcs(folder)
            all_uploaded_images[folder] = urls

        return jsonify({
            "status": "Notebook executed and images uploaded!",
            "uploaded_images": all_uploaded_images
        })

    except Exception as e:
        return jsonify({"status": "Execution failed", "error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
