---
name: g03-flutter-apply-material3-guidelines
description: 'Aplica las guías de Material Design 3 en apps Flutter: theming, esquemas de color dinámicos y uso correcto de componentes. Usar al diseñar o refactorizar pantallas y componentes de UI.'
metadata:
  tipo: skill
  area:
  - mobile
  - diseno
  fase:
  - desarrollo
  tecnologias:
  - flutter
  - dart
  herramientas:
  - claude-code
  - codex
  requiere: []
  grupo: '03'
  autor:
    nombre: Lautaro German Reinoso
    github: LautiGR116
  colaboradores:
  - nombre: Ignacio Nicolás Correa Rodríguez
    github: NachoCor2007
  responsables:
  - LautiGR116
  madurez: usado-en-proyecto
  relacionados: []
---
# Skill: Apply Google Material Design 3 (M3) Guidelines in Flutter

## 1. When to Use This Skill
Apply this skill whenever the user asks to:
- Design or style a screen, dialog, form, or UI component in Flutter.
- Apply or refactor the app theme (`AppTheme` / `ThemeData`).
- Work with the project's established color scheme (`ColorScheme` / `AppColors`).
- Ensure UI components follow Google's Material Design 3 accessibility, elevation, and layout standards.

---

## 2. Fundamental Material 3 Rules in Flutter

### A. Theming & Color System
- **Mandatory M3 Flag:** Always ensure `useMaterial3: true` is set in `ThemeData`.
- **Established Project Color Scheme:** The project uses an established brand `ColorScheme` defined in the app theme (`AppTheme` / `AppColors`). Always respect and consume this pre-configured `ColorScheme` rather than generating ad-hoc schemes or using deprecated `primarySwatch`.
- **Context-Aware & Theme Colors:** Always prefer consuming theme tokens via `Theme.of(context).colorScheme` (e.g. `colorScheme.primary`, `colorScheme.surface`). However, if explicit design system tokens (such as `AppColors` or `AppSemanticColors`) are specified by the project guidelines or developer, their direct use is permitted:
  - Primary actions: `colorScheme.primary` / `colorScheme.onPrimary`
  - Container/Card backgrounds: `colorScheme.surface` / `colorScheme.surfaceContainer`
  - Secondary elements: `colorScheme.secondary` / `colorScheme.secondaryContainer`
  - Error states: `colorScheme.error` / `colorScheme.onError`

### B. Typography & Text Styles
- Use M3 typography scale from `Theme.of(context).textTheme`:
  - Headers: `headlineLarge`, `headlineMedium`, `headlineSmall`
  - Titles: `titleLarge`, `titleMedium`, `titleSmall`
  - Body text: `bodyLarge`, `bodyMedium`, `bodySmall`
  - Labels/Buttons: `labelLarge`, `labelMedium`
- **NEVER** instantiate standalone `TextStyle()` for standard UI text; always copy or merge with existing text theme rules using `.copyWith()`.

### C. Component Selection Guidelines
- **Buttons:**
  - High-emphasis main action: Use `ElevatedButton` (styled with `colorScheme.primary` and `colorScheme.onPrimary`) or `FilledButton`.
  - Secondary emphasis: `ElevatedButton` (with `secondaryContainer`) or `OutlinedButton`.
  - Low-emphasis / Inline: `TextButton`.
  - Avoid legacy Material 2 button widgets (e.g., `RaisedButton`, `FlatButton`).
- **Navigation:**
  - Bottom navigation: Use custom design system floating navigation bars (e.g., floating `Container` with `Row` and flexible nav items) or M3 `NavigationBar` with `NavigationDestination`. Do NOT use legacy `BottomNavigationBar`.
  - Drawer / Rail: Use `NavigationDrawer` or `NavigationRail` for larger viewports.
- **Cards & Surface Containers:**
  - Prefer using `Card` with M3 variants: `Card()` (elevated), `Card.filled()`, or `Card.outlined()`.
- **Feedback & Dialogs:**
  - Dialogs: Use `AlertDialog` with M3 rounded corners and `colorScheme.surfaceContainerHigh`.
  - SnackBars: Always wrap with `SnackBar(behavior: SnackBarBehavior.floating)` for modern M3 floating aesthetics.

### D. Shapes & Elevation
- Material 3 replaces heavy drop shadows with **tonal elevation** (color overlays based on `surfaceTintColor`).
- Respect default M3 border radiuses (e.g., 12dp for cards, 16dp for dialogs, 28dp for FABs/Buttons).

---

## 3. Anti-Patterns & Strict Constraints

- **DO NOT** use `primarySwatch` or legacy Material 2 color properties (e.g., `accentColor`).
- **DO NOT** hardcode static background colors unless custom design system tokens (e.g., `AppColors`) are explicitly indicated by the developer.
- **DO NOT** use legacy `BottomNavigationBar`; use standard M3 `NavigationBar` or a custom floating navigation bar according to project guidelines.
- **DO NOT** lock elements with fixed heights/widths when M3 padding or `SizedBox` spacing can maintain flexibility.

---

## 4. Code Examples

### Correct App Theme Integration
```dart
MaterialApp(
  title: 'Planify',
  theme: AppTheme.light,
  home: const HomeScreen(),
);
```

### Correct M3 Card Component
```dart
Card.filled(
  color: Theme.of(context).colorScheme.surfaceContainerHigh,
  child: Padding(
    padding: const EdgeInsets.all(16.0),
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Juntada de Viernes',
          style: Theme.of(context).textTheme.titleMedium?.copyWith(
                color: Theme.of(context).colorScheme.onSurface,
              ),
        ),
        const SizedBox(height: 8),
        Text(
          'Confirmados: 5 amigos',
          style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                color: Theme.of(context).colorScheme.onSurfaceVariant,
              ),
        ),
        const SizedBox(height: 12),
        FilledButton.tonal(
          onPressed: () {},
          child: const Text('Ver Detalle'),
        ),
      ],
    ),
  ),
);
```

---

## 5. Using This With Any Agent

Nothing in this file assumes Claude specifically — it's plain markdown with no tool syntax baked in. Point your agent at it directly: reference it from your agent's own project-instructions file (`AGENTS.md` for Codex CLI, `GEMINI.md` for Gemini CLI, or the equivalent for whatever you use), or just name the file path in your prompt. Works the same in Codex, Gemini, Claude, or no agent at all — reading it yourself.

## Ejemplo de uso

**Pedido:** "Pasá la pantalla de configuración a Material 3."

**Resultado:** La pantalla con el ThemeData de Material 3, los componentes actualizados y los colores tomados del esquema del tema en lugar de valores fijos.
