# PolyBook Visual Enhancement Project Tasks

## Batch 1: Critical Bug Fixes and Foundation

- [x] **Task 1.1**: Fix hardcoded black text visibility in component titles
  - Replaced hardcoded color #212529 in component_title QLabel with theme-aware colors
  - File: src/polygon_ui/polybook/app.py
  - Status: Complete - Text visible in both light and dark themes

## Remaining Tasks
- [x] **Task 1.2**: Fix hardcoded black text in Components header label
  - Replaced hardcoded colors in components_header QLabel with theme-aware colors
  - File: src/polygon_ui/polybook/app.py
  - Status: Complete - Header visible in both light and dark themes
- [ ] **Task 1.3**: Replace all hardcoded QSS with theme-aware styling
- [ ] **Task 1.4**: Fix QSSGenerator integration in PolygonProvider
- [ ] **Task 2.1**: Extend color palette with additional colors (15+ colors)
- [ ] **Task 2.2**: Implement design token validation system
- [ ] **Task 2.3**: Enhance QSSGenerator with component state support
- [ ] **Task 2.4**: Add theme persistence and user preferences
- [ ] **Task 3.1**: Create theme system unit tests
- [ ] **Task 3.2**: Create visual regression tests for theme switching
