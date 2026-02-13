---
title: "CIS Controls Personal Security Program - Week 1"
date: 2026-01-18
summary: "Program structure selection and CIS Controls review."
---

# Project Mission - north star
Challenge and deepen my security engineering skills by deploying and running the technical components of a cyber security program on my personal network. 

# Documentation:
## Overview & Introductory Docs
- https://learn.cisecurity.org/controls-v8.1-guide-to-implementation-groups
- https://learn.cisecurity.org/CIS-Controls-v8.1-Roadmap-to-the-CIS-Critical-Security-Controls
- https://learn.cisecurity.org/cost-of-cyber-defense-v1.1-pdf

## Core CIS 8.1 Doc
- https://learn.cisecurity.org/cis-controls-v8-1-guide-pdf

## CIS Policy Templates
- https://www.cisecurity.org/controls/policy-templates

## Tools and Implemenation Support
- https://learn.cisecurity.org/Essential-Cyber-Hygiene-v8.1
- https://www.cisecurity.org/advisory
- https://www.cisecurity.org/controls/resources?crc=environment-specific-guidance
    - https://learn.cisecurity.org/CIS-Controls-v8-Mobile-Companion-Guide
    - https://learn.cisecurity.org/controls-v8-1-iot

# Narrative
## Program Selection
Today, I'm looking at programs for implementing a cyber security program on my personal network. I want to deepen my security engineering skills, so I thought it would be fun and interesting to build out a personal security program and run it. 

I'm looking at various frameworks and standards in an effort to start at a higher level and establish an overal structure. Once various program elements are identified, specific tools, vendors, and devices will be implemented. 

I've decided on the CIS Controls framework, since it goes a bit deeper into technical requirements detail than the NIST CSF, and is freely available, unlike ISO 27001. Bonus points because the CIS guides are nicely formated and easy to work through.

I looked briefly at the controls details in NIST publications, SP 800-53 and SP 800-171, but decided against going with these for several reasons. I wanted to stick with something approachable, and applicable, and I felt that these standards were targeted too closely to government and government-adjacent audiences that are dealing with national security type concerns. I feel I can maintain greater momentum on this project going with the more adaptable CIS controls. 

## CIS Implementation Groups
One of the first step in CIS is to identify the Implementation Group (IG) we are in. IGs help break down the controls into different levels of complexity and criticality. Higher groups include all the controls of the lower groups, with additional controls being added. There are three IGs and every program starts with IG1. Higher groups become applicable if there are regulations affecting your industry or other obligations, such as with promises made regarding the sensitivity of your data.

Data classification is going to be the main driving factor in our IG selection at this point. Since we've just got one family's copy of personal and financial data, with no regulated data and no promises made about storing other's data, that puts us squarely in IG group 1.

### Implementation Groups and Data Classification 
IG1
- Data is low sensitivity
- Stores unregulated employee and company financial information
- No regulatory or compliance oversight

IG2 
- Stores and processes sensitive client or enterprise information
- Pockets of regulatory or compliance oversight

IG3
- Stores and processes sensitive and confidential data
- Subject to regulatory and compliance oversight

*Taken from: Guide to Implementation Groups (IG) CIS Critical Security Controls v8.1*

From looking at these IG control levels in the past, though, I believe there will be room to pick and choose IG2 group controls that make sense for my personal program, will strengthen our security posture in an appropriate way, and deepen my technical understanding and abilities in these additional areas.

### Other CIS IG Considerations

Another aspect mentioned by CIS for IG selection is technology. While higher IGs are often leveraging commercial products or custom-built solutions, we'll be using primarily open-source tools that are common for IG1 programs.

Threat types are another area mentioned during IG selection. We don't expect to be the target of sophisticated, targeted attacks, or industry-specific threats, more commonly related to IG groups two and three. Non-targeted, drive-by style attacks are our most common threat. Again, IG1 will suit us well here. 

I've not gone into every area of IG selection consideration, just the most obvious and applicable ones. For a deeper drive into Implementation Groups, I recommend visiting the CIS pages with more information on this topic, such as [this one](https://www.cisecurity.org/controls/implementation-groups).

## Onramp to the Controls

I'm going to split devices on my network into two categories:
- "Business" devices
- Guest devices

Business devices are devices that I personally own where I can install monitoring and management software. Guest devices are other devices in my network that I don't own or control, but are still permitted to be there. 

This begins to depart from the language of the CIS documentation, where it only refers to Enterprise devices, and assumes the program has full control over all devices. Initially, CIS doesn't appear to allow for "guest" devices beyond mentioning isolating them. In general, this will be a goal of my approach as well. Ideally, I can have several levels of device segregation. Core network, admin and management devices only. "Business" network with devices that I own and control. Another network for close family and people who I generally trust to maintain their devices in a somewhat reasonable way. Finally, a pure guest network. 

## Policy Development and Maintenance

Another thing that I notice as I dig into the specific controls and safeguards, is that policies seem to go out the window. Whereas in the more introductory Roadmap and Cost guides they are mentioned repeatedly.

I think I would like to take a crack at developing and maintain policies as they relate to my personal network and controls. I have experience with this from my current employer, and it's convenient that CIS provides [policy templates](https://www.cisecurity.org/controls/policy-templates) to pull from for organization and structure. 

I may find over time that it's too much work, or it's taking away from my core project goal of advancing my technical implementation skills; and if so, then I'll stop. I may also find that it's supportive and helpful to have these guiding principles to refer back to. Who knows?

I really like the idea of having an LLM-powered cyber security analyst supporting my program. I could develop a routine for the analyst to take stock of configuration changes within the program (or maybe I just have to report them to this "analyst" program), and then can perform independent, automated checks against the policies docs and either recommend configuration or policy adjustments to keep everything aligned. 

## Conclusion

That's going to be it for today's session. I made a lot of progress in terms of identifying a controls program and framework to structure my technical implementations around. The Center for Internet Security (CIS) Controls 8.1 won out for that analysis. So far the guides are very approachable and readable. You can tell the program has been mature for a considerable time, and they are continuing to refine the program approach, as wells as provide support research, such as cost estimations and breakdowns, tools recommendations, and the Community Defence Model that showcases the overal effectiveness of the program. 

The Next steps are to identify a tool stack and break out a bunch of subtasks. This [Cyber Hygiene guide](
https://learn.cisecurity.org/Essential-Cyber-Hygiene-v8.1) has a bunch of tool recommendations across each control. I'll probably also send the task to Claude to get additional insight into tool recommendations. 

Thanks for reading!

*Andrew Antles*