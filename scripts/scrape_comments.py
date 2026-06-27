from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_RECENT
import pandas as pd
import os
import time
from tqdm import tqdm

# === KONFIGURASI ===
INPUT_PATH = "data/raw/video_list_filtered.csv"
OUTPUT_PATH = "data/raw/comments_raw.csv"
MAX_COMMENTS_PER_VIDEO = 300   
SLEEP_BETWEEN_VIDEOS = 2       


def scrape_comments_for_video(downloader, video_row: dict, max_comments: int):
    """Scrape komentar untuk satu video, kembalikan list of dict."""
    comments = []
    try:
        generator = downloader.get_comments_from_url(
            video_row["url"], sort_by=SORT_BY_RECENT
        )
        for i, comment in enumerate(generator):
            if i >= max_comments:
                break
            comments.append({
                "video_id": video_row["video_id"],
                "video_title": video_row["title"],
                "channel": video_row["channel"],
                "keyword": video_row.get("keyword", ""),
                "comment_id": comment.get("cid"),
                "text": comment.get("text"),
                "author": comment.get("author"),
                "time_text": comment.get("time"),   # contoh: "2 minggu lalu"
                "likes": comment.get("votes"),
                "reply_count": comment.get("reply_count", 0),
            })
    except Exception as e:
        print(f"[WARNING] Gagal scrape video {video_row.get('video_id')}: {e}")

    return comments


def main():
    if not os.path.exists(INPUT_PATH):
        print(f"[ERROR] File {INPUT_PATH} tidak ditemukan.")
        print("Jalankan dulu 01_search_videos.py, lalu buat video_list_filtered.csv secara manual.")
        return

    video_df = pd.read_csv(INPUT_PATH)
    print(f"[INFO] {len(video_df)} video akan di-scrape komentarnya.")

    downloader = YoutubeCommentDownloader()
    all_comments = []

    for _, row in tqdm(video_df.iterrows(), total=len(video_df), desc="Scraping videos"):
        comments = scrape_comments_for_video(downloader, row.to_dict(), MAX_COMMENTS_PER_VIDEO)
        all_comments.extend(comments)
        time.sleep(SLEEP_BETWEEN_VIDEOS)

    df = pd.DataFrame(all_comments)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"\n[INFO] Total komentar terkumpul: {len(df)}")
    print(f"[INFO] Disimpan ke: {OUTPUT_PATH}")
    print("\n=== Preview ===")
    print(df[["video_title", "text"]].head())


if __name__ == "__main__":
    main()
