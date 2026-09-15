# Documentation Index

Quick reference for finding the right documentation for your needs.

## 🚀 Getting Started

**New to the project?** Start here:

1. **[README.md](README.md)** - Quick start and installation
2. **[AGENTS.md](AGENTS.md)** - Project structure and workflow
3. **[.claude/single-venue-report/README.md](.claude/single-venue-report/README.md)** - AI analysis pipeline

## 👤 For Different Audiences

### End Users / Report Consumers

- **[README.md](README.md)** - How to generate reports
- **[README.md#Customization](README.md#customization)** - How to customize report output

### Data Analysts / Report Generators

- **[AGENTS.md](AGENTS.md)** - Full workflow and architecture
- **[AGENTS.md#Report-Generation-Workflow](AGENTS.md#report-generation-workflow)** - Step-by-step generation
- **[AGENTS.md#AI-Analysis-Architecture](AGENTS.md#ai-analysis-architecture)** - How AI analysis works

### Software Developers

- **[README.md#For-Developers](README.md#for-developers)** - Architecture and key files
- **[AGENTS.md#For-Developers](AGENTS.md#for-developers)** - Implementation details and caching
- **[.claude/single-venue-report/README.md#For-Developers](.claude/single-venue-report/README.md#for-developers)** - Pipeline internals

### Prompt Engineers / AI Specialists

- **[.claude/single-venue-report/README.md](.claude/single-venue-report/README.md)** - Pipeline overview
- **[.claude/single-venue-report/synthesis.md](.claude/single-venue-report/synthesis.md)** - Main synthesis prompt
- **[.claude/single-venue-report/venue-overview-skill.md](.claude/single-venue-report/venue-overview-skill.md)** - Overview writing guidance
- **[.claude/single-venue-report/ups-downs-skill.md](.claude/single-venue-report/ups-downs-skill.md)** - Findings selection guidance
- **[.claude/single-venue-report/impact-drivers-skill.md](.claude/single-venue-report/impact-drivers-skill.md)** - Impact explanation guidance
- **[.claude/single-venue-report/recommendations-skill.md](.claude/single-venue-report/recommendations-skill.md)** - Recommendations generation guidance
- **[.claude/single-venue-report/overview-metrics-guidance.md](.claude/single-venue-report/overview-metrics-guidance.md)** - Metrics handling reference

## 📚 Documentation by Topic

### Installation & Setup

- **[README.md#Installation](README.md#installation)** - Install dependencies and Claude CLI
- **[README.md#Requirements](README.md#requirements)** - System requirements

### Usage & Workflows

- **[README.md#Quick-Start](README.md#quick-start)** - One-command report generation
- **[README.md#Usage](README.md#usage)** - Different usage patterns
- **[AGENTS.md#Report-Generation-Workflow](AGENTS.md#report-generation-workflow)** - Manual step-by-step workflow

### Customization

- **[README.md#Customization](README.md#customization)** - How to customize reports
- **[.claude/single-venue-report/README.md#How-to-Use-These-Files](.claude/single-venue-report/README.md#how-to-use-these-files)** - Detailed customization guide

### Architecture & Design

- **[AGENTS.md#AI-Analysis-Architecture](AGENTS.md#ai-analysis-architecture)** - 3-stage pipeline overview
- **[AGENTS.md#Synthesis-Skills](AGENTS.md#synthesis-skills)** - Skill-based synthesis design
- **[.claude/single-venue-report/README.md#How-They-Work-Together](.claude/single-venue-report/README.md#how-they-work-together)** - Detailed pipeline flow

### Performance & Optimization

- **[AGENTS.md#For-Developers](AGENTS.md#for-developers)** - Performance considerations
- **[README.md#For-Developers](README.md#for-developers)** - Caching strategy
- **[.claude/single-venue-report/README.md#Caching-Strategy](.claude/single-venue-report/README.md#caching-strategy)** - Cache implementation

### Debugging & Troubleshooting

- **[README.md#For-Developers](README.md#for-developers)** - Debugging tips
- **[AGENTS.md#For-Developers](AGENTS.md#for-developers)** - Debugging and error handling
- **[.claude/single-venue-report/README.md#For-Developers](.claude/single-venue-report/README.md#for-developers)** - Pipeline debugging

### Development & Extension

- **[AGENTS.md#For-Developers](AGENTS.md#for-developers)** - Adding new skills and modifying the pipeline
- **[README.md#For-Developers](README.md#for-developers)** - Adding new metrics
- **[.claude/single-venue-report/README.md](.claude/single-venue-report/README.md)** - Complete pipeline documentation

## 🔍 Quick Lookup

### "How do I...?"

**...generate a report?**
→ [README.md#Quick-Start](README.md#quick-start)

**...customize the overview narrative?**
→ [README.md#Customization](README.md#customization) → [.claude/single-venue-report/venue-overview-skill.md](.claude/single-venue-report/venue-overview-skill.md)

**...change which ups/downs are selected?**
→ [README.md#Customization](README.md#customization) → [.claude/single-venue-report/ups-downs-skill.md](.claude/single-venue-report/ups-downs-skill.md)

**...modify the recommendations structure?**
→ [README.md#Customization](README.md#customization) → [.claude/single-venue-report/recommendations-skill.md](.claude/single-venue-report/recommendations-skill.md)

**...understand the AI analysis pipeline?**
→ [AGENTS.md#AI-Analysis-Architecture](AGENTS.md#ai-analysis-architecture) → [.claude/single-venue-report/README.md](.claude/single-venue-report/README.md)

**...debug an analysis error?**
→ [README.md#For-Developers](README.md#for-developers) → [AGENTS.md#For-Developers](AGENTS.md#for-developers)

**...add a new metric?**
→ [README.md#For-Developers](README.md#for-developers)

**...optimize performance for large batches?**
→ [AGENTS.md#For-Developers](AGENTS.md#for-developers)

**...understand the caching strategy?**
→ [.claude/single-venue-report/README.md#Caching-Strategy](.claude/single-venue-report/README.md#caching-strategy)

## 📋 File Structure

```
ai-reporting-tool/
├── README.md                          ← Start here
├── AGENTS.md                          ← Detailed workflow
├── DOCUMENTATION_INDEX.md             ← You are here
├── DOCUMENTATION_UPDATES_COMPLETE.md  ← What was updated
│
├── python/
│   ├── generate_all_reports.py        ← Master orchestrator
│   ├── ai_analysis.py                 ← 3-stage pipeline implementation
│   ├── report_content.py              ← Shared analysis logic
│   └── ...
│
├── .claude/single-venue-report/
│   ├── README.md                      ← Pipeline guide
│   ├── metrics_analysis.md            ← Stage 1 prompt
│   ├── comment_analysis.md            ← Stage 2 prompt
│   ├── synthesis.md                   ← Stage 3 prompt
│   ├── venue-overview-skill.md        ← Skill: overview
│   ├── ups-downs-skill.md             ← Skill: findings
│   ├── impact-drivers-skill.md        ← Skill: impact
│   ├── recommendations-skill.md       ← Skill: recommendations
│   └── overview-metrics-guidance.md   ← Reference: metrics
│
├── templates/
│   ├── metrics.json                   ← Metric thresholds
│   ├── venue-1page-browser.html       ← HTML template
│   └── ...
│
└── example-data/
    └── *.csv                          ← Sample survey data
```

## 🔗 Cross-References

### README.md references:
- AGENTS.md (for detailed workflow)
- .claude/single-venue-report/README.md (for pipeline details)
- .claude/single-venue-report/overview-metrics-guidance.md (for metrics handling)

### AGENTS.md references:
- README.md (for quick start)
- .claude/single-venue-report/README.md (for synthesis pipeline)
- .claude/single-venue-report/overview-metrics-guidance.md (for metrics handling)

### .claude/single-venue-report/README.md references:
- README.md (for quick start)
- AGENTS.md (for project workflow)
- All skill files (for detailed guidance)

## 📝 Documentation Updates

See [DOCUMENTATION_UPDATES_COMPLETE.md](DOCUMENTATION_UPDATES_COMPLETE.md) for:
- What was created/enhanced
- Documentation structure
- Key improvements
- What's documented now

---

**Last Updated:** 2026-09-15

**Total Documentation:** 861 lines across 3 main files + 8 skill files in `.claude/single-venue-report/`
