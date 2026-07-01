# 投喂式启动入口

把赛题原文、题目 PDF、题目 Word、题目截图或说明文本放到这里。

支持优先级：
1. `.txt` / `.md`：最稳定
2. `.docx`：可自动抽取正文
3. `.pdf`：需要本地 Python 环境安装 `pypdf` 或 `PyPDF2`
4. `.png` / `.jpg`：只登记文件，脚本不会自动 OCR，建议同时放文字版题目

数据文件请放入 `03_data/raw/`。

放好后，在项目根目录运行：

```bash
python scripts/start_from_inputs.py
```
