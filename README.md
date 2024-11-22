# Audio Extractor Service

A Flask-based service that extracts audio from video files and optionally trims them to a maximum size of 10MB.

## Repository

[https://github.com/ChornyiDev/AudioSliser.git](https://github.com/ChornyiDev/AudioSliser.git)

## Requirements

- Python 3.8+
- ffmpeg

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ChornyiDev/AudioSliser.git
   cd AudioSliser
   ```

2. Install ffmpeg:

   - **Ubuntu/Debian:**
     ```bash
     sudo apt-get update
     sudo apt-get install ffmpeg
     ```

   - **CentOS:**
     ```bash
     sudo yum install ffmpeg
     ```

   - **macOS:**
     ```bash
     brew install ffmpeg
     ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the server:
   ```bash
   python app.py
   ```

2. Make a POST request to `/process-video` with JSON body:
   ```json
   {
       "video_url": "https://example.com/video.mp4"
   }
   ```

The service will:
- Download the video
- Extract the audio
- Convert it to MP3
- Trim to 10MB if necessary
- Return the audio file
- Clean up temporary files automatically

## API Endpoints

### POST /process-video

Request body:
```json
{
    "video_url": "string (required)"
}
```

Response:
- Success: Audio file (MP3)
- Error: JSON with error message

## Error Handling

The service handles various errors including:
- Invalid URLs
- Download failures
- Conversion issues
- File size limitations

All temporary files are automatically cleaned up, even in case of errors.

## Additional Recommendations for Server Installation

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # for Linux/macOS
   # or
   .venv\Scripts\activate  # for Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure ffmpeg is installed:
   ```bash
   ffmpeg -version
   ```

4. For production use, it is recommended to:
   - Use Gunicorn or uWSGI instead of the built-in Flask server
   - Set up Nginx as a reverse proxy
   - Configure SSL/TLS
   - Set request size limits
   - Configure logging

5. Example of running with Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

6. Basic Nginx configuration:
   ```nginx
   server {
       listen 80;
       server_name your_domain.com;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.
```
