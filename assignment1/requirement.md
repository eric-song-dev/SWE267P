Password Hash Assignment
Due Wednesday by 11:59pm Points 100 Submitting a file upload Available Apr 2 at 12am - Apr 18 at 11:59pm
In this assignment students will explore password hashes, techniques and tools for dehashing/cracking. The student should submit a brief report documenting all work performed, including any analysis and use of tools carried out to complete the exercises in this assignment. Use screenshots where appropriate.

Part 1: Hash generation/cracking online
[*] Generate MD5 hashes for the passwords below using two different free online services eg: https://md5decrypt.net/en/

qwertyuiop

über_alles!

Lösenord

lakers2023!

Verify on your local system using md5sum that the hashes generated online make sense. Hint. The newline character should not be included in the hash.
Attempt to crack the generated MD5 hashes using two free online services (see above).
Document the hash generation and cracking with screen shots. Were there any differences in the results If yes, then explain why and which results are correct. Provide a brief analysis that discusses why the hashes generated online may differ, including pros and cons of online hash generation/dehashing services.
Part 2: MD5 hash cracking locally on Kali Linux VM using Hashcat
Setup Kali and Hashcat
Perform local hash cracking in a Kali Linux VM using the tool Hashcat.

Make an account with 
DownloadVMWare Workstation or FusionLinks to an external site. (for Mac)
You probably need to make an account with Broadcom to do this.
Download Kali Linux VM 4

https://www.kali.org/get-kali/#kali-virtual-machinesLinks to an external site.

Use VMware Player to run the Kali Linux
Login with user Kali and password
Ensure the Kali VM has at least 4Gb RAM (the more the better).
Some Setup Tips

More information about Hashcat at https://hashcat.net/wiki/doku.php?id=hashcat
Links to an external site.
Links to an external site.More information about Kali https://www.kali.org/docs/

Drag the text file linkedin_500k_hashes.txt Download linkedin_500k_hashes.txt
 with the target hashes we will work on from your host machine to the guest Kali Linux VM desktop.


More information about Kali tools https://www.kali.org/tools/
Since Hashcat performs better with a GPU and more RAM, install and run it on a more powerful system than a Kali VM for better performance.
Cracking Tasks

1. Identify the hash type(s) used in the target file.

Analyze the target hashes to determine their type(s).
Perform manual analysis or tool in Hint. This is a common hash type.
Hint. If required, split target hash file into separate files for each hash type.

 

2. Crack hashes using Hashcat and a word list.

Feed the target hashes into Hashcat and crack with Rockyou.
The wordlist is located in the directory /usr/share/wordlists and needs to be decompressed.
Make sure to specify the correct Hashcat mode for the hashes to be cracked.
Some Additional Tips

Hashcat is located in /usr/share/Hashcat and can also be started via the GUI in the Kali menu “05 - Password attacks”.
Allocate at least 4GB of RAM in the Kali Linux VM to run Hashcat. Hint. Attack mode -a 0 is dictionary mode (default)
Hash mode -m <mode> sets hash type
The --potfile-disable option means that cracked hashes are not saved to default file hashcat.potfile.
The --remove option deletes successfully cracked hashes from the target hash file.
The -o <file> option saves cracked hashes to a separate file.
The Hashcat potfile stores all cracked hashes by default at ~/.local/share/hashcat/hashcat.potfile
3. Crack target hashes with Hashcat using a wordlist and standard rules.

Try adding a rule to the Rockyou dictionary
Some Additional Tips

Hashcat rules are located in the rules subdirectory /usr/share/Hashcat/rules
The -r <rule> option sets rule to be used.
Try the best64 rule.
Then try the InsidePro-PasswordsPro rule.
 

4. Crack target hashes with Hashcat using a curated and larger wordlist.

Use a search engine to find a dictionary that cracks more than Rockyou.
Some Additional Tips

Size matters but overly huge wordlists do not necessarily mean that they are better.
Look for wordlists that have been curated by people from the hash cracking scene.
 

5. Write a description of what Hashcat cracking methods were used, which dictionaries, performance aspects and a summary of the results, including number of hashes cracked and how long it took.

Part 3: Passphrase cracking
1. Crack the target passphrase file using custom word list with custom rules.

Users often create longer passwords (passphrases) that are more secure based on their hobbies, interests and favorite things/persons.
Determine the hash type of the target file hashes_passphrases.txt Download hashes_passphrases.txt
 
Feed Hashcat with the passphrase hashes and use a dictionary and rules that are tailored to passphrases.
2. Try adding another rule to customize the rules list even more and make the passphrase dictionary more complex.

An Additional Tip

You can stack rules to mangle your dictionary further by adding another -r <rule1> -r <rule2>
 

3. Try creating your own custom rule by editing an existing rule to increase the number of cracked hashes.

Some Additional Tips

Reviewing the contents of passphrase-rule2, we can see that Leetspeak is applied to the first few characters in the passphrase.
Edit rule2 to extend the Leetspeak substitution for more initial characters in the password.
Add more symbols at beginning and end of the passphrase since many users do this to make their passwords more complex while easy to remember.
4. Write a description of what Hashcat cracking methods were used, which dictionaries, performance aspects and a summary of the results, including number of hashes cracked and how long it took.

 

Part 4: Document password cracking
1. Use Hashcat to crack a password protected Libreoffice document hashcat.odt Download hashcat.odt

The password hash can be extracted from the document using a tool provided with the John tool in the Kali VM.
Select the appropriate hash type from the Hashcat.
Feed Hashcat with the hash and start with a dictionary .
Some Additional Tips

The John tool is located in the Kali directory /usr/share/john.
The hash needs to be fed into Hashcat between twp single quotes.
 

2. Write a description of what Hashcat cracking methods were used, which dictionaries, performance aspects and a summary of the results, including number of hashes cracked and how long it took.