# Assignment 5 详细完成指南

这份文档不用提交，是给你自己一步一步完成作业用的。最终提交的是 `report.md` 导出的 PDF。你照着这里做实验、截图、把结果填回 `report.md` 就可以。

建议所有截图都放在 `assignment5/diagram/` 目录下，文件名必须和 `report.md` 里的图片名一致。

## 0. 最终要准备的文件

`assignment5/` 目录里最后建议有：

- `requirement.txt`：老师给的要求，不改。
- `report.md`：英文报告草稿，最后从它导出 PDF。
- `guide.md`：这份中文指南，不提交。
- `proxy-listener.png`
- `proxy-manager-config.png`
- `proxy-intercept-test.png`
- `juice-shop-apt-failed.png`
- `juice-shop-running-ss.png`
- `juice-shop-home.png`
- `scoreboard-tutorials-completed.png`
- `progress-save-restore.png`
- `scoreboard-solved.png`
- `dom-xss-solved.png`
- `bonus-payload-solved.png`
- `privacy-policy-solved.png`
- `login-admin-solved.png`
- `password-strength-solved.png`
- `view-basket-solved.png`
- `forged-feedback-solved.png`
- `admin-section-solved.png`
- `payback-time-solved.png`

## 1. 安装 Burp Suite

打开 Kali Terminal，运行：

```bash
sudo apt update
sudo apt install burpsuite
```

如果系统问：

```text
Continue? [Y/n]
```

输入：

```text
y
```

然后回车。

安装完成后，启动 Burp：

```bash
burpsuite
```

也可以从 Kali 左上角菜单打开：

```text
Applications -> Web Application Analysis -> Burp Suite
```

## 2. 第一次打开 Burp Suite

你现在看到的是 Burp 的欢迎界面。

第一页这样选：

1. 选择：

   ```text
   Temporary project in memory
   ```

2. 点击右下角：

   ```text
   Next
   ```

第二页这样选：

1. 选择：

   ```text
   Use Burp defaults
   ```

2. 点击：

   ```text
   Start Burp
   ```

进入主界面后，先把拦截关掉，否则浏览器访问网页时会卡住。

操作：

1. 点击上方：

   ```text
   Proxy
   ```

2. 点击：

   ```text
   Intercept
   ```

3. 如果按钮显示：

   ```text
   Intercept is on
   ```

   点一下，让它变成：

   ```text
   Intercept is off
   ```

## 3. 检查 Burp 代理监听端口

作业要求你配置一个 web proxy，并说明它监听在哪个端口。这里使用默认配置：

```text
127.0.0.1:8080
```

在 Burp 里检查：

1. 点击上方：

   ```text
   Proxy
   ```

2. 找到：

   ```text
   Proxy settings
   ```

   有的版本是在右上角齿轮或 Settings 里，需要进入后找：

   ```text
   Tools -> Proxy
   ```

3. 找到：

   ```text
   Proxy listeners
   ```

4. 确认列表里有一条类似：

   ```text
   Interface: 127.0.0.1:8080
   Running: yes
   ```

如果没有这一条：

1. 点击：

   ```text
   Add
   ```

2. Binding 里设置：

   ```text
   Bind to port: 8080
   Bind to address: Loopback only / 127.0.0.1
   ```

3. 保存。

这一步截图，保存为：

```text
proxy-listener.png
```

截图里最好能看到 `127.0.0.1:8080` 和 listener enabled/running。

如果你想用命令行确认 `8080` 是否被监听，可以开一个新 Terminal：

```bash
ss -tulpn | grep 8080
```

能看到 `8080` 就说明 Burp 正在监听。

## 4. 安装 FoxyProxy 浏览器扩展

推荐用 Firefox，因为 Kali 默认一般自带 Firefox ESR。

打开 Firefox：

1. 点击 Kali 左上角 Firefox 图标，或者在 Terminal 输入：

   ```bash
   firefox
   ```

2. 打开 Firefox 后，点击右上角三条线菜单。

