<h1 align="center">
  <img src="https://img.shields.io/badge/ambient--uaf-%20-blueviolet?style=for-the-badge&logo=linux&logoColor=white" width="400"><br>
  🧠 <b>ambient-uaf</b> ⚙️  
</h1>

<p align="center">
  <b>Safe sandbox and testing environment for Use-After-Free (UAF) research</b><br>
  <i>Designed for controlled, educational, and authorized testing only.</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square">
  <img src="https://img.shields.io/badge/platform-Linux-lightgrey?style=flat-square">
  <img src="https://img.shields.io/badge/language-C/C++-blue?style=flat-square">
  <img src="https://img.shields.io/badge/status-Lab%20Ready-orange?style=flat-square">
</p>

<figure align="center">
  <img src="https://img.icons8.com/?size=512&id=44660&format=png" width="120" alt="Security Icon">
  <figcaption><i>Isolated VM-based lab for safe UAF experiments</i></figcaption>
</figure>

<h2>🧩 Overview</h2>

<p>
<b>ambient-uaf</b> is a secure and documented environment for testing and studying
<strong>Use-After-Free (UAF)</strong> vulnerabilities in a <b>controlled virtual lab</b>.
It provides setup guides, compiler flags, and tools like AddressSanitizer and Valgrind
to detect and analyze memory safety issues safely.
</p>

> ⚠️ <b>Disclaimer:</b> This project is for educational and authorized research only.  
> Do not execute tests on third-party systems. Use inside isolated environments.

<h2>📁 Project Structure</h2>

ambient-uaf/
├── vm-setup/ # VM setup guides (VirtualBox / QEMU)
├── examples/ # Minimal C/C++ UAF demonstration programs
│ └── uaf_example.c
├── tools/ # ASan, Valgrind, and logging utilities
└── README.md # Documentation


<h2>🧠 Key Features</h2>

- 🧱 Step-by-step instructions for isolated **Virtual Machines (VMs)**  
- 🔍 Integration with **AddressSanitizer (ASan)** and **Valgrind (Memcheck)**  
- 💾 Safe workflow with snapshots, no shared folders, and log collection  
- 🧰 Debugging examples with GDB and `rr` (record-replay)  
- 📋 Legal and ethical research guidelines  

<h2>⚙️ Requirements</h2>

<ul>
  <li>VirtualBox / QEMU / VMware</li>
  <li>Linux-based guest OS (Ubuntu, Debian, Arch)</li>
  <li><code>gcc</code>, <code>clang</code>, <code>valgrind</code>, <code>gdb</code>, <code>rr</code></li>
  <li>Snapshots enabled and isolated network (Host-only / Air-gap)</li>
</ul>

<h2>🚀 Quickstart (Summary)</h2>

```
# Inside your Linux VM
sudo apt update
sudo apt install build-essential valgrind gdb rr

# Compile example with AddressSanitizer
gcc -fsanitize=address -g -O1 examples/uaf_example.c -o uaf_example_asan

# Run with ASan
ASAN_OPTIONS=detect_leaks=1 ./uaf_example_asan
```

Run with Valgrind:

```
valgrind --leak-check=full --track-origins=yes ./uaf_example_asan

```

Debug with GDB:
```
gdb ./uaf_example_asan
run
bt
```

<h2>🧪 Example (uaf_example.c)</h2>

```c
#include <stdio.h>
#include <stdlib.h>

/*
 * Simple Use-After-Free demonstration.
 * The pointer is accessed after being freed,
 * which triggers a memory safety violation.
 */

int main() {
    int *ptr = malloc(sizeof(int)); // Allocate memory
    *ptr = 42;                      // Write to allocated memory

    free(ptr);                      // Memory is released

    // ❌ Dangerous: Access after free (UAF)
    printf("Value after free: %d\n", *ptr);

    return 0;
}


<h2>🔒 Safe Workflow</h2>
🧰 Create a clean VM (snapshot immediately).
❌ Disable clipboard and shared folders.
🌐 Set network mode to <b>Host-only</b> or <b>No Network</b>.
🔁 Test binaries inside the VM only.
💾 Export logs and restore snapshot before new tests.
<h2>📘 Educational Purpose</h2>
<p>
This repository aims to support students and researchers studying memory corruption,
offering a reproducible and safe environment for experiments.
</p>
🧩 UAF (Use-After-Free) occurs when memory is accessed after being freed —
this lab helps visualize and detect such issues without risk to real systems.
<h2>🤝 Contributing</h2>
<p>
Contributions are welcome — please ensure that any additions follow the same safety and ethical principles.
Do not include or share real-world exploits.
</p>
<h2>📜 License</h2>
<p align="center">
  <b>MIT License</b> — for educational and research use.<br>
  Created and maintained for safe vulnerability analysis learning.
</p>
<figure align="center">
  <img src="https://img.icons8.com/?size=512&id=111700&format=png" width="100" alt="Lab Icon">
  <figcaption><i>Build safely. Test ethically.</i></figcaption>
</figure>
```
::contentReference[oaicite:0]{index=0}
