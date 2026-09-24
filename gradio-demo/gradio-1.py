## 1.pip install gradio
import gradio

# 2.函数：接受一个名字，返回一个带问候的字符串
def say_hello(name):
    return f'Hello {name}!'

# 3. 创建gradio ui
# fn：指定要执行的函数
# inputs:输入的组件类型，text 表示文本框，用户可以输入文字内容
# outputs：输出组件类型
demo = gradio.Interface(
    fn=say_hello,
    inputs="text",
    outputs="text"
)

#  启动web应用
# launch() 会开启一个web服务器
demo.launch()