function buildFooter() {
  const footer = document.getElementById("footer");
  const currentYear = new Date().getFullYear();

  // Copyright paragraph with dynamic year
  const copyright = document.createElement("p");
  copyright.setAttribute("id", "copyright");
  copyright.innerHTML = `&copy; ${currentYear} AndrewAntles.net`;

  // Social links nav
  const socialNav = document.createElement("nav");
  socialNav.setAttribute("class", "social-links");
  socialNav.setAttribute("aria-label", "Social media links");

  const linkedInLink = document.createElement("a");
  linkedInLink.setAttribute("href", "https://www.linkedin.com/in/andrew-antles");
  linkedInLink.setAttribute("target", "_blank");
  linkedInLink.setAttribute("rel", "noopener noreferrer");
  linkedInLink.setAttribute("aria-label", "LinkedIn profile");

  const linkedInImg = document.createElement("img");
  linkedInImg.setAttribute("src", "../public/img/company-logos/linkedin/In-Blue-128.png");
  linkedInImg.setAttribute("alt", "LinkedIn Logo");
  linkedInLink.appendChild(linkedInImg);

  const githubLink = document.createElement("a");
  githubLink.setAttribute("href", "https://github.com/andrewantles");
  githubLink.setAttribute("target", "_blank");
  githubLink.setAttribute("rel", "noopener noreferrer");
  githubLink.setAttribute("aria-label", "GitHub profile");

  const githubImg = document.createElement("img");
  githubImg.setAttribute("src", "../public/img/company-logos/github/github-mark.png");
  githubImg.setAttribute("alt", "GitHub Logo");
  githubLink.appendChild(githubImg);

  socialNav.appendChild(linkedInLink);
  socialNav.appendChild(githubLink);

  footer.appendChild(copyright);
  footer.appendChild(socialNav);
}

buildFooter();
