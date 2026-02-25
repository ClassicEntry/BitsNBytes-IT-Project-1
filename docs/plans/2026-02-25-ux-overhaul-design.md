# PyExploratory UX Overhaul — Design Document

**Date:** 2026-02-25
**Approach:** Exploratory-Style Step Panel (Full Redesign)
**Target audience:** Data analysts
**Inspiration:** Exploratory.io, Linear, Vercel Dashboard, Arc browser
**Constraints:** Stay in Dash, keep all 18 cleaning ops + 14 charts + 5 ML tasks

---

## 1. Layout Architecture

Replace the current sidebar + tabs layout with a **3-zone workspace**.

```
┌──────────┬──────────────────────────────┬─────────────────┐
│          │         CONTEXT BAR          │                 │
│          │  [Dataset: test_data.csv]    │                 │
│          │  [1,200 rows × 14 cols]      │                 │
│  SIDE-   ├──────────────────────────────┤   STEP PANEL    │
│  BAR     │                              │                 │
│  (~200px)│                              │  ┌───────────┐  │
│          │      MAIN WORKSPACE          │  │ 1. Upload  │  │
│  nav     │      (fluid width)           │  │ 2. Drop NA │  │
│  upload  │                              │  │ 3. Rename  │  │
│  export  │   Data table is the base     │  │ 4. Chart   │  │
│  import  │   layer. Charts, ML, and     │  │ 5. KMeans  │  │
│          │   summary render as overlays │  └───────────┘  │
│          │   or inline expansions.      │                 │
│          │                              │  [+ Add Step]   │
└──────────┴──────────────────────────────┴─────────────────┘
```

- **Sidebar** (left, ~200px): Refined — better icons, upload, export/import
- **Main workspace** (center, fluid): Data table as base layer. Charts/ML/summary as overlay panels or inline expansions
- **Step panel** (right, ~280px, collapsible): Ordered list of all operations. Click any step to rewind. Powered by extended `action_log.py` + `history.py`
- **Context bar** (top of main area): Dataset name, row/col count, memory, settings gear icon

The 4-tab system (Summary, Table, Charts, ML) is **removed**. All operations are accessed via the step panel's "+ Add Step" button.

---

## 2. Step Panel & Workflow

### Step Types

| Icon | Type | Color Accent | What it records |
|------|------|-------------|-----------------|
| ⬆ | Upload | #4a9eff (blue) | File name, row/col count, timestamp |
| 🧹 | Clean | #00c46a (green) | Operation name, column, parameters |
| 📊 | Chart | #ff9f43 (orange) | Chart type, axes, configuration |
| 🤖 | ML | #a855f7 (purple) | Task, parameters, key metric |

### Step Card Anatomy

```
┌─────────────────────────────────┐
│ 🧹  Drop NA on column "Age"    │  ← title
│     Removed 12 rows            │  ← result summary
│     2m ago                      │  ← relative timestamp
│     [↕] [⊘] [✕]               │  ← reorder / disable / delete
└─────────────────────────────────┘
```

### Interactions

- **Click a step** → main workspace rewinds to show data at that point
- **"+ Add Step" button** → dropdown with categories: Clean, Visualize, ML, Summary Stats
- **"Clean"** → compact inline form in the step panel (operation, column, params)
- **"Visualize"** → chart builder slides in from the right as an overlay panel
- **"ML"** → ML task config slides in from the right as an overlay panel
- **"Summary Stats"** → toggles expandable header above the table with KPI tiles
- **Disable/enable** a step without deleting (toggle effect)
- **Delete** a step with confirmation

### Data Flow

Extends existing `action_log.py` to also track chart and ML steps, with a `disabled` flag per step. `history.py` snapshots support click-to-rewind.

---

## 3. Visual Design System

### Color Palette

```
Background layers:
  bg-deep:      #111113    (sidebar, step panel)
  bg-surface:   #1a1a1d    (main workspace — blue-tinted dark)
  bg-card:      #222226    (cards, step items)
  bg-hover:     #2a2a30    (hover states)
  bg-active:    #333338    (selected/active items)

Accent:
  primary:      #00c46a    (buttons, active links, success)
  primary-dim:  #00c46a33  (subtle backgrounds, selected highlights)

Text:
  text-primary:   #f0f0f0
  text-secondary: #a0a0a0
  text-muted:     #666666

Step type accents:
  upload:  #4a9eff  (blue)
  clean:   #00c46a  (green)
  chart:   #ff9f43  (orange)
  ml:      #a855f7  (purple)

Borders: #3a3a3b (subtle, 1px)
```

### Visual Effects

```
Glassmorphism on cards:
  background:      rgba(34, 34, 38, 0.8)
  backdrop-filter:  blur(12px)
  border:          1px solid rgba(255, 255, 255, 0.06)

Gradients:
  sidebar:      linear-gradient(180deg, #111113, #0d0d10)
  context-bar:  linear-gradient(90deg, #1a1a1d, #1e1e22)
  primary-btn:  linear-gradient(135deg, #00c46a, #00a85a) + glow shadow

Glow effects:
  active step:    box-shadow: 0 0 20px rgba(0, 196, 106, 0.15)
  focused input:  box-shadow: 0 0 0 2px rgba(0, 196, 106, 0.3)
  primary btn:    box-shadow: 0 4px 16px rgba(0, 196, 106, 0.25)

Animations:
  step-enter:   slide-in-right + fade (200ms ease-out)
  panel-slide:  translateX with spring easing (250ms)
  chart-render: fade-in + scale-up (300ms)
  hover-lift:   translateY(-1px) + shadow increase (150ms)
  toast-enter:  slide-down + fade from top-right (200ms)
```

