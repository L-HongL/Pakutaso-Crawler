# Pakutaso 图片下载器

这是一个基于 Playwright 的 Pakutaso 图片素材下载脚本。脚本会打开 Microsoft Edge，通过关键词搜索或直接访问搜索结果页面，逐页下载大尺寸图片。

## 功能

- 支持输入搜索关键词，或输入 Pakutaso 页面网址
- 支持设置下载数量，默认下载 20 张
- 自动翻页并保存图片到运行目录下的 `image` 文件夹
- 运行时显示图片文件名和保存路径

## 环境要求

- Windows
- Microsoft Edge 浏览器
- Python 3.9 或更高版本（运行 Python 脚本时）

## 安装依赖

在项目目录打开终端，运行：

```bash
python -m pip install beautifulsoup4 lxml playwright
```

Playwright 通常还需安装浏览器组件：

```bash
python -m playwright install chromium
```

脚本通过 Playwright 的 `channel="msedge"` 启动本机 Microsoft Edge，因此需要已安装 Edge。

## 运行

```bash
python 爬虫.py
```

根据提示输入搜索内容：

- 输入关键词，例如 `AI`
- 或输入 Pakutaso 页面网址，例如 `https://www.pakutaso.com/ai/aisozai.html`

然后输入下载数量；直接按回车使用默认值 20。脚本会打开 Edge 浏览器，请保持浏览器窗口运行，直到下载结束。

下载图片保存在当前工作目录的 `image` 文件夹中。若要下载更多图片，可在启动时输入更大的数量。

## 运行打包程序

项目附带 PyInstaller 生成的 Windows 可执行文件：

```text
 dist/Pakutaso下载器.exe
```

双击运行或在终端中启动后，按提示输入关键词或页面网址及下载数量。使用前请确保电脑已安装 Microsoft Edge。

## 注意事项

- Pakutaso 是日文网站，使用日文关键词或先在网站找到目标页面、再粘贴页面网址，通常更容易得到预期结果。
- 网站访问或下载失败时，可能与网络连接、网站页面结构变化或访问限制有关；脚本连接超时时会报错。
- 请遵守 Pakutaso 网站的使用条款及图片授权要求，确认素材用途符合对应许可。
