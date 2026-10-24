---
name: g03-flutter-apply-glassmorphism-design
description: Aplica un estilo glassmorphism (paneles translúcidos con desenfoque, profundidad y movimiento suave) a pantallas Flutter usando BackdropFilter y los tokens de diseño propios del proyecto. Usar cuando una pantalla o componente se ve genérico y tiene que verse más profesional.
metadata:
  tipo: skill
  area:
  - diseno
  - mobile
  fase:
  - diseno
  - desarrollo
  tecnologias:
  - flutter
  herramientas:
  - claude-code
  - codex
  requiere: []
  grupo: '03'
  autor:
    nombre: Julieta Iglesias
    github: JuliIglesias
  responsables:
  - JuliIglesias
  madurez: usado-en-proyecto
  relacionados: []
---
# Skill: Premium Glassmorphism for Planify (Flutter)

## 1. When to Use This Skill

Apply this skill whenever:
- A screen, card, nav bar, dialog, or sheet needs to look premium/high-end rather than default Material.
- The user explicitly asks for "glass", "frosted", "blur", "glassmorphism", or "que se sienta pro".
- You're reviewing a screen's visual polish and it reads as generic or template-like — flat white `Card`, hard grey border, plain drop shadow.

This skill governs **surface treatment**: translucency, depth, blur, elevation, and the motion that goes with it. It does **not** replace `flutter-apply-material3-guidelines` — that skill still governs which widget to reach for (`FilledButton` vs `TextButton`, `NavigationBar` vs a custom bar, the M3 typography scale) and the base `ColorScheme`. Use both together: M3 guidelines decide the component and its semantic color; this skill decides how that component's *surface* is rendered.

### On Figma
Figma is a reference for layout, content, and brand color — not the final word on surface treatment. Where a Figma comp shows a flat card and this skill calls for glass, prefer the glass treatment unless that specific screen has a real functional reason to stay flat (e.g. something meant to be screenshotted or exported). If it's genuinely unclear whether to deviate, ask instead of silently overriding the comp.

---

## 2. Why Most "Glass" UI Looks Cheap Instead of Premium

Glassmorphism is easy to implement badly. A translucent white box with a blur behind it does not automatically look premium — it looks premium only when a few specific conditions hold. This section is the checklist that separates "looks like a template" from "looks pro." It was adapted from a public checklist of generic-AI-UI anti-patterns, rewritten from scratch for Flutter/Material 3 and anchored to Planify's own tokens rather than invented ones.

### A. Glass needs something to blur
`BackdropFilter` blurs whatever sits *behind* the widget. If the background is a flat solid color (today, `AppColors.background`, `0xFFECF4FF`), a blurred panel over it looks almost identical to a plain translucent panel — the effect reads as nothing. Glass only reads as glass when there's visual variation behind it: a soft gradient, a large soft-edged color blob, an image, or content scrolling underneath a fixed panel (e.g. a glass app bar over scrolling cards). Before adding a glass panel anywhere, check what's actually behind it — if it's flat, either add gentle background variation first (see §4.E) or don't use glass there.

### B. Depth comes from layered translucency, not from a single blur
A single `BackdropFilter` + one translucent white fill reads as "frosted sticker," not "glass object." Real depth needs at least two things stacked: (1) the blur itself, and (2) a thin, slightly brighter border (a 1px gradient or semi-transparent white line) tracing the edge, which is what sells the idea of a physical pane of glass catching light. A soft, colored (never pure black) shadow underneath reinforces it further. See §4.B for what to stack.

### C. Never a flat black or grey shadow
Default Flutter `Card` elevation shadows read as generic because they're neutral grey/black. For any glass or elevated surface here, tint the shadow toward `AppColors.primary` or `AppColors.darkBlue` at very low opacity instead of `Colors.black`. This alone is one of the biggest tells between "default Material" and "designed."

### D. Generous spacing over generous decoration
Premium UI leans on whitespace more than on ornament. Use `AppSpacing.lg`/`AppSpacing.xl` (24/32) for the padding around glass panels and section breathing room, not `AppSpacing.sm`/`AppSpacing.md`. A glass panel crammed edge-to-edge with content looks cheap regardless of how good the blur is.

