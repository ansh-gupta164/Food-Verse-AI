"""
Kitchen Hygiene and Food Safety Assessment Service: Evaluates food preparation environments,
cross-contamination controls, PPE usage, surface sanitation, and optional bounded video frame sampling.
"""

import io
import os
import tempfile
from typing import Any, Dict, List, Optional, Tuple
from services.ai_service import AIService
from utils.constants import HYGIENE_DISCLAIMER, MAX_VIDEO_FRAMES
from utils.sample_data import SAMPLE_HYGIENE_REPORT

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    cv2 = None
    CV2_AVAILABLE = False


class HygieneService:
    """
    Manages kitchen hygiene visual inspection and scoring.
    """

    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service

    def extract_video_frames(self, video_bytes: bytes, max_frames: int = MAX_VIDEO_FRAMES) -> Tuple[bool, str, List[Tuple[bytes, str]]]:
        """
        Safely samples up to `max_frames` evenly spaced keyframes from uploaded video bytes using OpenCV.
        """
        if not CV2_AVAILABLE:
            return False, "OpenCV (cv2) is not installed in the environment for video decoding.", []

        temp_video = None
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as f:
                f.write(video_bytes)
                temp_video = f.name

            cap = cv2.VideoCapture(temp_video)
            if not cap.isOpened():
                return False, "Could not decode video file stream. Ensure codec is standard H.264 MP4.", []

            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
            duration_sec = total_frames / fps if fps > 0 else 0

            if duration_sec > 60:
                cap.release()
                return False, f"Video duration ({duration_sec:.1f}s) exceeds the maximum allowed 60 seconds limit.", []

            if total_frames <= 0:
                cap.release()
                return False, "Empty or unreadable video file.", []

            # Sample evenly spaced frame indices
            step = max(1, total_frames // max_frames)
            sampled_frames: List[Tuple[bytes, str]] = []

            for i in range(0, min(total_frames, max_frames * step), step):
                cap.set(cv2.CAP_PROP_POS_FRAMES, i)
                ret, frame = cap.read()
                if ret and frame is not None:
                    # Resize frame for efficient token usage and fast network transmission
                    h, w = frame.shape[:2]
                    target_w = 640
                    target_h = int(h * (target_w / w))
                    resized = cv2.resize(frame, (target_w, target_h), interpolation=cv2.INTER_AREA)

                    # Encode to JPEG
                    ret2, buffer = cv2.imencode(".jpg", resized, [cv2.IMWRITE_JPEG_QUALITY, 85])
                    if ret2:
                        sampled_frames.append((buffer.tobytes(), "image/jpeg"))

                if len(sampled_frames) >= max_frames:
                    break

            cap.release()

            if not sampled_frames:
                return False, "No valid frames could be extracted from video.", []

            return True, f"Successfully sampled {len(sampled_frames)} frames across {duration_sec:.1f}s.", sampled_frames

        except Exception as e:
            return False, f"Video processing error: {str(e)}", []
        finally:
            if temp_video and os.path.exists(temp_video):
                try:
                    os.remove(temp_video)
                except Exception:
                    pass

    def assess_kitchen_hygiene(
        self,
        image_bytes: Optional[bytes] = None,
        video_bytes: Optional[bytes] = None,
        mime_type: str = "image/jpeg",
        force_demo: bool = False
    ) -> Dict[str, Any]:
        """
        Assesses kitchen hygiene from image or video frames using Gemini or curated benchmarks.
        """
        if force_demo or not self.ai_service.is_live():
            report = SAMPLE_HYGIENE_REPORT.copy()
            return {
                "source": "Curated Demo Hygiene Audit",
                "is_ai_generated": False,
                "data": report,
                "disclaimer": HYGIENE_DISCLAIMER,
                "warning": "Demo Mode: Displaying standard kitchen hygiene audit benchmark. Configure Gemini API key for live computer vision."
            }

        prompt = """
        You are an HACCP certified Commercial Food Safety & Kitchen Hygiene Inspector.
        Conduct an objective visual hygiene audit of this food preparation environment.

        Examine visible parameters:
        1. Personal Hygiene & PPE: Hairnets, beard guards, clean apron, glove barrier for ready-to-eat items.
        2. Surface Sanitation: Countertops, floor drains, cutting board condition, grease/residue buildup.
        3. Cross-Contamination Controls: Physical separation of raw animal proteins and ready-to-eat produce, color-coded utensils.
        4. Storage & Chemical Safety: Sealed containers, date labels, separation of sanitizing chemicals from food contact surfaces.

        Return a strict JSON object with this exact schema:
        {
            "overall_score": 80,
            "rating": "Excellent" | "Acceptable / Good Standard" | "Needs Improvement" | "Critical Risk",
            "summary": "Concise executive summary of visible hygiene conditions",
            "rubric_breakdown": {
                "Surface Cleanliness & Sanitation": 20,
                "Cross-Contamination Prevention": 20,
                "Personal Protective Equipment (PPE)": 20,
                "Food Storage & Chemical Separation": 20
            },
            "observations": [
                {
                    "category": "Cross-Contamination / Surface Cleanliness / PPE / Storage",
                    "observation": "Specific visual observation noted",
                    "risk": "Assessment of microbiological, physical, or chemical hazard",
                    "action": "Concrete, actionable corrective SOP recommendation"
                }
            ]
        }

        Rubric guidelines:
        - Each of the 4 categories is scored out of 25 (total 100).
        - Do not grant unearned points. Be strict, transparent, and educational.
        """

        sys_inst = "You are a professional HACCP food safety compliance officer. Output strict valid JSON."

        # Case A: Video frame analysis
        if video_bytes:
            success_extract, msg, frames = self.extract_video_frames(video_bytes)
            if not success_extract:
                return {
                    "source": "Video Processing Error",
                    "is_ai_generated": False,
                    "data": SAMPLE_HYGIENE_REPORT.copy(),
                    "disclaimer": HYGIENE_DISCLAIMER,
                    "warning": f"Could not process video: {msg}. Switched to fallback benchmark."
                }

            success_ai, raw_text, parsed_json = self.ai_service.analyze_frames(
                frames_bytes=frames,
                prompt=prompt + f"\nNote: You are reviewing {len(frames)} chronologically sampled video frames.",
                system_instruction=sys_inst
            )
        # Case B: Static image analysis
        elif image_bytes:
            success_ai, raw_text, parsed_json = self.ai_service.analyze_image(
                image_bytes=image_bytes,
                mime_type=mime_type,
                prompt=prompt,
                system_instruction=sys_inst
            )
        else:
            return {
                "source": "Demo Benchmark",
                "is_ai_generated": False,
                "data": SAMPLE_HYGIENE_REPORT.copy(),
                "disclaimer": HYGIENE_DISCLAIMER,
                "warning": "No media provided. Showing standard audit sample."
            }

        if success_ai and parsed_json and isinstance(parsed_json, dict) and "overall_score" in parsed_json:
            # Validate score bounds
            try:
                score = int(parsed_json.get("overall_score", 75))
                parsed_json["overall_score"] = max(0, min(100, score))
            except Exception:
                parsed_json["overall_score"] = 75

            return {
                "source": "Live Gemini Multimodal AI",
                "is_ai_generated": True,
                "data": parsed_json,
                "disclaimer": HYGIENE_DISCLAIMER,
                "warning": None
            }

        # Fallback on AI parse failure
        return {
            "source": "Fallback Demo (AI Error)",
            "is_ai_generated": False,
            "data": SAMPLE_HYGIENE_REPORT.copy(),
            "disclaimer": HYGIENE_DISCLAIMER,
            "warning": f"Could not parse live AI hygiene evaluation. Displaying verified benchmark report."
        }
