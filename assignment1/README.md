# Password Hash Assignment Report

## Part 1: Hash generation/cracking online

### 1.1 Online Hash Generation
> Generate MD5 hashes using free online services.

#### Free Online Services
1. https://md5decrypt.net/en/
2. https://10015.io/tools/md5-encrypt-decrypt

**Screenshots of https://md5decrypt.net/en/ Hash Generation:**
![alt text](image/image-1.png)
![alt text](image/image-2.png)
![alt text](image/image-3.png)
![alt text](image/image-4.png)

**Screenshots of https://10015.io/tools/md5-encrypt-decrypt Hash Generation:**
![alt text](image/image-5.png)
![alt text](image/image-6.png)
![alt text](image/image-7.png)
![alt text](image/image-8.png)

### 1.2 Local Verification (using md5sum)
> Verify on your local system using md5sum that the hashes generated online make sense.

```shell
~ » echo -n "qwertyuiop" | md5sum                                                                                                                                                    130 ↵ ericsong@ERICS-MACBOOK-PRO
6eea9b7ef19179a06954edd0f6c05ceb  -
(base) ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
~ » echo -n "über_alles\!" | md5sum                                                                                                                                                        ericsong@ERICS-MACBOOK-PRO
e44a7cf74cb368dec4e0c0a8af7e6e77  -
(base) ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
~ » echo -n "Lösenord" | md5sum                                                                                                                                                            ericsong@ERICS-MACBOOK-PRO
88fc757bb99a74998a3c7de1b8181c20  -
(base) ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
~ » echo -n "lakers2023\!" | md5sum                                                                                                                                                        ericsong@ERICS-MACBOOK-PRO
3b2cd0dc7af78aef77c35e33a9b75b8e  -
```

**Screenshots of Local Verification:**
![alt text](image/image-0.png)

### 1.3 Online Hash Cracking
> Attempt to crack the generated MD5 hashes using two free online services.

#### Free Online Services
1. https://md5decrypt.net/en/
2. https://10015.io/tools/md5-encrypt-decrypt

**Screenshots of https://md5decrypt.net/en/ Hash Cracking:**
![alt text](image/image-9.png)
![alt text](image/image-10.png)
![alt text](image/image-11.png)
![alt text](image/image-12.png)

**Screenshots of https://10015.io/tools/md5-encrypt-decrypt Hash Cracking:**
![alt text](image/image-13.png)
![alt text](image/image-14.png)
![alt text](image/image-15.png)
![alt text](image/image-16.png)

### 1.4 Analysis
> Were there any differences in the results? If yes, then explain why and which results are correct. Provide a brief analysis that discusses why the hashes generated online may differ, including pros and cons of online hash generation/dehashing services.

Yes, there were notable differences in the results, stemming from two primary technical nuances: newline characters and character encoding.

**1. The Newline Character (`\n`) Discrepancy**
Initially, when I generated the hash locally using the command `echo "qwertyuiop" | md5sum`, the resulting hash did not match the online service. Upon further investigation into the `echo` command, I discovered that it automatically appends a newline character (`\n`) to the end of the specified string by default. By explicitly adding the `-n` flag (e.g., `echo -n "qwertyuiop" | md5sum`), `echo` is instructed to output *only* the exact string provided, without appending any extra characters. This adjustment successfully resolved the discrepancy for standard strings.

**2. Character Encoding of Non-ASCII Characters**
For the strings "über_alles!" and "Lösenord", the results from `https://md5decrypt.net/en/` completely differed from both the local execution and the other online service. The root cause here revolves around non-ASCII characters (such as the German umlauts `ü` and `ö`). Different tools process and encode input strings using entirely different character encoding schemas before applying the hashing algorithm. While I attempted to replicate the online service's results locally by converting the UTF-8 string into various other encodings (e.g., `echo -n "über_alles!" | iconv -f UTF-8 -t ISO-8859-1 | md5sum`), the hashes still did not match `md5decrypt.net`. This suggests the site is using an elusive or non-standard encoding format. Ultimately, the local results utilizing standard UTF-8 encoding are the most standard and "correct."

**Pros and Cons of Online Hash Services**
*   **Pros:** They are highly convenient, require zero local setup or computational power, and are excellent for quick, on-the-fly hash generation or simple reverse dictionary lookups.
*   **Cons:** They introduce severe security and privacy risks, as submitting raw passwords exposes them over the internet to third-party servers. Furthermore, they are inherently unreliable when handling special, non-ASCII characters due to opaque, undocumented character encoding treatments (as demonstrated above).

---

## Part 2: MD5 hash cracking locally on macOS using Hashcat

### 2.1 Identify the Hash Type
> Analyze the target hashes to determine their type(s). 

**Analysis / Hash Mode:**

**Step 1 — Manual Analysis**

Inspecting a sample of hashes from `linkedin_500k_hashes.txt` (e.g., `37d2ef282dfcc97eb77245ff5d24e311d58625fe`) reveals:

