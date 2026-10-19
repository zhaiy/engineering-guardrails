# 来源与致谢 / Sources and acknowledgements

本仓库的指令、说明与合成示例是为编码代理任务编写的原创整理。下面的资料提供背景和设计启发；本仓库没有复制书籍段落或示例代码，也不声称逐章提炼、完整覆盖或替代这些书籍。链接不表示作者、出版社或平台认可本项目。MIT 许可证仅适用于本仓库原创内容。

The instructions, documentation, and synthetic examples are an original synthesis for coding-agent tasks. The sources below provide background and inspiration, not copied passages or code. This project does not claim exhaustive extraction, replace the books, or imply endorsement. Referenced material retains its original rights.

## 工程判断 / Engineering judgment

| 资料 | 在本仓库中的启发 |
| --- | --- |
| Martin Fowler, [*Refactoring*, second edition](https://martinfowler.com/books/refactoring.html) | 通过小步修改和验证控制重构风险，区分重构与行为变化。 |
| Martin Fowler, [YAGNI](https://martinfowler.com/bliki/Yagni.html) | 用当前需求评估抽象和扩展点，避免为推测的未来需求增加复杂度。 |
| Google, [What to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html) | 从功能、设计、复杂度、测试和上下文评估变更。 |
| Joshua Bloch, [*Effective Java*, third edition](https://www.pearson.com/en-us/subject-catalog/p/effective-java/P200000000138/9780134686042) | Java API、对象、异常与并发相关判断的背景；具体建议仍须匹配项目 JDK 与契约。 |
| Brian Goetz et al., [*Java Concurrency in Practice*](https://jcip.net/) | Java 并发推理的背景，尤其是共享状态和并发正确性。 |

这些是概念层面的参考关系，不是对书中具体条目、页码或原文的逐项映射。涉及特定 API 和版本时，应以项目配置及对应版本的官方文档为准。

These are conceptual influences, not item-by-item mappings to book text. Consult the project's configuration and version-appropriate official documentation for specific APIs and runtime behavior.

## Java API 与框架契约 / Java API and framework contracts

- [Java 8 BigDecimal](https://docs.oracle.com/javase/8/docs/api/java/math/BigDecimal.html)：数值比较与 scale、精度的区别。
- [Spring transaction annotations](https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/annotations.html)：事务代理边界；使用时查阅项目对应版本。

## 技能格式与安装 / Skill format and installation

- [OpenAI — Build skills](https://learn.chatgpt.com/docs/build-skills)：技能目录、渐进加载、显式与隐式调用及 Codex 元数据。
- [Vercel Labs — Skills CLI v1.7.2](https://github.com/vercel-labs/skills/tree/v1.7.2)：README 中的安装、列举、范围选择与卸载命令。
- [Skills CLI v1.7.2 package declaration](https://github.com/vercel-labs/skills/blob/v1.7.2/package.json)：安装器版本与 Node.js 最低版本。

本项目采用这些公开格式与工具进行本地技能分发。安装器支持哪些代理，不等于本技能在那些代理上已经完成效果验证；实际验证范围见 [评估说明](evaluation.md)。

The installer supports multiple agents; that does not establish this skill's effectiveness on each one. See [Evaluation](evaluation.md) for the actual scope and evidence.