3. 点击：

   ```text
   Add-ons and themes
   ```

   也可以直接在地址栏输入：

   ```text
   about:addons
   ```

4. 在搜索框里搜索：

   ```text
   FoxyProxy
   ```

5. 找到：

   ```text
   FoxyProxy Standard
   ```

   或者：

   ```text
   FoxyProxy Basic
   ```

   两个都可以。推荐 `FoxyProxy Standard`。

6. 点击：

   ```text
   Add to Firefox
   ```

7. 弹出权限确认时，点击：

   ```text
   Add
   ```

8. 如果 Firefox 问是否允许在 Private Windows 使用，可以不用勾，直接完成。

安装完成后，Firefox 右上角工具栏会出现 FoxyProxy 图标。如果没看到：

1. 点击右上角拼图图标 Extensions。
2. 找到 FoxyProxy。
3. 点击旁边的齿轮或 pin，把它固定到工具栏。

## 5. 在 FoxyProxy 里添加 Burp 代理

现在要告诉浏览器：当启用 FoxyProxy 时，把浏览器流量发给 Burp 的 `127.0.0.1:8080`。

操作：

1. 点击 Firefox 右上角的 FoxyProxy 图标。

2. 点击：

   ```text
   Options
   ```

   或者：

   ```text
   Manage Proxies
   ```

3. 点击：

   ```text
   Add
   ```

   有的版本写的是：

   ```text
   Add Proxy
   ```

4. 填写代理名称：

   ```text
   Burp
   ```

5. Proxy Type 选择：

   ```text
   HTTP
   ```

6. Hostname / Address / Host 填：

   ```text
   127.0.0.1
   ```

7. Port 填：

   ```text
   8080
   ```

8. Username 和 Password 留空。

9. 不需要设置 pattern，也不需要设置 SOCKS。

10. 点击：

    ```text
    Save
    ```

这一步截图，保存为：

```text
proxy-manager-config.png
```

截图里最好能看到：

- Name: `Burp`
- Type: `HTTP`
- Host: `127.0.0.1`
- Port: `8080`

## 6. 启用 FoxyProxy 的 Burp 配置

添加完代理以后，还要启用它。

操作：

1. 点击 Firefox 右上角 FoxyProxy 图标。

2. 选择类似下面的选项：

   ```text
   Use Burp for all URLs
   ```

   或者：

   ```text
   Burp
   ```

   或者：

   ```text
   Use Enabled Proxies By Patterns and Order
   ```

   不同版本名字稍微不一样。最简单是选“所有 URL 都走 Burp”。

3. 启用后，FoxyProxy 图标通常会变颜色。

如果要关闭代理：

1. 再次点击 FoxyProxy 图标。
2. 选择：

   ```text
   Turn Off
   ```

   或者：

   ```text
   Disable FoxyProxy
   ```

   或者：

   ```text
   Use Firefox settings
   ```

## 7. 测试 Burp + FoxyProxy 是否工作

先确认 Burp 正在运行，并且：

```text
Proxy -> Intercept -> Intercept is off
```

然后：

1. Firefox 中启用 FoxyProxy 的 `Burp` 配置。

2. 在 Firefox 地址栏访问：

   ```text
   http://example.com
   ```

   或者之后访问：

   ```text
   http://127.0.0.1:42000
   ```

3. 回到 Burp。

4. 点击：

   ```text
   Proxy -> HTTP history
   ```

5. 如果能看到浏览器请求，比如 `GET /`、`example.com`、`127.0.0.1:42000`，说明代理成功。

这一步截图，保存为：

```text
proxy-intercept-test.png
```

截图里最好能看到 Burp 的 HTTP history 里有请求记录。

常见问题：

- 如果 Firefox 打不开网页，先检查 Burp 是否开着。
- 如果网页一直 loading，检查 Burp 的 Intercept 是否是 off。
- 如果 Burp HTTP history 没有请求，检查 FoxyProxy 是否真的启用了 `Burp`。
- 如果端口不是 `8080`，Burp 和 FoxyProxy 两边必须一致。

