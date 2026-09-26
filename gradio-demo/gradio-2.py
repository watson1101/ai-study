# 1.import
import gradio
import numpy as np

# pip install opencv-python
import cv2 # opencv lib, for image & video

# 2.图像转铅笔画
def img_to_sketch(image):

    # 3.彩色图片转为灰度图（L模式表灰度，每个像素只有一个亮度值0-256）
    gray_image = image.convert("L")

    # 4.将灰度图转为numpy 数组以便于数学计算，然后取反，255-原值，亮变暗暗变亮，模拟取反的效果
    inverted_image = 255 - np.array(gray_image)

    # 5.对取反后的图像进行高斯模糊（平滑），模拟“模糊负片”
    blu = cv2.GaussianBlur(inverted_image, (5, 5), 0)

    # 6.再次取反，恢复为正常亮度（模糊正片）
    inverted_blu = 255 - blu

    # 7.核心步骤
    # 将原始灰度图除以模糊正片，得到素描效果
    # 除法操作会增强边缘对比度，暗部被保留，亮部被抑制，形成铅笔线条感
    # scale=100 是为了将结果放大到 0-255 范围（除法结果通常小于1）
    pencil_sketch = cv2.divide(np.array(gray_image), inverted_blu, scale=100)

    # 8.返回素描图数组，gradio 会自动识别成图片
    return pencil_sketch

# 9.创建 gradio 界面，
demo = gradio.Interface(
    fn=img_to_sketch, # 要执行的函数
    inputs=[gradio.Image(label="upload image", type="pil")], # 输入为图片组件，类型为 pil
    outputs=[gradio.Image(label="铅笔画✏")], # 输出，显示素描结果
    title="图像转铅笔画"
)

# 启动web应用，打开浏览器
demo.launch()