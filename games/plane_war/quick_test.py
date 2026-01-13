import pygame
import sys

# 初始化pygame
pygame.init()

# 创建窗口
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("快速测试")

# 测试字体
print("测试字体...")
try:
    font = pygame.font.SysFont('stheitimedium', 24)
    print(f"字体创建成功: {font}")
    text = font.render("测试中文字体", True, (255, 255, 255))
    print(f"文本渲染成功: {text}")
except Exception as e:
    print(f"字体错误: {e}")
    font = pygame.font.SysFont(None, 24)
    text = font.render("Test English", True, (255, 255, 255))

# 测试键盘
print("测试键盘控制...")
x, y = 200, 150

# 运行几帧
for i in range(100):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            print(f"帧{i}: 按键 {pygame.key.name(event.key)}")
    
    # 获取按键状态
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= 1
        print(f"帧{i}: 左箭头")
    if keys[pygame.K_RIGHT]:
        x += 1
        print(f"帧{i}: 右箭头")
    
    # 绘制
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 0, 0), (x, y, 20, 20))
    screen.blit(text, (10, 10))
    pygame.display.flip()
    
    # 控制帧率
    pygame.time.delay(16)  # 约60fps

print("测试完成")
pygame.quit()