完成后，在 `report.md` 里填写：

```text
[PROXY SETUP CHALLENGE: ...]
```

如果没有遇到问题，可以写：

```text
No major issue; the main step was enabling FoxyProxy and keeping Burp running with intercept disabled during normal browsing.
```

## 8. 如果需要代理 HTTPS：导入 Burp CA 证书

本作业主要访问本地 Juice Shop：

```text
http://127.0.0.1:42000
```

这是 HTTP，不是 HTTPS，所以通常可以不导入证书。

如果你要访问 HTTPS 网站并让 Burp 解密流量，就要导入 Burp CA。

操作：

1. 确认 Burp 正在运行。

2. 确认 Firefox 已经启用 FoxyProxy 的 Burp 配置。

3. 在 Firefox 地址栏访问：

   ```text
   http://burp
   ```

4. 页面打开后，点击：

   ```text
   CA Certificate
   ```

   会下载一个证书文件，通常叫：

   ```text
   cacert.der
   ```

5. Firefox 右上角三条线菜单。

6. 打开：

   ```text
   Settings
   ```

7. 搜索：

   ```text
   certificates
   ```

8. 点击：

   ```text
   View Certificates
   ```

9. 进入：

   ```text
   Authorities
   ```

10. 点击：

    ```text
    Import
    ```

11. 选择刚下载的 `cacert.der`。

12. 勾选：

    ```text
    Trust this CA to identify websites
    ```

13. 点击 OK。

之后 HTTPS 网站的请求也可以在 Burp 里看到。注意：只在自己的实验环境中这样做，实验结束后可以删除这个证书或关闭 FoxyProxy。

## 9. 记录 apt 安装 Juice Shop 失败

你这台 Kali VM 是 ARM (`arm64`) 环境，所以 `sudo apt install juice-shop` 可能找不到包。这个失败过程可以写进报告，作为“installation challenge”。

打开 Kali Terminal，先运行：

```bash
sudo apt update
sudo apt install juice-shop
```

你现在看到的错误是：

```text
Unable to locate package juice-shop
```

这不是你输错了，而是当前 Kali repository 里没有适合这个 ARM VM 的 `juice-shop` apt 包。

把这个失败画面截图，保存为：

```text
juice-shop-apt-failed.png
```

这张图放进报告，用来说明为什么没有使用 `juice-shop-start` / `juice-shop-stop` 的 Kali package 方法。

## 10. 安装 Podman

接下来用 Podman 跑官方 Juice Shop container。这和旧的 `assignment5-backup` 方法一致。

安装 Podman：

```bash
sudo apt install podman
```

如果系统问：

```text
Continue? [Y/n]
```

输入：

```text
y
```

然后回车。

安装完成后检查版本：

```bash
podman --version
```

能看到版本号就说明 Podman 安装成功。

## 11. 用 Podman 启动 Juice Shop

运行：

```bash
podman run -d --name juice-shop -p 127.0.0.1:42000:3000 docker.io/bkimminich/juice-shop
```

这条命令的意思：

- `podman run`：启动一个容器。
- `-d`：后台运行。
- `--name juice-shop`：容器名字叫 `juice-shop`。
- `-p 127.0.0.1:42000:3000`：把 VM 本机的 `42000` 端口映射到容器里的 `3000` 端口。
- `docker.io/bkimminich/juice-shop`：使用官方 Juice Shop container image。

如果是第一次运行，它会自动下载 image。等命令执行完成后，检查容器是否在运行：

```bash
podman ps
```

你希望看到一行包含：

```text
juice-shop
docker.io/bkimminich/juice-shop
0.0.0.0:42000 或 127.0.0.1:42000
```

如果提示容器名已经存在：

```text
the container name "juice-shop" is already in use
```

说明之前创建过容器。直接启动旧容器：

```bash
podman start juice-shop
```

## 12. 验证 Juice Shop 端口

```bash
ss -ltnp | grep 42000
```

你希望看到类似：

