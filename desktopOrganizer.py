import os
from os import scandir
from os.path import splitext, exists, join
from time import sleep
import time

import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ? folder to track e.g. Windows: "C:\\Users\\UserName\\Downloads"
source_dir = ""
dest_dir_sfx = ""
dest_dir_music = ""
dest_dir_video = ""
dest_dir_image = ""
dest_dir_documents = ""
dest_dir_torrent = ""
dest_dir_applications = ""
dest_dir_installers = ""
dest_dir_archives = ""
dest_dir_textfiles = ""
dest_dir_scripts = ""

# ? supported image types
image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd",
                    ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf",
                    ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]
# ? supported Video types
video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]
# ? supported Audio types
audio_extensions = [".m4a", ".flac", "mp3", ".wav", ".wma", ".aac"]
# ? supported Document types
document_extensions = [".doc", ".docx", ".odt",
                       ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]
# ? supported Torrent files
torrent_extensions = [".torrent"]
# ? supported Application files
application_extensions = [".exe", ".bat"]
# ? supported Installer files
installer_extensions = [".msi", ".pkg"]
# ? supported Archive files
archive_extensions = [".zip", ".rar", ".7z", ".tar", ".gz"]
# ? supported Text files
textfile_extensions = [".txt", ".md", ".csv"]
# ? supported Programming scripts
script_extensions = [".py", ".js", ".html", ".css", ".cpp", ".java", ".php", ".c", ".sh"]


def make_unique(dest, name):
    filename, extension = splitext(name)
    counter = 1
    logging.info(f"Checking if file {name} already exists in {dest}.")
    # * IF FILE EXISTS, ADDS NUMBER TO THE END OF THE FILENAME
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        logging.info(f"File {name} already exists. Renaming to {name}.")
        counter += 1
    return name


def move_file(dest, entry, name):
    source_path = entry.path  # Full path to the source file
    temp_name = make_unique(dest, name)  # Generate a unique name for the destination
    temp_dest_path = join(dest, temp_name)  # Path where the file will be moved

    try:
        # Check if the destination file already exists and rename it if necessary
        if os.path.exists(temp_dest_path):
            logging.info(f"File {temp_name} already exists in {dest}. Trying a temporary rename.")
            temp_dest_path = join(dest, make_unique(dest, temp_name))  # Generate a new unique name
            logging.info(f"New unique name for the destination file is {temp_dest_path}.")

        # Move the file to the destination
        logging.info(f"Attempting to move file from {source_path} to {temp_dest_path}.")
        os.rename(source_path, temp_dest_path)  # Rename/move the file
        logging.info(f"File {name} successfully moved to {dest}.")

    except FileNotFoundError:
        logging.error(f"File not found error: {source_path}. File might have been moved or deleted.")
    except PermissionError as e:
        logging.error(f"Permission error moving file {name}: {e}.")
        time.sleep(2)  # Retry after a brief pause
    except Exception as e:
        logging.error(f"Unexpected error: {e}.")


class MoverHandler(FileSystemEventHandler):
    # ? THIS FUNCTION WILL RUN WHENEVER THERE IS A CHANGE IN "source_dir"
    def on_modified(self, event):
        logging.info(f"Change detected in {source_dir}. Sorting files.")
        self.sort_files()

    # * New function to sort files immediately when the program starts
    def sort_files(self):
        logging.info(f"Scanning {source_dir} to sort existing files.")
        with scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                if entry.is_file():  # Only process files, skip directories
                    logging.info(f"Found file {name}. Determining file type.")
                    self.check_audio_files(entry, name)
                    self.check_video_files(entry, name)
                    self.check_image_files(entry, name)
                    self.check_document_files(entry, name)
                    self.check_torrent_files(entry, name)
                    self.check_application_files(entry, name)
                    self.check_installer_files(entry, name)
                    self.check_archive_files(entry, name)
                    self.check_textfiles(entry, name)
                    self.check_script_files(entry, name)

    def check_audio_files(self, entry, name):  # * Checks all Audio Files
        for audio_extension in audio_extensions:
            if name.endswith(audio_extension) or name.endswith(audio_extension.upper()):
                logging.info(f"Audio file {name} detected.")
                if entry.stat().st_size < 10_000_000 or "SFX" in name:  # ? 10Megabytes
                    dest = dest_dir_sfx
                    logging.info(f"File {name} categorized as sound effect (SFX).")
                else:
                    dest = dest_dir_music
                    logging.info(f"File {name} categorized as music.")
                move_file(dest, entry, name)

    def check_video_files(self, entry, name):  # * Checks all Video Files
        for video_extension in video_extensions:
            if name.endswith(video_extension) or name.endswith(video_extension.upper()):
                logging.info(f"Video file {name} detected.")
                move_file(dest_dir_video, entry, name)

    def check_image_files(self, entry, name):  # * Checks all Image Files
        for image_extension in image_extensions:
            if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                logging.info(f"Image file {name} detected.")
                move_file(dest_dir_image, entry, name)

    def check_document_files(self, entry, name):  # * Checks all Document Files
        for documents_extension in document_extensions:
            if name.endswith(documents_extension) or name.endswith(documents_extension.upper()):
                logging.info(f"Document file {name} detected.")
                move_file(dest_dir_documents, entry, name)

    def check_torrent_files(self, entry, name):  # * Checks all Torrent Files
        for torrent_extension in torrent_extensions:
            if name.endswith(torrent_extension) or name.endswith(torrent_extension.upper()):
                logging.info(f"Torrent file {name} detected.")
                move_file(dest_dir_torrent, entry, name)

    def check_application_files(self, entry, name):  # * Checks all Application Files
        for application_extension in application_extensions:
            if name.endswith(application_extension) or name.endswith(application_extension.upper()):
                logging.info(f"Application file {name} detected.")
                move_file(dest_dir_applications, entry, name)

    def check_installer_files(self, entry, name):  # * Checks all Installer Files
        for installer_extension in installer_extensions:
            if name.endswith(installer_extension) or name.endswith(installer_extension.upper()):
                logging.info(f"Installer file {name} detected.")
                move_file(dest_dir_installers, entry, name)

    def check_archive_files(self, entry, name):  # * Checks all Archive Files
        for archive_extension in archive_extensions:
            if name.endswith(archive_extension) or name.endswith(archive_extension.upper()):
                logging.info(f"Archive file {name} detected.")
                move_file(dest_dir_archives, entry, name)

    def check_textfiles(self, entry, name):  # * Checks all Text Files
        for textfile_extension in textfile_extensions:
            if name.endswith(textfile_extension) or name.endswith(textfile_extension.upper()):
                logging.info(f"Text file {name} detected.")
                move_file(dest_dir_textfiles, entry, name)

    def check_script_files(self, entry, name):  # * Checks all Script Files
        for script_extension in script_extensions:
            if name.endswith(script_extension) or name.endswith(script_extension.upper()):
                logging.info(f"Script file {name} detected.")
                move_file(dest_dir_scripts, entry, name)


# ! NO NEED TO CHANGE BELOW CODE
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    logging.info(f"Starting file sorting script.")

    event_handler = MoverHandler()

    # * Call the sort_files method right when the program starts to sort existing files
    logging.info(f"Sorting files in {source_dir} as the program starts.")
    event_handler.sort_files()

    # * Continue to observe the folder for changes
    observer = Observer()
    observer.schedule(event_handler, source_dir, recursive=True)
    observer.start()

    logging.info(f"Started watching directory {source_dir}.")

    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        logging.info(f"Script interrupted. Stopping observer.")
        observer.stop()
    observer.join()
    logging.info(f"File sorting script ended.")
