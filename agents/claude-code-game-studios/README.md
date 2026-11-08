# Claude Code Game Studios — 49 agentes

Biblioteca de **49 subagentes** do projeto [Claude Code Game Studios](https://github.com/Donchitos/Claude-Code-Game-Studios), copiados sem alterações nas definições.

- **Fonte:** `Donchitos/Claude-Code-Game-Studios`
- **Versão:** v1.2.0
- **Commit de origem:** [`05ad7c8a5b8a`](https://github.com/Donchitos/Claude-Code-Game-Studios/commit/05ad7c8a5b8aa2aa86bbd3439ae7cf7295cac418)
- **Definições:** [`definitions/`](./definitions/) — 49 arquivos Markdown.
- **Licença:** MIT — Copyright (c) 2026 Donchitos, [LICENSE](./LICENSE).

## Instalação global no Claude Code

Após clonar este repositório, copie **somente as definições** para a pasta global do Claude Code.

**macOS / Linux / Git Bash**

```bash
git clone https://github.com/lenixeduardo/skills.git
cd skills
mkdir -p ~/.claude/agents
cp agents/claude-code-game-studios/definitions/*.md ~/.claude/agents/
```

**Windows (PowerShell)**

```powershell
git clone https://github.com/lenixeduardo/skills.git
Set-Location skills
New-Item -ItemType Directory -Force -Path "$HOME/.claude/agents" | Out-Null
Copy-Item "agents/claude-code-game-studios/definitions/*.md" "$HOME/.claude/agents/"
```

Para uso em apenas um projeto, substitua o destino por `<projeto>/.claude/agents/`.

**Limitação importante:** a inclusão nesta biblioteca não instala os agentes automaticamente em um computador. Vários agentes fazem referência às skills, documentos e configurações do template CCGS (como `project.yaml`, `.claude/docs/`, `.claude/skills/`). Para os fluxos completos do estúdio, configure também o projeto de origem. O formato dos agentes foi desenvolvido para Claude Code e não garante compatibilidade direta com Codex ou Cursor.

## Atualizações

O [manifest.json](./manifest.json) registra os 49 caminhos originais e os hashes dos blobs, permitindo comparar novas versões antes de substituir customizações locais.