```text
LISTEN ... 127.0.0.1:42000 ...
```

这一步截图，保存为：

```text
juice-shop-running-ss.png
```

然后在 Firefox 地址栏访问：

```text
http://127.0.0.1:42000
```

如果页面能打开 OWASP Juice Shop 首页，截图保存为：

```text
juice-shop-home.png
```

## 13. 停止和重新启动 Juice Shop

停止容器：

```bash
podman stop juice-shop
```

确认端口已经关闭：

```bash
ss -ltnp | grep 42000
```

如果没有任何输出，说明 `42000` 端口已经不再监听，Juice Shop 停止成功。

重新启动同一个容器：

```bash
podman start juice-shop
```

再次确认：

```bash
podman ps
ss -ltnp | grep 42000
```

如果你想彻底删除容器，才使用：

```bash
podman rm juice-shop
```

如果容器还在运行，删除前要先：

```bash
podman stop juice-shop
```

报告里现在已经写好了这次安装挑战：apt 找不到 `juice-shop`，所以改用 Podman 运行官方 container。

## 14. 熟悉 Juice Shop 基本功能

重新启动 Juice Shop：

```bash
podman start juice-shop
```

浏览器打开：

```text
http://127.0.0.1:42000
```

按下面顺序做：

test@test.com

1. 关闭欢迎弹窗或 cookie 提示。
2. 点击右上角 Account。
3. 进入 Login。
4. 找到注册入口，创建一个测试用户。
5. 登录这个用户。
6. 回到首页，浏览商品。
7. 选一个商品加入 Basket。
8. 打开 Basket。
9. 进入 Checkout。
10. 添加一个地址。
11. 添加一个虚构的 payment card。
12. 完成购买。
13. 查看订单详情。
14. 再浏览 Customer Feedback、Complaint、Support Chat 等页面。

同时可以打开 Burp：

```text
Proxy -> HTTP history
```

观察 Juice Shop 前端和后端之间的 API 请求。报告里只需要简短写：通过代理能看到页面没有直接显示的 API 请求和响应数据。

## 15. 挑战通用准备

下面 10 个任务都在你自己的 Juice Shop 本地靶场里完成，地址是：

```text
http://127.0.0.1:42000
```

开始前确认：

1. Juice Shop 容器在运行：

   ```bash
   podman ps
   ```

2. Burp 正在运行，listener 是：

   ```text
   127.0.0.1:8080
   ```

3. Firefox 右上角 FoxyProxy 选择 `Burp`。

4. Firefox 允许本地地址走代理。打开：

   ```text
   about:config
   ```

   搜索并确认：

   ```text
   network.proxy.allow_hijacking_localhost = true
   ```

5. Burp 的 Intercept 平时保持 off，需要改请求时再打开，或者用：

   ```text
   HTTP history -> Send to Repeater
   ```

## 16. Scoreboard

目标：打开隐藏的 Score Board 页面。

怎么做：

1. 浏览器直接访问：

   ```text
   http://127.0.0.1:42000/#/score-board
   ```

2. 页面出现 challenge 列表后，Scoreboard 会 solved。

3. 如果没有 solved，点击 Scoreboard 那一行旁边的橙色帽子 tutorial，按提示再打开一次页面。

截图：

1. 回到 Score Board。
2. 找到 `Scoreboard` 这一行，确认状态是 solved。
3. 截图保存为：

   ```text
   assignment5/diagram/scoreboard-solved.png
   ```

原理：

Juice Shop 是单页应用，前端 route 可以直接从地址栏访问。Score Board 没有明显放在主页面入口里，但 route 仍然存在。这个任务说明：隐藏 UI 入口不等于真正的访问控制。

报告可填：

```text
What worked: Directly opening /#/score-board revealed the challenge tracking page.
What did not work: Looking only through the product UI did not reveal the page.
```

## 17. DOM XSS

目标：通过搜索框触发 DOM-based XSS。

怎么做：

1. 打开首页：

   ```text
   http://127.0.0.1:42000
   ```

