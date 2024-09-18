# Desktop-Organizer

```markdown
# File Organizer Script

## Overview

This Python script automatically organizes files in a specified source directory by moving them to designated folders based on their file types. It uses the `watchdog` library to monitor file changes and performs sorting both when the script starts and when changes are detected.

## Features

- Monitors a source directory for changes in real-time.
- Moves files into categorized folders based on their file types:
  - Audio files (`.mp3`, `.wav`, `.flac`, etc.)
  - Video files (`.mp4`, `.avi`, `.mkv`, etc.)
  - Image files (`.jpg`, `.png`, `.gif`, etc.)
  - Document files (`.pdf`, `.docx`, `.xlsx`, etc.)
  - Additional categories: Torrents, Applications, Installers, Archives, etc.
- Handles file name conflicts by renaming files to ensure uniqueness.
- Logs operations and errors for easier troubleshooting.

## Requirements

- Python 3.x
- `watchdog` library

You can install the required library using pip:

```bash
pip install watchdog
```

## Configuration

Before running the script, configure the following variables in the script:

- `source_dir`: Path to the source directory to monitor.
- `dest_dir_sfx`: Path to the destination directory for small audio files and sound effects.
- `dest_dir_music`: Path to the destination directory for larger audio files.
- `dest_dir_video`: Path to the destination directory for video files.
- `dest_dir_image`: Path to the destination directory for image files.
- `dest_dir_documents`: Path to the destination directory for document files.
- `dest_dir_torrent`: Path to the destination directory for torrent files.
- `dest_dir_application`: Path to the destination directory for application files.
- `dest_dir_installer`: Path to the destination directory for installer files.
- `dest_dir_archive`: Path to the destination directory for archive files.

## Usage

1. Configure the paths in the script.
2. Run the script:

```bash
python main.py
```

3. The script will start monitoring the source directory and sort files into the respective folders. It will also sort files present in the source directory when the script starts.

## Logging

The script logs all operations, including file movements and errors. Check the console output or log files for details.

## Troubleshooting

- **FileNotFoundError**: Ensure the file exists and is not being used by another process.
- **PermissionError**: Check file permissions and try running the script with elevated privileges if needed.
- **Unexpected Errors**: Review the log file for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- The `watchdog` library for file system monitoring.
- The Python community for continuous support and development.

```

Make sure to replace placeholder paths and descriptions with actual values and details relevant to your project. This `README.md` provides a comprehensive overview and guide for users to understand and use your script effectively.