### E. Rounded, generous corners — reuse the existing scale
Don't invent new radius values. `AppRadius.card` (16) is the floor for a glass surface; prefer `AppRadius.lg` (20) or `AppRadius.xl` (28) for hero panels, sheets, and anything meant to feel like a centerpiece. Sharp or barely-rounded corners undercut the "soft glass" feeling immediately.

### F. Motion should be physical, not linear
Glass panels appearing with a flat fade or a linear slide feel synthetic. Prefer a short scale + fade + slight vertical offset on entry (`Curves.easeOutCubic` or similar, 250–400ms), and on tap, a subtle `AnimatedScale` down to ~0.97 rather than an instant `InkWell` ripple on glass surfaces specifically (ripples don't read well on translucent fills). Keep motion restrained — this is a student-built app judged on a 2,000-concurrent-user and low-end-device reality, not a marketing site; see §5 on performance.

### G. Text on glass must stay legible against *any* background
Because the panel is translucent, its contrast depends on what's behind it — which can change as the user scrolls or as background content changes. Never place body text directly on a bare blurred panel; add a low-opacity solid scrim (a `Container` color layer between the blur and the content, e.g. `AppColors.surface.withValues(alpha: 0.55–0.7)`) so text contrast holds regardless of what's underneath. Check this against both the lightest and busiest background states the panel can appear over, not just the happy-path screenshot.

---

## 3. Anti-Patterns — Do Not Do These

- ❌ `BackdropFilter` directly over `AppColors.background` with nothing else going on behind it (see §2.A) — it will visually do nothing and isn't worth the render cost.
- ❌ Pure black/grey `BoxShadow` under a glass panel — tint it (see §2.C).
- ❌ Skipping the scrim layer and putting `bodyMedium`/`bodySmall` text straight on `BackdropFilter` output (see §2.G) — this is an accessibility problem, not just a style nitpick.
- ❌ Inventing ad-hoc blur/opacity/radius numbers per screen. Centralize them (see §5) so every glass surface in the app looks like the same design language, not five different experiments.
- ❌ Wrapping long scrolling lists, or many small tappable items, each in their own `BackdropFilter` (see §5 — this is a real performance cliff, not a style rule).
- ❌ Using glass for *every* surface. Reserve it for surfaces that benefit from feeling elevated/premium — hero cards, nav bars, sheets, key CTAs. A screen where everything is glass has no hierarchy and stops looking premium.

---

## 4. Flutter Implementation Patterns

This section deliberately does **not** hand you a finished, drop-in `GlassSurface` widget. Copying a complete component teaches you nothing about *why* it looks the way it does — same principle the `jira-tickets` skill already applies to code snippets in tickets: a snippet shows the shape of the API, never the finished solution. What follows is the mechanism, the layers you need to assemble, and the questions you have to answer yourself while building it. Build your own widget from this; don't skip straight to a working one you found online.

### A. The primitive: `BackdropFilter`

The one piece of Flutter API you can't discover by reasoning about design — you need to know it exists — is this pairing:

```dart
import 'dart:ui'; // ImageFilter lives here, not in package:flutter/material.dart

ClipRRect(
  borderRadius: BorderRadius.circular(/* ... */),
  child: BackdropFilter(
    filter: ImageFilter.blur(sigmaX: /* ... */, sigmaY: /* ... */),
    child: /* ... */,
  ),
);
```

`ClipRRect` bounds the blur to a rounded region (without it, the blur bleeds across the whole render layer, not just your panel). `BackdropFilter` blurs whatever is painted *behind* its position in the tree, not its own child — the `child` you give it is what gets composited *on top of* the blurred result, not what gets blurred. That distinction matters: it's why §2.A says the blur needs real content behind it to look like anything.

### B. What you still have to design

`BackdropFilter` alone gives you a blur, not glass. Building the actual surface means stacking, in your own widget:

1. **A rounded, clipped region** (the `ClipRRect` above) — radius from `AppRadius`, per §2.E. Which value, and why that one over another for this particular surface?
2. **The blur itself** — a `blurSigma`. Too low and it doesn't read as frosted; too high and it costs more to render (§5) for no visual gain past a point. Pick a value, then look at it against real content behind it and adjust — don't guess a "right" number from this document.
3. **A translucent fill acting as a scrim** (§2.G) — this is what guarantees text contrast no matter what's behind the panel. What Flutter type do you reach for to layer a semi-transparent color under content inside a rounded, bordered box? (Hint: you already used it constantly in `flutter-apply-material3-guidelines` for cards — same widget, different `color`.)
4. **A thin, bright border** tracing the edge (§2.B) — this is what sells "pane of glass" over "smudged sticker." What property of that same widget lets you add a 1px line, and what color/opacity reads as "catching light" rather than just "grey outline"?
5. **A tinted shadow** underneath (§2.C) — same widget family again, one more property. Tinted toward which existing `AppColors` value, and why that one instead of a generic dark grey?

If you can answer all five and assemble them into one reusable widget at `lib/core/widgets/` (naming and placement per `flutter-project-structure-guidelines`), you understand glassmorphism in Flutter — not just this one component.

### C. Tap feedback on glass

§2.F says ripples don't read well on translucent fills, and a scale-down feels more physical. The pieces you need:
- A widget that reports `onTapDown` / `onTapUp` / `onTapCancel` separately (not just `onTap`) so you can react to press-and-release as two distinct moments.
- A widget that animates a scale transform smoothly when a `scale` value changes, without you writing your own `AnimationController` for something this simple.

Look up both, wire them together so the panel shrinks slightly on press and springs back on release, and decide what scale factor (how close to `1.0`) feels subtle rather than jumpy — try a couple of values on a real device before settling.

### D. Entry motion

§2.F also asks for panels to *arrive* with a scale/fade/slight-vertical-offset rather than a flat linear fade. If the screen already animates other elements in with an `AnimationController` or a transition widget, reuse that mechanism rather than inventing a second animation system just for glass panels — consistency in *how* things animate matters as much as the motion itself. If you're not sure how the screen you're working on currently handles entrance animation, check before adding a new pattern.

### E. Giving glass something to blur

If a screen's background is currently flat `AppColors.background`, add gentle variation behind the glass content — most simply, a soft radial/linear gradient using existing brand colors:

```dart
Container(
  decoration: const BoxDecoration(
    gradient: LinearGradient(
      begin: Alignment.topLeft,
      end: Alignment.bottomRight,
      colors: [AppColors.lightBlue, AppColors.background, AppColors.secondary],
      stops: [0.0, 0.5, 1.0],
    ),
  ),
  child: /* screen content, glass panels on top */,
);
```

This stays inside the existing palette — it's a gradient of colors already in `AppColors`, not new brand colors. For a bottom nav bar or app bar that stays fixed while content scrolls underneath, the scrolling content itself is usually enough variation — no extra gradient needed there.

---

## 5. Performance Guardrails

`BackdropFilter` is expensive: it forces a separate compositing pass and repaints the blur every frame it's visible, including every frame something scrolls behind it. This matters concretely for Planify because the Charter's scale target (2,000 concurrent users) says nothing about *client-side* frame budget, but the same audience of students will run this on a real range of low-to-mid-end Android phones, not just a fast dev device — a janky UI reads as "cheap," which defeats the entire point of this skill.

- **Cap it.** A handful of glass surfaces per screen (hero card, nav bar, one sheet) is fine. Wrapping every list item or every chip in its own `BackdropFilter` is not — use a flat `AppColors.surface` fill with the tinted-shadow trick from §2.C for repeated small elements instead, and reserve real glass for a small number of standout surfaces.
- **Static over scrolling where possible.** A `BackdropFilter` that stays fixed (an app bar, a bottom nav, a persistent sheet) is cheaper than one that scrolls with the content, because the content moving underneath it still forces a repaint of the blur each frame either way — but a fixed glass element at least doesn't also need to reposition. Prefer fixed glass chrome around scrolling content over glass elements that themselves scroll.
- **`RepaintBoundary` around glass widgets** that sit next to frequently-rebuilding siblings (e.g. a live-updating counter, an animated badge), so the blur isn't recomputed on every unrelated rebuild.
- **Test on a real low-end device or emulator profile before calling a glass screen done** — not just the fastest phone on the team. If it visibly drops frames while scrolling, reduce `blurSigma`, reduce how many glass surfaces are stacked/visible at once, or fall back to the flat-fill + tinted-shadow treatment for that screen.

---

## 6. Design Tokens: Extend, Don't Invent

Every glass surface should read as the same design language, which means the blur sigma, fill opacity, and border opacity should come from one place, not be re-typed per screen. If this skill gets adopted for real:

- Add the glass constants (default `blurSigma`, `fillOpacity`, border/shadow opacity) to `lib/core/theme/` in `planify-mobile` — either a new small `app_glass.dart` alongside the existing `app_radius.dart`/`app_spacing.dart`, or as constants on `GlassSurface` itself if the team prefers fewer files. Either way, **one source of truth**, following the same pattern already established by `AppRadius`/`AppSpacing`.
- Reuse `AppColors`, `AppRadius`, and `AppSpacing` as shown in §4 — do not introduce parallel color/radius/spacing values for glass surfaces specifically.
- `AppTheme` currently only defines `light`. If/when a dark theme is added, glass needs different treatment (lower fill opacity reads as murky on dark backgrounds; the border needs to shift toward a brighter, more saturated line to stay visible) — flag this explicitly rather than assuming the same numbers work in both.

---

## 7. Pre-Output Checklist

Before considering a glassmorphism treatment done, confirm:

- [ ] There's real visual variation behind every glass panel (§2.A) — not a flat background with a pointless blur.
- [ ] Every glass surface has a scrim under any text (§2.G), checked against the busiest background state it can appear over.
- [ ] Shadows are tinted (`AppColors.darkBlue`/`primary` at low alpha), never plain black (§2.C).
- [ ] Radius comes from `AppRadius` (`card`/`lg`/`xl`), not a one-off number.
- [ ] Padding comes from `AppSpacing` (`lg`/`xl` for glass panels), not cramped defaults.
- [ ] Glass is used selectively — hero surfaces and chrome, not everything on the screen.
- [ ] Verified on a low-end device/profile — no visible jank while scrolling behind a fixed glass element (§5).
- [ ] `flutter-apply-material3-guidelines` is still respected for the widget choice and semantic color underneath the glass treatment — this skill changes *how the surface renders*, not which component to use.

---

## 8. Using This With Any Agent

Nothing in this file assumes Claude specifically. It's plain markdown with no tool syntax baked in, so it works the same way whether you're using Codex CLI, Gemini CLI, Claude Code, or any other coding agent — or reading it yourself with no agent at all.

- **Codex CLI**: point it at this file directly in your prompt (e.g. "follow `mobile/.agents/skills/flutter-apply-glassmorphism-design/SKILL.md` while building this screen"), or reference it from your project's `AGENTS.md` alongside the other agent/skill files you've copied in, the same way you'd reference any other project convention doc.
- **Gemini CLI**: same idea, via `GEMINI.md` instead of `AGENTS.md` — or just name the file path in your prompt either way.
- **Any chat-based agent**: paste the relevant section(s) into your prompt, or open the file in your editor side by side while you work — the guidance (why glass looks cheap, the anti-patterns, the performance guardrails) applies regardless of who's typing the code.
- This file never tells an agent to run a command or call a tool on your behalf — every action in it (choosing a `blurSigma`, testing on a device, wiring up the widget) is something you do, with the file as reference. That's deliberate, and it's why it ports across agents with nothing to adapt.

## Ejemplo de uso

**Pedido:** "Hacé que la pantalla de detalle del evento se vea más pro."

**Resultado:** La pantalla con superficies translúcidas, jerarquía visual y animaciones suaves construidas con los colores, radios, espaciados y tipografías del proyecto, sin inventar valores nuevos.
