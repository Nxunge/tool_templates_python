# tool_templates_python

一个基于python的快速构建win32执行程序的模板



1. 依赖python 3.7.9-win32
2. 编译步骤:

```
pip install -r requirements.txt
pyinstaller --name program --onefile --hidden-import=win32timezone --hidden-import=pywintypes --hidden-import=pythoncom main.py --add-data "plugins;plugins"
```

2. 运行文件只需要dist文件夹下的"program.exe"
3. 所有要执行的业务代码,写到plugins文件夹下,例子参考test.py,会动态加载执行
