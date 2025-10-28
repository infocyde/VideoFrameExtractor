import streamlit as st
import os
import cv2
import numpy as np
from moviepy import VideoFileClip
from pathlib import Path
from PIL import Image

st.set_page_config(page_title="Video Keyframe Extractor", layout="centered")
st.title("🎬 Extract First and Last Keyframes")

uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi", "mkv", "webm"])

def extract_keyframes_hq(video_path):
    """
    Extracts the first and last keyframes from a video at highest quality.
    Uses moviepy for better frame extraction.
    """
    clip = VideoFileClip(video_path)
    duration = clip.duration

    # Prepare file paths
    video_name = Path(video_path).stem
    parent_dir = Path(video_path).parent

    first_frame_path = parent_dir / f"{video_name}_first.png"
    last_frame_path = parent_dir / f"{video_name}_last.png"



    #FYI
    # For TIFF (lossless, larger files):
    #first_frame_pil.save(str(first_frame_path), 'TIFF', compression='none')

    # For high-quality JPEG (smaller files, minimal loss):
    #first_frame_pil.save(str(first_frame_path), 'JPEG', quality=100, subsampling=0)

    # --- Extract first frame using moviepy (better quality) ---
    try:
        first_frame = clip.get_frame(0)  # Get frame at t=0
        # Convert RGB to BGR for consistency if needed, or save directly
        first_frame_pil = Image.fromarray(first_frame)
        first_frame_pil.save(str(first_frame_path), 'PNG', compress_level=0)  # No compression
    except Exception as e:
        st.warning(f"Could not extract first frame: {e}")
        first_frame_path = None

    # --- Extract last frame ---
    try:
        # Get frame slightly before the end to avoid edge cases
        last_frame_time = max(0, duration - 0.1)
        last_frame = clip.get_frame(last_frame_time)
        last_frame_pil = Image.fromarray(last_frame)
        last_frame_pil.save(str(last_frame_path), 'PNG', compress_level=0)  # No compression
    except Exception as e:
        st.warning(f"Could not extract last frame: {e}")
        last_frame_path = None

    clip.close()
    return first_frame_path, last_frame_path


if uploaded_file is not None:
    # Save upload to disk temporarily
    save_dir = Path("uploaded_videos")
    save_dir.mkdir(exist_ok=True)
    video_path = save_dir / uploaded_file.name

    with open(video_path, "wb") as f:
        f.write(uploaded_file.read())

    st.write("Processing video… ⏳")

    first_frame, last_frame = extract_keyframes_hq(str(video_path))

    if first_frame:
        st.success(f"✅ First frame saved: {first_frame.name}")
        st.image(str(first_frame), caption="First Keyframe", width='stretch')
    else:
        st.error("❌ Could not extract the first frame.")

    if last_frame:
        st.success(f"✅ Last frame saved: {last_frame.name}")
        st.image(str(last_frame), caption="Last Keyframe", width='stretch')
    else:
        st.error("❌ Could not extract the last frame.")

    st.info(f"Images are saved in: `{video_path.parent}`")