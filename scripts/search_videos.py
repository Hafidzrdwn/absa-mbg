import scrapetube
import pandas as pd
import os
from datetime import datetime

# === KONFIGURASI ===
KEYWORDS = [
    "Makan Bergizi Gratis",
    "MBG keracunan",
    "Reviu MBG",
    "MBG anggaran",
    "MBG BGN",
]

VIDEOS_PER_KEYWORD = 15 
OUTPUT_PATH = "data/raw/video_list.csv"


def search_videos(keyword: str, limit: int = 15):
    """
    Cari video YouTube berdasarkan keyword, tanpa API key.
    Mengembalikan list of dict berisi info dasar tiap video.
    """
    print(f"[INFO] Mencari video untuk keyword: '{keyword}' ...")
    results = []
    try:
        videos = scrapetube.get_search(keyword, limit=limit)
        for v in videos:
            video_id = v.get("videoId")
            title = v.get("title", {}).get("runs", [{}])[0].get("text", "")
            channel = (
                v.get("longBylineText", {})
                .get("runs", [{}])[0]
                .get("text", "")
            )
            published = v.get("publishedTimeText", {}).get("simpleText", "")

            results.append({
                "video_id": video_id,
                "title": title,
                "channel": channel,
                "published_text": published,
                "keyword": keyword,
                "url": f"https://www.youtube.com/watch?v={video_id}",
            })
    except Exception as e:
        print(f"[WARNING] Gagal mencari untuk keyword '{keyword}': {e}")

    print(f"[INFO] Ditemukan {len(results)} video untuk '{keyword}'")
    return results


def main():
    all_results = []
    for kw in KEYWORDS:
        all_results.extend(search_videos(kw, limit=VIDEOS_PER_KEYWORD))

    df = pd.DataFrame(all_results)

    before = len(df)
    df = df.drop_duplicates(subset="video_id", keep="first")
    print(f"[INFO] Total video unik: {len(df)} (dari {before} sebelum dedup)")

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"[INFO] Disimpan ke: {OUTPUT_PATH}")

    print("\n=== LANGKAH SELANJUTNYA (WAJIB MANUAL) ===")
    print(f"1. Buka {OUTPUT_PATH}")
    print("2. Review tiap baris, hapus video yang tidak relevan dengan topik MBG")
    print("3. Simpan hasil filter sebagai: data/raw/video_list_filtered.csv")
    print("4. Baru jalankan: python scripts/02_scrape_comments.py")


if __name__ == "__main__":
    main()
