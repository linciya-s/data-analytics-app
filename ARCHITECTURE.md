# App Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         DATA ANALYTICS APP                              │
└─────────────────────────────────────────────────────────────────────────┘

                              ┌─────────────┐
                              │  app.py     │ (Main Application)
                              └──────┬──────┘
                                     │
                ┌────────────────────┼────────────────────┐
                │                    │                    │
         ┌──────▼──────┐      ┌──────▼──────┐     ┌──────▼──────┐
         │   config.py │      │  styles/    │     │   utils/    │
         │             │      │  main.css   │     │ filehandler │
         │  Settings & │      │             │     │             │
         │  Constants  │      │  Styling &  │     │  Functions  │
         │             │      │  Animations │     │             │
         └─────────────┘      └─────────────┘     └──────┬──────┘
                                                          │
                                                  ┌───────▼────────┐
                                                  │ History System │
                                                  │                │
                                                  │ • load_history │
                                                  │ • save_history │
                                                  │ • add_analysis │
                                                  │ • delete_rec   │
                                                  │ • clear_all    │
                                                  └────────────────┘
```

## Data Flow

```
User Uploads File
      ↓
File Extension Check
      ↓
Read File (CSV/Excel/JSON/PDF)
      ↓
Create DataFrame
      ↓
PERSIST: add_analysis_to_history() ← NEW!
      ↓
Save to ~/.data_analytics_app/history.json
      ↓
Reload history to session state
      ↓
Display in Sidebar + Analysis Tabs + History Tab
```

## Tab Structure

```
┌─────────────────────────────────────────────────────────────────────────┐
│ Navigation Bar (7 Tabs)                                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│ 📊 Data     📈 Visual-   🔍 Data      ⬇️ Down-   ☁️ Word    🤖 Class-  │ 📜 Analysis │
│ Overview   izations    Quality      load     Cloud    ification       │ History     │
│                                                                    │
│ (Existing Tabs)                                      (NEW TAB) ──→ │
│                                                                    │
└────────────────────────────────────────────────────────────────────────┘
```

## History Tab Structure

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         📜 Analysis History                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Statistics Dashboard                                                   │
│  ┌─────────────┬──────────┬────────────┬──────────────┐               │
│  │ 📊 Total:   │ 📈 Rows: │ 📋 Cols:   │ 💾 Size:     │               │
│  │ 3           │ 550      │ 19         │ 6.5 MB       │               │
│  └─────────────┴──────────┴────────────┴──────────────┘               │
│                                                                          │
│  View Mode Selection                                                    │
│  ┌──────────────────────────────────────────────────────────┐          │
│  │ [📱 Card View] [📊 List View]                           │          │
│  └──────────────────────────────────────────────────────────┘          │
│                                                                          │
│  Content (Dynamic based on view mode)                                  │
│  ┌──────────────────────────────────────────────────────────┐          │
│  │ Card View:                                               │          │
│  │ ┌────────────┐ ┌────────────┐ ┌────────────┐            │          │
│  │ │  File 1    │ │  File 2    │ │  File 3    │            │          │
│  │ │  Metadata  │ │  Metadata  │ │  Metadata  │            │          │
│  │ │ Actions    │ │ Actions    │ │ Actions    │            │          │
│  │ └────────────┘ └────────────┘ └────────────┘            │          │
│  │                                                           │          │
│  │ OR List View:                                            │          │
│  │ File      │ Date    │ Rows │ Columns │ Size │ Numeric   │          │
│  │ ───────────────────────────────────────────────────────  │          │
│  │ File1.csv │1/15/24  │ 500  │ 8       │ 2.34 │ 5         │          │
│  │ File2.csv │1/14/24  │ 200  │ 6       │ 1.23 │ 3         │          │
│  │ File3.csv │1/13/24  │ 50   │ 5       │ 0.45 │ 2         │          │
│  └──────────────────────────────────────────────────────────┘          │
│                                                                          │
│  Bulk Actions                                                           │
│  ┌──────────────────────────────────────────────────────────┐          │
│  │ [📥 Export as JSON] [🧹 Clear All History]              │          │
│  └──────────────────────────────────────────────────────────┘          │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## Card View Detail

```
┌─────────────────────────────────┐
│ 📄 sales_data.csv              │ ← File Badge
├─────────────────────────────────┤
│ January 15, 2024 • 14:30        │ ← Timestamp
├─────────────────────────────────┤
│ Rows: 5,000      Numeric: 8     │ ── Statistics
│ Columns: 15      Categorical: 7 │   Section
│ Size: 2.45 MB                   │
├─────────────────────────────────┤
│ [📂 View]  [🗑️ Delete]        │ ← Action Buttons
└─────────────────────────────────┘
```

## Sidebar Structure

```
┌─────────────────────────┐
│    ⚙️ Settings          │
├─────────────────────────┤
│                         │
│ 📜 Analysis History     │
│ Total Analyses: 3       │
│                         │
│ [View All] [Clear All]  │
│                         │
│ Recently Analyzed:      │
│ 📄 file1.csv            │
│    100 rows • 5 cols    │
│ 📄 file2.csv            │
│    200 rows • 8 cols    │
│ 📄 file3.csv            │
│    150 rows • 6 cols    │
│                         │
└─────────────────────────┘
```

## File Storage Structure

```
User Home Directory (~)
│
└── .data_analytics_app/
    │
    └── history.json (Auto-created)
        │
        └── [
              {
                "id": 1705333200000,
                "filename": "sales_data.csv",
                "file_type": "csv",
                "timestamp": "2024-01-15T14:30:00",
                "rows": 5000,
                "columns": 15,
                "size_mb": 2.45,
                "numeric_cols": 8,
                "categorical_cols": 7
              },
              {...},
              ... (up to 50 records)
            ]
