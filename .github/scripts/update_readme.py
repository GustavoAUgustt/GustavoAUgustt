#!/usr/bin/env python3
import requests
import os
import re

GITHUB_USERNAME = "GustavoAUgustt"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_user_repos():
    repos = []
    page = 1
    
    while True:
        url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"
        params = {
            "sort": "updated",
            "direction": "desc",
            "per_page": 100,
            "page": page,
            "type": "owner"
        }
        
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    
    return repos

def format_repos(repos):
    repos = [r for r in repos if r["name"] != GITHUB_USERNAME]
    repos.sort(key=lambda x: x["updated_at"], reverse=True)
    top_repos = repos[:10]
    
    markdown = "## 📚 Meus Repositórios\n\n"
    
    for repo in top_repos:
        name = repo["name"]
        description = repo.get("description") or "Sem descrição"
        url = repo["html_url"]
        stars = repo["stargazers_count"]
        language = repo.get("language") or "Sem linguagem"
        
        markdown += f"### [{name}]({url})\n"
        markdown += f"**Descrição:** {description}\n"
        markdown += f"**Linguagem:** {language} | ⭐ {stars}\n\n"
    
    return markdown

def update_readme(repos_markdown):
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()
    
    start_marker = "<!-- REPOS:START -->"
    end_marker = "<!-- REPOS:END -->"
    
    if start_marker not in content:
        pacman_marker = '<img src="https://raw.githubusercontent.com/GustavoAUgustt/GustavoAUgustt/main/pacman.svg"'
        repos_section = f"\n{start_marker}\n{repos_markdown}{end_marker}\n\n"
        
        if pacman_marker in content:
            content = content.replace(pacman_marker, repos_section + pacman_marker)
        else:
            content += f"\n{repos_section}"
    else:
        pattern = f"{re.escape(start_marker)}.*?{re.escape(end_marker)}"
        content = re.sub(pattern, f"{start_marker}\n{repos_markdown}{end_marker}", content, flags=re.DOTALL)
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

def main():
    print("🔄 Buscando repositórios...")
    repos = get_user_repos()
    print(f"✅ Encontrados {len(repos)} repositórios")
    
    print("📝 Formatando markdown...")
    repos_markdown = format_repos(repos)
    
    print("✏️  Atualizando README.md...")
    update_readme(repos_markdown)
    
    print("✨ Pronto!")

if __name__ == "__main__":
    main()
