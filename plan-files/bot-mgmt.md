# Bot mitigation strategies for personal websites in 2025

**Website owners can now block AI training crawlers while preserving search engine visibility—but robots.txt alone won't protect you.** The key insight: Google-Extended, ClaudeBot, and GPTBot can all be blocked via robots.txt without affecting your SEO, because major search engines use separate crawler tokens for AI training versus indexing. However, compliance is voluntary, and documented violations from companies like Perplexity demonstrate why layered technical enforcement through services like Cloudflare has become essential. For personal portfolio sites, the optimal strategy combines a comprehensive robots.txt with Cloudflare's free AI blocking features, requiring about 15 minutes of setup for robust protection.

## Blocking AI crawlers while allowing search engines

The fundamental challenge is distinguishing between crawlers that index your site for search results versus those harvesting content for AI model training. Fortunately, major companies have created separate user-agent tokens for these purposes, making selective blocking possible.

**Google's clean separation** is the most elegant solution. Google-Extended is a control token that governs AI training (Gemini, Vertex AI) but doesn't affect Googlebot's search indexing. Blocking Google-Extended has zero impact on your search rankings—Google has explicitly confirmed this. The same pattern applies to Apple's Applebot-Extended, which controls Apple Intelligence training separately from Siri and Safari features.

OpenAI operates three distinct crawlers: **GPTBot** (training), **OAI-SearchBot** (ChatGPT search features), and **ChatGPT-User** (user-initiated browsing). A critical December 2025 change removed robots.txt compliance for ChatGPT-User, meaning OpenAI now treats user-requested page fetches as exempt from robots.txt directives. Anthropic similarly separates ClaudeBot (training) from Claude-User (user queries), though both officially respect robots.txt.

Here's a production-ready robots.txt configuration that blocks major AI training crawlers while allowing search engines:

```
# AI Training Crawlers - Block
User-agent: GPTBot
Disallow: /

User-agent: ClaudeBot
Disallow: /

User-agent: anthropic-ai
Disallow: /

User-agent: Google-Extended
Disallow: /

User-agent: CCBot
Disallow: /

User-agent: Meta-ExternalAgent
Disallow: /

User-agent: PerplexityBot
Disallow: /

User-agent: Bytespider
Disallow: /

User-agent: cohere-ai
Disallow: /

User-agent: Amazonbot
Disallow: /

User-agent: Applebot-Extended
Disallow: /

# Search Engines - Allow
User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: DuckDuckBot
Allow: /
```

The fundamental limitation: robots.txt is purely voluntary. A 2025 court ruling in Ziff Davis v. OpenAI characterized robots.txt as "more akin to a sign than a barrier," lacking legal enforceability under DMCA. TollBit's Q1 2025 report found bots ignoring robots.txt directives increased from **3.3% to 12.9%** quarterly, representing 26 million scrapes that bypassed stated directives.

## Cloudflare's AI blocking toolkit

Cloudflare has emerged as the most practical defense layer for personal websites, offering AI-specific blocking features across all plan tiers—including free accounts. The core capabilities launched between July 2024 and July 2025 have fundamentally changed how site owners can enforce their preferences.

**Block AI Bots** is a one-click toggle available on free plans (Security → Bots → Configure Bot Fight Mode). When enabled, it blocks GPTBot, ClaudeBot, CCBot, Bytespider, Meta-ExternalAgent, and other known AI crawlers at the network level—actual enforcement rather than polite requests. Over **1 million customers** have enabled this feature since its July 2024 launch. As of July 2025, Cloudflare enabled this blocking by default for all new domains.

**AI Labyrinth** (launched March 2025) acts as an active defense mechanism. When enabled, Cloudflare embeds invisible links with nofollow tags that human visitors cannot see. Unauthorized crawlers following these links enter a maze of AI-generated pages containing factual but irrelevant content, wasting their resources while fingerprinting their behavior for Cloudflare's detection systems. This doesn't affect SEO since proper nofollow tags are used.