- Every hash is exactly **40 hexadecimal characters** long.
- 40 hex chars × 4 bits/char = **160 bits** — the exact digest size produced by **SHA-1** (Secure Hash Algorithm 1).
- All characters are lowercase `[0-9a-f]`, with no salt prefix/suffix or any other decoration.

**Step 2 — Tool Confirmation (`hashcat --identify`)**

Running `hashcat --identify 37d2ef282dfcc97eb77245ff5d24e311d58625fe` on the sample hash yields:

```shell
~/Courses/SWE267P/assignment1 » hashcat --identify 37d2ef282dfcc97eb77245ff5d24e311d58625fe                                                                                                ericsong@ERICS-MACBOOK-PRO
The following 7 hash-modes match the structure of your input hash:

      # | Name                                                       | Category
  ======+============================================================+======================================
    100 | SHA1                                                       | Raw Hash
   6000 | RIPEMD-160                                                 | Raw Hash
    170 | sha1(utf16le($pass))                                       | Raw Hash
   4700 | sha1(md5($pass))                                           | Raw Hash salted and/or iterated
  18500 | sha1(md5(md5($pass)))                                      | Raw Hash salted and/or iterated
   4500 | sha1(sha1($pass))                                          | Raw Hash salted and/or iterated
    300 | MySQL4.1/MySQL5                                            | Database Server

```

The top match is **SHA1 (mode 100)**, confirming plain unsalted SHA-1. So the hashes were stored as simple `SHA1($password)`.

**Conclusion:** Hash type is **SHA-1 (unsalted)** → Hashcat mode `**-m 100`**.


### 2.2 Crack hashes using Hashcat and Rockyou Wordlist

**Command Used:**
```shell
~/Courses/SWE267P/assignment1 » hashcat -m 100 -a 0 linkedin_500k_hashes.txt rockyou.txt -o cracked_2_2.txt --potfile-disable
```

| Flag | Meaning |
|---|---|
| `hashcat` | Invokes the hashcat binary. |
| `-m 100` | Sets the hash type to **SHA-1** (raw, unsalted, non-iterated). Each algorithm has a fixed numeric ID; 100 = plain SHA-1. |
| `-a 0` | Sets the attack mode to **dictionary (straight)**. Hashcat reads candidates line-by-line from the wordlist, computes SHA-1 for each, and compares against the full target hash set. |
| `linkedin_500k_hashes.txt` | The target hash file — 500,000 40-character SHA-1 hashes, one per line. |
| `rockyou.txt` | The wordlist — 14,344,392 real-world passwords leaked in the 2009 RockYou breach, the most widely used wordlist in password cracking. |
| `-o cracked_2_2.txt` | Appends successfully cracked `hash:plaintext` pairs to this output file for later inspection (does not affect terminal output). |
| `--potfile-disable` | Disables hashcat's potfile cache (`~/.local/share/hashcat/hashcat.potfile`). By default hashcat skips any hash it has already cracked in a previous run, which prevents `-o` from being written on a re-run. This flag forces a full re-execution every time. |

**Results and Performance:**

| Metric | Value |
|---|---|
| Hash Mode | 100 (SHA1) |
| Wordlist | rockyou.txt (14,344,391 passwords) |
| Device | Apple M4 GPU (OpenCL, 10MCU) |
| Speed | 372.3 kH/s |
| **Recovered** | **144,622 / 500,000 (28.92%)** |
| Time Taken | ~39 seconds |

