from PIL import Image
import matplotlib.pyplot as plt
import os

def slice_image_by_click(image_path: str, output_folder: str, num_clicks_x: int, num_clicks_y: int):
    """
    依據使用者點擊設定的 X 與 Y 軸切割線，對圖片進行分割。
    
    程式流程：
      1. 顯示圖片讓使用者依序點擊設定縱向切割線（只取 X 座標）。
      2. 顯示圖片讓使用者依序點擊設定水平切割線（只取 Y 座標）。
      3. 分別將左右邊界 (0 與圖片寬度) 及上下邊界 (0 與圖片高度) 加入，並排序。
      4. 根據這些邊界將圖片切割成多個區塊，並依序儲存。
    
    參數：
      image_path   : 輸入圖檔路徑
      output_folder: 輸出資料夾
      num_clicks_x : 設定縱向切割線的點擊次數（中間線數）
      num_clicks_y : 設定水平切割線的點擊次數（中間線數）
    """
    # 1. 讀取圖片
    image = Image.open(image_path)
    img_width, img_height = image.size

    # 2. 取得縱向切割線 (X 座標)
    plt.figure("設定縱向切割線 (X 軸)")
    plt.imshow(image)
    plt.title(f"請點擊 {num_clicks_x} 次以設定縱向切割線 (僅取 X 座標)")
    clicks_x = plt.ginput(num_clicks_x, timeout=0)
    plt.close()
    # 擷取 X 座標並排序，再加入左右邊界：0 與圖片寬度
    x_coords = sorted([int(x) for x, y in clicks_x])
    boundaries_x = [0] + x_coords + [img_width]
    print("設定的縱向邊界 (X):", boundaries_x)

    # 3. 取得水平切割線 (Y 座標)
    plt.figure("設定水平切割線 (Y 軸)")
    plt.imshow(image)
    plt.title(f"請點擊 {num_clicks_y} 次以設定水平切割線 (僅取 Y 座標)")
    clicks_y = plt.ginput(num_clicks_y, timeout=0)
    plt.close()
    # 擷取 Y 座標並排序，再加入上下邊界：0 與圖片高度
    y_coords = sorted([int(y) for x, y in clicks_y])
    boundaries_y = [0] + y_coords + [img_height]
    print("設定的水平邊界 (Y):", boundaries_y)

    # 4. 建立輸出資料夾（若不存在）
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 5. 根據 X 與 Y 的邊界進行切割
    index = 0
    for i in range(len(boundaries_y) - 1):
        top = boundaries_y[i]
        bottom = boundaries_y[i+1]
        for j in range(len(boundaries_x) - 1):
            left = boundaries_x[j]
            right = boundaries_x[j+1]
            cropped_image = image.crop((left, top, right, bottom))
            output_path = os.path.join(output_folder, f"slice_{index}.png")
            cropped_image.save(output_path)
            index += 1

    print(f"切割完成！共切出 {index} 張圖片。")

if __name__ == "__main__":
    # 請將 IMAGE_PATH 替換為你圖片的實際路徑
    IMAGE_PATH = "/Users/zhouhongyu/WebstormProjects/Waiting_for_the_web_page/other/pngegg.png"
    OUTPUT_FOLDER = "slices_by_click"
    
    # 範例：縱向點擊 4 次（產生 5 段），水平點擊 5 次（產生 6 段）
    NUM_CLICKS_X = 4
    NUM_CLICKS_Y = 5

    slice_image_by_click(IMAGE_PATH, OUTPUT_FOLDER, NUM_CLICKS_X, NUM_CLICKS_Y)
