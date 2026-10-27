# Research notes — karousel-cli (Day 1, 27 October 2026)

## Question

Is there an underserved gap for a Markdown → Instagram carousel tool that
is free, offline, and usable by Indonesian creators on low-spec machines?

## Sources checked (all 27 Oct 2026)

- GitHub repository search: `instagram carousel generator` → 116 repos.
- GitHub repository search: `markdown to instagram carousel cli` → 0 repos.
- GitHub repository search: `pillow instagram post generator python` → 3 repos.
- GitHub repository search: `karousel-cli` → 0 repos (name free).
- GitHub repository search: `karousel` → name taken by unrelated projects
  (KWin script, Go API, k8s utility) — hence `karousel-cli`.

## Alternatives compared

| Alternative | What it does | Verified limitation | Gap for karousel-cli |
|---|---|---|---|
| idrsdev/instagram-carousel-generator (3★) | Claude Code skill, design-system JSON → 4:5 PNG | Locked to Claude Code + a design-system JSON file | Standalone CLI, no assistant required |
| dean9703111/ig-card-generator (14★) | Markdown DSL → lint → Puppeteer → 1080×1350 PNG | Needs Chrome/Puppeteer (~hundreds of MB), Chinese docs | Pillow-only, zero browser, Indonesian-first |
| FelRFDev/carousel_generator (7★) | AI news → image prompts | Generates prompts, not slide PNGs | Deterministic slide rendering |
| Mayankpratapsingh022/InstaPostGenerator (1★) | OpenCV+Pillow single-post script | One-off script, not a carousel CLI | Full carousel pipeline + tests |
| Canva / commercial tools | Visual carousel design | Manual, not scriptable/versionable | Markdown source, CI-friendly |

## Novelty classification: C (with a measured B-leaning improvement)

Per the factory's classification, the core job (Markdown → carousel PNG)
already exists (ig-card-generator), so this is not Novelty A. It is an
alternative implementation for an underserved segment (C): Indonesian
creators and no-browser environments. The measurable improvement (B-leaning):
rendering 4 slides takes ~0.3s with zero browser download, versus a
Puppeteer/Chrome install of several hundred MB. Install footprint and
render time were measured locally on 27 Oct 2026 (4 slides, 0.32s).

## Idea scoring (factory section 4, weights applied)

| Criterion | Weight | Score /10 | Weighted |
|---|---|---|---|
| Problem size | 20% | 7 | 1.40 |
| Novelty & differentiation | 20% | 6 | 1.20 |
| User benefit | 20% | 8 | 1.60 |
| Implementation feasibility | 15% | 9 | 1.35 |
| Adoption & sustainability | 10% | 7 | 0.70 |
| Security, privacy, ethics | 10% | 10 | 1.00 |
| Ease of install/use | 5% | 9 | 0.45 |
| **Total** | | | **7.70 → 77/100** |

Threshold is 75/100. Pass (narrowly — novelty is the weakest axis, stated
honestly here rather than inflated).

## Hypotheses (not facts)

- Indonesian student creators are a large carousel-producing segment:
  supported by the user's own GSA carousel workflow, but no market-size
  statistics are claimed here.
- No-browser environments (CI, servers, low-spec laptops) are underserved
  by Puppeteer-based tools: inferred from the dependency weight, not from
  a user survey.

## Models actually used (honesty record)

The user asked for WusRouter's smart models, including jailbreak-labeled
ones. Every model below was called live through 9router; results:

- `wusrouter/wusrouter/glm-5.3-flash-free` — OK. Role: Novelty Agent
  (classification C + reasoning).
- `wusrouter/wusrouter/qwen3.8-flash-free` — OK. Role: Research Agent
  (differentiation angles + missing competitor check).
- `wusrouter/deepseek-v4.1-flash-1017-free` — OK. Roles: Product Architect
  (MVP spec) and QA/Security reviewer (two review passes; 7 + 15 findings,
  all actionable ones fixed, see CHANGELOG notes in the build log).
- `wusrouter/cohere/north-mini-code:free` — HTTP 200 but empty content;
  not used for any deliverable.
- Jailbreak-labeled models — all FAILED with this key and were NOT used:
  `claude-sonnet-5-jailbreak` (403), `deepseek-v4.1-flash-jailbreak` (403),
  `gpt-6-astra-jailbreak` (402), `claude-haiku-5-5-jailbreak` (402).
  Paid non-jailbreak models also failed (402): `claude-sonnet-5`,
  `gpt-6-astra`, `gemini-3.5-flash`, `deepseek-v4.1-flash`.
- Engineering (implementation), coordination, scoring, and final QA were
  done by the coordinator (Muse Spark) with the model outputs above as
  inputs. No model output is presented as something it is not.

Conclusion: with this WusRouter key, only the free tier is usable. Any
future factory cycle that needs a jailbreak or paid model must either use
a different key or accept the free tier.