```shell
~/Courses/SWE267P/assignment1 (main*) » hashcat -m 100 -a 0 linkedin_500k_hashes.txt rockyou.txt -o cracked_2_2.txt --potfile-disable                                                      ericsong@ERICS-MACBOOK-PRO
hashcat (v7.1.2) starting

METAL API (Metal 371.5)
=======================
* Device #01: Apple M4, skipped

OpenCL API (OpenCL 1.2 (Jan 16 2026 07:22:26)) - Platform #1 [Apple]
====================================================================
* Device #02: Apple M4, GPU, 6062/12124 MB (1136 MB allocatable), 10MCU

Minimum password length supported by kernel: 0
Maximum password length supported by kernel: 256

Hashes: 500000 digests; 500000 unique digests, 1 unique salts
Bitmaps: 16 bits, 65536 entries, 0x0000ffff mask, 262144 bytes, 5/13 rotates
Rules: 1

Optimizers applied:
* Zero-Byte
* Early-Skip
* Not-Salted
* Not-Iterated
* Single-Salt
* Raw-Hash

ATTENTION! Pure (unoptimized) backend kernels selected.
Pure kernels can crack longer passwords, but drastically reduce performance.
If you want to switch to optimized kernels, append -O to your commandline.
See the above message to find out about the exact limits.

Watchdog: Temperature abort trigger set to 100c

Host memory allocated for this attack: 687 MB (2447 MB free)

Dictionary cache built:
* Filename..: rockyou.txt
* Passwords.: 14344392
* Bytes.....: 139921507
* Keyspace..: 14344385
* Runtime...: 0 secs

Cracking performance lower than expected?

* Append -O to the commandline.
  This lowers the maximum supported password/salt length (usually down to 32).

* Append -w 3 to the commandline.
  This can cause your screen to lag.

* Append -S to the commandline.
  This has a drastic speed impact but can be better for specific attacks.
  Typical scenarios are a small wordlist but a large ruleset.

* Update your backend API runtime / driver the right way:
  https://hashcat.net/faq/wrongdriver

* Create more work items to make use of your parallelization power:
  https://hashcat.net/faq/morework

Approaching final keyspace - workload adjusted.


Session..........: hashcat
Status...........: Exhausted
Hash.Mode........: 100 (SHA1)
Hash.Target......: linkedin_500k_hashes.txt
Time.Started.....: Tue Apr 14 19:43:24 2026 (39 secs)
Time.Estimated...: Tue Apr 14 19:44:03 2026 (0 secs)
Kernel.Feature...: Pure Kernel (password length 0-256 bytes)
Guess.Base.......: File (rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#02........:   372.3 kH/s (0.06ms) @ Accel:1024 Loops:1 Thr:64 Vec:1
Recovered........: 144622/500000 (28.92%) Digests (total), 144622/500000 (28.92%) Digests (new)
Remaining........: 355378 (71.08%) Digests
Recovered/Time...: CUR:N/A,N/A,N/A AVG:N/A,N/A,N/A (Min,Hour,Day)
Progress.........: 14344385/14344385 (100.00%)
Rejected.........: 0/14344385 (0.00%)
Restore.Point....: 14344385/14344385 (100.00%)
Restore.Sub.#02..: Salt:0 Amplifier:0-1 Iteration:0-1
Candidate.Engine.: Device Generator
Candidates.#02...: 0844132938 -> $HEX[042a0337c2a156616d6f732103]
Hardware.Mon.SMC.: Fan0: 0%
Hardware.Mon.#02.: Util: 44% Pwr:585mW

Started: Tue Apr 14 19:43:23 2026
Stopped: Tue Apr 14 19:44:03 2026
```

### 2.3 Crack target hashes using Rockyou Wordlist + Standard Rules
> Try adding rules to the Rockyou dictionary (e.g., best64, InsidePro-PasswordsPro).

**Command Used (best64):**
`[💻 在此处写出使用 best64.rule 的命令]`

**Command Used (InsidePro-PasswordsPro):**
`[💻 在此处写出使用 InsidePro-PasswordsPro.rule 的命令]`

**Results and Performance:**
`[📸 在此处插入截图并填写破解结果对比]`

### 2.4 Crack target hashes using a curated and larger wordlist
> Use a search engine to find a dictionary that cracks more than Rockyou.

**Dictionary Used (Name and Source):**
`[📝 在此填写你找到的精选大字典名称和下载链接]`

**Command Used:**
`[💻 在此填写使用的命令]`

**Results and Performance:**
`[📸 在此处插入截图并填写新的破解成绩]`

### 2.5 Summary for Part 2
> Description of what Hashcat cracking methods were used, which dictionaries, performance aspects and a summary of the results (number of hashes cracked and time taken).

`[📝 在此总结 Part 2 的破解方法、字典、性能表现（例如体现 macOS 原生优势）以及最终总结果]`

---

## Part 3: Passphrase cracking

### 3.1 Crack passphrases using custom word list with custom rules
> Determine the hash type of the target file `hashes_passphrases.txt`.

**Hash Type Identification:**
`[📝 在此填写识别出的 Hashcat Mode ID (-m)]`

**Command and Results:**
`[📸 在此处插入截图并填写破解命令和结果]`

### 3.2 Try adding another rule (Stacking Rules)
> Customize the rules list even more (-r rule1 -r rule2).

**Command and Results:**
`[📸 在此处插入截图并填写叠加规则后的破解结果]`

### 3.3 Create a custom rule
> Try creating your own custom rule by editing an existing rule (e.g., extending Leetspeak substitution in rule2 and adding symbols).

**Custom Rule Description:**
`[📝 在此描述你自己修改的规则内容和思路]`

**Command and Results:**
`[📸 在此处插入截图并填写最终命令和破解出来的数量]`

### 3.4 Summary for Part 3
> Description of what Hashcat cracking methods were used, filters/rules, performance aspects, and results.

`[📝 在此总结 Part 3 中用来攻破 Passphrase 的规则组合、性能以及总花费时间]`

---

## Part 4: Document password cracking

### 4.1 Extract Hash from LibreOffice Document (hashcat.odt)
> The password hash can be extracted from the document using the John tool (`office2john.py`).

**Command Used and Extracted Hash:**
`[📸 在此处写出你的工具提取命令并贴出部分提取结果截图]`

### 4.2 Crack Hash with Hashcat
> Feed Hashcat with the hash and start with a dictionary.

**Command Used:**
`[💻 在此处写出使用的 Hashcat 命令，及找到的对应文件 Mode ID (-m)]`

**Results (Password Found & Time Taken):**
`[📸 在此处插入爆破成功的截图，并写出该文档密码]`

### 4.3 Summary for Part 4
> Description of what Hashcat cracking methods were used, which dictionaries, performance aspects and a summary of the results.

`[📝 在此总结成功解开 office 文档所用的方法和耗费的时间]`