2. 点击右上角搜索图标。

3. 先输入普通文本测试：

   ```text
   apple
   ```

4. 再输入 payload：

   ```html
   <iframe src="javascript:alert(`xss`)">
   ```

5. 如果出现 alert，或者 Score Board 显示 `DOM XSS` solved，就完成了。

6. 截图保存为：

   ```text
   assignment5/diagram/dom-xss-solved.png
   ```

原理：

DOM XSS 发生在浏览器端。应用把用户输入交给前端 JavaScript 渲染，如果没有正确做 escaping 或使用安全 DOM API，输入可能被当作 HTML/JavaScript 执行。这里 payload 被插入 DOM 后，`iframe` 的 `javascript:` 会触发脚本执行。

报告可填：

```text
What worked: The iframe JavaScript payload in the search box triggered the DOM XSS.
What did not work: Normal search strings only returned product results.
```

## 18. Bonus Payload

目标：使用 Juice Shop 指定的 bonus XSS payload。

怎么做：

1. 打开首页搜索框。

2. 输入：

   ```html
   <iframe src="javascript:alert(`xss`)">
   ```

3. 如果你在 DOM XSS 里已经用了这个 payload，`Bonus Payload` 可能已经自动 solved。

4. 如果还没 solved，回 Score Board，点 `Bonus Payload` 旁边的橙色帽子 tutorial，按提示重新提交。

截图：

1. 回到 Score Board。
2. 找到 `Bonus Payload` 这一行，确认状态是 solved。
3. 截图保存为：

   ```text
   assignment5/diagram/bonus-payload-solved.png
   ```

原理：

这个任务强调 payload 形态。不同 XSS payload 依赖不同上下文，有些只在 HTML context 中有效，有些需要事件处理器或特殊标签。这个 payload 利用 `iframe src="javascript:..."` 在浏览器解析 DOM 时执行脚本。

报告可填：

```text
What worked: Reusing the guided iframe payload solved the bonus payload challenge.
What did not work: Plain text or incomplete HTML did not execute.
```

## 19. Privacy Policy

目标：找到并打开 privacy policy 页面。

怎么做：

1. 优先从 UI 找：

   ```text
   Account -> Privacy & Security -> Privacy Policy
   ```

2. 如果菜单里找不到，直接访问：

   ```text
   http://127.0.0.1:42000/#/privacy-security/privacy-policy
   ```

3. 回 Score Board 确认 `Privacy Policy` solved。

截图：

1. 回到 Score Board。
2. 找到 `Privacy Policy` 这一行，确认状态是 solved。
3. 截图保存为：

   ```text
   assignment5/diagram/privacy-policy-solved.png
   ```

原理：

这是应用探索任务，不是漏洞利用。安全测试时，隐私政策、帮助页面、关于页面经常暴露路由命名、功能模块、依赖和应用结构。

报告可填：

```text
What worked: Opening the privacy policy route completed the challenge.
What did not work: Browsing only product pages did not expose the page.
```

## 20. Login Admin

目标：登录管理员账号。

怎么做：

1. 退出当前用户。

2. 打开：

   ```text
   Account -> Login
   ```

3. Email 输入：

   ```text
   ' or 1=1--
   ```

4. Password 输入任意非空值，例如：

   ```text
   test
   ```

5. 点击 Login。

6. 如果登录成功，并且 Score Board 显示 `Login Admin` solved，就完成了。

截图：

1. 回到 Score Board。
2. 找到 `Login Admin` 这一行，确认状态是 solved。
3. 截图保存为：

   ```text
   assignment5/diagram/login-admin-solved.png
   ```

原理：

这是 SQL injection 导致的认证绕过。后端如果把 email/password 直接拼进 SQL，而不是用参数化查询，`' or 1=1--` 会让查询条件恒真，并注释掉后续条件。应用可能返回第一条用户记录，通常就是管理员。

报告可填：

```text
What worked: A SQL injection payload in the email field bypassed login.
What did not work: Normal invalid credentials were rejected.
```