**AI Crawl Control** (formerly AI Audit) provides visibility into which AI services access your content, their request frequency, and which pages they target most. The free tier includes monitoring; a private beta offers pay-per-crawl monetization with 402 Payment Required responses for sites wanting to license rather than block.

For more granular control, custom WAF rules can target specific behaviors:

```
# Block AI Crawler category (Pro+ plans)
Expression: (cf.verified_bot_category in {"AI Crawler"})
Action: Block

# User-agent based blocking (all plans)
Expression: (lower(http.user_agent) contains "gptbot") or 
            (lower(http.user_agent) contains "claudebot") or
            (lower(http.user_agent) contains "ccbot")
Action: Block
```

Super Bot Fight Mode (Pro tier, $20/month) adds the ability to challenge or block "definitely automated" traffic with configurable responses, skip rules for legitimate webhooks, and bot analytics dashboards. The Business tier extends this to "likely automated" traffic using machine learning detection.

## The compliance reality gap

Do AI companies actually respect robots.txt? The answer is nuanced: major companies claim compliance, but documented violations reveal significant gaps between policy and practice.

**Perplexity AI has the most extensively documented violations.** A Cloudflare investigation in August 2025 confirmed the company uses "stealth crawlers" with undeclared IP addresses, spoofed user-agent strings impersonating Chrome on macOS, and rotating ASN numbers to evade detection. Wired's June 2024 investigation identified specific AWS IP addresses scraping Condé Nast properties despite explicit blocks. Perplexity's CEO responded that robots.txt is "not a legal framework"—technically correct, though ethically questionable.

Anthropic's ClaudeBot generated controversy when iFixit CEO Kyle Wiens reported approximately **1 million requests in 24 hours**, though the bot reportedly stopped after robots.txt was updated. The sheer volume—even if compliant—illustrates why rate limiting matters.

Cloudflare's data reveals the crawl-to-referral imbalance: Google sends roughly 14 crawls per human referral it generates, while OpenAI's GPTBot averages **1,700:1** and Anthropic's ClaudeBot reaches **73,000:1**. This asymmetry explains why publishers increasingly view AI crawling as extraction without reciprocal value.

Adoption of AI crawler blocking has accelerated dramatically. Among the top 1,000 websites, GPTBot blocking increased from **5% to 35.7%** between August 2023 and August 2024. Major publishers including The New York Times, The Guardian, CNN, Reuters, and Bloomberg now block multiple AI crawlers.

## Threats beyond AI training

AI crawlers represent just one category of automated traffic targeting websites. Cloudflare's 2024 Application Security Report found approximately one-third of all web traffic is automated, with **93% of bot traffic potentially malicious** (not from verified legitimate sources).

**Vulnerability scanners** constantly probe for exposed sensitive files: `.env` configurations, `.git` repositories, `wp-config.php` backups, and common CMS admin paths. These requests appear in virtually every server log—automated tools testing thousands of sites for exploitable misconfigurations. Blocking access to these paths via .htaccess or server configuration is essential:

```apache
<FilesMatch "\.(env|git|sql|bak|backup)$">
    Order allow,deny
    Deny from all
</FilesMatch>
```

**Email harvesting bots** scan pages for text matching email patterns, compiling addresses for spam campaigns. Personal portfolio sites with visible contact information are prime targets. Mitigation involves using contact forms instead of displayed addresses, or obfuscating email display through JavaScript rendering.

**Form spam bots** automatically submit content through contact forms, guestbooks, and comment sections. The honeypot technique—adding hidden form fields that only bots fill—remains effective alongside CAPTCHA challenges. Services like Akismet provide additional spam filtering layers.

**Content scraping bots** extract text, images, and creative work for republication elsewhere. Beyond copyright concerns, duplicate content appearing on scraper sites can damage search rankings. Rate limiting and bot management services provide the primary defenses.

**Layer 7 DDoS attacks** use seemingly legitimate HTTP requests to overwhelm application resources. Unlike network-level attacks, these mimic real traffic patterns, making detection difficult. CDN/WAF services with DDoS protection are the standard defense for personal sites lacking dedicated infrastructure.

