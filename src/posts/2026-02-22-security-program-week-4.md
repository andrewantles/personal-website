---
title: "CIS Controls Personal Security Program - Week 4"
date: 2026-02-22
summary: "Setting up first tooling on new security node"
author: "Andrew Antles"
thumbnail_alt: "[TODO]"
---

# Project Mission - North Star
Challenge and deepen my security engineering skills by deploying and running the technical components of a cyber security program on my personal network. 

# Documentation
## Tools and Implemenation Support
- https://learn.cisecurity.org/Essential-Cyber-Hygiene-v8.1

# Time Tracking:
|start|end|color|desc|
|-|-|-|-|
|08:00|08:30|OG|Off-and-on looking at tooling|
|08:30|09:15|OG|Starting blog page, getting tooling options gathered, beginning analysis.

# Narative

The biggest things I want to get set up today is a network asset tracking system. Bonus is to have at least bandwidth analysis capabilities per network device, with a goal of having a path to deeper network activity logging.

I took a quick scan through my trusty CIS Hygiene Guide, and identified two quick options: Open-AudIT, and Nmap. I also a looked back a few research tasks I had Claude run several weeks back.

Altogether, I was looking at the following options:
- Nmap
- Open-AudIT
- Netbox
- Snipe-IT

My first thought is that to reduce maintenance regarding dependencies and software updates, I could use scheduled Nmap scans, and do something simple like store the results in a CSV or something. A SQLite DB, or something similar, might be a good, light-weight option as well.

Maybe I'll start by checking the network requirements of the non-Nmap options, above. 

Yes, because I don't need a flashy UI. Remember - I want to be able to run this with my AI assistant, so UIs just create extra parsing. I want to continue training my brain to look at things at a lower level, so I can partner better with my AI assistant. 


## Another thing

Another thing that came up as I dug through the various tooling recommendations was that I would like to encrypt the drive on my Pi. That way, even if it was tampered with or stolen, it would have that layer of protection. This would help mitigate a concern I raised in the Week 3 [**NEED LINK**] blog post regarding locking down the boot options. In the case that an adversary booted the Pi to another boot device, the storage would be encrypted and inaccessible. This helps in the event of downright theft of the Pi as well. 