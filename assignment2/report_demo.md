# PharmaX 风险评估报告 — TA Demo 讲稿 / TA Demo Script

> 本文件用于明天向 TA 演示 `report.pdf` 时的中英文对照讲稿。每节按照「原文 → 中文翻译 → Demo 讲解 → 可能的 TA 提问」的顺序编排。
>
> This document is the bilingual demo script for tomorrow's TA presentation of `report.pdf`. Each section follows the order of "Original → Chinese Translation → Demo Talk → Possible TA Questions".

---

## 📋 目录 / Table of Contents

1. [开场白 / Opening](#开场白--opening)
2. [第 1 节 · Introduction](#第-1-节--introduction)
3. [第 2 节 · Assumptions](#第-2-节--assumptions)
4. [第 3 节 · Findings & Recommendations](#第-3-节--findings--recommendations)
   - [Finding 1 · Phishing](#finding-1--phishing-and-spear-phishing-attacks)
   - [Finding 2 · Ransomware](#finding-2--ransomware-deployment)
   - [Finding 3 · Insider Threat](#finding-3--insider-threat-and-unauthorized-consultant-access)
   - [Finding 4 · Supply Chain (CodeX)](#finding-4--supply-chain-compromise-via-codex-cicd-pipeline)
   - [Finding 5 · Unpatched Vulnerabilities](#finding-5--exploitation-of-unpatched-vulnerabilities)
   - [Finding 6 · Data Exfiltration](#finding-6--data-exfiltration-of-medical-research-ip)
   - [Finding 7 · VPN Compromise](#finding-7--vpn-compromise-and-remote-worker-exploitation)
   - [Finding 8 · Third-Party Provider Breach](#finding-8--third-party-provider-breach-cloudx-hostingx-secx)
   - [Finding 9 · Physical Security](#finding-9--physical-security-breach-and-document-theft)
   - [Finding 10 · DDoS / Outage](#finding-10--ddos-attack-or-infrastructure-failure-affecting-cloud-connect)
5. [第 4 节 · Conclusion](#第-4-节--conclusion)
6. [常见 TA 问题汇总 / FAQ Cheat Sheet](#常见-ta-问题汇总--faq-cheat-sheet)

---

## 开场白 / Opening

**🇨🇳 中文：**
> 老师好，我是 Zhenyu Song。今天我要演示的是为 PharmaX 这家中型制药公司做的高层定性 Top 10 安全风险评估报告。整份报告遵循 NIST SP 800-30 Rev.1 的方法论，使用了 Appendix D（威胁源）、Appendix E（威胁事件）、Appendix G（可能性）、Appendix H（影响）和 Appendix I（风险确定）这几个表格。报告分为 4 个部分：Introduction、Assumptions、Findings & Recommendations、Conclusion。

**🇬🇧 English:**
> Hi Professor / TA, I'm Zhenyu Song. Today I'll be demoing my high-level qualitative Top 10 security risk assessment report for PharmaX, a mid-sized pharmaceutical company. The whole report follows the NIST SP 800-30 Rev.1 methodology, using Appendix D (Threat Sources), Appendix E (Threat Events), Appendix G (Likelihood), Appendix H (Impact), and Appendix I (Risk Determination). The report has four sections: Introduction, Assumptions, Findings & Recommendations, and Conclusion.

---

## 第 1 节 · Introduction

### 📄 原文 / Original

> This report is a high-level qualitative security risk assessment for PharmaX. The goal is to identify and prioritize the top 10 security risks and provide recommendations for each one. The methodology follows NIST SP 800-30, using threat events from Table E-2, threat sources from Appendix D, and the qualitative risk scales from Appendix G (Likelihood), Appendix H (Impact), and Appendix I (Risk Determination).
>
> **Why This Assessment Is Needed**
> PharmaX has never done a security risk assessment before. The company's security maturity is low, and security awareness among employees and management is weak. They handle sensitive customer data and proprietary medical research data, but there is no formal documentation of critical assets or data flows. A penetration test was done in the past by an external company, but the report was not taken seriously by management and ended up sitting on a shelf.
>
> On top of that, PharmaX relies heavily on several third-party companies (CloudX, HostingX, SecX, CodeX) for critical infrastructure and development. About half the workforce works remotely. All of this creates a large and complex attack surface that needs to be assessed.

### 🀄 中文翻译

> 本报告是针对 PharmaX 的一份高层定性安全风险评估。目标是识别并对前 10 项安全风险进行优先级排序，并为每一项提供建议。方法论遵循 NIST SP 800-30，使用 Table E-2 的威胁事件、Appendix D 的威胁源，以及 Appendix G（可能性）、Appendix H（影响）、Appendix I（风险确定）的定性评估表。
>
> **为什么需要这次评估**
> PharmaX 之前从未做过安全风险评估。公司的安全成熟度较低，员工和管理层的安全意识也比较薄弱。他们处理敏感的客户数据和专有的医学研究数据，但没有正式的关键资产或数据流文档。过去外部公司做过一次渗透测试，但报告没有被管理层重视，最后被搁置在书架上。
>
> 此外，PharmaX 高度依赖多家第三方公司（CloudX、HostingX、SecX、CodeX）来提供关键基础设施和开发服务。大约一半的员工远程办公。这些综合因素造成了一个庞大且复杂的攻击面，必须进行评估。

### 🎤 Demo 讲解 / Demo Talk

**🇨🇳：**
这一节我先说明报告的目标和方法论。重点是 PharmaX 之前从未做过安全风险评估，安全成熟度低、过去的渗透测试报告还被管理层束之高阁，再加上有 4 个第三方供应商和 50% 的远程员工，攻击面非常大。所以这次评估非常必要。

**🇬🇧:**
In this section I lay out the goal and methodology of the report. The key motivation is that PharmaX has never done a risk assessment before — security maturity is low, the previous pen test report was shelved by management, and on top of that they depend on four third-party vendors and have 50% of staff working remotely. That makes the attack surface very large, so the assessment is overdue.

### ❓ TA 可能提问 / Possible TA Questions

| # | 中文 | English |
|---|---|---|
| Q1 | 你为什么选 NIST 800-30 而不是 ISO 27005 或 FAIR？ | Why did you pick NIST 800-30 over ISO 27005 or FAIR? |
| **A** | 因为作业要求里明确指定了 NIST SP 800-30 Rev.1 的方法论（Appendix D/E/G/H/I），而且它的定性风险打分表对一份高层报告来说最直观、最容易让管理层看懂。 | The assignment explicitly requires the NIST SP 800-30 Rev.1 methodology (Appendices D/E/G/H/I), and its qualitative scoring tables are the most intuitive way to present a high-level report to non-technical management. |
| Q2 | "高层定性"评估是什么意思？ | What does "high-level qualitative" mean here? |
| **A** | 「高层」指我们不深入到具体配置，比如某台服务器的具体补丁版本；「定性」指我们用 Low / Moderate / High / Very High 这种描述性等级，而不是用具体的损失金额（量化）。这是 NIST 800-30 推荐给资源有限、还没有定量数据的组织的入门方法。 | "High-level" means we don't go down to specific configurations, e.g., the patch version of a specific server. "Qualitative" means we use descriptive ratings (Low / Moderate / High / Very High) instead of dollar-amount loss figures. NIST recommends this approach for organizations that lack the quantitative data needed for a fully quantitative assessment. |

---

## 第 2 节 · Assumptions

### 📄 原文 / Original

> Since the assignment description does not cover every detail of PharmaX's environment, the following assumptions are made. These are needed to properly evaluate the risks and none of them contradict the information given in the assignment.
>
> 1. **No formal security policies exist.** No documented incident response plans, acceptable use policies, data classification policies, or BC/DR plans.
> 2. **No security awareness training.** Employees and consultants have not gone through any structured cybersecurity training.
> 3. **The VPN does not use multi-factor authentication (MFA).**
> 4. **No formal patch management and no EDR deployed.**
> 5. **External consultants and some executives use personal, unmanaged laptops, and there is no formal onboarding/offboarding process.**
> 6. **The CI/CD pipeline managed by CodeX has access to PharmaX source code.**
> 7. **No third-party risk management program.**
> 8. **SecX only monitors firewall traffic.**
> 9. **Medical research data is treated as trade secrets and high-value intellectual property.**
> 10. **Physical security at office locations is basic.**

### 🀄 中文翻译

> 由于作业描述没有覆盖 PharmaX 环境的所有细节，做出以下假设。这些假设都是为了能正确评估风险所必需的，且与作业中给出的信息均不矛盾。
>
> 1. **不存在正式的安全策略。** 没有事件响应计划、可接受使用策略、数据分类策略，也没有业务连续性/灾难恢复计划。
> 2. **没有安全意识培训。** 员工和外部顾问都没有接受过结构化的网络安全培训。
> 3. **VPN 没有启用多因素认证（MFA）。**
> 4. **没有正式的补丁管理流程，也没有部署 EDR。**
> 5. **外部顾问和部分高管使用个人非托管笔记本电脑，且没有正式的入/离职流程。**
> 6. **CodeX 管理的 CI/CD 管道可以访问 PharmaX 的源代码。**
> 7. **没有第三方风险管理项目。**
> 8. **SecX 只监控防火墙流量。**
> 9. **医学研究数据被视为商业机密和高价值知识产权。**
> 10. **办公室物理安全只是基础水平。**

### 🎤 Demo 讲解 / Demo Talk

**🇨🇳：**
这一节是整份报告的「地基」。作业里只描述了 PharmaX 的高层情况，很多细节没说，所以我必须做假设。我做了 10 条假设，每一条都没有违反作业里已经给出的事实。例如作业说 Cloud Connect 是 CloudX 提供的，那我就不会假设别的公司提供网络。这些假设直接为后面 10 个 Finding 提供依据。

**🇬🇧:**
This section is the foundation of the whole report. The assignment only describes PharmaX at a high level, so many details are missing — I had to fill them in with assumptions. I made 10 assumptions, and none of them contradicts the facts given. For example, the assignment says Cloud Connect is provided by CloudX, so I don't assume any other company provides networking. These assumptions directly support the 10 findings that follow.

### ❓ TA 可能提问 / Possible TA Questions

| # | 中文 | English |
|---|---|---|
| Q1 | 你怎么保证你的假设没有和作业描述矛盾？ | How do you ensure your assumptions don't contradict the assignment description? |
| **A** | 我对照作业里每一条事实——比如 "Cloud Connect 由 CloudX 提供"、"SecX 提供安全监控"、"CodeX 在越南提供应用开发"——我的假设只是在这些已知事实之外**填补缺失的细节**（例如有没有 MFA、有没有 EDR），而不是替换掉它们。 | I cross-checked every fact stated in the assignment — e.g., "Cloud Connect is provided by CloudX," "SecX provides security monitoring," "CodeX provides app development from Vietnam." My assumptions only **fill in missing details** (like whether MFA or EDR exists), without replacing any stated fact. |
| Q2 | 为什么假设没有 MFA？说不定 CloudX 的 VPN 默认就有 MFA。 | Why assume there's no MFA? CloudX's VPN might enable MFA by default. |
| **A** | 因为作业明确说公司"安全成熟度低"，并且管理层把渗透测试报告搁置了。在这种环境下，最有可能的情况就是只用密码而没有 MFA。同时这也是一个**保守评估**——如果实际上有 MFA，我们的风险评分会下降，但绝不会被低估。 | The assignment explicitly states the company has "low security maturity" and that management shelved a pen test report. In that environment, password-only auth is the most realistic baseline. It's also a **conservative assumption** — if MFA does exist, the risk drops, but we will not have under-estimated it. |
| Q3 | 你假设了 10 条，会不会太多了？ | Aren't 10 assumptions too many? |
| **A** | 因为作业要求覆盖 Top 10 风险，而 PharmaX 的环境涉及人员、第三方、网络、终端、数据、物理几个维度，10 条假设刚好让每个维度都有清晰前提，避免在 Findings 部分临时加假设。 | The Top 10 findings span people, third parties, networks, endpoints, data, and physical dimensions. Ten assumptions give each dimension a clear baseline so I don't have to introduce ad-hoc assumptions inside the findings section. |

---

## 第 3 节 · Findings & Recommendations

### 📊 风险概览表 / Risk Summary Table

| # | Threat Event | Likelihood | Impact | Risk |
|---|---|---|---|---|
| 1 | Phishing / Spear Phishing | High | High | **High** |
| 2 | Ransomware | High | Very High | **Very High** |
| 3 | Insider Threat / Consultant Access | Moderate | High | **Moderate** |
| 4 | Supply Chain Compromise via CodeX | Moderate | Very High | **High** |
| 5 | Unpatched Vulnerabilities | High | High | **High** |
| 6 | Data Exfiltration of Research IP | Moderate | Very High | **High** |
| 7 | VPN / Remote Worker Compromise | High | Moderate | **Moderate** |
| 8 | Third-Party Provider Breach | Moderate | Very High | **High** |
| 9 | Physical Security Breach | Low | Moderate | **Low** |
| 10 | DDoS on Cloud Connect | Moderate | High | **Moderate** |

**🇨🇳 整体讲解：** 我把 10 个 Finding 按照 NIST 800-30 的格式都列了出来：威胁事件（来自 Table E-2）、威胁源（Appendix D）、漏洞、可能性、影响、综合风险、建议。下面我挑几个高风险的重点讲。

**🇬🇧 Overall:** I listed all 10 findings in the NIST 800-30 format: Threat Event (Table E-2), Threat Sources (Appendix D), Vulnerabilities, Likelihood, Impact, Overall Risk, and Recommendations. I'll focus the demo on the highest-risk ones.

---

### Finding 1 · Phishing and Spear Phishing Attacks

#### 📄 原文 / Original

> **Threat Event (Table E-2):** Craft phishing attacks; Craft spear phishing attacks
>
> All 160 employees and consultants use Outlook email and web browsers with Internet access. Since there is no security awareness training (Assumption #2) and employees have weak security awareness, phishing emails are very likely to trick someone into giving up credentials or clicking malicious links. Spear phishing targeting executives is also a concern since the board has little security experience.
>
> **Likelihood: High** — Phishing is the most common attack vector, and PharmaX has zero training to defend against it.
> **Impact: High** — Stolen credentials could give attackers access to customer PII, payment data, and medical research IP.
> **Overall Risk: High**
>
> **Recommendations:** Mandatory security awareness training; Email security gateway with sandboxing/URL analysis; Quarterly phishing simulations; MFA on email and critical systems.

#### 🀄 中文翻译

> **威胁事件（Table E-2）：** 实施钓鱼攻击；实施鱼叉式钓鱼攻击。
>
> 全部 160 名员工和顾问都使用 Outlook 邮箱和能上网的浏览器。由于没有安全意识培训（假设 #2）、员工安全意识薄弱，钓鱼邮件非常容易骗到有人交出凭据或点击恶意链接。针对高管的鱼叉式钓鱼也是个隐患，因为董事会几乎没有安全经验。
>
> **可能性：High** — 钓鱼是最常见的攻击向量，PharmaX 完全没有培训来防御。
> **影响：High** — 被盗的凭据可能让攻击者拿到客户 PII、支付数据和医学研究 IP。
> **综合风险：High**
>
> **建议：** 强制安全意识培训；带沙箱/URL 分析的邮件安全网关；至少每季度做一次钓鱼演练；邮件和关键系统部署 MFA。

#### 🎤 Demo 讲解 / Demo Talk

**🇨🇳：** 钓鱼是最经典也最常见的攻击。PharmaX 的弱点是 160 个用户全部联网，但又零培训。我把可能性和影响都打成 High，建议优先做培训和 MFA，因为这是性价比最高的。

**🇬🇧:** Phishing is the most classic and common attack vector. PharmaX's weakness is having all 160 users on Internet-connected mail with zero training. I scored both likelihood and impact as High, and prioritized awareness training and MFA — these are the highest ROI controls.

#### ❓ TA 可能提问 / Possible TA Questions

| 中文 | English |
|---|---|
| 你为什么把 Likelihood 评成 High 而不是 Very High？ | Why is Likelihood "High" rather than "Very High"? |
| **A:** Very High 在 Appendix G 的定义里是"几乎确定一年内会发生数十次成功攻击"。考虑到 CloudX 至少有基础的反垃圾邮件，部分钓鱼会被拦下来，所以 High 更合适。 | **A:** Per Appendix G, "Very High" means "almost certainly hundreds of successful events per year." Since CloudX has basic anti-spam that blocks some attempts, "High" — frequent but not guaranteed — fits better. |

---

### Finding 2 · Ransomware Deployment

#### 📄 原文 / Original

> **Threat Event (Table E-2):** Deliver known malware to internal organizational information systems; Deliver targeted malware for control of internal systems and exfiltration of data
>
> Attackers could deliver ransomware through email or compromised websites to encrypt PharmaX's data and demand payment. Since there is no EDR or formal patch management (Assumption #4) and no incident response plan (Assumption #1), PharmaX would be highly vulnerable and poorly prepared to respond.
>
> **Likelihood: High** — Pharma companies are high-value targets for ransomware.
> **Impact: Very High** — Ransomware could encrypt medical research data, customer records, and business systems across both data centers. Recovery could take weeks and cost millions.
> **Overall Risk: Very High**
>
> **Recommendations:** Deploy EDR; Set up immutable, offline backups; Create and test an incident response plan; Develop a BC/DR plan.

#### 🀄 中文翻译

> **威胁事件：** 向内部信息系统投递已知恶意软件；投递定向恶意软件以控制内部系统并窃取数据。
>
> 攻击者可以通过邮件或被攻陷的网站投递勒索软件，加密 PharmaX 的数据并勒索赎金。由于没有 EDR、没有正式补丁管理（假设 #4）、也没有事件响应计划（假设 #1），PharmaX 既容易被攻陷，也难以从容应对。
>
> **可能性：High** — 制药公司是勒索软件的高价值目标。
> **影响：Very High** — 勒索软件可能加密两个数据中心的医学研究数据、客户记录和业务系统。恢复可能需要数周时间，损失数百万美元。
> **综合风险：Very High**
>
> **建议：** 部署 EDR；建立不可变的离线备份并定期测试恢复；制定并演练事件响应剧本；制定 BC/DR 计划。

#### 🎤 Demo 讲解 / Demo Talk

**🇨🇳：** 这是整个报告里**唯一**一个 Very High 的风险，也是我最强调的。原因是制药行业是勒索软件的"重灾区"，而 PharmaX 同时在三个关键控制上存在缺失：没有 EDR、没有补丁、没有事件响应计划。任何一个缺失都很糟糕，三个叠加就是灾难级。

**🇬🇧:** This is the **only** Very High risk in the entire report and the one I emphasize most. The pharmaceutical industry is a top target for ransomware, and PharmaX has gaps in three critical controls simultaneously: no EDR, no patching, no IR plan. Any one of these is bad — all three together is catastrophic.

#### ❓ TA 可能提问 / Possible TA Questions

| 中文 | English |
|---|---|
| 为什么 Ransomware 的影响是 Very High，而 Phishing 是 High？两者起点都是邮件啊。 | Why is ransomware impact "Very High" but phishing only "High"? Both start with email. |
| **A:** Phishing 的直接影响是凭据泄漏，攻击者还需要进一步行动；而 Ransomware 一旦执行就会加密两个数据中心的所有数据，包含医学研究和客户记录，业务直接停摆。所以影响等级更高。 | **A:** Phishing's immediate impact is stolen credentials — the attacker still needs follow-on actions. Ransomware, once executed, encrypts everything across both data centers — research, customer data, business systems — and operations stop. Hence the higher impact rating. |
| 为什么需要 *immutable / offline* 备份？普通备份不行吗？ | Why specifically *immutable / offline* backups? Aren't normal backups enough? |
| **A:** 现代勒索软件会主动搜索网络上挂载的备份并一并加密。Immutable 备份只能写入不能删除，offline 备份不在网络上，这两个特性才能保证勒索软件加密不到。 | **A:** Modern ransomware actively hunts and encrypts mounted network backups. Immutable backups can be written but not deleted, and offline backups aren't reachable on the network — both properties are required to survive ransomware. |

---

### Finding 3 · Insider Threat and Unauthorized Consultant Access

#### 📄 原文 / Original

> **Threat Event (Table E-2):** Obtain unauthorized access; Conduct insider-based social engineering to obtain information
>
> The 20 external consultants use personal, unmanaged laptops and there is no formal process for revoking access when people leave (Assumption #5). There are also no regular access reviews or privileged access management controls.
>
> **Likelihood: Moderate · Impact: High · Overall Risk: Moderate**
>
> **Recommendations:** RBAC + least privilege; Formal onboarding/offboarding with immediate revocation; MDM/NAC for device compliance; Quarterly access reviews.

#### 🀄 中文翻译

> **威胁事件：** 获取未授权访问；通过内部人员的社会工程手段获取信息。
>
> 20 名外部顾问使用个人非托管笔记本电脑，且员工离职时没有正式的撤销访问流程（假设 #5）；同时缺少定期访问权限复查和特权访问管理。
>
> **可能性：Moderate · 影响：High · 综合风险：Moderate**
>
> **建议：** RBAC + 最小权限；规范化入/离职流程，离职即撤销访问；MDM / NAC 设备合规性检查；季度访问权限复查。

#### 🎤 Demo 讲解 / Demo Talk

**🇨🇳：** 重点是 20 个外部顾问加上部分高管使用**个人非托管笔记本**。即使他们没恶意，也可能因为设备不安全间接导致泄漏；而且没有离职流程，前员工的账户可能长期保留。这是个 People + Process 的问题。

**🇬🇧:** The key issue is the 20 external consultants and several executives using **personal, unmanaged laptops**. Even without malicious intent, an insecure device can cause indirect leaks, and without an offboarding process, former employees may retain access for a long time. This is fundamentally a people + process problem.

#### ❓ TA 可能提问 / Possible TA Questions

| 中文 | English |
|---|---|
| 为什么 Likelihood 只是 Moderate？ | Why is likelihood only "Moderate"? |
| **A:** 大多数顾问不会主动作恶，所以可能性不是 High；但缺乏控制让"无意泄漏"和"恶意行为"都成为现实可能，所以也不是 Low。 | **A:** Most consultants won't act maliciously, so it's not High; but the lack of controls makes both accidental leakage and malicious actions realistic, so it's not Low either. |

---

### Finding 4 · Supply Chain Compromise via CodeX CI/CD Pipeline

#### 📄 原文 / Original

> **Threat Event (Table E-2):** Compromise design, manufacture, and/or distribution of information system components; Insert targeted malware into organizational information systems
>
> CodeX in Vietnam provides and manages PharmaX's entire CI/CD pipeline. Since PharmaX has no oversight (Assumption #6) and no third-party risk management program (Assumption #7), an attacker could compromise CodeX's infrastructure to inject malicious code, or a CodeX insider could introduce a backdoor.
>
> **Likelihood: Moderate · Impact: Very High · Overall Risk: High**
>
> **Recommendations:** Require SOC 2 Type II / ISO 27001; Code signing & integrity checks for CI/CD artifacts; Code reviews + SAST/DAST on CodeX deliverables; Right-to-audit clause in the contract.

#### 🀄 中文翻译

> **威胁事件：** 攻陷信息系统组件的设计、制造或分发流程；向组织信息系统中植入定向恶意软件。
>
> 越南的 CodeX 提供并管理 PharmaX 的整个 CI/CD 管道。由于 PharmaX 没有监管（假设 #6），也没有第三方风险管理项目（假设 #7），攻击者可以攻陷 CodeX 的基础设施注入恶意代码，CodeX 的内部人员也可能植入后门。
>
> **可能性：Moderate · 影响：Very High · 综合风险：High**
>
> **建议：** 要求 SOC 2 Type II 或 ISO 27001 认证；CI/CD 产物代码签名 + 完整性校验；对 CodeX 交付的代码做 Code Review + SAST/DAST；合同里加 right-to-audit 条款。

#### 🎤 Demo 讲解 / Demo Talk

**🇨🇳：** 这是 SolarWinds 之后整个行业最关心的话题。CodeX 控制着 PharmaX 整个 CI/CD，等于一只看不见的手在写 PharmaX 的代码。最严重的情况是恶意代码被打包进发给客户的软件——影响远不止 PharmaX 自己。

**🇬🇧:** This is the topic the whole industry has been focused on since SolarWinds. CodeX controls PharmaX's entire CI/CD — effectively, an invisible hand is writing PharmaX's code. The worst case is malicious code shipping in software delivered to customers, which spreads the impact far beyond PharmaX itself.

#### ❓ TA 可能提问 / Possible TA Questions

| 中文 | English |
|---|---|
| 你建议让 CodeX 提供 SOC 2 报告，但 CodeX 不一定愿意配合，怎么办？ | You recommend requiring SOC 2 from CodeX, but CodeX may not comply — what then? |
| **A:** 这个谈判通常通过续约时把"提供 SOC 2 / ISO 27001"写进合同条款来实现，并配合 right-to-audit 条款。如果 CodeX 不愿意配合，那就是一个红旗，说明应该考虑替换或要求他们建立基础合规。 | **A:** This is usually negotiated at contract renewal by writing "must provide SOC 2 / ISO 27001" into the contract, together with a right-to-audit clause. If CodeX refuses, that's a red flag suggesting either replacement or requiring them to build baseline compliance. |

---

### Finding 5 · Exploitation of Unpatched Vulnerabilities

#### 📄 原文 / Original

> **Threat Event (Table E-2):** Exploit recently discovered vulnerabilities; Exploit vulnerabilities on internal organizational information systems
>
> PharmaX uses Microsoft Office, Edge/Chrome browsers, internal mail servers, domain controllers, and specialized pharma software. Without formal patch management (Assumption #4), critical vulnerabilities could remain unpatched for a long time. The outdated infrastructure documentation means the IT team might not even know about all the systems that need patching.
>
> **Likelihood: High · Impact: High · Overall Risk: High**
>
> **Recommendations:** Automated patch management; Vulnerability management with monthly scans + remediation SLAs; Up-to-date asset inventory.

#### 🀄 中文翻译

> **威胁事件：** 利用最近发现的漏洞；利用组织内部信息系统的漏洞。
>
> PharmaX 使用 Microsoft Office、Edge/Chrome 浏览器、内部邮件服务器、域控制器，以及专业的制药软件。由于没有正式的补丁管理（假设 #4），关键漏洞可能长期得不到修复。技术基础设施文档过时也意味着 IT 团队甚至不知道全部系统的存在，更谈不上打补丁。
>
> **可能性：High · 影响：High · 综合风险：High**
>
> **建议：** 自动化补丁管理；月度漏洞扫描 + 修复 SLA；保持资产清单实时更新。

#### 🎤 Demo 讲解 / Demo Talk

**🇨🇳：** 这一项被很多公司当成"基本功"，但 PharmaX 既没有自动化补丁，也没有最新的资产清单——意味着可能漏掉某些系统打不到补丁。这种系统通常是公开 CVE 工具（比如 Shodan）就能扫到的。

**🇬🇧:** Many companies treat patching as table stakes, but PharmaX has neither automated patching nor an up-to-date asset inventory — meaning some systems may never get patched. These are exactly the kinds of systems that public CVE scanners (like Shodan) find immediately.

---

### Finding 6 · Data Exfiltration of Medical Research IP

#### 📄 原文 / Original

> **Threat Event (Table E-2):** Obtain sensitive information via exfiltration; Compromise organizational information systems to facilitate exfiltration of data/information
>
> PharmaX's medical research data is high-value IP (Assumption #9). Attackers could use compromised credentials or malware to find and steal this data. Since SecX only monitors firewall traffic (Assumption #8), internal lateral movement and data staging would go completely undetected.
>
> **Likelihood: Moderate · Impact: Very High · Overall Risk: High**
>
> **Recommendations:** Data classification; Network segmentation between research and business networks; SIEM beyond just firewall traffic; DLP for unauthorized data transfers.

#### 🀄 中文翻译

> **威胁事件：** 通过数据外泄获取敏感信息；攻陷组织信息系统以便数据外泄。
>
> PharmaX 的医学研究数据是高价值 IP（假设 #9）。攻击者可以利用被盗凭据或恶意软件找到并窃取数据。由于 SecX 只监控防火墙流量（假设 #8），内部的横向移动和数据集结完全检测不到。
>
> **可能性：Moderate · 影响：Very High · 综合风险：High**
>
> **建议：** 数据分类；研发网络与业务网络做网络分段；SIEM 不止覆盖防火墙流量；部署 DLP 检测未授权外传。

#### 🎤 Demo 讲解 / Demo Talk

**🇨🇳：** 制药公司的研发数据是国家级别和竞争对手都盯着的目标。SecX 只看防火墙流量等于"只看大门，不管屋里"，攻击者一旦进来就完全没人监管。

**🇬🇧:** Research data at pharma companies is a target for both nation-states and competitors. SecX only watching firewall traffic is like "watching the front door but ignoring everything inside" — once an attacker is in, no one is watching.

---

### Finding 7 · VPN Compromise and Remote Worker Exploitation

#### 📄 原文 / Original

> **Threat Event (Table E-2):** Exploit split tunneling; Exploit known vulnerabilities in mobile systems (e.g., laptops)
>
> About 80 people (50% of 160) work remotely and connect via CloudX's VPN. Without MFA on the VPN (Assumption #3), a stolen password is all an attacker needs.
>
> **Likelihood: High · Impact: Moderate · Overall Risk: Moderate**
>
> **Recommendations:** MFA on VPN immediately; Disable split tunneling; NAC for device compliance; Company-managed laptops or MDM-enforced standards.

#### 🀄 中文翻译

> **威胁事件：** 利用分流隧道（split tunneling）；利用笔记本电脑等移动设备的已知漏洞。
>
> 大约 80 人（160 人的 50%）远程办公并通过 CloudX 的 VPN 接入。VPN 没有 MFA（假设 #3），攻击者只要拿到一个密码就能登入。
>
> **可能性：High · 影响：Moderate · 综合风险：Moderate**
>
> **建议：** 立即给 VPN 启用 MFA；禁用 split tunneling；用 NAC 做设备合规检查；要求公司托管笔记本或用 MDM 强制安全基线。

#### 🎤 Demo 讲解 / Demo Talk

**🇨🇳：** VPN + MFA 是行业最低成本、最高收益的修复，所以我把它列在 Conclusion 的"立即执行"里。

**🇬🇧:** VPN + MFA is the highest-ROI control in the industry — that's why I put it in the "Immediate" bucket of the Conclusion.

---

### Finding 8 · Third-Party Provider Breach (CloudX, HostingX, SecX)

#### 📄 原文 / Original

> PharmaX depends heavily on CloudX (networking, firewalls, VPN), HostingX (data centers), and SecX (security monitoring). A breach at any of these providers could directly compromise PharmaX. With no third-party risk management (Assumption #7), PharmaX has no way to verify or influence these providers' security posture.
>
> **Likelihood: Moderate · Impact: Very High · Overall Risk: High**
>
> **Recommendations:** Build a TPRM program with annual assessments; Require SOC 2 Type II; Incident notification & right-to-audit clauses; Contingency plans for provider failure.

#### 🀄 中文翻译

> PharmaX 高度依赖 CloudX（网络、防火墙、VPN）、HostingX（数据中心）、SecX（安全监控）。任何一家被攻陷都可能直接拖累 PharmaX。由于没有第三方风险管理（假设 #7），PharmaX 没办法验证或影响这些供应商的安全状态。
>
> **可能性：Moderate · 影响：Very High · 综合风险：High**
>
> **建议：** 建立 TPRM 项目，年度对所有关键供应商做安全评估；要求 SOC 2 Type II；合同里加事件通报义务和 right-to-audit 条款；制定供应商故障的应急计划。

#### 🎤 Demo 讲解 / Demo Talk

**🇨🇳：** Finding 4 是 CodeX 的供应链问题，Finding 8 是基础设施供应商的问题——分开讲是因为补救手段不一样：一个看代码完整性，一个看托管和监控。

**🇬🇧:** Finding 4 is the CodeX supply-chain problem; Finding 8 is the infrastructure-provider problem. I separated them because the controls differ — one focuses on code integrity, the other on hosting and monitoring.

---

### Finding 9 · Physical Security Breach and Document Theft

#### 📄 原文 / Original

> PharmaX has three office locations and still keeps printed files in filing cabinets. An attacker who gains physical access — through tailgating or social engineering — could steal documents, access unattended workstations, or plug in rogue devices.
>
> **Likelihood: Low · Impact: Moderate · Overall Risk: Low**
>
> **Recommendations:** Clean desk policy + locked cabinets; Auto screen lock after 5 minutes; Visitor management with sign-in / escort; Move toward fully electronic documentation.

#### 🀄 中文翻译

> PharmaX 有三个办公地点，至今还在文件柜里保存纸质文件。攻击者通过尾随或社会工程进入办公区后，可以偷文件、操作没锁屏的工作站，或在网络上插入恶意设备。
>
> **可能性：Low · 影响：Moderate · 综合风险：Low**
>
> **建议：** 清洁桌面策略 + 锁柜；5 分钟自动锁屏；访客签到与陪同制度；尽快全面电子化文档。

#### 🎤 Demo 讲解 / Demo Talk

**🇨🇳：** 这是整份报告里**唯一**一个 Low 风险，原因是物理攻击需要攻击者实地到场，威胁池小很多。但即使是 Low 我还是写了，体现 Top 10 的完整性。

**🇬🇧:** This is the **only** Low risk in the report — physical attacks require the attacker to be on-site, which shrinks the threat pool. I still included it because the Top 10 should cover the spectrum, not just the high-risk ones.

#### ❓ TA 可能提问 / Possible TA Questions

| 中文 | English |
|---|---|
| 既然是 Low risk，为什么还要写进 Top 10？ | If it's Low risk, why include it in the Top 10? |
| **A:** Top 10 不是"Top 10 高风险"而是"识别出的 10 项主要风险"——一份完整的报告需要覆盖所有风险维度。即使 Low，也提供了清洁桌面、自动锁屏这种几乎零成本的建议。 | **A:** The "Top 10" is not "Top 10 high risks" but "the 10 main identified risks" — a complete report should cover all dimensions. Even at Low, the recommendations (clean desk, auto-lock) are essentially zero-cost. |

---

### Finding 10 · DDoS Attack or Infrastructure Failure Affecting Cloud Connect

#### 📄 原文 / Original

> **Threat Event (Table E-2):** Conduct DDoS / DoS attacks
> **Threat Event (Table E-3, Non-Adversarial):** Infrastructure failure/outage (telecommunications, electrical power)
>
> All PharmaX offices connect through Cloud Connect as the sole network backbone. Disruption — adversarial or non-adversarial — leads to total loss of email, file access, and telephony.
>
> **Likelihood: Moderate · Impact: High · Overall Risk: Moderate**
>
> **Recommendations:** Improve DDoS mitigation with CloudX; Backup network connectivity (secondary ISP / SD-WAN); BCP for prolonged outages; SLAs with uptime + DDoS guarantees.

#### 🀄 中文翻译

> **威胁事件：** DDoS / DoS 攻击；非对抗性的基础设施故障（通信、电力）。
>
> PharmaX 所有办公室都通过 Cloud Connect 这一条网络主干连接。一旦中断——无论是攻击造成还是非对抗性事件造成——邮件、文件访问、电话全部失效。
>
> **可能性：Moderate · 影响：High · 综合风险：Moderate**
>
> **建议：** 与 CloudX 一起评估并提升 DDoS 缓解能力；准备备用网络连接（备用 ISP 或 SD-WAN）；制定长时网络中断的 BCP；SLA 中包含可用性保证和 DDoS 响应承诺。

#### 🎤 Demo 讲解 / Demo Talk

**🇨🇳：** 这是 Top 10 里**唯一**同时引用了 Table E-2（adversarial）和 Table E-3（non-adversarial）的 Finding。NIST 800-30 强调风险评估要覆盖**人为攻击**和**非人为故障**两个维度，所以我特意把它们一起写——实际上 Cloud Connect 失效带来的业务影响是一样的。

**🇬🇧:** This is the **only** finding in the Top 10 that pulls from both Table E-2 (adversarial) and Table E-3 (non-adversarial). NIST 800-30 explicitly says risk assessment should cover both **adversarial attacks** and **non-adversarial failures**, so I combined them — the business impact of a Cloud Connect outage is the same regardless of cause.

#### ❓ TA 可能提问 / Possible TA Questions

| 中文 | English |
|---|---|
| 你为什么把 DDoS 和基础设施故障合并成一个 Finding？ | Why combine DDoS and infrastructure failure into one finding? |
| **A:** 因为它们的根本风险是同一个——Cloud Connect 是单点故障。无论是被打 DDoS 还是 CloudX 自己设备坏了，PharmaX 损失的是同样的业务连续性，所以推荐的缓解措施（备用 ISP、BCP）也一样。这正好体现了 Table E-2 和 E-3 在风险评估里的协同。 | **A:** They share the same root risk — Cloud Connect is a single point of failure. Whether it's a DDoS or CloudX equipment failure, PharmaX loses the same business continuity, and the mitigations (backup ISP, BCP) are identical. It also shows how Tables E-2 and E-3 work together in a risk assessment. |

---

## 第 4 节 · Conclusion

### 📄 原文 / Original

> PharmaX faces serious security risks driven by its low security maturity and heavy dependence on third-party providers with no oversight. The most critical risk is ransomware (Very High), followed by several High-risk findings including phishing, supply chain attacks, unpatched vulnerabilities, data exfiltration, and third-party breaches.
>
> The recommended priority order is:
> 1. **Immediate:** MFA on VPN, security awareness training, patch management basics.
> 2. **Short-term:** EDR deployment, incident response plan, third-party risk management program.
> 3. **Long-term:** SIEM, data classification, network segmentation, formal security governance with board-level oversight.

### 🀄 中文翻译

> PharmaX 面临严重的安全风险，主要原因是安全成熟度低，且严重依赖第三方供应商但缺乏监督。最关键的风险是 Ransomware（Very High），紧随其后是 Phishing、Supply Chain、Unpatched Vulnerabilities、Data Exfiltration 和 Third-Party Breaches 这几个 High 风险。
>
> 推荐的优先级如下：
> 1. **立即执行：** VPN 上 MFA、安全意识培训、基础补丁管理。
> 2. **短期：** EDR 部署、事件响应计划、第三方风险管理项目。
> 3. **长期：** SIEM、数据分类、网络分段、董事会层级的安全治理。

### 🎤 Demo 讲解 / Demo Talk

**🇨🇳：** 我把建议按时间分了三档——这是为了让 PharmaX 的管理层能"看一眼就知道该花什么钱，先解决什么"。立即层都是低成本高收益；短期层成本中等；长期层是结构性投资，需要董事会层面推动。

**🇬🇧:** I bucketed the recommendations into three time horizons so PharmaX management can tell "at a glance" what to fund and in what order. Immediate items are low-cost high-impact; Short-term items are medium cost; Long-term items are structural investments that need board-level sponsorship.

### ❓ TA 可能提问 / Possible TA Questions

| 中文 | English |
|---|---|
| 如果 PharmaX 一年只能投一笔钱解决一件事，你建议哪个？ | If PharmaX could only fund one thing in the next year, what would you recommend? |
| **A:** VPN + MFA + 安全意识培训打包成一组——成本低、覆盖面广，能同时显著降低 Phishing、VPN compromise、Insider 三个 Finding 的风险。 | **A:** VPN MFA + security awareness training as a single package — low cost, broad coverage, simultaneously reduces Phishing, VPN Compromise, and Insider Threat risks. |

---

## 常见 TA 问题汇总 / FAQ Cheat Sheet

### 🔥 方法论类 / Methodology

| 中文 | English |
|---|---|
| **Q:** 你怎么决定 Likelihood 和 Impact 的等级？ | **Q:** How did you decide the Likelihood and Impact ratings? |
| **A:** 严格按 Appendix G（Likelihood）和 Appendix H（Impact）的 5 级定性表（Very Low / Low / Moderate / High / Very High）来评。综合风险来自 Appendix I 的 Table I-2 矩阵，把 Likelihood × Impact 映射到一个等级。 | **A:** Strictly per Appendix G (Likelihood) and Appendix H (Impact) with their 5-level qualitative scales (Very Low / Low / Moderate / High / Very High). Overall risk comes from the Table I-2 matrix in Appendix I, which maps Likelihood × Impact into one rating. |
| **Q:** 这是定性评估，那有没有打算后续做定量？ | **Q:** Since this is qualitative, do you plan a quantitative follow-up? |
| **A:** 是的。定性评估是 PharmaX 第一次做风险评估的合适起点。后续可以基于这份报告挑出 High / Very High 的项做定量分析（比如年化损失期望 ALE），用真实成本数据支持预算决策。 | **A:** Yes. Qualitative is the right starting point for PharmaX's first-ever assessment. We can then take the High / Very High items and do quantitative analysis (e.g., Annualized Loss Expectancy) backed by real cost data to support budget decisions. |

### 🔧 假设类 / Assumptions

| 中文 | English |
|---|---|
| **Q:** 假设和真实情况不一样会不会让整份报告失效？ | **Q:** What if your assumptions turn out to be wrong — does that invalidate the report? |
| **A:** 不会失效，但会需要"更新"。NIST 800-30 把风险评估视为持续过程：第一轮基于假设产生 baseline，下一轮在 PharmaX 提供真实文档后修正每条 Finding。 | **A:** Not invalidated, just updated. NIST 800-30 treats risk assessment as a continuous process: round one builds a baseline from assumptions; the next round refines each finding once PharmaX provides real documentation. |

### 📊 评分类 / Scoring

| 中文 | English |
|---|---|
| **Q:** 你的 Top 10 里只有一个 Very High，是不是太保守？ | **Q:** Only one Very High in your Top 10 — isn't that too conservative? |
| **A:** Very High 在 NIST 定义里是"灾难级 + 几乎确定"。Ransomware 同时满足两个条件——既是极高频率攻击向量，又会造成全公司停摆。其他 Finding 都不同时满足这两个条件，所以保留 Very High 的"专属性"是有意义的。 | **A:** Very High in NIST means "catastrophic + nearly certain." Ransomware uniquely meets both — it's both a very frequent attack vector and would shut the entire company down. None of the others satisfy both simultaneously, so reserving "Very High" makes the rating meaningful. |
| **Q:** 你为什么没把 Insider Threat 评成 High？ | **Q:** Why didn't you rate Insider Threat as High? |
| **A:** Insider 的 Impact 是 High，但 Likelihood 是 Moderate（多数员工不会作恶）。按 Table I-2 矩阵，Moderate × High = Moderate。 | **A:** Insider Impact is High, but Likelihood is Moderate (most employees won't act maliciously). Per Table I-2, Moderate × High = Moderate. |

### 💰 建议类 / Recommendations

| 中文 | English |
|---|---|
| **Q:** 所有建议都做完，PharmaX 大概要花多少钱？ | **Q:** What would the total cost be if PharmaX implemented every recommendation? |
| **A:** 这份报告是高层定性的，没有做成本估算。但「立即」类（MFA、培训、补丁）通常每年几万美金量级；「短期」类（EDR、IR plan、TPRM）几十万到上百万；「长期」类（SIEM、网络分段、治理）会进入百万级且需要专门项目和人员。 | **A:** This high-level qualitative report doesn't include costing. Roughly, "Immediate" items (MFA, training, patching) are typically tens of thousands per year; "Short-term" items (EDR, IR plan, TPRM) are hundreds of thousands; "Long-term" items (SIEM, segmentation, governance) reach the seven-figure range and need dedicated programs and staff. |

### 🎯 全局类 / Big Picture

| 中文 | English |
|---|---|
| **Q:** 这份报告下一步会怎么用？ | **Q:** How will this report be used next? |
| **A:** 三步：(1) 提交给管理层和董事会，确保这次不会"再被搁在书架上"；(2) 把建议拆成项目计划和负责人；(3) 6–12 个月后做第二轮评估，跟踪缓解效果。 | **A:** Three steps: (1) Present to management and the board so the report doesn't end up "on a shelf" again; (2) Break recommendations into project plans with owners; (3) Re-run the assessment in 6–12 months to track mitigation progress. |
| **Q:** 上次的渗透测试报告被搁置了，你怎么避免这次也一样？ | **Q:** Last time the pen test report was shelved — how do you avoid the same fate? |
| **A:** 这就是为什么 Conclusion 里强调"董事会层级的安全治理"。董事会缺乏安全经验，所以要把风险结论翻译成业务语言（停业天数、监管罚款、IP 损失），让他们看得懂、签得字。 | **A:** That's exactly why the Conclusion emphasizes "board-level security governance." The board lacks security expertise, so we have to translate findings into business language (downtime days, regulatory fines, IP loss) so they actually understand and approve action. |

---

## 🎬 收尾语 / Closing

**🇨🇳：** 整份报告的核心思路是：**用 NIST 800-30 这把尺子，把 PharmaX 的"低安全成熟度 + 高第三方依赖"翻译成可执行、有优先级的建议**。Top 10 已经按风险等级排序，建议按时间维度分桶，让 PharmaX 既能看懂为什么有这些风险，也能从明天开始解决最紧迫的几个。谢谢老师！

**🇬🇧:** The core idea of the report is: **use NIST 800-30 as the yardstick to translate PharmaX's "low security maturity + heavy third-party dependence" into actionable, prioritized recommendations.** The Top 10 is sorted by risk level, and the recommendations are bucketed by timeframe, so PharmaX both understands why each risk exists and can start solving the most urgent ones tomorrow. Thank you!

---

## 🧭 Demo 总结 Q&A / Demo Summary Q&A

### 🌐 Q1：总述讲讲你这份 report 干了啥 / Overall, what did your report do?

**🇨🇳：**
我这份 report 是为 PharmaX 这家中型制药公司做的一份**高层定性 Top 10 安全风险评估**，整体按照 NIST SP 800-30 Rev.1 的方法论展开。具体做了四件事：

1. **Introduction** — 说明评估目标和方法论，并解释为什么这次评估是必须做的（PharmaX 从未做过、安全成熟度低、强依赖第三方、50% 远程办公、上一次渗透测试报告被搁置）。
2. **Assumptions** — 因为作业描述并没有覆盖所有细节，我列了 10 条假设作为整份报告的「地基」，每条都不与作业里给出的事实矛盾（比如假设没有 MFA、没有 EDR、没有第三方风险管理）。
3. **Findings & Recommendations** — 这是核心，我按 NIST 格式列了 10 个 Finding，每个都包含：威胁事件（Table E-2 / E-3）、威胁源（Appendix D）、漏洞、可能性（Appendix G）、影响（Appendix H）、综合风险（Appendix I 矩阵）、以及对应建议。10 项里有 1 项 Very High、5 项 High、3 项 Moderate、1 项 Low。
4. **Conclusion** — 把所有建议按"立即 / 短期 / 长期"三个时间维度排好优先级，让管理层一眼就能决定先投哪些预算。

简单说，就是**把 PharmaX 模糊的"安全很差"变成了一份可执行、有优先级、董事会能看懂的风险路线图**。

**🇬🇧:**
This report is a **high-level qualitative Top 10 security risk assessment** for PharmaX, a mid-sized pharma company, built strictly on the NIST SP 800-30 Rev.1 methodology. Four things were done:

1. **Introduction** — States the goal and methodology, and explains why this assessment was overdue (no prior assessment, low security maturity, heavy third-party dependence, 50% remote workforce, prior pen test report shelved).
2. **Assumptions** — Since the assignment doesn't cover every detail, I listed 10 assumptions as the foundation of the report. None of them contradicts any fact in the assignment (e.g., no MFA, no EDR, no third-party risk management).
3. **Findings & Recommendations** — The core. Ten findings in the NIST format: Threat Event (Table E-2 / E-3), Threat Sources (Appendix D), Vulnerability, Likelihood (Appendix G), Impact (Appendix H), Overall Risk (Appendix I matrix), and Recommendations. The mix is 1 Very High, 5 High, 3 Moderate, 1 Low.
4. **Conclusion** — Prioritizes every recommendation into Immediate / Short-term / Long-term buckets so management can decide budget allocation at a glance.

In short, it **turns PharmaX's vague "we have weak security" into an actionable, prioritized, board-readable risk roadmap.**

---

### 🚦 Q2：讲三个 risk —— 最紧急的、一般的、不急的 / Walk through three risks: most urgent, medium, lowest priority

> 这里我各挑一个代表性的 Finding 来讲。
> Below I pick one representative finding for each tier.

#### 🔴 最紧急 / Most Urgent — Finding 2：Ransomware（Risk = Very High）

**🇨🇳：**
- **为什么最紧急：** 这是整份报告里**唯一一个 Very High** 风险。制药公司是勒索软件的"重灾区"，再加上 PharmaX 三个关键控制全部缺失——没有 EDR、没有补丁管理、没有事件响应计划——任何一个缺失都很糟糕，三个叠加就是灾难级。
- **一旦发生：** 两个数据中心的医学研究数据、客户记录、业务系统全部被加密，没有 IR/DR 计划意味着恢复要花数周、损失数百万美元。
- **必须立即做：** 部署 EDR、做不可变离线备份、写并演练 IR 剧本、建立 BC/DR 计划。

**🇬🇧:**
- **Why most urgent:** The **only Very High** risk in the entire report. Pharma is a top ransomware target, and PharmaX has gaps in three critical controls simultaneously — no EDR, no patch management, no IR plan. Any one is bad; all three together is catastrophic.
- **If it hits:** Medical research data, customer records, and business systems across both data centers get encrypted. With no IR/DR plan, recovery would take weeks and cost millions.
- **Immediate actions:** Deploy EDR, set up immutable offline backups, write and rehearse an IR playbook, build a BC/DR plan.

#### 🟡 一般紧急 / Medium Priority — Finding 7：VPN Compromise（Risk = Moderate）

**🇨🇳：**
- **为什么是中等：** Likelihood 是 High（80 个远程员工 + 没有 MFA + 个人笔记本，攻击者拿到一个密码就能进），但 Impact 是 Moderate——攻击者只是拿到一个网络立足点，要碰到核心数据还需要继续提权和横向移动。所以 Impact × Likelihood = Moderate。
- **特别值得讲的点：** 这是**性价比最高**的一个 Finding。给 VPN 加 MFA 几乎是零成本、即装即用，能立刻消除最常见的远程入侵向量。这就是为什么我把它放在 Conclusion 的"立即执行"列表里。
- **建议：** 立即给 VPN 启用 MFA、禁用 split tunneling、用 NAC 做设备合规检查、对个人笔记本强制 MDM 基线。

**🇬🇧:**
- **Why medium:** Likelihood is High (80 remote workers + no MFA + personal laptops — one stolen password is enough), but Impact is Moderate — an attacker only gets a network foothold and still needs to escalate to reach high-value data. So Likelihood × Impact = Moderate.
- **Why it's worth highlighting:** This is the **highest-ROI finding**. Turning on MFA for the VPN is essentially zero-cost and instantly eliminates the most common remote intrusion vector. That's why it's in the "Immediate" bucket of the Conclusion.
- **Recommendations:** Enable VPN MFA immediately, disable split tunneling, deploy NAC for device compliance, enforce MDM baselines on personal laptops.

#### 🟢 不紧急 / Lowest Priority — Finding 9：Physical Security Breach（Risk = Low）

**🇨🇳：**
- **为什么不紧急：** 是整份报告里**唯一的 Low**。物理攻击需要攻击者实地到场，威胁池天然小很多；而且 PharmaX 大部分敏感数据已经电子化，单纯偷文件造成的影响有限。所以 Likelihood = Low、Impact = Moderate，整体是 Low。
- **为什么还要写进 Top 10：** Top 10 是"识别出的 10 项主要风险"而不是"Top 10 高风险"，一份完整报告需要覆盖所有风险维度。我列出来的几条建议（清洁桌面、5 分钟自动锁屏、访客签到）都是**几乎零成本**的，可以放在长期治理里慢慢做。
- **建议：** 清洁桌面策略 + 锁柜、自动锁屏、访客签到与陪同制度、加快全面电子化。

**🇬🇧:**
- **Why lowest:** The **only Low** risk in the report. Physical attacks require the attacker to be on-site, which naturally limits the threat pool; and most of PharmaX's sensitive data is already electronic, so document theft alone has limited impact. Hence Likelihood = Low, Impact = Moderate, Overall = Low.
- **Why still in the Top 10:** "Top 10" means the ten main identified risks, not the ten highest. A complete report must cover all dimensions. The recommendations (clean desk, 5-minute auto-lock, visitor sign-in) are essentially **zero-cost** and can be folded into long-term governance.
- **Recommendations:** Clean desk policy + locked cabinets, auto screen lock, visitor management with sign-in/escort, accelerate full digitization.

---

### 📌 三档对比一句话总结 / One-line Comparison

| Tier | Finding | Why this tier | Action timing |
|---|---|---|---|
| 🔴 最紧急 / Most Urgent | Ransomware (Very High) | 三个关键控制全缺失 + 业务停摆 / Three critical controls missing + business shutdown | Immediate |
| 🟡 一般 / Medium | VPN Compromise (Moderate) | 易发但只是入口，且 MFA 零成本 / Easy to exploit but only a foothold; MFA is essentially free | Immediate (cheapest fix) |
| 🟢 不急 / Lowest | Physical Security (Low) | 攻击者必须实地到场 + 数据已电子化 / Attacker must be on-site + data is already electronic | Long-term, low-cost |