```

## Animation Timeline

```
Page Load
   ↓
Header appears ← Smooth background
   ↓
Content loads ← Fade-in animation
   ↓
Cards render ← Sequential fade-in with staggered timing
   ↓
User interaction
   ↓
Hover card ← Lift animation (translateY effect)
   ↓
Click button ← State change with color transition
   ↓
Page updates ← Smooth reflow animation
```

## CSS Variable Structure

```
:root {
  /* Primary Colors */
  --primary-gradient: linear-gradient(135deg, #4F46E5, #7C3AED)
  --primary-dark: #4F46E5
  --primary-light: #6366F1
  
  /* Status Colors */
  --success-color: #10B981
  --danger-color: #EF4444
  --warning-color: #F59E0B
  --info-color: #3B82F6
  
  /* Spacing System */
  --spacing-xs: 0.25rem
  --spacing-sm: 0.5rem
  --spacing-md: 1rem      ← Base unit
  --spacing-lg: 1.5rem
  --spacing-xl: 2rem
  --spacing-2xl: 3rem
  
  /* Shadows Hierarchy */
  --shadow-sm: 0 1px 2px
  --shadow-md: 0 4px 6px     ← Default for cards
  --shadow-lg: 0 10px 15px   ← Hover state
  --shadow-xl: 0 20px 25px   ← Large components
  
  /* Transitions */
  --transition-fast: 150ms
  --transition-base: 250ms   ← Standard animations
}
```

## State Management Flow

```
Session State
│
├── analysis_history
│   └── [List of history records from persistent storage]
│
├── current_file
│   └── Name of currently loaded file
│
└── selected_history_id
    └── ID of selected history record
```

## Component Hierarchy

```
App
├── Header
│   └── Title + Description
├── Sidebar
│   ├── Settings Section
│   └── History Section
│       ├── Statistics
│       ├── Action Buttons
│       └── Recent Files List
├── Main Content Area
│   └── Tabs
│       ├── Tab 1: Data Overview
│       ├── Tab 2: Visualizations
│       ├── Tab 3: Data Quality
│       ├── Tab 4: Download
│       ├── Tab 5: Word Cloud
│       ├── Tab 6: Classification
│       └── Tab 7: Analysis History ← NEW
│           ├── Statistics Dashboard
│           ├── View Mode Toggle
│           ├── Content Area
│           │   ├── Card View
│           │   └── List View
│           └── Bulk Actions
└── Footer (Implicit)
```

## Function Call Chain for File Upload

```
User Uploads File
      ↓
file_uploader() detects upload
      ↓
File type determined
      ↓
read_csv_file() / read_excel_file() / read_json_file() / read_pdf_file()
      ↓
DataFrame created
      ↓
get_column_types() analyzes columns
      ↓
add_analysis_to_history(filename, df, file_type) ← KEY FUNCTION
      ├─ Creates metadata record
      ├─ Deduplicates if needed
      ├─ Generates unique ID
      ├─ Calls save_history()
      │   └─ Writes to ~/.data_analytics_app/history.json
      └─ Returns record
      ↓
load_history() reloads into session
      ↓
UI displays in tabs and sidebar
```

## CSS Animation Pipeline

```
Load Event
   ↓
fadeInUp animation triggers
   ↓
.history-card { animation: fadeInUp 0.5s ease-out forwards }
   ↓
Card elements render in sequence
   ↓
Hover Event
   ↓
transform: translateY(-6px) applied
   ↓
box-shadow updated
   ↓
border-color transitions smoothly
   ↓
All transitions use var(--transition-base): 250ms ease-in-out
```

---

This architecture ensures:
✅ Clean separation of concerns
✅ Maintainable code structure
✅ Responsive, performant UI
✅ Persistent data management
✅ Professional user experience