## 21. Password Strength

目标：用弱密码登录管理员账号。

怎么做：

1. 退出当前用户。

2. 打开登录页面。

3. Email 输入：

   ```text
   admin@juice-sh.op
   ```

4. Password 输入：

   ```text
   admin123
   ```

5. 点击 Login。

6. 回 Score Board 确认 `Password Strength` solved。

截图：

1. 回到 Score Board。
2. 找到 `Password Strength` 这一行，确认状态是 solved。
3. 截图保存为：

   ```text
   assignment5/diagram/password-strength-solved.png
   ```

原理：

这是弱口令问题。即使没有 SQL injection，只要管理员使用容易猜到的密码，攻击者也可能通过常见密码或字典攻击登录。防御方式包括强密码策略、MFA、登录速率限制和异常登录检测。

报告可填：

```text
What worked: The known weak admin password allowed login.
What did not work: Random guessed passwords did not work.
```

## 22. View Basket

目标：查看另一个用户的 basket。

怎么做：

1. 登录普通测试用户。

2. 添加一个商品到 basket。

3. 打开 Basket 页面。

4. 在 Burp 中看：

   ```text
   Proxy -> HTTP history
   ```

5. 找类似请求：

   ```text
   GET /rest/basket/<your-basket-id>
   ```

6. 右键请求，选择：

   ```text
   Send to Repeater
   ```

7. 在 Repeater 里把 basket id 改成其他数字，例如：

   ```text
   /rest/basket/1
   ```

   或：

   ```text
   /rest/basket/2
   ```

8. 点击 Send。如果响应里出现其他 basket 内容，回 Score Board 看是否 solved。

截图：

1. 回到 Score Board。
2. 找到 `View Basket` 这一行，确认状态是 solved。
3. 截图保存为：

   ```text
   assignment5/diagram/view-basket-solved.png
   ```

原理：

这是 broken access control / IDOR。basket id 是可猜的对象编号，如果后端只根据 URL 里的 id 返回对象，而不检查当前用户是否有权限，就会泄露其他用户的 basket。

报告可填：

```text
What worked: Changing the basket id in the basket API request exposed another basket.
What did not work: The normal UI only showed my own basket.
```

## 23. Forged Feedback

目标：伪造反馈提交者。

怎么做：

1. 登录普通测试用户。

2. 打开 Customer Feedback 页面。

3. 填一条普通 feedback。

4. 如果有 captcha，先正常填正确答案。

5. 提交时打开 Burp Intercept，或者提交后在 HTTP history 里找：

   ```text
   POST /api/Feedbacks/
   ```

6. 把请求发送到 Repeater。

7. 在 JSON body 里找类似：

   ```json
   "UserId": 2
   ```

8. 改成另一个用户 id，例如：

   ```json
   "UserId": 1
   ```

9. 点击 Send。

10. 回 Score Board 确认 `Forged Feedback` solved。

截图：

1. 回到 Score Board。
2. 找到 `Forged Feedback` 这一行，确认状态是 solved。
3. 截图保存为：

   ```text
   assignment5/diagram/forged-feedback-solved.png
   ```

原理：

这是信任客户端身份字段的问题。反馈属于谁应该由后端根据 session/token 判断，而不是相信请求 body 中的 `UserId`。如果客户端能改 `UserId`，就可以冒充其他用户提交反馈。

报告可填：

```text
What worked: Modifying the feedback UserId submitted feedback as another user.
What did not work: Normal feedback submission only used my own identity.
```

## 24. Admin Section

目标：访问 admin section。

怎么做：

1. 先完成 `Login Admin` 或 `Password Strength`，确保你处于管理员登录状态。

2. 直接访问：

   ```text
   http://127.0.0.1:42000/#/administration
   ```

3. 如果管理页面打开，回 Score Board 确认 `Admin Section` solved。

4. 截图保存为：

   ```text
   assignment5/diagram/admin-section-solved.png
   ```

原理：

