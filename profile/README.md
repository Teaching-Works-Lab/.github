# Teaching Works Lab

面向高校课程建设与教学运行的可复用 Codex Skills 与 Plugins。

这里的仓库不是一条必须从头跑到尾的流水线。它们按任务独立安装、按证据关系组合：培养方案提供课程约束，课程工作流生成课程基座、考核设计和课程大纲，试卷处理与资料归档在需要时作为并行工具使用。

## 从这里开始

| 你的任务 | 使用仓库 | 典型输入 | 主要产出 |
| --- | --- | --- | --- |
| 从培养方案建立一个专业的数据 Skill | [training-program-skill-factory](https://github.com/Teaching-Works-Lab/training-program-skill-factory) | 培养方案 PDF、复核决定 | 可查询、可审核的专业 Skill |
| 查询智能制造工程 2025 版课程依据 | [intelligent-manufacturing-syllabus](https://github.com/Teaching-Works-Lab/intelligent-manufacturing-syllabus) | 课程名称或代码 | 课程字段、指标点关系、派生追踪 |
| 建立课程基座、设计考核或编制课程大纲 | [course-teaching-workflows](https://github.com/Teaching-Works-Lab/course-teaching-workflows) | PPT、教材、参考大纲、培养方案依据 | `course-foundation.md`、`assessment-plan.md`、大纲 DOCX |
| 编制教案（Markdown 可编辑 + Word 定稿） | [lesson-plan-compiler](https://github.com/Teaching-Works-Lab/lesson-plan-compiler) | PPT、教材、课程大纲、培养方案依据 | `教案-working.md`、`教案.docx` |
| 对比、修正或套用试卷 Word 模板 | [exam-word-skill](https://github.com/Teaching-Works-Lab/exam-word-skill) | DOCX、PDF、标准模板 | 差异报告、规范化试卷 DOCX |
| 整理和检查课程考核归档材料 | [course-assessment-archive-skill](https://github.com/Teaching-Works-Lab/course-assessment-archive-skill) | 制度要求、已有材料、角色范围 | 目录树、文件映射、缺项与责任清单 |
| 运营学习通课程（题库、章节、作业发布、资料库） | [chaoxing-ops](https://github.com/Teaching-Works-Lab/chaoxing-ops) | 题目内容、课程参数（`courseId` / `clazzId` / `cpi` / `enc`） | 题库 `.xls`、已发布的测验/作业、已上传的课程资料 |
| 查询其他机械与车辆专业 2025 版课程依据 | [mechanical-engineering-syllabus](https://github.com/Teaching-Works-Lab/mechanical-engineering-syllabus)（及 upgrade、energy-and-power、vehicle 各版本） | 课程名称或代码 | 课程字段、指标点关系、派生追踪 |
| 归档课程教学成果（大纲 + 教案） | [course-teaching-archive](https://github.com/Teaching-Works-Lab/course-teaching-archive) | 已编制的课程大纲、教案 | 按年份分版本的原子化归档目录 |
| 把 Word 官方模板变成可复用填写 Skill，或填写校内项目申请书 | [word-template-auto-fill-skill](https://github.com/Teaching-Works-Lab/word-template-auto-fill-skill) | `.docx` 模板 + 内容 JSON | 格式零改动的已填 DOCX / 新专用 Skill |

## 它们怎样协作

```mermaid
flowchart TD
    A[培养方案 PDF] --> B[Training Program Skill Factory]
    B -->|生成但不自动安装| C[专业培养方案数据 Skill]
    C -->|可选培养方案依据| D[Course Teaching Workflows]
    E[PPT / 教材 / 教案 / 参考大纲] --> D
    D --> F[课程基座]
    D --> G[考核设计]
    D --> H[课程大纲 Markdown / DOCX]
    D --> K[教案 Markdown / DOCX]
    H -.需要试卷文档处理.-> I[Exam Word Skill]
    G -.需要资料归档检查.-> J[Course Assessment Archive Skill]
    I <-.可选协作.-> J
    H -.教学成果存档.-> L[Course Teaching Archive]
    M[学习通教师端 mooc2-ans] --> N[Chaoxing Ops]
    N --> O[题库 / 章节 / 测验 / 作业发布 / 资料库]
    P[Word 官方模板 .docx] --> Q[Docx Template to Skill]
    Q -->|生成但不自动安装| R[模板专用填写 Skill]
    T[内容 JSON] --> S[格式零改动的已填 DOCX]
    P --> V[CZJTU Project Application 2026]
    R --> S
    T --> V
    V --> S
    S -.verify_fill 独立验收.-> U[白名单外 0 处改动报告]
```

关系分为四类：

- **捆绑安装**：`course-teaching-workflows` 一次安装提供课程基座、考核设计和课程大纲编制三个 Skill。
- **可选协作**：试卷 Word、考核归档和专业数据 Skill 独立安装；任务需要时再组合。
- **生成产物**：培养方案工厂生成新的专业 Skill，但不会静默安装它；Word 模板元技能生成的专用填写 Skill 同样不会静默安装。
- **独立运营层**：`chaoxing-ops` 面向学习通平台实操（题库导入、章节管理、作业发布、资料库上传），不依赖课程文档链路。`word-template-auto-fill-skill` 是独立的模板填写层：元技能产出专用 Skill，申请书实例直接套用官方模板，两者都用 `verify_fill.py` 独立验收格式保真。`course-teaching-archive` 是纯存档仓库，不含可执行 Skill。

## 安装与触发不是一回事

先添加本组织的 Marketplace：

```text
codex plugin marketplace add Teaching-Works-Lab/.github
```

然后只安装当前任务需要的 Plugin，例如：

```text
codex plugin add course-teaching-workflows@teaching-works-lab
codex plugin add intelligent-manufacturing-syllabus@teaching-works-lab
```

添加 Marketplace 只是获得可安装目录，不会自动安装全部 Plugin。安装一个 Plugin 也不会自动安装它的可选协作项或生成产物。

> `chaoxing-ops` 走文件系统安装（`git clone https://github.com/Teaching-Works-Lab/chaoxing-ops.git ~/.workbuddy/skills/chaoxing-ops`），不在 Marketplace 目录内；安装与运行要求见其仓库 README。`word-template-auto-fill-skill` 同样不在 Marketplace 内，用包内 `python install.py` 安装两个 Skill（依赖 lxml，装后跑 `check_env.py`）。`course-teaching-archive` 是纯存档仓库，直接查阅即可。

## WorkBuddy 兼容

本组织所有 Skill 同时兼容 WorkBuddy：根目录 `SKILL.md` 与 Codex Skill 同构，按各仓库 README 的「WorkBuddy 安装（Skill）」段克隆到 `~/.workbuddy/skills/<name>` 即可，`@skill:<name>` 显式调用。Codex Marketplace 与 WorkBuddy skills 目录是两套并行发现机制，可同时安装、互不干扰；多 Skill 捆绑包（`course-teaching-workflows`）在 WorkBuddy 下按三个子 Skill 分别安装。

安装后可以让 Codex 根据请求与 Skill 描述自动选择，也可以显式调用：
```text
$training-program-skill-factory
$intelligent-manufacturing-syllabus
$course-foundation-builder
$course-assessment-planner
$course-syllabus-compiler
$lesson-plan-compiler
$exam-word
$course-assessment-archive
```

在 WorkBuddy 下同名 Skill 用 `@skill:<name>` 显式调用；新安装的 Skill 在下次会话起可识别：

```text
@skill:chaoxing-ops
@skill:docx-template-to-skill
@skill:czjtu-project-application-2026
```

当任务重要、名称相近或希望固定工作方式时，优先显式调用。

## 给 AI 和维护者

- [`catalog.yaml`](https://github.com/Teaching-Works-Lab/.github/blob/main/catalog.yaml) 是仓库角色、输入输出、触发名称和关系的机器可读清单。
- [`.agents/plugins/marketplace.json`](https://github.com/Teaching-Works-Lab/.github/blob/main/.agents/plugins/marketplace.json) 是可选择安装的 Plugin 目录。
- GitHub Project 只用于路线图和 Issue 进度；它不表示运行依赖，也不负责安装。
- 每个仓库自己的 `README.md` 和 `SKILL.md` 仍是该工具的规范说明。

所有仓库默认保持公开、可审查，并区分来源事实、派生关系、待编制内容和生成结果。
