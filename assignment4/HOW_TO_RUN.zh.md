# 复现指南（仅供参考，不在提交范围内）

> 这份文档是为我自己验证 Claude 跑出来的数据准备的，**不会作为作业的一部分提交**。
> 提交的内容只有 `report.md` + `screenshots/` + `scripts/` + `data/`。

## 环境前置

```bash
brew install subfinder jq                  # 已安装
python3 --version                          # 系统自带即可
```

## 一次性跑完整条流水线

```bash
cd assignment4

# Step 1: 子域枚举 → data/subdomains.txt
bash scripts/01_enum.sh uci.edu

# Step 1.5: 过滤掉明显是内网/工作站/摄像头的主机名（节省 step 2 一半时间）
grep -E -v \
  -e '\.ucinet\.uci\.edu$' \
  -e '\.reshsg\.uci\.edu$' \
  -e '\.mobile\.uci\.edu$' \
  -e '\.is\.mc\.uci\.edu$' \
  -e '\.fac\.mc\.uci\.edu$' \
  -e '^[0-9a-f]{12}\.' \
  -e '^[0-9]+-' \
  -e '-pc\.' -e '-cam[0-9]*\.' -e '-camera[0-9]*\.' -e '-nvr\.' \
  -e '-vl[0-9]+\.' -e '-vlan[0-9]+\.' \
  -e '-printer\.' -e '-laptop\.' -e '-imac\.' -e '-macbook\.' -e '-dhcp\.' \
  data/subdomains.txt | sort -u > data/subdomains_filtered.txt

# Step 2: DNS 解析 → data/resolved.csv
bash scripts/02_resolve.sh data/subdomains_filtered.txt

# Step 3: 云属归类 → data/cloud_hosts.csv
python3 scripts/03_cloud_attr.py data/resolved.csv

# Step 3.5: 只保留云上的子域（去掉 UCI 校内 + RFC1918），probe 才有意义
awk -F, 'NR==1 || ($3!="UCI on-prem" && $3!="UCI on-prem / UCnet" && $3!="RFC1918 (leaked)")' \
    data/cloud_hosts.csv > data/cloud_hosts_external.csv

# Step 4: HTTP 探测 → data/probe.csv
bash scripts/04_probe.sh data/cloud_hosts_external.csv
```

每一步都会把结果写到 `data/` 里，下一步直接读上一步的输出。
两个 "过滤步骤"（1.5 和 3.5）没单独做成脚本，因为它们就是一行 grep / awk，放在脚本里反而不直观。

---

## 分步说明

### Step 1 — 子域枚举（`01_enum.sh`）

```bash
bash scripts/01_enum.sh uci.edu
```

做了两件事：
1. `subfinder -d uci.edu -all` — 被动从几十个公开数据源（VirusTotal、Censys、SecurityTrails、CT logs 镜像等）收集子域。
2. `curl https://crt.sh/?q=%25.uci.edu&output=json` — 直接查 Certificate Transparency 日志里给 `*.uci.edu` 签发过证书的记录。

输出：

- `data/subdomains_subfinder.txt` — subfinder 原始结果
- `data/subdomains_crtsh.txt`     — crt.sh 原始结果
- `data/subdomains.txt`           — 合并去重后的总表

**坑：** subfinder 会把很多明显是内网/单台机器的主机名也拉进来（摄像头、VLAN 网关、个人 PC 等）。我用一组正则做了二次过滤，得到 `data/subdomains_filtered.txt`，过滤规则在 report.md 的 Methodology 里写了。

### Step 2 — DNS 解析（`02_resolve.sh`）

```bash
bash scripts/02_resolve.sh data/subdomains_filtered.txt
```

对每个子域 `dig @1.1.1.1 +short A`，只保留 IPv4 A 记录。CNAME 链由 dig 自己跟踪到 A。**xargs -P 200** 并发跑，整体耗时几分钟。

验证一两条：

```bash
dig +short A www.uci.edu
grep '^www.uci.edu,' data/resolved.csv
```

两边的 IP 应当一致。

### Step 3 — 云属归类（`03_cloud_attr.py`）

```bash
python3 scripts/03_cloud_attr.py data/resolved.csv
```

逻辑：

1. 拉 AWS / GCP / Oracle / Cloudflare 官方发布的 IPv4 CIDR 列表（JSON / TXT），逐 IP 匹配。
2. 没匹配上的 IP 通过 **Team Cymru** 的 `whois -h whois.cymru.com` 批量查 ASN holder，再按关键字归类（Microsoft → Azure，UCnet → 校内，等等）。

输出 `data/cloud_hosts.csv`，最后一列 `detail` 是 AWS region / GCP service / ASN holder 这样的小线索。

**抽查：** 找一条标 AWS 的：

```bash
awk -F, '$3=="AWS"{print $2; exit}' data/cloud_hosts.csv | xargs -I{} whois {} | grep -i amazon | head -3
```

### Step 4 — HTTP 探测（`04_probe.sh`）

```bash
bash scripts/04_probe.sh data/cloud_hosts_external.csv
```

