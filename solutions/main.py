import time
from library import download_video, read_video_urls
from multiprocessing import Pool

if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"

    csv_path = "data/video_urls.csv"
    urls = read_video_urls(csv_path)
    print(urls)

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
    """

    # 8. Ensure reports folder exists
    from pathlib import Path
    Path("reports").mkdir(exist_ok=True)

    # 9. Save report
    with open("reports/sequential_report.md", "w") as f:
        f.write(report_text)