| Threat Type | Risk Level | Primary Mitigation |
|-------------|------------|-------------------|
| Vulnerability scanning | High | Block sensitive paths, WAF rules |
| Email harvesting | High | Contact forms, obfuscation |
| Form spam | Very High | CAPTCHA, honeypot fields |
| Content scraping | Medium | Rate limiting, CDN |
| Layer 7 DDoS | Medium | CDN with DDoS protection |

## Trade-offs and practical considerations

Aggressive bot blocking carries real costs beyond implementation effort. A Wharton/Rutgers study from December 2025 found publishers blocking AI crawlers via robots.txt experienced a **23% total traffic decline** and **14% human traffic decline**—counterintuitive findings suggesting potential indirect effects on discoverability.

The maintenance burden increases with comprehensiveness. Over 60 documented AI crawler user-agents exist, with new ones appearing regularly. Anthropic's merger of "anthropic-ai" and "Claude-Web" into "ClaudeBot" temporarily gave the new identifier unrestricted access to sites that hadn't updated their configurations. Services like Dark Visitors or Cloudflare's managed robots.txt can automate these updates.

Blocking certain crawlers affects specific functionality: blocking facebookexternalhit breaks Facebook/Instagram link previews; blocking OAI-SearchBot removes your site from ChatGPT search results. Personal sites must weigh these trade-offs against protection preferences.

**For personal portfolio websites, a tiered approach balances protection with effort:**

**Tier 1 (5 minutes, free):** Add the comprehensive robots.txt configuration above. Verify with Google's robots.txt tester.

**Tier 2 (15 minutes, free):** Add Cloudflare with the Block AI Bots toggle enabled. This provides network-level enforcement rather than relying on crawler cooperation.

**Tier 3 (30+ minutes, ongoing):** Implement server-level user-agent blocking, enable AI Labyrinth, monitor AI Crawl Control for access patterns, and consider auto-updating services for comprehensive crawler list maintenance.

## Emerging standards and future outlook

Several initiatives attempt to create clearer frameworks beyond robots.txt. **TDMRep** (Text and Data Mining Reservation Protocol) is a W3C Community Group specification designed for EU Copyright Directive compliance, using a `tdmrep.json` file in the `.well-known` directory. Adoption remains limited—only 45 hosts with tdmrep.json were found in a January 2024 survey—though 143 of the top 250 French websites have implemented it.

**llms.txt** proposes a different approach: rather than blocking, it guides AI systems to curated content during inference. Think of it as a recommended reading list for AI assistants. Cloudflare, Anthropic, and documentation platforms like Mintlify have adopted it, though no major AI crawler actively requests llms.txt during operation.

The legal landscape offers limited protection currently. While 51+ copyright lawsuits against AI companies are active (including NYT v. OpenAI and multiple actions against Perplexity), court rulings have been mixed. Some fair use determinations have favored AI training; others—like OpenAI's German GEMA case—found copyright violations. Anthropic reached a **$1.5 billion settlement** in August 2025 for author class actions, the first major AI training settlement.

Crucially, all emerging standards share robots.txt's fundamental limitation: voluntary compliance. Technical enforcement through CDN/WAF services remains necessary for actual protection rather than stated preferences.

## Conclusion

The 2025 bot mitigation landscape offers personal website owners genuine tools for controlling AI crawler access without sacrificing search visibility. The separation between search indexing and AI training crawlers—particularly Google-Extended versus Googlebot—provides a clean technical solution. Cloudflare's free AI blocking features democratize enforcement that previously required enterprise infrastructure.

However, the compliance gap between stated policies and actual behavior means robots.txt serves as a preference signal rather than a barrier. Perplexity's documented violations demonstrate that some companies treat these signals as optional. The practical recommendation for personal portfolio sites is layered defense: comprehensive robots.txt for compliant crawlers, Cloudflare's Block AI Bots toggle for enforcement, and acceptance that determined actors may bypass both. The 15-minute investment in Cloudflare setup provides the highest protection-to-effort ratio currently available.