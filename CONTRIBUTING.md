# Contributing

欢迎提交具体反例、文档修正和有证据支持的改进。Issues and pull requests in Chinese or English are welcome.

## 提出改进

请描述一个具体任务：原本需要什么行为，技能引导了什么行为，以及为什么需要调整。附上可公开的最小示例；移除凭据、个人路径、客户数据和未授权公开的代码。

保持核心指令简短、通用。语言或框架细节放入按需加载的参考文件。建议应尊重适用的仓库指引、运行时版本与已有契约，并说明适用条件；不要将风格偏好写成普遍规则。

## 提交变更

1. 将改动限制在一个明确问题，同步更新中英文 README 中受影响的说明。
2. 修改行为指引时，加入能暴露该问题的合成任务或反例；参考 [评估说明](docs/evaluation.md) 执行相关检查，并保留失败结果。
3. 在仓库根目录运行 `python3 scripts/validate.py`，报告实际结果。文档修正无需为凑覆盖率新增代码测试。
4. PR 中说明问题、改动原因、验证命令与结果，以及未覆盖的情况。

报告代理评估时，记录技能版本、模型、提示词、运行环境和评分依据。区分结构校验、任务执行、人工判断与生产证据；不要把单次通过写成稳定提升，也不要据此宣称其他代理已验证。

## 来源与许可

贡献应是你有权以本仓库 MIT 许可证提供的原创内容。新增参考资料时，更新 [来源说明](docs/sources.md)，优先链接作者、出版社或官方文档。请勿复制受版权保护的书籍段落、代码示例或内部资料；引用某本书不意味着本仓库完整提炼或替代了它。

## English overview

Keep each contribution focused on a concrete failure or improvement. Preserve repository constraints and existing contracts, place language-specific guidance in conditional references, and keep the core concise. Provide public synthetic examples, run `python3 scripts/validate.py`, and follow the [evaluation procedure](docs/evaluation.md) for behavioral changes. Report evidence and limitations honestly, update both READMEs when needed, and contribute only material you can license under MIT.
