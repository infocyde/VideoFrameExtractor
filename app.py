import streamlit as st
import os
import cv2
# from moviepy.editor import VideoFileClip
from moviepy import VideoFileClip
from pathlib import Path

st.set_page_config(page_title="Video Keyframe Extractor", layout="centered")
st.title("🎬 Extract First and Last Keyframes")

uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi", "mkv", "webm"])

def extract_keyframes(video_path):
    """
    Extracts the first and last keyframes from a video and saves them as PNGs.
    Returns file paths for display.
    """
    clip = VideoFileClip(video_path)
    duration = clip.duration
    cap = cv2.VideoCapture(video_path)

    # Prepare file paths
    video_name = Path(video_path).stem
    parent_dir = Path(video_path).parent

    first_frame_path = parent_dir / f"{video_name}_first.png"
    last_frame_path = parent_dir / f"{video_name}_last.png"

    # --- First frame ---
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, frame = cap.read()
    if success:
        cv2.imwrite(str(first_frame_path), frame, [cv2.IMWRITE_PNG_COMPRESSION, 0])
    else:
        first_frame_path = None

    # --- Last frame ---
    cap.set(cv2.CAP_PROP_POS_MSEC, (duration - 0.1) * 1000)
    success, frame = cap.read()
    if success:
        cv2.imwrite(str(last_frame_path), frame, [cv2.IMWRITE_PNG_COMPRESSION, 0])
    else:
        last_frame_path = None

    cap.release()
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

    first_frame, last_frame = extract_keyframes(str(video_path))

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
