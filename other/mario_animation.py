import pygame
import sys
import os
from typing import List

def play_mario_animation(image_paths: List[str], frame_duration: int = 500) -> None:
    """
    輪流播放2-3張馬里奧圖片
    
    參數:
        image_paths: 圖片路徑列表（2-3張圖片）
        frame_duration: 每張圖片顯示的時間（毫秒），默認500ms
    """
    # 初始化Pygame
    pygame.init()
    
    try:
        # 加載圖片
        images = [pygame.image.load(path) for path in image_paths]
        
        # 獲取圖片尺寸並創建窗口
        width = max(img.get_width() for img in images)
        height = max(img.get_height() for img in images)
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Mario Animation')
        
        # 初始化計時器和當前圖片索引
        clock = pygame.time.Clock()
        last_switch = pygame.time.get_ticks()
        current_image_index = 0
        
        # 主循環
        running = True
        while running:
            current_time = pygame.time.get_ticks()
            
            # 處理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            # 切換圖片
            if current_time - last_switch > frame_duration:
                current_image_index = (current_image_index + 1) % len(images)
                last_switch = current_time
            
            # 清空屏幕
            screen.fill((255, 255, 255))
            
            # 顯示當前圖片
            current_image = images[current_image_index]
            screen.blit(current_image, ((width - current_image.get_width()) // 2,
                                       (height - current_image.get_height()) // 2))
            
            # 更新顯示
            pygame.display.flip()
            clock.tick(60)
    
    except pygame.error as e:
        print(f"Pygame錯誤：{e}")
    except Exception as e:
        print(f"發生錯誤：{e}")
    finally:
        pygame.quit()

def main():
    # 設置圖片路徑
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    mario_dir = os.path.join(base_dir, 'img', 'mario')
    
    # 列出可用的圖片
    available_images = [f for f in os.listdir(mario_dir) if f.endswith('.png')]
    
    if len(available_images) < 2:
        print("錯誤：在img/mario目錄下找不到足夠的PNG圖片")
        return
    
    print("可用的圖片：")
    for i, img in enumerate(available_images):
        print(f"{i+1}. {img}")
    
    try:
        # 獲取用戶想要使用的圖片數量
        num_images = int(input("\n請選擇要使用的圖片數量（2或3）："))
        if num_images not in [2, 3]:
            print("錯誤：只能選擇2或3張圖片")
            return
        
        # 獲取用戶選擇的圖片
        image_paths = []
        for i in range(num_images):
            choice = int(input(f"請選擇第{i+1}張圖片（輸入編號）：")) - 1
            if not (0 <= choice < len(available_images)):
                print("錯誤：無效的選擇")
                return
            image_paths.append(os.path.join(mario_dir, available_images[choice]))
        
        # 開始動畫
        print("\n按ESC鍵退出動畫")
        play_mario_animation(image_paths)
        
    except ValueError:
        print("錯誤：請輸入有效的數字")
    except Exception as e:
        print(f"發生錯誤：{e}")

if __name__ == "__main__":
    main()