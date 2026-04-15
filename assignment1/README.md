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
hashcat --identify 37d2ef282dfcc97eb77245ff5d24e311d58625fe                                                                                                ericsong@ERICS-MACBOOK-PRO
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
hashcat -m 100 -a 0 linkedin_500k_hashes.txt rockyou.txt -o cracked/cracked_2_2.txt --potfile-disable
```

| Flag | Meaning |
|---|---|
| `hashcat` | Invokes the hashcat binary. |
| `-m 100` | Sets the hash type to **SHA-1** (raw, unsalted, non-iterated). Each algorithm has a fixed numeric ID; 100 = plain SHA-1. |
| `-a 0` | Sets the attack mode to **dictionary (straight)**. Hashcat reads candidates line-by-line from the wordlist, computes SHA-1 for each, and compares against the full target hash set. |
| `linkedin_500k_hashes.txt` | The target hash file — 500,000 40-character SHA-1 hashes, one per line. |
| `rockyou.txt` | The wordlist — 14,344,392 real-world passwords leaked in the 2009 RockYou breach, the most widely used wordlist in password cracking. |
| `-o cracked/cracked_2_2.txt` | Appends successfully cracked `hash:plaintext` pairs to this output file for later inspection (does not affect terminal output). |
| `--potfile-disable` | Disables hashcat's potfile cache (`~/.local/share/hashcat/hashcat.potfile`). By default hashcat skips any hash it has already cracked in a previous run, which prevents `-o` from being written on a re-run. This flag forces a full re-execution every time. |

**Results and Performance:**

![alt text](image/image.png)

| Metric | Value |
|---|---|
| Hash Mode | 100 (SHA1) |
| Wordlist | rockyou.txt |
| Device | Apple M4 GPU (OpenCL, 10MCU) |
| **Recovered** | **144,622 / 500,000 (28.92%)** |
| Time Taken | ~39 seconds |

### 2.3 Crack target hashes using Rockyou Wordlist + Standard Rules
> Try adding rules to the Rockyou dictionary (e.g., best64, InsidePro-PasswordsPro).

> **Note on best64 vs best66:** Hashcat's canonical "best64" rule set was later extended to `best66.rule` (66 rules). No `best64.rule` ships with modern Hashcat distributions; `best66.rule` is its direct successor and superset, so it is used here.

**Command Used (best66):**
```shell
hashcat -m 100 -a 0 linkedin_500k_hashes.txt rockyou.txt -r rules/best66.rule -o cracked/cracked_2_3_best66.txt --potfile-disable
```

**Command Used (InsidePro-PasswordsPro):**
```shell
hashcat -m 100 -a 0 linkedin_500k_hashes.txt rockyou.txt -r rules/InsidePro-PasswordsPro.rule -o cracked/cracked_2_3_insidepro.txt --potfile-disable
```

**Flag Reference:**

| Flag | Meaning |
|---|---|
| `-m 100` | Hash type: SHA-1 (same as 2.2). |
| `-a 0` | Dictionary (straight) attack mode. |
| `-r <rule>` | Apply a mangling rule file; each word in the wordlist is transformed by every rule before hashing, multiplying the effective keyspace. |
| `--potfile-disable` | Force a full re-run, bypassing the cached potfile. |
| `-o <file>` | Write cracked `hash:plaintext` pairs to the specified output file. |

**Results and Performance:**

![alt text](image/image-17.png)

![alt text](image/image-18.png)

| Metric | best66 | InsidePro-PasswordsPro |
|---|---|---|
| Hash Mode | 100 (SHA1) | 100 (SHA1) |
| Rule File | best66.rule (66 rules) | InsidePro-PasswordsPro.rule (3,234 rules) |
| Wordlist | rockyou.txt | rockyou.txt |
| Effective Keyspace | 946,729,410 | 46,389,741,090 |
| Device | Apple M4 GPU (OpenCL, 10MCU) | Apple M4 GPU (OpenCL, 10MCU) |
| **Recovered** | **229,459 / 500,000 (45.89%)** | **302,154 / 500,000 (60.43%)** |
| Time Taken | ~1 min 10 secs | ~2 mins 46 secs |

**Analysis:**

Adding mangling rules dramatically increases the number of cracked hashes compared to the plain dictionary attack (28.92% in 2.2).

- **best66** (66 rules, ~947 M candidates): Recovered **45.89%** — a +17% gain over the baseline in roughly 2× the time. The rule set applies common transformations such as capitalizing the first letter, appending/prepending digits and symbols, and toggling case, covering the most frequent real-world password patterns efficiently.
- **InsidePro-PasswordsPro** (3,234 rules, ~46 B candidates): Recovered **60.43%** — a further +14.5% gain at the cost of ~2× more time. Its larger rule set captures more exotic transformations (leet-speak variants, mixed-case patterns, multi-character substitutions), at the expense of a ~49× larger keyspace that still completes in under 4 minutes on the Apple M4 GPU.

### 2.4 Crack target hashes using a curated and larger wordlist
> Use a search engine to find a dictionary that cracks more than Rockyou.

**Dictionary Used (Name and Source):**

**CrackStation Human-Only Wordlist** — curated by Defuse Security from real human password leaks across multiple website database breaches.

- Source: https://crackstation.net/crackstation-wordlist-password-cracking-dictionary.htm
- Direct download: `https://crackstation.net/files/crackstation-human-only.txt.gz`
- ~63.9 million passwords (4.5× larger than RockYou's 14.3M)
- 247 MiB compressed / 683 MiB uncompressed
- License: Creative Commons Attribution-ShareAlike 3.0

**Command Used:**
```shell
hashcat -m 100 -a 0 linkedin_500k_hashes.txt crackstation-human-only.txt -o cracked/cracked_2_4.txt --potfile-disable
```

| Flag | Meaning |
|---|---|
| `-m 100` | Hash type: SHA-1 (same as 2.2). |
| `-a 0` | Dictionary (straight) attack mode. |
| `crackstation-human-only.txt` | Curated wordlist of ~63.9M real human passwords from leaked website databases. |
| `-o cracked/cracked_2_4.txt` | Save cracked `hash:plaintext` pairs to output file. |
| `--potfile-disable` | Force full re-run, bypassing cached potfile. |

**Results and Performance:**

![alt text](image/image-19.png)

| Metric | Value |
|---|---|
| Hash Mode | 100 (SHA1) |
| Wordlist | crackstation-human-only.txt |
| Wordlist Size | 63,941,069 passwords (683 MiB) |
| Device | Apple M4 GPU (OpenCL, 10MCU) |
| **Recovered** | **181,345 / 500,000 (36.27%)** |
| Time Taken | ~52 secs |

**Analysis:**

The CrackStation Human-Only wordlist recovered **36.27%** of hashes — a **+7.35% gain** over the plain RockYou baseline (28.92%) without using any rules. This improvement comes from the wordlist containing 4.5× more real-world human passwords sourced from a wider variety of leaked databases beyond the original 2009 RockYou breach. Despite the larger keyspace (~64M vs ~14M candidates), the Apple M4 GPU processed the entire list in just over a minute, demonstrating efficient GPU acceleration on macOS without any virtualisation overhead.

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