这个任务结合隐藏路由和权限控制。前端 route 可以被猜到或从 JavaScript 文件中发现，但真正的安全边界必须由后端授权检查提供。只隐藏入口不是安全控制。

报告可填：

```text
What worked: Accessing /#/administration with an admin session solved the challenge.
What did not work: Trying the route without admin access did not provide useful access.
```

## 25. Payback Time

目标：修改 basket/order 请求，让订单产生负数金额或返款效果。

怎么做：

1. 登录测试用户。

2. 添加一个商品到 Basket，例如 Apple Juice。

3. 打开 Basket 页面。

4. 在 Burp HTTP history 里找修改数量的请求，通常类似：

   ```text
   PUT /api/BasketItems/<basket-item-id>
   ```

   请求 body 可能类似：

   ```json
   {"quantity":2}
   ```

5. 右键请求，选择：

   ```text
   Send to Repeater
   ```

6. 在 Repeater 里把 quantity 改成负数，例如：

   ```json
   {"quantity":-100}
   ```

7. 点击 Send。

8. 如果响应接受负数，回浏览器刷新 Basket。

9. 继续 checkout 并完成订单。

10. 回 Score Board 确认 `Payback Time` solved。

11. 截图保存为：

    ```text
    assignment5/diagram/payback-time-solved.png
    ```

原理：

这是业务逻辑漏洞。商品数量、价格和订单总额不能信任客户端提交的数据。后端应该重新计算价格，并拒绝负数数量。如果后端接受负数，订单总额可能变成负数，付款流程就会变成“返款”效果。

报告可填：

```text
What worked: Modifying basket item quantity to a negative value changed order behavior.
What did not work: The normal UI did not allow entering a negative quantity directly.
```

## 26. 保存和恢复挑战进度

作业要求测试 save/restore progress。

在 Score Board 页面或菜单里找：

```text
Save Backup
Restore Backup
```

或者类似文字：

```text
Save challenge progress
Restore challenge progress
```

操作：

1. 点击保存进度。
2. 下载一个 progress 文件。
3. 记住文件保存位置，通常在 Downloads。
4. 再点击恢复进度。
5. 选择刚才保存的文件。
6. 确认页面显示进度恢复成功。

这一步截图，保存为：

```text
progress-save-restore.png
```

## 27. 填写 report.md

打开 `assignment5/report.md`，搜索 `[`，把所有 placeholder 填掉或保留成你要交的真实内容。

必须重点填：

- `[YOUR NAME]`
- `[DATE COMPLETED]`
- `[PROXY SETUP CHALLENGE: ...]`
- `[TIME SPENT: DOM XSS]`
- `[DOM XSS HELP USED: ...]`
- `[DOM XSS WHAT WORKED]`
- `[DOM XSS WHAT DID NOT WORK]`
- `[TIME SPENT: SCOREBOARD]`
- `[SCOREBOARD HELP USED: ...]`
- `[SCOREBOARD WHAT WORKED]`
- `[SCOREBOARD WHAT DID NOT WORK]`
- `[TIME SPENT: BONUS PAYLOAD]`
- `[BONUS PAYLOAD HELP USED: ...]`
- `[BONUS PAYLOAD WHAT WORKED]`
- `[BONUS PAYLOAD WHAT DID NOT WORK]`
- `[TIME SPENT: PRIVACY POLICY]`
- `[PRIVACY POLICY HELP USED: ...]`
- `[PRIVACY POLICY WHAT WORKED]`
- `[PRIVACY POLICY WHAT DID NOT WORK]`
- `[TIME SPENT: LOGIN ADMIN]`
- `[LOGIN ADMIN HELP USED: ...]`
- `[LOGIN ADMIN WHAT WORKED]`
- `[LOGIN ADMIN WHAT DID NOT WORK]`
- `[TIME SPENT: PASSWORD STRENGTH]`
- `[PASSWORD STRENGTH HELP USED: ...]`
- `[PASSWORD STRENGTH WHAT WORKED]`
- `[PASSWORD STRENGTH WHAT DID NOT WORK]`
- `[TIME SPENT: VIEW BASKET]`
- `[VIEW BASKET HELP USED: ...]`
- `[VIEW BASKET WHAT WORKED]`
- `[VIEW BASKET WHAT DID NOT WORK]`
- `[TIME SPENT: FORGED FEEDBACK]`
- `[FORGED FEEDBACK HELP USED: ...]`
- `[FORGED FEEDBACK WHAT WORKED]`
- `[FORGED FEEDBACK WHAT DID NOT WORK]`
- `[TIME SPENT: ADMIN SECTION]`
- `[ADMIN SECTION HELP USED: ...]`
- `[ADMIN SECTION WHAT WORKED]`
- `[ADMIN SECTION WHAT DID NOT WORK]`
- `[TIME SPENT: PAYBACK TIME]`
- `[PAYBACK TIME HELP USED: ...]`
- `[PAYBACK TIME WHAT WORKED]`
- `[PAYBACK TIME WHAT DID NOT WORK]`
- `[OPTIONAL EXTERNAL SOLUTION LINK USED: ...]`