### Typography

- **Headings / Body:** Inter (13-14px body, scale up for headings)
- **Data / Code:** JetBrains Mono (monospace)
- **Spacing:** 8px grid system. Padding: 12px compact / 16px standard / 24px spacious

### Components

- **Buttons:** 6px radius, primary green gradient fill, ghost/outline for secondary
- **Cards:** 8px radius, glassmorphic, no shadow
- **Table:** Row striping, sticky header with shadow, column type badges (# numeric, A text, 📅 datetime)
- **Inputs:** Dark fields, subtle border, green focus ring with glow
- **Toasts:** Top-right, color-coded (green/red/blue), auto-dismiss 4s

---

## 4. Navigation & Interaction Patterns

### Primary Flow

```
Upload data → see table + context bar → add steps via "+" → view results inline
```

### "+ Add Step" Menu

```
┌──────────────────────────┐
│  + Add Step              │
├──────────────────────────┤
│  🧹  Clean / Transform   │  → 18 ops
│  📊  Visualize            │  → chart builder panel
│  🤖  Machine Learning     │  → ML task panel
│  📋  Summary Stats        │  → toggle summary overlay
└──────────────────────────┘
```

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+K` | Quick search / jump to operation |
| `Ctrl+Z` | Undo last step |
| `Ctrl+Shift+Z` | Redo |
| `Ctrl+S` | Save changes |
| `Ctrl+E` | Export script |
| `]` | Toggle step panel |

### Context Bar

```
┌─────────────────────────────────────────────────────────────────┐
│  📄 test_data.csv   |  1,200 rows × 14 cols  |  3.2 MB  |  ⚙  │
└─────────────────────────────────────────────────────────────────┘
```

### Slide-in Panels

Chart builder and ML config slide in from the right, overlaying the step panel. Results render in the main workspace. Close panel to return to step view.

### Summary Stats

No longer a tab. Clicking "Summary Stats" from + menu toggles an expandable header section above the table with KPI tiles. Column header click shows a stat popover.

---

## 5. Error Handling, Feedback & Loading States

### Loading States

- **Initial data load:** Skeleton loader mimicking table structure (pulsing grey rows)
- **Chart generation:** Animated placeholder with chart-type icon pulsing
- **ML training:** Progress bar with phase text ("Training model...", "Computing metrics...")
- **Step execution:** Spinning indicator in step card until complete

### Success Feedback

- **Toast (green):** Descriptive message ("Dropped 12 NA rows from Age column"), 4s auto-dismiss
- **Step card:** Brief pulse in accent color on creation

### Error Feedback

- **Toast (red):** Error message + suggestion ("Column 'age' not found. Did you mean 'Age'?")
- **Inline validation:** Real-time warnings on invalid inputs before clicking Apply
- **Step card error state:** Red left-border, error icon, expandable detail

### Destructive Operation Confirmation

- Upgraded modal: dark glassmorphic overlay, clear description, affected row count
- Step panel: ⚠ warning icon on destructive steps

### Empty States

- No data: full-workspace drag-and-drop zone + sample dataset buttons
- No steps: "Start by uploading a dataset" with illustration
- No chart: "Configure your chart above and click Generate"

---

## 6. Testing Strategy

### Unchanged

All `core/` tests remain untouched: `test_cleaning_ops.py`, `test_ml*.py`, `test_validators.py`, `test_history.py`, `test_file_parser.py`.

### New/Updated Tests

- Step panel state management (creation, ordering, disable/enable, rewind)
- Extended action_log (chart/ML step recording, disabled flag)
- Layout rendering smoke tests

### Visual QA

Use Playwright (MCP tools) to visually verify the redesign during implementation — layout renders, step panel works, interactions behave correctly.

---

## 7. Architecture Impact

### Files Modified

| File | Change |
|------|--------|
| `app.py` | New 3-zone layout, remove tab dispatch |
| `config.py` | New color/style constants, font imports |
| `pages/data_analysis.py` | Complete rewrite — workspace + step panel + context bar |
| `tabs/*.py` | Repurposed as panel content builders (no longer tabs) |
| `callbacks/*.py` | Updated to work with step panel workflow |
| `core/action_log.py` | Extended for chart/ML steps, disabled flag |
| `components/styles.py` | New design system styles |
| `components/tables.py` | Updated table styling |

### New Files

| File | Purpose |
|------|---------|
| `components/step_panel.py` | Step panel layout builder |
| `components/context_bar.py` | Context bar layout builder |
| `components/slide_panel.py` | Slide-in panel wrapper |
| `callbacks/step_panel.py` | Step panel interaction callbacks |
| `assets/custom.css` | Animations, glassmorphism, glow effects |
| `assets/fonts/` | Inter + JetBrains Mono (or Google Fonts CDN) |

### Patterns Preserved

- `core/` stays pure (no Dash imports)
- Strategy pattern in `cleaning_ops.py` unchanged
- NamedTuple results from ML modules unchanged
- Snapshot-based undo/redo in `history.py` reused for step rewind