注意输入是上面 Step 3.5 过滤后的 `cloud_hosts_external.csv`（~2.9K 个云上子域），不是全部的 `resolved.csv`（~60K 含 UCI 校内）。校内主机用 dig 已经能看出托管在哪了，再 probe 一遍意义不大、还很慢。

对每个唯一子域先试 `https://`，失败再试 `http://`，记录状态码、`Server:` 头、HTML `<title>`。**xargs -P 30** 并发跑，太高会触发学校 WAF 限流。

输出 `data/probe.csv` 是写 report 的核心素材：

```bash
# 按 title 排序看有没有眼熟的 admin/dashboard 字样
awk -F, 'NR>1 && $4!=""' data/probe.csv | sort -t, -k4 | less
```

---

## 复跑 / 清理

```bash
rm -rf assignment4/data/*    # 全清
# 然后从 Step 1 重新跑
```

## 数字对得上吗？

跑完后用这几条命令对 `report.md` 里的数字：

```bash
wc -l data/subdomains.txt data/subdomains_filtered.txt          # 枚举到的总量
awk -F, 'NR>1{print $2}' data/resolved.csv | sort -u | wc -l    # 唯一 IP 数
awk -F, 'NR>1{print $3}' data/cloud_hosts.csv | sort | uniq -c  # 各 provider 子域数
awk -F, 'NR>1 && $2>=200 && $2<400' data/probe.csv | wc -l       # 活的 HTTP 服务数
```

数据对得上就交差。

---

## 截图清单：report.md 里的 7 个 TODO 怎么补

每个 TODO 对应一张图，放到 `screenshots/` 目录下，文件名要和 report.md 里引用的一致。
macOS 区域截图快捷键：`Cmd + Shift + 4`，鼠标拖一下框，图会自动落到桌面，再 `mv` 到目标位置。

### TODO 1 — `screenshots/subfinder.png`

终端里跑 subfinder 跑一半的样子（不用跑完）：

```bash
subfinder -d uci.edu
```

跑出几十行 `... .uci.edu` 的时候按 `Cmd+Shift+4` 截整个 terminal 窗口。

### TODO 2 — `screenshots/crtsh.png`

浏览器打开：

```
https://crt.sh/?q=%25.uci.edu
```

等表格出来，截图能看到表头 + 几行证书记录就行。

### TODO 3 — `screenshots/rfc1918_leak.png`

终端跑这三条，把输出一起截下来：

```bash
dig +short ad-rds-lic3.ad.uci.edu
dig +short ad-sn-mid04.ad.uci.edu
dig +short ad-rdpgw-test.ad.uci.edu
```

每条应该返回一个 `10.65.x.x`，证明私网 IP 真的在公开 DNS 里出现了。

### TODO 4 — `screenshots/trs_prod.png` + `screenshots/trs_stage_default.png`

两张图（同一个 TODO 注释里）。浏览器分别打开：

```
# prod，看到 "Index - UC Law SF Time Reporting System - TRS" 这种标题
https://app-01-direct-lb.trs-uclawsf-prod.aws.uci.edu

# stage，看到 Apache 默认 "Test Page for the Apache HTTP Server"
https://app-01-direct-lb.trs-uclawsf-stage.aws.uci.edu
```

两张图分别保存为上面两个文件名。如果证书报错点 advanced → proceed 就好（截图反而能体现安全问题）。

### TODO 5 — `screenshots/apache_test_page.png`

浏览器打开任意一个：

```
https://apps.athletics.uci.edu       # Apache 默认页
https://kualidocs.oit.uci.edu        # 同上
https://app.commencement.uci.edu     # Rocky Linux 默认页
```

随便挑一个截图，能看到 "Test Page for the Apache HTTP Server" 或 "HTTP Server Test Page powered by: Rocky Linux"。

### TODO 6 — `screenshots/sandbox_personal.png`

浏览器打开 library sandbox 里的某个个人 droplet：

```
https://alice.sandbox.lib.uci.edu         # "UCI Libraries Digital Sandbox Service"
https://afburke.sandbox.lib.uci.edu       # "Test Site" — 默认 Apache 没配置
```

截图能看到 title 就行。

### TODO 7 — `screenshots/saas_tenant.png`

挑一个第三方 SaaS 上的 UCI 子域，浏览器打开后截 landing page：

```
https://antnet.uci.edu                    # PeopleGrove，URL bar 留着能看到 *.uci.edu
https://research.test-pantheon.bio.uci.edu # Pantheon 上的 staging
```

截图重点是地址栏（uci.edu 域名）+ 页面右下角/footer 能看到第三方平台的 logo / "Powered by ..."。

---

## 一句话核对清单

- [ ] `screenshots/` 下有 8 个 PNG（trs 那个 TODO 算两张）
- [ ] `report.md` 里 `grep TODO` 没有结果（图加完后注释可以删，也可以留着没关系）
- [ ] `data/` 下 `subdomains.txt / subdomains_filtered.txt / resolved.csv / cloud_hosts.csv / cloud_hosts_external.csv / probe.csv` 都在
- [ ] `scripts/` 下四个脚本都有可执行权限
