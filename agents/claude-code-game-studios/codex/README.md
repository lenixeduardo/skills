# Claude Code Game Studios — Codex (49 subagentes)

Estas são as **49 definições nativas TOML para Codex** do pacote Claude Code Game Studios v1.2.0. Elas são derivadas integralmente das definições originais em [../definitions/](../definitions/) e usam o prefixo `ccgs-` para evitar colisões com outros agentes.

O Codex usa `~/.codex/agents/*.toml` para agentes pessoais e `.codex/agents/*.toml` para agentes específicos de um projeto. Os campos obrigatórios (`name`, `description`, `developer_instructions`) estão presentes em todos os arquivos. Não foi fixado um modelo: o agente herda o modelo e as permissões da sessão pai.

## Instalação global (Windows, macOS e Linux)

Requisitos: Git e Python 3.11+.

```bash
git clone https://github.com/lenixeduardo/skills.git
cd skills
python3 agents/claude-code-game-studios/codex/manage.py validate
python3 agents/claude-code-game-studios/codex/manage.py install --dry-run
python3 agents/claude-code-game-studios/codex/manage.py install
```

No PowerShell Windows, substitua `python3` por `py -3.11`:

```powershell
git clone https://github.com/lenixeduardo/skills.git
Set-Location skills
py -3.11 agents/claude-code-game-studios/codex/manage.py validate
py -3.11 agents/claude-code-game-studios/codex/manage.py install
```

Para um projeto apenas:

```bash
python3 agents/claude-code-game-studios/codex/manage.py install --destination /caminho/do/projeto/.codex/agents
```

O instalador **não sobrescreve arquivos diferentes automaticamente**. Para atualizar agentes já customizados, `install --force` cria backups em `~/.codex/agents/.backups/` antes de substituir. `generate` reconstrói os TOMLs após atualização das definições originais, enquanto `validate` verifica formato TOML, nomes, conteúdo preservado e hashes Git da origem.

Reinicie o Codex se a lista de agentes não for atualizada. Você pode solicitar: "Delegue a revisão de segurança ao agente `ccgs-security-engineer`" ou "Use `ccgs-gameplay-programmer` para implementar a mecânica".

## Adaptação e limites

Cada TOML contém o guia original completo e um contrato de compatibilidade com Codex, que:

- Traduz semanticamente ferramentas do Claude Code (Read, Write/Edit, Bash, AskUserQuestion, Agent etc.) para as ferramentas realmente disponíveis no Codex.
- Mantém as regras de escopo, revisão, colaboração e aprovação, respeitando os controles da sessão pai.
- Preserva as referências aos documentos e workflows CCGS como recursos *opcionais*, sem alegar que hooks do Claude Code são executados pelo Codex.
- Não impõe modelos `opus`/`sonnet` do Claude ao Codex.

**Atenção:** isto instala papéis especializados como subagentes, não o pipeline completo de 74 skills, hooks e documentos do CCGS. Algumas tarefas avançadas dependem do template original e/ou de uma engine instalada. A validação estática não substitui um teste de execução em um Codex real.

Fonte e licença: [Donchitos/Claude-Code-Game-Studios](https://github.com/Donchitos/Claude-Code-Game-Studios), commit `05ad7c8a5b8aa2aa86bbd3439ae7cf7295cac418` (v1.2.0), MIT — veja [../LICENSE](../LICENSE).
