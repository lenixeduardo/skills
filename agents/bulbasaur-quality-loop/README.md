# Bulbasaur 3D — três agentes Codex

Trio de produção inspirado no framework Claude Code Game Studios: implementador, revisor visual e auditor final independente.

## Instalação global

Copie os três arquivos `.toml` para `~/.codex/agents/`. Os nomes usam prefixo `ccgs-` e não substituem os 49 agentes existentes.

## Processo de QA

1. **Implementador:** corrige forma, material, topology, rig e oito clips; exporta GLB.
2. **Revisor:** inspeciona as vistas 3/4, frontal, lateral, traseira e a composição mobile. Identifica desvios P0/P1.
3. **Auditor:** valida o GLB real, os 8 clips, rig, desempenho, evidências visuais e atribui nota ponderada.
4. Se **nota menor que 8/10** ou falha P0, volta ao implementador e repete. A **meta é 9,5**, somente após evidências reais.

**Rubrica:** fidelidade visual 45%; geometria/topologia 15%; rigging 15%; animações 15%; performance/integração 10%. Sem evidência visual, reportar inconclusivo — nunca dar nota fictícia.

**Referências:** [IdleDex](https://github.com/lenixeduardo/idledex/blob/main/app/escolha-inicial/page.tsx), sprite [Bulbasaur](https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png) e mockups do projeto Pokémon Tamagotchi.
