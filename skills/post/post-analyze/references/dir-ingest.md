# 目录级参考解析规则

## 支持类型
- 文档: .md .txt .pdf .docx
- 表格: .xlsx .csv
- 图片: .png .jpg .jpeg .webp

## 递归策略
- 默认递归扫描全部子目录。
- 过滤隐藏目录与临时文件。

## 抽样与索引
- 文档: 提取标题, 目录, 前后 N 行, 关键词命中段落。
- 表格: 提取表头与前两行, 保留列名。
- PDF/Docx: 优先目录与摘要页, 再抽样关键段落。
- 图片: 先 OCR, 再生成摘要。

## OCR 规则
- OCR 结果作为强证据进入分析。
- 每条 OCR 结果附带置信标签与来源标记。
- 低置信度内容在正文中建议标注出处或不确定性。

## 相关性筛选
- 先生成 resource_index, 再筛选 Top-K 进入深度分析。
- K 依据目录规模调整, 目标保持成本可控。

## 产出格式(建议)
- resource_index: [{source, type, updated_at, summary, confidence}]
