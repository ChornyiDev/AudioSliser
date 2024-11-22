from flask import Flask, send_file, request, jsonify
from pydub import AudioSegment
import os
import requests
import sys

app = Flask(__name__)

@app.route('/process-video', methods=['POST'])
def process_video():
    temp_files = []  # Track files to clean up
    try:
        if not request.is_json:
            print("Request is not JSON")
            return jsonify({"error": "Content-Type must be application/json"}), 400

        data = request.get_json()
        print(f"Received data: {data}")

        if not data or 'video_url' not in data:
            print("No video URL in request")
            return jsonify({"error": "video_url is required"}), 400

        video_url = data['video_url']
        print(f"Starting to process video: {video_url}")
        
        output_dir = "downloads"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        audio_path = download_and_process_audio(video_url, output_dir)
        if audio_path:
            temp_files.append(audio_path)
        
        if not audio_path or not os.path.exists(audio_path):
            print(f"Audio path not found: {audio_path}")
            return jsonify({"error": "Failed to process video"}), 500

        print(f"Sending file: {audio_path}")
        response = send_file(
            audio_path,
            mimetype='audio/mpeg',
            as_attachment=True,
            download_name='output_audio.mp3'
        )

        # Clean up after sending response
        @response.call_on_close
        def cleanup():
            for file_path in temp_files:
                try:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        print(f"Cleaned up file: {file_path}")
                except Exception as e:
                    print(f"Error cleaning up {file_path}: {str(e)}")

        return response

    except Exception as e:
        # Clean up files if there's an error
        for file_path in temp_files:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"Cleaned up file on error: {file_path}")
            except Exception as cleanup_error:
                print(f"Error cleaning up {file_path}: {str(cleanup_error)}")
        
        print(f"Error in process_video: {str(e)}", file=sys.stderr)
        return jsonify({"error": str(e)}), 500

def download_and_process_audio(video_url, output_dir, max_size_mb=10):
    temp_video_path = None
    try:
        print(f"Downloading from URL: {video_url}")
        
        # Download video
        temp_video_path = os.path.join(output_dir, "temp_video")
        response = requests.get(video_url, stream=True)
        response.raise_for_status()
        
        with open(temp_video_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        print(f"Downloaded to: {temp_video_path}")

        # Convert to mp3
        output_path = os.path.join(output_dir, "output_audio.mp3")
        audio = AudioSegment.from_file(temp_video_path)
        audio.export(output_path, format="mp3")
        print(f"Converted to MP3: {output_path}")

        # Clean up temp video file
        if temp_video_path and os.path.exists(temp_video_path):
            os.remove(temp_video_path)
            print(f"Cleaned up temp video file: {temp_video_path}")

        # Check and trim if necessary
        file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"File size: {file_size_mb:.2f}MB")

        if file_size_mb > max_size_mb:
            print(f"Trimming audio to {max_size_mb}MB...")
            ratio = max_size_mb / file_size_mb
            target_duration = len(audio) * ratio
            trimmed_audio = audio[:int(target_duration)]
            trimmed_audio.export(output_path, format="mp3")
            print("Trimming complete")

        return output_path

    except Exception as e:
        # Clean up temp video file if there's an error
        if temp_video_path and os.path.exists(temp_video_path):
            try:
                os.remove(temp_video_path)
                print(f"Cleaned up temp video file on error: {temp_video_path}")
            except Exception as cleanup_error:
                print(f"Error cleaning up temp file: {str(cleanup_error)}")
        
        print(f"Error in download_and_process_audio: {str(e)}", file=sys.stderr)
        return None

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