如果你没有使用外部答案，最后那个 optional reference 可以删掉。

## 28. 导出 PDF

作业要求提交 PDF，不是提交 Markdown。

可以用其中一种方式：

### 方法 A：VS Code

1. 用 VS Code 打开 `assignment5/report.md`。
2. 打开 Markdown Preview。
3. 使用 Markdown PDF 扩展导出 PDF，或者复制预览到浏览器打印。

### 方法 B：浏览器打印

1. 用 Markdown 工具把 `report.md` 预览成 HTML。
2. 检查图片都显示。
3. 浏览器打印。
4. Destination 选：

   ```text
   Save to PDF
   ```

### 方法 C：Typora / Obsidian

1. 打开 `report.md`。
2. 确认图片都显示。
3. Export / Print to PDF。

导出前确认：

- 图片都显示，不是 broken image。
- 没有忘记填的 placeholder。
- `guide.md` 不提交。
- PDF 能正常打开。

## 29. 最后自查清单

- Burp Suite 已安装。
- Burp 选择了 Temporary project in memory。
- Burp 使用默认配置启动。
- Burp proxy listener 是 `127.0.0.1:8080`。
- `proxy-listener.png` 已截图。
- FoxyProxy 已安装。
- FoxyProxy 已添加 `Burp` 代理，HTTP `127.0.0.1:8080`。
- `proxy-manager-config.png` 已截图。
- Firefox 启用 FoxyProxy 后，Burp HTTP history 能看到请求。
- `proxy-intercept-test.png` 已截图。
- `sudo apt install juice-shop` 的失败画面已截图为 `juice-shop-apt-failed.png`。
- Podman 已安装。
- `podman run` 或 `podman start juice-shop` 能启动 Juice Shop。
- `ss -ltnp | grep 42000` 能看到监听。
- `juice-shop-running-ss.png` 已截图。
- `juice-shop-home.png` 已截图。
- `podman stop juice-shop` 能停止。
- 已完成普通购物流程。
- 已完成 Scoreboard。
- `scoreboard-solved.png` 已截图。
- 已完成 DOM XSS。
- `dom-xss-solved.png` 已截图。
- 已完成 Bonus Payload。
- `bonus-payload-solved.png` 已截图。
- 已完成 Privacy Policy。
- `privacy-policy-solved.png` 已截图。
- 已完成 Login Admin。
- `login-admin-solved.png` 已截图。
- 已完成 Password Strength。
- `password-strength-solved.png` 已截图。
- 已完成 View Basket。
- `view-basket-solved.png` 已截图。
- 已完成 Forged Feedback。
- `forged-feedback-solved.png` 已截图。
- `scoreboard-tutorials-completed.png` 已截图。
- 已测试 progress save/restore。
- `progress-save-restore.png` 已截图。
- Admin Section 已完成并截图。
- Payback Time 已完成并截图。
- `report.md` placeholders 已填完。
- PDF 已导出并确认可以打开。
