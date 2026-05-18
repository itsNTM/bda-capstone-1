import time
import csv
from library import download_video, read_video_urls, get_video_metadata
from multiprocessing import Pool

if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"

    csv_path = "data/video_urls.csv"
    urls = read_video_urls(csv_path)
    print(urls)
   
    #metadata
    metadata_rows = []
    
    for url in urls:
        metadata = get_video_metadata(url)
        metadata_rows.append(metadata)

    with open("data/video_metadata.csv", "w", newline="") as file:
        fieldnames = ["title", "duration", "uploader", "view_count", "ext", "url"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(metadata_rows)

    # #serial
    # #start timer 
    # start = time.perf_counter()

    # #download start after timer
    # for url in urls:
    #     print("Downloading:", url)
    #     download_video(url)

    # #stop timer
    # end = time.perf_counter()
    # elapsed = end - start

    # #calculate total time
    # serial_time = round(elapsed, 2)
    # print(f"Serial execution: {serial_time}")

    #parallel
    #start timer 
    start = time.perf_counter()

    with Pool() as pool:
        results = pool.map(download_video, urls)

    #stop timer
    end = time.perf_counter()
    elapsed = end - start

    #calculate total time
    parallel_time = round(elapsed, 2)
    print(f"Parallel execution: {parallel_time}")
    
    #handle failures
    failed = []
    for result in results:
        if result["status"] == "failed":
            failed.append(result)
            print("Failed:", result["url"])
            print("Error:", result["error"])

    #report
    serial_time = 10.9
    speedup = round(((serial_time - parallel_time) / serial_time) * 100, 2)
    report_text = f"""# Report
    #Serial execution
    Total time: {serial_time} seconds
    # Parallel execution
    Total time: {parallel_time} seconds
    #Comparison
    Speed improvement: {speedup}%

    ## Download status
    Successful downloads: {len(urls) - len(failed)}
    Failed downloads: {len(failed)}
    """
    if failed:
        report_text += "\n### Failed URLs\n"
        for f in failed:
            report_text += f"\nURL: {f['url']}\nError: {f['error']}\n"

    # Ensure reports folder exists
    from pathlib import Path
    Path("reports").mkdir(exist_ok=True)

    # Save report
    with open("reports/sequential_report.md", "w") as f:
        f.write(report_text)
