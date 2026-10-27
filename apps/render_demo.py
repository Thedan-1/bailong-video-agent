"""Run the one-shot demo directly from a checkout."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "packages" / "bailong-video" / "src"))

from bailong_video.demo import main  # noqa: E402


if __name__ == "__main__":
    main()
