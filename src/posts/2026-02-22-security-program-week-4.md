---
title: "CIS Controls Personal Security Program - Week 4"
date: 2026-03-01
summary: "Setting up first tooling on new security node"
author: "Andrew Antles"
thumbnail_alt: "[TODO]"
unlisted: true
---

# Project Mission - North Star
Challenge and deepen my security engineering skills by deploying and running the technical components of a cyber security program on my personal network. 

# Documentation
## Additional Framework History:
- https://learn.cisecurity.org/CIS-Controls-v8-guide-pdf
- https://learn.cisecurity.org/cis-controls-v8-1-guide-pdf
## Tools and Implemenation Support
- https://learn.cisecurity.org/Essential-Cyber-Hygiene-v8.1

# Time Tracking:
|start|end|color|desc|
|-|-|-|-|
|08:00|08:30|OG|Off-and-on looking at tooling|
|08:30|09:15|OG|Starting blog page, getting tooling options gathered, beginning analysis.

|start|end|color|desc|
|-|-|-|-|
|08:00||G|Tooling options review and catch-up

# Narative

The goal for today was to setup network inventorying and basic monitoring. 

I took a quick scan through my trusty CIS Hygiene Guide, and identified two quick options: Open-AudIT, and Nmap. I also a looked back at a few research tasks I had Claude run several weeks back.

Altogether, I was looking at the following options:
- Nmap
- Open-AudIT
- Netbox
- Snipe-IT

I wasn't really happy with these though. The non-Nmap solutions were all geared toward an IT-type inventory system, and I need more than that. I need something that can perform analysis and monitoring. Something where I can get some activity baselines. And, something that can act as a network activity source for feeding to a SIEM or analysis platform later.

I sent Claude off on another research task with refined requirements while I took a shower and made coffee. The result was clear and matched a previous look that I'd taking into this in the past: ntopng. 

ntop is a European company, and what started out as an open-source network monitoring program, is now offered with enterprise support and on purpose-built hardware. The company's [About Us](https://www.ntop.org/about-us/the-company/) page was very reassuring, and with the product's maturity and range of security-minded features, I was ready to take the plunge. 

The next thing I confirmed was whether I could interact with ntop via CLI or API. I need to be able to script automations and interact via LLM agent. Thankfully, the [API documentation](https://www.ntop.org/guides/ntopng/api/index.html) offered what appears to be a fairly robust setup.

I'd considered using Nmap scans running on a schedule, but it's just too much for me to try to manage at the moment. With so many variables, I just need to keep this program moving along. It's not that Nmap scans are hard to schedule and run. It's moreso the engineering that goes along with developing an network inventory system based on Nmap. I would have to establish storage after evaluating options (probably SQLite or similar to start), and then develop logic for maintaining, updating, and adding entries to the storage. This brings along with ot debugging and monitoring to confirm everything is running as expected, error checking, bug squashing, etc. I really just need this thing to run right now. So, after finding a package like ntop that felt pretty comfortable with and excited about, it was definitely the right move to maintain momentum early in the program. Finally, a system based on scheduled Nmap scans wouldn't give me the network activity metrics per-device. 

# Install and Login

The install went [as advertised](https://www.ntop.org/support/documentation/software-installation/), and before long, I was looking at a login page for ntop. As a reminder, I'm running this on a Raspberry Pi 4B. 

**INSERT LOGIN SCREEN IMAGE**

A few things I noticed right away: No TLS. Accessible from anywhere on the same subnet. 

The default credentials weren't a problem, because it prompted me to update those at first login, but that doesn't do me a lot of good if I have a local attacker listening for credentials sent in plaintext. I also don't have a management VLAN setup (yet, perhaps later), so I'm not thrilled that it defaults to open HTTP access. 

Two actions items added...

# First Look

Overall, I'm quite pleased with the layout and the information provided. They definitely hit the mark with the colorful dashboards. It also seems to be detecting some of my network host without any setup or configuration. I'm feeling hopeful.

**SCREENSHOT OF DASHBOARD** 


## Settings Tweaks

Don't need 12 hour sessions.
There is support for centralized authentication, as opposed to locally managed users/passwords. 
Set everything to monitor by MAC address since IPs are dynamically assigns via DHCP.
Kicked off the first network discovery scan.

## Additional Setup
Logging into my switch to configure the mirror port, I find that it also does not have TLS enabled on it's web interface. If I can't get all of these talking with certificate pairs, I'm going to need to look hard at setting up a management VLAN. The main barrier to entry here is that I'm most likely looking at a switch upgrade since my 8-port is just about maxed out. 

I logged into my router gateway, which also happens to be my DHCP server, and established static IPs for the switch and the Raspberry Pi. These are the main two management devices that I need to be able to know where they are at all times. 


## Another thing

Another thing that came up as I dug through the various tooling recommendations was that I would like to encrypt the drive on my Pi. That way, even if it was tampered with or stolen, it would have that layer of protection. This would help mitigate a concern I raised in the Week 3 [**NEED LINK**] blog post regarding locking down the boot options. In the case that an adversary booted the Pi to another boot device, the storage would be encrypted and inaccessible. This helps in the event of downright theft of the Pi as well. 


## Freeform notes:
- Hygeine guide only covers CIS Implementation Group 1 (out of 3). 
- Safeguard 1.1: Establish and Maintain Detailed Enterprise Asset Inventory
    - records the network address (if static), hardware address, machine name, enterprise asset owner, department for each asset, and whether the asset has been approved to connect
    - Review and update the inventory of all enterprise assets bi-annually, or more frequently

ntopng is the tool we're going with. Now weighing installation options - binary or container

Nothing weird about the company

In an effort to get up and running quickly, I'm deciding to eschew the use of containers due to the added complexity, summarized here: https://www.ntop.org/best-practices-for-using-ntop-tools-on-containers/. 


Action items:
* Set up TLS on ntop
* Lock down the HTTP access to ntop - either restricted to locally, or from just my laptop via static IP
    - Configured at: **Preferences > User Interface > Access Control List** 