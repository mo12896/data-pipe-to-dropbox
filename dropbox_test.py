from pathlib import Path
import dropbox
from dropbox.exceptions import AuthError
import os

import matplotlib.pyplot as plt
from dotenv import load_dotenv


def generate_local_sample_image(filename: str):
    """Convenience Script for generating a sample plot and saving it locally"""
    fig = plt.figure()
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

    # draw lines
    l1, = ax.plot([0.1, 0.5, 0.9], [0.1, 0.9, 0.5], "bo-",
                  mec="b", lw=5, ms=10, label="Line 1")
    l2, = ax.plot([0.1, 0.5, 0.9], [0.5, 0.2, 0.7], "rs-",
                  mec="r", lw=5, ms=10, label="Line 2")

    plt.savefig(filename)


class DataUploadToDropBox:
    def __init__(self, access_token: str):
        self.access_token = access_token

    def upload_file(self, local_file_path, dropbox_file_path):
        """Upload a file from the local machine to a path in the Dropbox app directory.

        Args:
            local_file_path (str): The path to the local file.
            dropbox_file_path (str): The path to the file in the Dropbox app directory.

        Example:
            upload_file(Path.cwd() / 'test.csv', '/stuff/test.csv')

        Returns:
            meta: The Dropbox file metadata.
        """

        # Create a connection to Dropbox.
        try:
            dbx = dropbox.Dropbox(self.access_token)
        except AuthError as e:
            print('Error connecting to Dropbox with access token: ' + str(e))

        # Upload the data to Dropbox.
        try:
            with local_file_path.open("rb") as f:
                meta = dbx.files_upload(f.read(), dropbox_file_path, mode=dropbox.files.WriteMode("overwrite"))

                return meta
        except Exception as e:
            print('Error uploading file to Dropbox: ' + str(e))


def main():
    filename = 'test_image.png'

    load_dotenv()
    # App Name: Mo-Master-Thesis-MIT
    DROPBOX_ACCESS_TOKEN = os.getenv('DROPBOX_ACCESS_TOKEN')

    generate_local_sample_image(filename)

    uploadData = DataUploadToDropBox(DROPBOX_ACCESS_TOKEN)

    local_file_path = Path.cwd() / filename
    dropbox_file_path = '/Apps/Overleaf/tum-thesis-latex/data/' + filename

    uploadData.upload_file(local_file_path, dropbox_file_path)


if __name__ == "__main__":
    main()



