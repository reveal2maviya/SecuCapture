# SecuCapture

![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Description

SecuCapture is a security-focused web application that enables the secure capture of video footage from the user's camera while providing the option to record geolocation data. This open-source project is dedicated to promoting data security and privacy in research and data capture scenarios.

SecuCapture uses Flask, JavaScript, and HTML to create a user-friendly interface, allowing users to grant permission to access their cameras securely and record video while protecting their data.

## Features

- Securely capture video footage with a focus on data security.
- Optional recording of geolocation data for research purposes.
- Automatically save captured videos to the "captured_videos" directory.
- Safeguarded storage of geolocation data in text files for later analysis.

## Open Source for Life

SecuCapture is committed to being open source for life. We believe in the power of collaboration and open development to advance technology and enhance data security in research and beyond.

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.x
- Flask
- A modern web browser that supports WebRTC for camera access

## Installation

1. Clone this repository to your local machine:
  ```bash
  git clone https://github.com/reveal2maviya/SecuCapture.git
```
2. Navigate to the project directory:
```bash
cd SecuCapture
```
3. Install the required Python packages:
```bash
pip install flask
```
## Usage

1. Start the application by running the following command:
```bash
python app.py
```

2. Open a web browser and go to `https://localhost:443/`.

3. The browser will ask for permission to access your camera. Grant the permission to start capturing video securely.

4. You can also choose to share your geolocation data by checking the consent checkbox.

5. The captured videos will be saved in the "captured_videos" directory, and geolocation data will be stored in text files.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- This project uses Flask for the backend and JavaScript for client-side functionality.
- Inspiration for this project comes from the need to capture video and geolocation data for research purposes.

## Contact

Maviya Shaikh  

Project Link: [GitHub Repository](https://github.com/reveal2maviya/SecuCapture)
