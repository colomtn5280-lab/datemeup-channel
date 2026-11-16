# DateMeUp: Craft & Polish Implementation Spec ("remove the vibe-coded feel")
**For:** Hermes  **From:** test/review pass, 2026-11-15  **Applies to:** iOS, Android, Web, API, GCP

> **Read §0 first.** You're already fixing everything in `DateMeUp-3-participant-test-and-store-readiness-2026-11-15.md`. This spec does **not** repeat those fixes. It builds the craft layer *on top of* them. Wherever a section touches an area you're fixing, it says **"depends on [ID]"** and only adds what's new.

---

## 0. Scope, boundaries, assumptions

### 0.1 Already in your fix queue: NOT in this spec
| Fix IDs (prior report) | Area | This spec's relationship |
|---|---|---|
| V1–V8 | Vote/note correctness, counters, toggle-off, swipe threshold, "waiting on" wording | §3 adds **feedback/animation** on top of correct voting. No logic changes. |
| D1–D5 | Dates, "Tonight", past events, default time | §8.1 uses your fixed date source of truth. No date logic here. |
| K1 | Calendar permissions / intent / .ics | §3.6 only restyles the *success/failure UI*. |
| I1–I9 | Invite API, username field, pending invites, multi-use links, Universal/App Links, join code | §6 adds **rendered share images + link previews** only. |
| C1–C5 | Counter-propose, no-consensus actions, deadlines | §4.3 adds the **"So close" moment** visual only. |
| G1–G6 | Group type, 2-person copy, avatar stack, refresh, initials, demo cleanup | §10 provides the **string catalog** your G2 fix can drop into. No separate fix. |
| F1–F2 | Friends web UI, request state | none |
| N1–N2 | Notification types, "Let them know" → nudge | §8.6 adds **copy style, rich images and action buttons** to the notifications you're adding. |
| IC1–IC3 | Invite card picker, sample data, togetherplans string | §6 adds the server renderer and art direction. Your data fixes stay yours. |
| M1–M4 | Match modal reappears/close, rating repeat, Android back stack, duplicate winner | §4.1 redesigns the match *moment*. It relies on your M1 (show once / closable) and adds `seen` tracking server-side. |
| DQ1–DQ2, A1–A4 | Discover category data, locale, onboarding persistence, version bump, Google sign-in | §7 redesigns onboarding *content*. A1 persistence stays yours. |
| §6 store checklist | Sign in with Apple, deletion, UGC, privacy, screenshots, deep-link files | Not repeated. |

### 0.2 Stack assumptions (adjust if different)
I haven't seen the source. These are inferred from the API shapes, bundle IDs and behavior:
- **Mobile:** Expo / React Native (EAS builds), TypeScript, `react-native-reanimated` v3, Expo Router or React Navigation.
- **Web:** React SPA on **Cloudflare Pages** (the old `togetherplans.pages.dev`).
- **API:** Node/TypeScript at `api.datemeup.app`, Prisma-style models (`Proposal`, `Option`, `Vote{sentiment: APPROVE|MAYBE|REJECT}`, `GroupMember`, `Invitation`).
- **Google Cloud:** project "DateMeUp", already used for OAuth plus Maps/Places keys.

If any of these is wrong, the patterns still hold. Swap the library names.

### 0.3 What "vibe-coded" means here (the tells we're removing)
Things I saw in testing, with where each is fixed:

| Tell | Where seen | Fixed in |
|---|---|---|
| Emoji used as UI art (🎉 🎯 🌙 ❤️ 👍 🤔 in buttons and headers) | Match, Sent, empty plan, Tonight, "Send to Trio Date Club ❤️", vote buttons | §1.6, §5 |
| Actions with no feedback (level 1) | Votes, Save note, Send | §3 |
| System `Alert` dialogs for errors | "Could not add to calendar" on iOS and Android | §3.6 |
| Layout jumps on interaction | Vote cards grow/shrink | §3.2 |
| Different words for the same thing per platform | Web "I'm in / Maybe / Don't think so" vs mobile "Yes / Maybe / No" | §10 |
| Spinners and blank image pop-in | Discover cards, proposal images | §11 |
| Generic flat tiles with emoji icons | Discover categories, Android card picker | §5, §6 |
| Dead-end success screens | "Sent to Trio Date Club 🎉 / View Plan / Back to Groups" | §4.2 |
| Ask for a permission with no context | Location prompt on "Add activity" | §7.2 |
| Plain-text shares with no preview | "Let them know", invite links | §6.3 |
| Web treated as a lesser companion | Web is the *first* surface invitees see | §9.3 |

### 0.4 Delivery order (all now, but sequenced so nothing blocks)
1. **Foundations** (§1 tokens, §10 strings, §2 haptics/motion libs): everything else uses them. *~3 days*
2. **Feedback layer** (§3) and **signature moments** (§4). *~5 days*
3. **Invite card renderer and link previews** (§6, GCP) in parallel with **illustration commission** (§5; the artist's lead time is the long pole, so place the order on day 1). *~5 days eng + 2–3 weeks art*
4. **Invisible craft backend** (§8) and **platform polish** (§9). *~8 days*
5. **Onboarding** (§7), when the art lands. *~3 days*
6. **Perf polish** (§11), **QA audit** (§14). *~3 days*

Everything ships behind feature flags (§13.4), so the art can land late without blocking release.

---

## 1. Design system foundation

There's one token source. Generate the CSS and TypeScript versions from `tokens.json` so web and mobile never drift.

### 1.1 `design/tokens.json`
```json
{
  "color": {
    "brand": { "teal-900": "#073B3A", "teal-700": "#0B6E6B", "teal-600": "#0E8A86", "teal-500": "#12A39E", "teal-100": "#D8F1EF", "teal-50": "#EEF8F7" },
    "accent": { "coral-500": "#FF6B57", "coral-100": "#FFE3DE", "amber-500": "#F5A524", "amber-100": "#FDEFD3" },
    "night": { "900": "#141126", "800": "#1E1A38", "600": "#3A3366", "glow": "#9B7BFF" },
    "ink": { "900": "#121417", "700": "#3B4048", "500": "#6B7280", "300": "#C9CDD3", "100": "#EEF0F2", "0": "#FFFFFF" },
    "surface": { "page": "#F6F5F2", "card": "#FFFFFF", "sunken": "#EFEDE8" },
    "vote": { "yes": "#12A39E", "yes-bg": "#D8F1EF", "maybe": "#F5A524", "maybe-bg": "#FDEFD3", "no": "#6B7280", "no-bg": "#EEF0F2" },
    "feedback": { "success": "#1F9D55", "warning": "#B7791F", "danger": "#D64545", "info": "#2B6CB0" }
  },
  "radius": { "xs": 6, "sm": 10, "md": 14, "lg": 20, "xl": 28, "pill": 999 },
  "space": { "0": 0, "1": 4, "2": 8, "3": 12, "4": 16, "5": 20, "6": 24, "8": 32, "10": 40, "12": 48 },
  "font": {
    "display": "Bricolage Grotesque",
    "body": "Inter",
    "size": { "xs": 12, "sm": 14, "md": 16, "lg": 18, "xl": 22, "2xl": 28, "3xl": 34, "4xl": 44 },
    "weight": { "regular": 400, "medium": 500, "semibold": 600, "bold": 700, "black": 800 },
    "lineHeight": { "tight": 1.1, "snug": 1.25, "normal": 1.45 }
  },
  "elevation": {
    "1": "0 1px 2px rgba(18,20,23,.06), 0 1px 1px rgba(18,20,23,.04)",
    "2": "0 4px 12px rgba(18,20,23,.08), 0 1px 3px rgba(18,20,23,.06)",
    "3": "0 12px 32px rgba(18,20,23,.12), 0 4px 8px rgba(18,20,23,.06)"
  },
  "motion": {
    "duration": { "instant": 90, "fast": 160, "base": 240, "slow": 380, "moment": 900 },
    "easing": {
      "standard": [0.2, 0, 0, 1],
      "enter": [0.05, 0.7, 0.1, 1],
      "exit": [0.3, 0, 0.8, 0.15],
      "emphasized": [0.2, 0, 0, 1.0]
    },
    "spring": {
      "press":  { "damping": 18, "stiffness": 420, "mass": 0.6 },
      "settle": { "damping": 16, "stiffness": 220, "mass": 0.9 },
      "bouncy": { "damping": 10, "stiffness": 180, "mass": 0.8 }
    }
  }
}
```
> **Fonts:** pick one display face with character for titles (Bricolage Grotesque is free on Google Fonts and fits the "playful but adult" tone) and one workhorse body face. That's two families max. Bundle them with `expo-font` on mobile and self-host `woff2` on web (no Google Fonts CDN request at runtime; it's faster and avoids a privacy disclosure). If the current bold geometric display font is a deliberate brand choice, keep it and only add Inter for body text.

### 1.2 Generator: `design/build-tokens.ts`
```ts
// Run: npx tsx design/build-tokens.ts  → web/src/styles/tokens.css + mobile/src/theme/tokens.ts
import fs from "node:fs";
const t = JSON.parse(fs.readFileSync("design/tokens.json", "utf8"));

const flat = (obj: any, prefix: string[] = [], out: Record<string, string> = {}) => {
  for (const [k, v] of Object.entries(obj)) {
    if (v && typeof v === "object" && !Array.isArray(v)) flat(v, [...prefix, k], out);
    else out[[...prefix, k].join("-")] = Array.isArray(v) ? `cubic-bezier(${v.join(",")})` : String(v);
  }
  return out;
};
const vars = flat({ color: t.color, radius: t.radius, space: t.space, elevation: t.elevation,
  "motion-duration": t.motion.duration, "motion-easing": t.motion.easing,
  "font-size": t.font.size });
const px = (k: string, v: string) => /^(radius|space|font-size)/.test(k) ? `${v}px` : /^motion-duration/.test(k) ? `${v}ms` : v;

fs.writeFileSync("web/src/styles/tokens.css",
`/* GENERATED — do not edit. Source: design/tokens.json */
:root{
${Object.entries(vars).map(([k, v]) => `  --${k}: ${px(k, v)};`).join("\n")}
  --font-display: "${t.font.display}", ui-sans-serif, system-ui, sans-serif;
  --font-body: "${t.font.body}", ui-sans-serif, system-ui, sans-serif;
}
@media (prefers-reduced-motion: reduce){
  :root{ ${Object.keys(t.motion.duration).map(k => `--motion-duration-${k}: 1ms;`).join(" ")} }
}
`);

fs.writeFileSync("mobile/src/theme/tokens.ts",
`// GENERATED — do not edit. Source: design/tokens.json
export const tokens = ${JSON.stringify(t, null, 2)} as const;
export type Tokens = typeof tokens;
`);
console.log("tokens built");
```

### 1.3 Web base styles: `web/src/styles/base.css`
```css
@import "./tokens.css";

@font-face{font-family:"Bricolage Grotesque";src:url("/fonts/BricolageGrotesque-var.woff2") format("woff2");font-weight:400 800;font-display:swap}
@font-face{font-family:"Inter";src:url("/fonts/Inter-var.woff2") format("woff2");font-weight:400 700;font-display:swap}

*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;text-rendering:optimizeLegibility;-webkit-font-smoothing:antialiased}
body{margin:0;background:var(--color-surface-page);color:var(--color-ink-900);font:400 var(--font-size-md)/1.45 var(--font-body)}
h1,h2,h3,.display{font-family:var(--font-display);letter-spacing:-0.02em;line-height:1.1;font-weight:800}
h1{font-size:clamp(28px,4vw,var(--font-size-4xl))} h2{font-size:var(--font-size-2xl)} h3{font-size:var(--font-size-xl)}

/* One focus style, everywhere. Visible on keyboard only. */
:focus{outline:none}
:focus-visible{outline:3px solid var(--color-brand-teal-500);outline-offset:2px;border-radius:var(--radius-sm)}

/* Buttons: one system */
.btn{--bg:var(--color-brand-teal-600);--fg:#fff;
  display:inline-flex;align-items:center;justify-content:center;gap:var(--space-2);
  min-height:48px;padding:0 var(--space-5);border:0;border-radius:var(--radius-pill);
  background:var(--bg);color:var(--fg);font:600 var(--font-size-md)/1 var(--font-body);
  cursor:pointer;user-select:none;-webkit-tap-highlight-color:transparent;
  transition:transform var(--motion-duration-instant) var(--motion-easing-standard),
             background-color var(--motion-duration-fast) var(--motion-easing-standard),
             box-shadow var(--motion-duration-fast) var(--motion-easing-standard)}
.btn:hover{background:color-mix(in oklab,var(--bg) 88%,black)}
.btn:active{transform:scale(.97)}
.btn[disabled],.btn[aria-busy="true"]{opacity:.6;cursor:default}
.btn--secondary{--bg:var(--color-brand-teal-50);--fg:var(--color-brand-teal-700)}
.btn--ghost{--bg:transparent;--fg:var(--color-brand-teal-700);box-shadow:inset 0 0 0 1.5px var(--color-brand-teal-600)}
.btn--danger{--bg:transparent;--fg:var(--color-feedback-danger)}

.card{background:var(--color-surface-card);border-radius:var(--radius-lg);box-shadow:var(--elevation-1);overflow:hidden}
.card--interactive{transition:box-shadow var(--motion-duration-fast),transform var(--motion-duration-fast)}
.card--interactive:hover{box-shadow:var(--elevation-2);transform:translateY(-1px)}

.skeleton{position:relative;overflow:hidden;background:var(--color-surface-sunken);border-radius:var(--radius-sm)}
.skeleton::after{content:"";position:absolute;inset:0;transform:translateX(-100%);
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.55),transparent);
  animation:shimmer 1.2s infinite}
@keyframes shimmer{to{transform:translateX(100%)}}
@media (prefers-reduced-motion: reduce){.skeleton::after{animation:none}}
```

### 1.4 Mobile theme hook: `mobile/src/theme/index.ts`
```ts
import { AccessibilityInfo, useColorScheme } from "react-native";
import { useEffect, useState } from "react";
import { Easing } from "react-native-reanimated";
import { tokens } from "./tokens";

export const ease = (k: keyof typeof tokens.motion.easing) => {
  const [a, b, c, d] = tokens.motion.easing[k];
  return Easing.bezier(a, b, c, d);
};
export const spring = tokens.motion.spring;
export const dur = tokens.motion.duration;

export function useReducedMotion() {
  const [reduced, setReduced] = useState(false);
  useEffect(() => {
    AccessibilityInfo.isReduceMotionEnabled().then(setReduced);
    const sub = AccessibilityInfo.addEventListener("reduceMotionChanged", setReduced);
    return () => sub.remove();
  }, []);
  return reduced;
}
export { tokens };
```
> Reanimated 3 also ships `useReducedMotion()` and `ReduceMotion.System` on animations. Prefer passing `reduceMotion: ReduceMotion.System` on every `withSpring`/`withTiming` config, and use the hook above only for swapping whole components (e.g., confetti → static badge).

### 1.5 Type scale component (mobile): `mobile/src/ui/Text.tsx`
```tsx
import { Text as RNText, TextProps } from "react-native";
import { tokens } from "../theme";
type Variant = "display" | "title" | "headline" | "body" | "caption" | "label";
const map: Record<Variant, object> = {
  display:  { fontFamily: "Bricolage-ExtraBold", fontSize: tokens.font.size["3xl"], lineHeight: 38, letterSpacing: -0.6 },
  title:    { fontFamily: "Bricolage-Bold",      fontSize: tokens.font.size["2xl"], lineHeight: 32, letterSpacing: -0.4 },
  headline: { fontFamily: "Inter-SemiBold",      fontSize: tokens.font.size.lg,     lineHeight: 24 },
  body:     { fontFamily: "Inter-Regular",       fontSize: tokens.font.size.md,     lineHeight: 22 },
  caption:  { fontFamily: "Inter-Regular",       fontSize: tokens.font.size.sm,     lineHeight: 18, color: tokens.color.ink["500"] },
  label:    { fontFamily: "Inter-SemiBold",      fontSize: tokens.font.size.sm,     lineHeight: 18, letterSpacing: 0.2 },
};
export function Text({ variant = "body", style, ...rest }: TextProps & { variant?: Variant }) {
  return <RNText maxFontSizeMultiplier={1.6} style={[{ color: tokens.color.ink["900"] }, map[variant], style]} {...rest} />;
}
```
`maxFontSizeMultiplier={1.6}` supports Dynamic Type without breaking layouts. **Test every screen at the largest accessibility size.**

### 1.6 Icons: replace emoji in UI chrome
- Base set: **Phosphor Icons** (`phosphor-react-native` and `@phosphor-icons/react`), duotone weight. It has a warmer personality than Lucide and is consistent across platforms.
- **Custom-drawn icons** (from the illustrator, §5) for the 16 Discover categories and the 3 vote states. Deliver them as SVG and render with `react-native-svg` / inline SVG.
- **Rule:** emoji are allowed **only in user-generated text** (notes, comments, group names). Never in buttons, headers, empty states or system messages. Grep and remove:
```bash
# from repo root: find emoji in UI string literals (excluding tests/fixtures)
rg -n --pcre2 '[\x{1F300}-\x{1FAFF}\x{2600}-\x{27BF}]' mobile/src web/src -g '!**/*.test.*' -g '!**/fixtures/**'
```
Expect hits like "Send to {group} ❤️", "Let them know 👍", "Yes 👍", "Maybe 🤔", "No 🙅", "Tonight near me 🌙", "It's a Match! 🎉", "Sent to … ❤️", "Pick an invite card 💌", "Add to calendar 📅", "After Dark 🌙". Replace each with a custom icon component or nothing.

---

## 2. Motion & haptics libraries

### 2.1 Haptics: `mobile/src/feedback/haptics.ts`
```ts
import * as Haptics from "expo-haptics";
import { Platform } from "react-native";
import { getPrefs } from "../state/prefs"; // user toggle in Settings → "Haptics" (default on)

type Kind = "tap" | "select" | "vote" | "success" | "warning" | "error" | "match";
export async function haptic(kind: Kind) {
  if (!getPrefs().haptics) return;
  try {
    switch (kind) {
      case "tap":     return Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
      case "select":  return Haptics.selectionAsync();
      case "vote":    return Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
      case "success": return Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
      case "warning": return Haptics.notificationAsync(Haptics.NotificationFeedbackType.Warning);
      case "error":   return Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);
      case "match": {
        // Signature pattern: three rising taps, then a success. ~420ms total.
        await Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
        await wait(90);
        await Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
        await wait(90);
        await Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Heavy);
        await wait(140);
        return Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
      }
    }
  } catch { /* devices without a haptic engine: ignore */ }
}
const wait = (ms: number) => new Promise(r => setTimeout(r, ms));
export const hapticsSupported = Platform.OS === "ios" || Platform.OS === "android";
```
Usage map (apply exactly this, no more):

| Event | Haptic |
|---|---|
| Vote button press | `vote` |
| Toggle / segmented control / chip select | `select` |
| Add to Date (Discover) | `tap` |
| Plan sent | `success` |
| Match reveal | `match` (once, synced with the animation peak) |
| Error sheet shown | `error` |
| Pull-to-refresh threshold crossed | `select` |

### 2.2 Web equivalent (no haptics, so sound plus motion only)
Don't use `navigator.vibrate`: it's Android-Chrome only, and on desktop it reads as a gimmick. Web gets motion only (§3, §4).

### 2.3 Optional UI sounds (off by default, Settings → "Sounds")
Two sounds only: `match.caf` (~600 ms soft chime) and `sent.caf` (~250 ms whoosh). Use `expo-audio`, preloaded at app start. **Default off**, and respect the silent switch (on iOS, set the audio mode so playback stays silent when the ringer is off).
```ts
import { createAudioPlayer, setAudioModeAsync } from "expo-audio";
await setAudioModeAsync({ playsInSilentMode: false });
const match = createAudioPlayer(require("../../assets/sfx/match.caf"));
export const playMatch = () => getPrefs().sounds && (match.seekTo(0), match.play());
```

### 2.4 Shared Pressable with press physics: `mobile/src/ui/PressableScale.tsx`
```tsx
import { Pressable, PressableProps } from "react-native";
import Animated, { useSharedValue, useAnimatedStyle, withSpring, ReduceMotion } from "react-native-reanimated";
import { spring } from "../theme";
const AP = Animated.createAnimatedComponent(Pressable);

export function PressableScale({ scaleTo = 0.96, style, onPressIn, onPressOut, ...rest }:
  PressableProps & { scaleTo?: number }) {
  const s = useSharedValue(1);
  const a = useAnimatedStyle(() => ({ transform: [{ scale: s.value }] }));
  return (
    <AP
      {...rest}
      onPressIn={e => { s.value = withSpring(scaleTo, { ...spring.press, reduceMotion: ReduceMotion.System }); onPressIn?.(e); }}
      onPressOut={e => { s.value = withSpring(1, { ...spring.settle, reduceMotion: ReduceMotion.System }); onPressOut?.(e); }}
      style={[a, style as any]}
    />
  );
}
```
**Every** tappable surface uses `PressableScale` (buttons, cards, chips). Delete raw `TouchableOpacity` usage; the opacity flash reads as default/unstyled.


---

## 3. Feedback layer: every action answers back

> **Depends on V1–V5** (correct vote/note logic). This section is presentation only.

### 3.1 Principles
1. **Optimistic + reconciled.** The UI changes within 1 frame of the tap. If the server disagrees, roll back with a visible shake and an inline message, never silently.
2. **The change is the feedback.** Prefer animating the thing that changed (the count ticks, the chip fills) over a toast. Toasts only for things that happen *off-screen* (e.g., "Note saved" when the note field collapses).
3. **No layout shift.** Reserve space for anything that can appear (note field, vote count, "you voted" line).

### 3.2 Vote control (mobile): `mobile/src/vote/VoteBar.tsx`
Replaces the three buttons on each option card. One component on iOS and Android.
```tsx
import { View, StyleSheet } from "react-native";
import Animated, { useSharedValue, useAnimatedStyle, withSpring, withSequence, withTiming, ReduceMotion,
  interpolateColor, useDerivedValue } from "react-native-reanimated";
import { PressableScale } from "../ui/PressableScale";
import { Text } from "../ui/Text";
import { VoteIcon } from "../icons/VoteIcon";      // custom drawn: yes / maybe / no
import { haptic } from "../feedback/haptics";
import { tokens, spring } from "../theme";
import { t } from "../i18n";

export type Sentiment = "APPROVE" | "MAYBE" | "REJECT";
const ORDER: Sentiment[] = ["APPROVE", "MAYBE", "REJECT"];
const C = {
  APPROVE: { fg: tokens.color.vote.yes, bg: tokens.color.vote["yes-bg"] },
  MAYBE:   { fg: tokens.color.vote.maybe, bg: tokens.color.vote["maybe-bg"] },
  REJECT:  { fg: tokens.color.vote.no, bg: tokens.color.vote["no-bg"] },
};

export function VoteBar({ value, onChange, disabled }: {
  value: Sentiment | null; onChange: (s: Sentiment) => Promise<void>; disabled?: boolean;
}) {
  const shake = useSharedValue(0);
  const shakeStyle = useAnimatedStyle(() => ({ transform: [{ translateX: shake.value }] }));

  const press = async (s: Sentiment) => {
    if (disabled) return;
    haptic("vote");
    try { await onChange(s); }                       // parent does optimistic update + server call
    catch {
      haptic("error");
      shake.value = withSequence(
        withTiming(-6, { duration: 50 }), withTiming(6, { duration: 50 }),
        withTiming(-4, { duration: 50 }), withTiming(0, { duration: 50 }));
    }
  };

  return (
    <Animated.View style={[styles.row, shakeStyle]} accessibilityRole="radiogroup"
      accessibilityLabel={t("vote.groupLabel")}>
      {ORDER.map(s => <VoteChip key={s} s={s} selected={value === s} onPress={() => press(s)} />)}
    </Animated.View>
  );
}

function VoteChip({ s, selected, onPress }: { s: Sentiment; selected: boolean; onPress: () => void }) {
  const p = useDerivedValue(() => withSpring(selected ? 1 : 0, { ...spring.settle, reduceMotion: ReduceMotion.System }));
  const box = useAnimatedStyle(() => ({
    backgroundColor: interpolateColor(p.value, [0, 1], [C[s].bg, C[s].fg]),
    transform: [{ scale: 1 + p.value * 0.02 }],
  }));
  const label = useAnimatedStyle(() => ({ color: interpolateColor(p.value, [0, 1], [C[s].fg, "#FFFFFF"]) }));
  return (
    <PressableScale onPress={onPress} style={{ flex: 1 }}
      accessibilityRole="radio" accessibilityState={{ checked: selected }} accessibilityLabel={t(`vote.${s}`)}>
      <Animated.View style={[styles.chip, box]}>
        <VoteIcon kind={s} selected={selected} size={18} />
        <Animated.Text style={[styles.label, label]}>{t(`vote.${s}`)}</Animated.Text>
      </Animated.View>
    </PressableScale>
  );
}
const styles = StyleSheet.create({
  row: { flexDirection: "row", gap: 8 },
  chip: { height: 44, borderRadius: 999, flexDirection: "row", alignItems: "center", justifyContent: "center", gap: 6 },
  label: { fontFamily: "Inter-SemiBold", fontSize: 15 },
});
```
`VoteIcon` is the illustrator's three glyphs. Animate the selected glyph with a small "pop" (scale 0.6→1.0 with a `bouncy` spring) when it becomes selected.

### 3.3 Option card with reserved space: `mobile/src/vote/OptionCard.tsx` (layout excerpt)
```tsx
// The note row is ALWAYS present (fixed 48pt). Collapsed = a "Add a note" text button; expanded = input.
// The vote count line is ALWAYS present ("No votes yet" / "3 votes"). No height changes on vote.
<View style={{ minHeight: CARD_MIN }}>
  <Image ... />                         {/* fixed aspect 16:9 with blurhash (§11) */}
  <Title /> <Meta />
  <VoteCount value={tally} />           {/* AnimatedNumber, below */}
  <VoteBar value={mine} onChange={vote} />
  <NoteRow optionId={o.id} />           {/* fixed 48pt; inline save state, no layout jump */}
</View>
```
**Animated count** (ticks and slides, so the vote is *felt*):
```tsx
import Animated, { FadeInDown, FadeOutUp, LinearTransition } from "react-native-reanimated";
export function VoteCount({ value }: { value: number }) {
  return (
    <Animated.View layout={LinearTransition} style={{ height: 18, overflow: "hidden" }}>
      <Animated.Text key={value} entering={FadeInDown.duration(180)} exiting={FadeOutUp.duration(140)}
        style={{ fontFamily: "Inter-Regular", fontSize: 13, color: "#6B7280" }}>
        {t("vote.count", { count: value })}
      </Animated.Text>
    </Animated.View>
  );
}
```

### 3.4 Note row with inline save state (no toast)
States: `idle → editing → saving → saved(1.2s) → idle`. The **Save** button morphs into a ✓ with "Saved", then back. The saved note then renders under your name in the "How everyone voted" breakdown. This assumes V2 makes notes persist.
```tsx
const [state, setState] = useState<"idle"|"editing"|"saving"|"saved">("idle");
// on save:
setState("saving"); haptic("tap");
await api.saveNote(optionId, text);           // your V1 fix: PATCH comment only, never touches sentiment
setState("saved"); setTimeout(() => setState("idle"), 1200);
// Render: <AnimatedSwap>{state === "saved" ? <Check/>+"Saved" : state === "saving" ? <Dots/> : "Save"}</AnimatedSwap>
```

### 3.5 Web vote control: `web/src/vote/VoteBar.tsx` + CSS
```tsx
export function VoteBar({ value, onChange }: { value: Sentiment|null; onChange:(s:Sentiment)=>Promise<void> }) {
  const [err, setErr] = useState(false);
  const press = async (s: Sentiment) => {
    try { await onChange(s); } catch { setErr(true); setTimeout(() => setErr(false), 400); }
  };
  return (
    <div role="radiogroup" aria-label={t("vote.groupLabel")} className={`vote ${err ? "vote--shake" : ""}`}>
      {(["APPROVE","MAYBE","REJECT"] as const).map(s => (
        <button key={s} role="radio" aria-checked={value===s} data-s={s}
          className="vote__chip" onClick={() => press(s)}>
          <VoteIcon kind={s} aria-hidden /> <span>{t(`vote.${s}`)}</span>
          <kbd className="vote__kbd" aria-hidden>{ {APPROVE:"Y",MAYBE:"M",REJECT:"N"}[s] }</kbd>
        </button>))}
    </div>);
}
```
```css
.vote{display:grid;grid-template-columns:repeat(3,1fr);gap:var(--space-2)}
.vote__chip{position:relative;height:44px;border:0;border-radius:var(--radius-pill);display:flex;align-items:center;justify-content:center;gap:6px;
  font:600 15px/1 var(--font-body);cursor:pointer;
  transition:background-color var(--motion-duration-fast) var(--motion-easing-standard),
             color var(--motion-duration-fast) var(--motion-easing-standard),
             transform var(--motion-duration-instant) var(--motion-easing-standard)}
.vote__chip:active{transform:scale(.96)}
.vote__chip[data-s=APPROVE]{background:var(--color-vote-yes-bg);color:var(--color-vote-yes)}
.vote__chip[data-s=MAYBE]{background:var(--color-vote-maybe-bg);color:var(--color-vote-maybe)}
.vote__chip[data-s=REJECT]{background:var(--color-vote-no-bg);color:var(--color-vote-no)}
.vote__chip[aria-checked=true][data-s=APPROVE]{background:var(--color-vote-yes);color:#fff}
.vote__chip[aria-checked=true][data-s=MAYBE]{background:var(--color-vote-maybe);color:#fff}
.vote__chip[aria-checked=true][data-s=REJECT]{background:var(--color-vote-no);color:#fff}
.vote__chip[aria-checked=true] svg{animation:pop var(--motion-duration-base) cubic-bezier(.3,1.6,.5,1)}
@keyframes pop{0%{transform:scale(.6)}100%{transform:scale(1)}}
.vote--shake{animation:shake 240ms linear}
@keyframes shake{20%{transform:translateX(-6px)}40%{transform:translateX(6px)}60%{transform:translateX(-4px)}80%{transform:translateX(0)}}
.vote__kbd{position:absolute;right:10px;font:500 11px/1 var(--font-body);opacity:0;transition:opacity var(--motion-duration-fast)}
.option-card:focus-within .vote__kbd,.option-card:hover .vote__kbd{opacity:.45}
@media (hover:none){.vote__kbd{display:none}}
```
**Keyboard voting on web:** when an option card has focus, `Y` / `M` / `N` vote and `J` / `K` move between options. Show the hint chip on hover or focus only.
```ts
useEffect(() => {
  const onKey = (e: KeyboardEvent) => {
    if ((e.target as HTMLElement).closest("input,textarea,[contenteditable]")) return;
    const card = document.activeElement?.closest<HTMLElement>("[data-option-id]"); if (!card) return;
    const map: Record<string, Sentiment> = { y:"APPROVE", m:"MAYBE", n:"REJECT" };
    if (map[e.key]) { e.preventDefault(); vote(card.dataset.optionId!, map[e.key]); }
    if (e.key === "j" || e.key === "k") {
      const cards = [...document.querySelectorAll<HTMLElement>("[data-option-id]")];
      const i = cards.indexOf(card) + (e.key === "j" ? 1 : -1);
      cards[Math.max(0, Math.min(cards.length - 1, i))]?.focus();
    }
  };
  window.addEventListener("keydown", onKey); return () => window.removeEventListener("keydown", onKey);
}, []);
```

### 3.6 Branded sheets instead of system alerts (all errors and confirmations)
> **Depends on K1** for calendar *function*. This replaces the *presentation* of every `Alert.alert` / `window.alert` / `confirm`.

Ban list (CI lint rule):
```js
// .eslintrc.cjs
rules: {
  "no-restricted-syntax": ["error",
    { selector: "CallExpression[callee.object.name='Alert'][callee.property.name='alert']", message: "Use <Sheet/> via useSheet()" },
    { selector: "CallExpression[callee.name=/^(alert|confirm|prompt)$/]", message: "Use <Sheet/> via useSheet()" }],
}
```
Mobile: `@gorhom/bottom-sheet` wrapped in `useSheet()`:
```tsx
// mobile/src/ui/sheet.tsx
export type SheetSpec = { art?: IllustrationName; title: string; body?: string;
  primary?: { label: string; onPress: () => void }; secondary?: { label: string; onPress?: () => void }; tone?: "neutral"|"error" };
export function useSheet(): (spec: SheetSpec) => void { /* pushes onto a single SheetHost at app root */ }

// Example: calendar result
sheet({
  art: "calendar-oops", tone: "error",
  title: t("calendar.failTitle"),                 // "Couldn't reach your calendar"
  body: t("calendar.failBody"),                   // "You can add it from the invite file instead. It works with any calendar app."
  primary: { label: t("calendar.downloadIcs"), onPress: shareIcs },   // .ics fallback from your K1
  secondary: { label: t("common.notNow") },
});
```
Success is **not** a sheet. On calendar success, the "Add to calendar" button morphs into "In your calendar ✓" (check icon, teal fill) with a `success` haptic.

### 3.7 Toasts: one system, used sparingly
Only for off-screen confirmations: "Invite link copied", "Note saved" (when collapsing), "Removed from plan". The toast sits bottom-center above the tab bar, has an icon and 1 line, stays 2.2 s, and you can swipe it away. It has an `aria-live="polite"` region on web and `AccessibilityInfo.announceForAccessibility` on mobile.

---

## 4. Signature moments

These are the 2–3 moments to spend real hours on, the way Chris did with his gradient. Prototype each one in isolation (a Storybook story or Expo dev screen) and review the recording at 0.25× speed before integrating.

### 4.1 "It's a Match": the reveal
> **Depends on M1** (closable, not re-shown). This adds server-side "seen" tracking so "shown once" works across devices, plus the new choreography.

**Choreography (total ≈ 1.6 s, skippable by tap):**
| t (ms) | What happens |
|---|---|
| 0 | Background dims to `night-900` at 70%. The other option cards fall away (translateY +40, opacity 0, staggered 40 ms). |
| 120 | The winning option card lifts to center (shared-element style: scale 0.92→1, elevation 1→3). |
| 300 | Member avatars fly in from the screen edges along curved paths and land in an arc above the card, one by one (stagger 80 ms). |
| 300–700 | Each avatar shows a small ✓ badge as it lands (the vote color). |
| 760 | **Peak:** the card border draws itself (stroke-dash animation) in the brand gradient (teal-500 → coral-500), `match` haptic plus optional sound, confetti burst (40 particles, brand palette, custom shapes: hearts, ticket stubs, stars from the illustrator). |
| 900 | Title types in: "**It's a plan.**" (not "It's a Match! 🎉"); subline "Everyone's in for {option} · {date}". |
| 1200 | Actions rise in: primary **Add to calendar**, secondary **Send invite card**, tertiary text link **See how everyone voted**. |
| any | Tap anywhere or swipe down dismisses to the decided plan view. |

Reduced motion: no flying or confetti. The card appears with a 200 ms crossfade, avatars appear in place, haptic stays.

**Backend: seen tracking**
```prisma
model ProposalMemberState {
  id                    String   @id @default(cuid())
  proposalId            String
  userId                String
  matchSeenAt           DateTime?
  noConsensusSeenAt     DateTime?
  lastViewedAt          DateTime @default(now())
  @@unique([proposalId, userId])
  @@index([userId])
}
```
```ts
// api/src/routes/proposals.moments.ts
router.post("/proposals/:id/moments/:moment/seen", auth, async (req, res) => {
  const { id, moment } = req.params;
  if (!["match", "noConsensus"].includes(moment)) return res.status(400).end();
  await assertMember(req.user.id, id);
  const field = moment === "match" ? "matchSeenAt" : "noConsensusSeenAt";
  await prisma.proposalMemberState.upsert({
    where: { proposalId_userId: { proposalId: id, userId: req.user.id } },
    create: { proposalId: id, userId: req.user.id, [field]: new Date() },
    update: { [field]: new Date() },
  });
  res.status(204).end();
});
// Include in GET /proposals/:id → { ..., me: { matchSeenAt, noConsensusSeenAt } }
```
Client rule: play the reveal if `status === "DECIDED" && !me.matchSeenAt`. Call `seen` at choreography t=760 ms (the peak), so a user who closes the app mid-reveal still sees it once more.

**Mobile implementation skeleton:** `mobile/src/moments/MatchReveal.tsx`
```tsx
import Animated, { useSharedValue, withDelay, withSpring, withTiming, useAnimatedStyle, runOnJS,
  Easing, ReduceMotion, useAnimatedProps } from "react-native-reanimated";
import Svg, { Rect, Defs, LinearGradient, Stop } from "react-native-svg";
const ARect = Animated.createAnimatedComponent(Rect);

export function MatchReveal({ proposal, members, onDone }: Props) {
  const reduced = useReducedMotion();
  const lift = useSharedValue(0), border = useSharedValue(0), ui = useSharedValue(0);
  useEffect(() => {
    lift.value = withDelay(120, withSpring(1, spring.settle));
    border.value = withDelay(760, withTiming(1, { duration: 520, easing: Easing.bezier(0.2, 0, 0, 1) },
      () => { runOnJS(peak)(); }));
    ui.value = withDelay(1200, withTiming(1, { duration: 280 }));
  }, []);
  const peak = () => { haptic("match"); playMatch(); api.seen(proposal.id, "match"); };

  const PERIM = 2 * (CARD_W + CARD_H);
  const borderProps = useAnimatedProps(() => ({ strokeDashoffset: PERIM * (1 - border.value) }));
  // … card style from `lift`, avatars from <FlyInAvatar index={i} total={n} delay={300 + i*80}/>,
  // <Confetti trigger={border.value === 1} palette={brand} shapes={["heart","ticket","star"]} />
  return (/* layout */ null as any);
}
```
**Confetti (mobile, no extra native deps):** 40 `Animated.View`s with randomized initial velocity, gravity and spin, driven by one shared `progress` value (0→1 over 1400 ms). Particle shapes come from the illustrator's SVGs. The single shared value keeps it at 60 fps on mid-range Android.
```tsx
function Particle({ seed, progress }: { seed: number; progress: SharedValue<number> }) {
  const r = mulberry32(seed);                         // deterministic randoms
  const vx = (r() - 0.5) * 520, vy = -(380 + r() * 320), spin = (r() - 0.5) * 720, g = 900;
  const style = useAnimatedStyle(() => {
    const t = progress.value * 1.4;
    return { opacity: 1 - progress.value ** 3,
      transform: [{ translateX: vx * t }, { translateY: vy * t + 0.5 * g * t * t }, { rotate: `${spin * t}deg` }] };
  });
  return <Animated.View style={[{ position: "absolute" }, style]}><Shape kind={SHAPES[seed % 3]} color={PALETTE[seed % 5]} /></Animated.View>;
}
```
**Web implementation:** same timeline using the Web Animations API plus a `<canvas>` confetti (≈60 lines). Use `document.startViewTransition` to morph the winning option card into the hero card, and skip it if `prefers-reduced-motion`.
```ts
export async function playMatch(winnerEl: HTMLElement) {
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  winnerEl.style.viewTransitionName = "winner";
  const go = () => { setStage("reveal"); };          // React state swap to the reveal layout
  if (!reduce && "startViewTransition" in document) await (document as any).startViewTransition(go).finished;
  else go();
  if (!reduce) confetti(document.querySelector("#confetti") as HTMLCanvasElement, { count: 60 });
  fetch(`/api/proposals/${id}/moments/match/seen`, { method: "POST", headers: authHeaders() });
}
```

### 4.2 "Plan sent": land on the plan, not a dead end
> **Depends on M3** (back stack). Replace the "Sent to Trio Date Club 🎉 / View Plan / Back to Groups" screen.

- Tapping **Send** compresses the option cards into a stack (scale 0.9, rotate ±3°) that flies up into the group's avatar cluster in the header (≈500 ms), with a `success` haptic.
- You then **land directly on the plan page**, already in voting state, with a calm banner at the top: "Sent to {group}. We'll ping you when everyone's voted." (dismissible, auto-collapses after 4 s).
- The creator's own vote section is highlighted first (pulse once), because the creator hasn't voted yet (R3 showed "0 of 3" right after creation).

### 4.3 "So close": the no-consensus moment
> **Depends on C3/C4** (the actual Lock-in / Start-over actions). This is the visual.

- Triggered once per member (`noConsensusSeenAt`), when the last vote arrives without a unanimous Yes.
- **Visual:** the illustrator's "near miss" vignette (two characters reaching, not quite touching). The best option's card tilts forward slightly with a "Closest: 2 yes · 1 maybe" ribbon.
- **Copy:** "**So close.** {bestOption} got the most love. Lock it in, or try a few new ideas?"
- **Haptic:** `warning` (gentle), never `error`. Nothing failed.

### 4.4 Group progress ring (ambient, always on)
> **Depends on V5** (correct counts) and **V7** (named copy).

On every plan header and group card: member avatars sit on a circular progress ring. Each avatar fills its arc segment in their vote color when they vote. The ring animates live via your realtime channel (or a poll every 15 s when focused). This one element replaces the "0 / 3 voted" text plus progress bar.
```tsx
// mobile/src/plan/VoterRing.tsx (react-native-svg); each segment = 360/n degrees minus 6° gap
segments.map((m, i) => <AnimatedArc key={m.id} start={i*seg+3} end={(i+1)*seg-3}
  color={m.vote ? voteColor(m.vote) : tokens.color.ink["100"]} progress={m.vote ? 1 : 0} />)
```

---

## 5. Illustration & icon system (the biggest "not vibe-coded" lever)

### 5.1 Commission brief (send to the artist on day 1)
**Title:** DateMeUp: character + spot illustration system
**Concept:** a cast of 4 simple characters (gender-ambiguous, varied skin tones and body types, not a stock "couple") who appear in pairs or trios. Each has one distinctive prop (scarf, round glasses, big headphones, a dog).
**Style direction:**
- loose hand-drawn ink line with slight wobble
- 2–3 flat fills from the brand palette (teal, coral, amber, plus night-purple for After Dark)
- risograph-like grain texture
- no gradients or 3D
- *Reference mood:* mid-century travel posters × modern editorial spot art. **Must not resemble** default AI "corporate Memphis" or the generic 3D emoji look.

**Deliverables (vector SVG plus layered source):**

| # | Asset | Use | Size |
|---|---|---|---|
| 1 | 4 characters, front/¾/side, 5 expressions each | base set for derivatives | — |
| 2 | Onboarding ×4 scenes | §7 | 1200×1200 |
| 3 | Empty states ×8 | no groups, no plans, no results, no friends, offline, after-dark locked, no notifications, all caught up | 600×480 |
| 4 | Moments ×4 | match, so-close, sent, invite-accepted | 1200×900 |
| 5 | Error spots ×4 | calendar-oops, network, permission-denied, generic | 480×360 |
| 6 | Category icons ×16 | Discover tiles | 96×96, 2px stroke grid |
| 7 | Vote glyphs ×3 (yes/maybe/no) + selected variants | vote bar | 24×24 |
| 8 | Confetti shapes ×6 | heart, ticket stub, star, spark, music note, fork | 24×24 |
| 9 | App icon concept ×3 | store icon refresh | 1024×1024 |
| 10 | Animation-ready layers for #2 and #4 | Rive rigging | layered SVG |

**Budget guide:** ~$1.5–4k for a mid-level freelance illustrator (Dribbble, Behance, or a "Contra" search for "editorial character illustration"). Insist on a **style test first** (one onboarding scene) before the full set.

### 5.2 Hybrid workflow (Chris's tip, applied)
1. The artist delivers the base characters plus the style sheet (#1).
2. For additional variations (e.g., more category scenes, seasonal ones), feed the style sheet into an image model as a **style reference**, generate, then **have the artist do a cleanup pass** on any that ship. Never ship raw AI output.
3. Keep the master files in `design/illustrations/` (SVG plus `.riv`).

### 5.3 Animation: Rive
Use **Rive** (not Lottie): it has state machines (idle → react → celebrate), small files, and the same runtime on iOS, Android and web.
- Mobile: `rive-react-native` (needs an EAS dev build).
- Web: `@rive-app/react-canvas`.
- Each animated asset exposes inputs: `celebrate` (trigger), `mood` (number 0–4), `reduced` (bool → static pose).

```tsx
// mobile/src/ui/Illustration.tsx
import Rive, { RiveRef } from "rive-react-native";
import { SvgXml } from "react-native-svg";
export function Illustration({ name, size = 200, animate = true, trigger }: Props) {
  const reduced = useReducedMotion();
  const ref = useRef<RiveRef>(null);
  useEffect(() => { if (trigger) ref.current?.fireState("main", "celebrate"); }, [trigger]);
  if (!animate || reduced || !RIVE[name]) return <SvgXml xml={SVG[name]} width={size} height={size} />;
  return <Rive ref={ref} resourceName={RIVE[name]} stateMachineName="main" style={{ width: size, height: size }} />;
}
```
Bundle `.riv` files in the app (they're small, ~30–150 KB each). Serve them on web from the asset CDN (§12.2).

### 5.4 Placement map (where the emoji go)
| Today | Replace with |
|---|---|
| 🎯 "No activities yet. Add some from Discover!" | `empty/no-plan` illustration + "Start with a few ideas. Your group votes, the app does the deciding." + **Browse ideas** |
| 🎉 Sent screen | §4.2 (no screen) |
| 🎉 Match | §4.1 |
| 🌙 Tonight near me | night-purple banner with the illustrator's moon/skyline spot; title "Tonight" |
| Emoji category tiles | §5.1 #6 icons on soft tinted tiles (one tint per category family, max 4 tints) |
| ❤️ / 👍 in button labels | removed; icons only where meaningful |
| Default `Alert` | §3.6 sheets with error spots |

---

## 6. Invite cards: server-rendered, shareable everywhere

> **Depends on IC1–IC3** (picker UI, sample data, strings) and **I5** (deep links). This adds the **rendering pipeline** so the same card looks identical in-app, as a shared image, and as a link preview.

### 6.1 Architecture
```
App/Web → POST /api/cards/render {proposalId, templateId, note?, photoAssetId?}
          → API checks membership → Cloud Tasks enqueue (or sync if cached)
Cloud Run "card-renderer" (Node 20, Satori + resvg) → PNG 1080×1350 + 1200×630 (OG)
          → gs://datemeup-cards/{proposalId}/{hash}.png  (public-read via CDN, unguessable hash)
          → API stores CardRender row → returns URLs
Share sheet uses the PNG + link;  /p/{shareToken} page uses the OG PNG
```
The cache key is `sha256(templateId + proposal.updatedAt + winnerId + note + photoAssetId + locale)`, so the card re-renders only when content changes.

### 6.2 Card renderer service: `services/card-renderer/src/index.ts`
```ts
import express from "express";
import satori from "satori";
import { Resvg } from "@resvg/resvg-js";
import { Storage } from "@google-cloud/storage";
import fs from "node:fs";
import { templates } from "./templates";        // JSX templates, one per design (32)

const fonts = [
  { name: "Bricolage", data: fs.readFileSync("fonts/BricolageGrotesque-ExtraBold.ttf"), weight: 800 as const, style: "normal" as const },
  { name: "Inter", data: fs.readFileSync("fonts/Inter-Regular.ttf"), weight: 400 as const, style: "normal" as const },
  { name: "Inter", data: fs.readFileSync("fonts/Inter-SemiBold.ttf"), weight: 600 as const, style: "normal" as const },
];
const bucket = new Storage().bucket(process.env.CARD_BUCKET!);
const app = express(); app.use(express.json({ limit: "256kb" }));

// Only the API may call this (Cloud Run IAM: --no-allow-unauthenticated, API's service account has run.invoker)
app.post("/render", async (req, res) => {
  const { key, templateId, data, sizes = [[1080, 1350], [1200, 630]] } = req.body as RenderReq;
  const T = templates[templateId]; if (!T) return res.status(400).json({ error: "unknown template" });
  const out: Record<string, string> = {};
  for (const [w, h] of sizes) {
    const svg = await satori(T({ ...data, w, h }), { width: w, height: h, fonts });
    const png = new Resvg(svg, { fitTo: { mode: "width", value: w } }).render().asPng();
    const path = `${data.proposalId}/${key}-${w}x${h}.png`;
    await bucket.file(path).save(png, { contentType: "image/png", resumable: false,
      metadata: { cacheControl: "public, max-age=31536000, immutable" } });
    out[`${w}x${h}`] = `${process.env.CDN_BASE}/${path}`;
  }
  res.json(out);
});
app.listen(process.env.PORT || 8080);
```
**Template example** (`templates/ticketStub.tsx`). Every template receives **only real data**, with no defaults that could leak sample names or dates. Required fields are type-enforced:
```tsx
export type CardData = { proposalId: string; title: string; venue: string; whenLabel: string; // pre-formatted in viewer tz by API (your D3 source of truth)
  people: string[]; note?: string; photoUrl?: string; accent: string; w: number; h: number };
export const ticketStub = (d: CardData) => (
  <div style={{ width: d.w, height: d.h, display: "flex", background: "#F6F1E7", padding: 64, fontFamily: "Inter" }}>
    <div style={{ flex: 1, display: "flex", flexDirection: "column", border: `4px dashed ${d.accent}`, borderRadius: 32, padding: 56, justifyContent: "space-between" }}>
      <div style={{ fontFamily: "Bricolage", fontSize: 88, lineHeight: 1, color: "#121417" }}>{d.title}</div>
      <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
        <div style={{ fontSize: 40, fontWeight: 600 }}>{d.whenLabel}</div>
        <div style={{ fontSize: 34, color: "#3B4048" }}>{d.venue}</div>
        {d.note ? <div style={{ fontSize: 30, fontStyle: "italic", color: "#3B4048" }}>“{d.note}”</div> : null}
      </div>
      <div style={{ fontSize: 28, color: "#6B7280" }}>{d.people.join(" · ")} · datemeup.app</div>
    </div>
  </div>);
```
Add a **template contract test**: render every template with a fixture whose values are random UUID-like strings, then assert that none of the known sample strings (`JAKE & SARAH`, `Blue Room`, `Sep 27`, `togetherplans`) appear in the SVG output.

**API side:**
```ts
router.post("/cards/render", auth, async (req, res) => {
  const { proposalId, templateId, note, photoAssetId } = req.body;
  const p = await loadProposalForMember(req.user.id, proposalId);
  const data = cardDataFrom(p, req.user, { note, photoAssetId });     // whenLabel from your date utility
  const key = sha256(JSON.stringify({ templateId, u: p.updatedAt, w: p.winnerId, note, photoAssetId, l: req.locale })).slice(0, 16);
  const cached = await prisma.cardRender.findUnique({ where: { proposalId_key: { proposalId, key } } });
  if (cached) return res.json(cached.urls);
  const urls = await callRenderer({ key, templateId, data });          // ID-token auth to Cloud Run
  await prisma.cardRender.create({ data: { proposalId, key, templateId, urls } });
  res.json(urls);
});
```
```prisma
model CardRender { id String @id @default(cuid()) proposalId String key String templateId String urls Json createdAt DateTime @default(now())
  @@unique([proposalId, key]) }
```

### 6.3 Link previews (iMessage, WhatsApp, Slack, Facebook)
The web is on Cloudflare Pages, so a **Pages Function** injects per-plan Open Graph tags into the SPA shell for `/p/:token` (and `/join/:token` from your I-series):
```ts
// web/functions/p/[token].ts
export const onRequestGet: PagesFunction<{ API: string }> = async (ctx) => {
  const token = ctx.params.token as string;
  const shell = await ctx.env.ASSETS.fetch(new URL("/index.html", ctx.request.url));
  const meta = await fetch(`${ctx.env.API}/public/plans/${encodeURIComponent(token)}/preview`,
    { cf: { cacheTtl: 300, cacheEverything: true } }).then(r => r.ok ? r.json() : null).catch(() => null);
  if (!meta) return shell;
  const esc = (s: string) => s.replace(/[&<>"]/g, c => ({ "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;" }[c]!));
  const tags = `
    <title>${esc(meta.title)} · DateMeUp</title>
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="DateMeUp">
    <meta property="og:title" content="${esc(meta.title)}">
    <meta property="og:description" content="${esc(meta.description)}">
    <meta property="og:image" content="${esc(meta.ogImage)}">
    <meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
    <meta property="og:url" content="${esc(ctx.request.url)}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="apple-itunes-app" content="app-id=${meta.appStoreId}, app-argument=${esc(ctx.request.url)}">`;
  return new HTMLRewriter().on("head", { element(e) { e.append(tags, { html: true }); } }).transform(shell);
};
```
**Public preview endpoint** (no auth, exposes only what an invitee should see):
```ts
router.get("/public/plans/:token/preview", rateLimit({ windowMs: 60_000, max: 60 }), async (req, res) => {
  const p = await prisma.proposal.findUnique({ where: { shareToken: req.params.token }, include: { group: true, options: true } });
  if (!p) return res.status(404).end();
  const og = await ensureCard(p, "og-default");                       // 1200×630 render, cached
  res.set("Cache-Control", "public, max-age=300").json({
    title: p.title,
    description: p.status === "DECIDED"
      ? `It's a plan: ${p.options.find(o => o.id === p.winnerId)?.name} · ${whenLabel(p)}`
      : `${p.options.length} ideas · vote by ${deadlineLabel(p)} · ${p.group.name}`,
    ogImage: og["1200x630"], appStoreId: process.env.APP_STORE_ID,
  });
});
```
**Privacy:** never include member names or emails in the OG description. Show the group name only if the group setting allows it (default: plan title + count only).

### 6.4 Native share with image + link
```ts
// mobile: share the rendered PNG and the link together
import * as Sharing from "expo-sharing"; import * as FileSystem from "expo-file-system";
const { "1080x1350": url } = await api.renderCard({ proposalId, templateId, note });
const local = FileSystem.cacheDirectory + `card-${proposalId}.png`;
await FileSystem.downloadAsync(url, local);
await Share.share({ url: local, message: `${title}: vote here ${planLink}` });  // iOS: url=image, message=text+link
```


---

## 7. Onboarding & permissions

> **Depends on A1** (onboarding persisted server-side so it shows once). This is the content and the motion.

### 7.1 Four screens, about 25 seconds, every one skippable
| # | Illustration (Rive, plays on enter) | Headline | Sub |
|---|---|---|---|
| 1 | Two characters staring at a phone, shrugging | **"What do you want to do?" "I don't know, you pick."** | We fixed that. |
| 2 | Cards fanning out from a hand | **Toss in a few ideas.** | Shows, dinners, hikes. Real things near you, this week. |
| 3 | Group of 3 with ✓ / ~ / ✗ badges popping | **Everyone votes, quietly.** | No group-chat pressure. Just Yes, Maybe or No. |
| 4 | Confetti, characters high-five | **When everyone's in, it's a plan.** | Calendar, invite card, done. |

Then show sign in, followed by **favorite categories** as illustrated icon chips (multi-select with a `select` haptic each), then a **permission primer** (§7.2) at the moment of first need, *not* during onboarding.

Motion: horizontal pager with parallax. The illustration moves at 0.6× scroll speed and the text at 1×, and page dots stretch into a pill. Pressing "Skip" crossfades straight to sign-in.

### 7.2 Permission primers (just-in-time, with context)
**Location:** shown the first time you open Discover or "Add activity":
> Illustration: character holding a little map. **"Show me what's nearby?"** We use your location only to find things to do around you, never to share where you are. [**Use my location**] [Choose a city instead]

Only "Use my location" triggers the OS prompt. "Choose a city" opens a city search (Places Autocomplete), and the app works fully without location.

**Notifications:** shown after the user sends or votes on their **first** plan (when the value is obvious):
> **"Want a heads-up when everyone's voted?"** [Notify me] [Not now]

**Calendar:** never pre-prompted. The OS prompt (from your K1) appears on the first "Add to calendar" tap, because the user just asked for it.

If the user previously denied a permission, show the denied-state sheet with an "Open Settings" deep link (`Linking.openSettings()`) and the `permission-denied` illustration.

---

## 8. Invisible craft: backend intelligence

Users won't notice these consciously, but they make the app feel like it *gets* the group.

### 8.1 Group-midpoint Discover ranking (Routes API)
Today Discover is centered on the creator ("Near Ashburn · 25 mi"). For a group plan, rank by **fairness**: the worst-case travel time across members.

**Opt-in data:** each member can set a *home area* (city-level or a dropped pin rounded to ~1 km) under Settings → "My area". It's **never shown to others**; it's only used for ranking.
```prisma
model UserArea { userId String @id lat Float lng Float label String updatedAt DateTime @updatedAt }
```
**Ranking service:**
```ts
// api/src/discover/fairness.ts
import { request } from "undici";
type LatLng = { lat: number; lng: number };

export function centroid(points: LatLng[]): LatLng {
  const r = Math.PI / 180;
  let x = 0, y = 0, z = 0;
  for (const p of points) { const la = p.lat * r, lo = p.lng * r;
    x += Math.cos(la) * Math.cos(lo); y += Math.cos(la) * Math.sin(lo); z += Math.sin(la); }
  const n = points.length; x /= n; y /= n; z /= n;
  return { lat: Math.atan2(z, Math.hypot(x, y)) / r, lng: Math.atan2(y, x) / r };
}

/** Max drive minutes from any member to each candidate. One Routes API matrix call (≤ 25×25). */
export async function worstCaseMinutes(origins: LatLng[], dests: LatLng[], departAt?: Date): Promise<number[]> {
  const body = {
    origins: origins.map(o => ({ waypoint: { location: { latLng: { latitude: o.lat, longitude: o.lng } } } })),
    destinations: dests.map(d => ({ waypoint: { location: { latLng: { latitude: d.lat, longitude: d.lng } } } })),
    travelMode: "DRIVE", routingPreference: "TRAFFIC_AWARE",
    ...(departAt && departAt > new Date() ? { departureTime: departAt.toISOString() } : {}),
  };
  const res = await request("https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix", {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-Goog-Api-Key": process.env.ROUTES_KEY!,
      "X-Goog-FieldMask": "originIndex,destinationIndex,duration,condition" },
    body: JSON.stringify(body),
  });
  const rows = (await res.body.json()) as any[];
  const worst = new Array(dests.length).fill(0);
  for (const r of rows) {
    if (r.condition !== "ROUTE_EXISTS") { worst[r.destinationIndex] = Infinity; continue; }
    const min = parseInt(String(r.duration).replace("s", ""), 10) / 60;
    worst[r.destinationIndex] = Math.max(worst[r.destinationIndex], min);
  }
  return worst;
}
```
**Use it:** when Discover is opened *from a group context*:
1. Center the source query on `centroid(memberAreas)`. Fall back to the creator's location if fewer than 2 members have an area.
2. Score the top 25 candidates with `worstCaseMinutes`.
3. Show the result as a subtle line on each card: "**≤ 28 min for everyone**" (not distances).

Cache the results in Memorystore or in-process LRU, keyed by `(groupId, candidateId, hour)`, for 30 min.

**Cost control:** Routes API matrix elements are billed per element. Cap at 25 destinations × ≤ 6 origins, compute only for group contexts, and cache. Budget alert in §12.

### 8.2 Group taste memory
Learn per-group affinity from votes, softly re-rank Discover, and avoid repeats.
```sql
-- api/prisma/migrations/xxxx_group_taste/migration.sql
CREATE MATERIALIZED VIEW group_category_affinity AS
SELECT p."groupId", o.category,
       SUM(CASE v.sentiment WHEN 'APPROVE' THEN 1.0 WHEN 'MAYBE' THEN 0.35 ELSE -0.8 END) AS score,
       COUNT(*) AS n,
       MAX(v."createdAt") AS last_vote
FROM "Vote" v JOIN "Option" o ON o.id = v."optionId" JOIN "Proposal" p ON p.id = o."proposalId"
WHERE v."createdAt" > now() - interval '180 days'
GROUP BY 1, 2;
CREATE UNIQUE INDEX ON group_category_affinity ("groupId", category);
-- refresh: Cloud Scheduler → POST /internal/jobs/refresh-taste (nightly) → REFRESH MATERIALIZED VIEW CONCURRENTLY group_category_affinity;
```
```ts
// api/src/discover/rank.ts
export function rank(items: Candidate[], ctx: { affinity: Map<string, {score: number; n: number}>; recentlyDone: Set<string>; worst?: number[] }) {
  return items.map((it, i) => {
    const a = ctx.affinity.get(it.category);
    const taste = a ? Math.tanh(a.score / Math.max(3, a.n)) : 0;          // -1..1, damped for small n
    const travel = ctx.worst ? -Math.min(1, Math.max(0, (ctx.worst[i] - 20) / 40)) : 0; // 20→0, 60+→-1
    const repeat = ctx.recentlyDone.has(it.placeKey) ? -0.6 : 0;          // decided in last 60 days
    const fresh = it.startsAt ? 0.15 : 0;                                 // dated events slightly up
    return { it, s: 0.45 * taste + 0.35 * travel + repeat + fresh + it.baseRelevance * 0.2 };
  }).sort((a, b) => b.s - a.s).map(x => x.it);
}
```
**Rule:** taste only **re-orders**, it never hides results. A group that votes No on comedy still sees comedy, just lower down. No "because you…" explanation UI in v1; the ranking stays invisible.

### 8.3 Weather awareness for outdoor options
For options in outdoor categories (Hiking Trails, Sports & Active outdoors, outdoor concerts) that have a known start time within 10 days, fetch the hourly forecast and add a quiet chip: "☂ 70% rain at 7 PM". It uses the **illustrator's weather glyph**, not an emoji.
```ts
// api/src/enrich/weather.ts — Google Maps Platform Weather API (hourly forecast)
export async function forecastAt(lat: number, lng: number, at: Date) {
  const hours = Math.ceil((at.getTime() - Date.now()) / 3.6e6) + 1;
  if (hours < 1 || hours > 240) return null;
  const url = new URL("https://weather.googleapis.com/v1/forecast/hours:lookup");
  url.searchParams.set("key", process.env.WEATHER_KEY!);
  url.searchParams.set("location.latitude", String(lat));
  url.searchParams.set("location.longitude", String(lng));
  url.searchParams.set("hours", String(Math.min(hours, 240)));
  const j: any = await (await fetch(url)).json();
  const h = (j.forecastHours ?? []).find((x: any) => Math.abs(new Date(x.interval.startTime).getTime() - at.getTime()) < 3.6e6);
  if (!h) return null;
  return { rainPct: h.precipitation?.probability?.percent ?? 0, tempC: h.temperature?.degrees, condition: h.weatherCondition?.type };
}
// Show chip only if rainPct ≥ 50, temp ≤ 0°C/32°F, or ≥ 35°C/95°F. Otherwise show nothing (no noise).
```
> Verify the Weather API field names against the current docs when implementing. The endpoint is part of Maps Platform; enable `weather.googleapis.com` (§12).

A **Cloud Scheduler** job re-checks decided outdoor plans 24 h before start. If the rain probability crosses 60%, send *one* push: "Heads up, rain likely for {plan} tomorrow at 7. Still on?" with [Still on] [Rethink] actions (§8.6).

### 8.4 "Make a night of it" pairing
When an event option has an end time (or an inferred one: concerts/sports +3 h, comedy +1.75 h), show on the **decided** plan: "**After: 3 spots open late within 10 min**". Tapping it opens a mini-Discover filtered to bars/dessert/late food, open at the end time, sorted by walking time. It uses Places API (New) Nearby Search with field masks:
```ts
const res = await fetch("https://places.googleapis.com/v1/places:searchNearby", {
  method: "POST",
  headers: { "Content-Type": "application/json", "X-Goog-Api-Key": process.env.PLACES_KEY!,
    "X-Goog-FieldMask": "places.id,places.displayName,places.primaryType,places.location,places.currentOpeningHours,places.regularOpeningHours,places.rating,places.photos" },
  body: JSON.stringify({ includedTypes: ["bar", "dessert_shop", "cafe", "restaurant"], maxResultCount: 12,
    locationRestriction: { circle: { center: { latitude: lat, longitude: lng }, radius: 900 } }, rankPreference: "DISTANCE" }),
}).then(r => r.json());
// Filter client-side: regularOpeningHours covers endTime on that weekday. Show top 3.
```

### 8.5 Event status awareness
From the events source (Ticketmaster Discovery API returns `dates.status.code`: `onsale`, `offsale`, `cancelled`, `postponed`, `rescheduled`):
- **`cancelled`/`postponed`** on an option in an OPEN or DECIDED plan: mark the card with a calm grey "Cancelled by venue" ribbon and notify members once.
- **`offsale`**: "Tickets no longer on sale" chip.
- **Don't invent scarcity.** Never show "almost sold out" unless the source explicitly provides it.

Run a nightly job (Cloud Scheduler → `/internal/jobs/refresh-event-status`) for options in plans with a start time in the next 30 days.

### 8.6 Notifications that feel personal and actionable
> **Depends on N1/N2** (which notifications exist and the nudge mechanism). This adds **copy style**, **rich images** and **action buttons**.

**Copy rules:** use a name first, put the plan title in the body, no exclamation marks, no emoji, max 1 line each.

| Event | Title | Body | Actions |
|---|---|---|---|
| New plan | Jake started a plan | "Date night · Friday": 2 ideas, vote by Thu 6 PM | I'm in · Open |
| Waiting on you | You're the last vote | G R and Demo voted on "Trio dinner" | Open |
| Match | It's a plan | Everyone's in for WBB v. NC Central · Fri 7 PM | Add to calendar |
| So close | Almost a plan | "Trio dinner" got 2 yes and 1 maybe. Pick one? | Open |
| Comment | G R | "Comedy show is a no for me, dinner works" | Reply |
| Weather | Rain likely tomorrow | 70% at 7 PM for "Hike + picnic" | Still on · Rethink |

**Rich image:** attach the rendered OG card (§6) to Match notifications. On iOS that needs a **Notification Service Extension** (expo plugin `expo-notifications` + a custom config plugin, or the community `expo-notification-service-extension-plugin`); on Android, Expo push supports `richContent.image`.

**Action categories (mobile):**
```ts
import * as Notifications from "expo-notifications";
await Notifications.setNotificationCategoryAsync("NEW_PLAN", [
  { identifier: "OPEN", buttonTitle: t("notif.open"), options: { opensAppToForeground: true } },
]);
await Notifications.setNotificationCategoryAsync("MATCH", [
  { identifier: "CALENDAR", buttonTitle: t("notif.addToCalendar"), options: { opensAppToForeground: true } },
]);
await Notifications.setNotificationCategoryAsync("COMMENT", [
  { identifier: "REPLY", buttonTitle: t("notif.reply"), textInput: { submitButtonTitle: t("notif.send"), placeholder: t("notif.replyPlaceholder") } },
]);
Notifications.addNotificationResponseReceivedListener(async (r) => {
  const { proposalId } = r.notification.request.content.data as any;
  if (r.actionIdentifier === "REPLY" && r.userText) await api.comment(proposalId, r.userText);
  if (r.actionIdentifier === "CALENDAR") router.push(`/plan/${proposalId}?action=calendar`);
});
```
> **Don't add one-tap "Vote Yes" from a notification** for multi-option plans. Voting without seeing the options is low-quality input. Use "Open" instead.

**Server send (Expo push):**
```ts
await expo.sendPushNotificationsAsync([{ to: token, title, body, categoryId: "MATCH",
  data: { proposalId, url: `datemeup://plan/${proposalId}` },
  richContent: { image: ogUrl }, threadId: proposalId /* iOS grouping */, channelId: "plans" /* Android */ }]);
```
**Android channels** (users can tune them in system settings; this also looks professional):
```ts
await Notifications.setNotificationChannelAsync("plans",    { name: "Plans & votes", importance: Notifications.AndroidImportance.HIGH });
await Notifications.setNotificationChannelAsync("chat",     { name: "Comments", importance: Notifications.AndroidImportance.DEFAULT });
await Notifications.setNotificationChannelAsync("reminders",{ name: "Reminders & weather", importance: Notifications.AndroidImportance.DEFAULT });
await Notifications.setNotificationChannelAsync("social",   { name: "Friends & invites", importance: Notifications.AndroidImportance.DEFAULT });
```
**Batching:** coalesce vote notifications per plan within 10 minutes ("G R and Demo voted"). Use Cloud Tasks with a `scheduleTime` of +10 min and dedup by `(userId, proposalId, "votes")`.

**Quiet hours:** no non-urgent pushes between 22:00 and 08:00 local time. Queue them for 08:00.

---

## 9. Platform-native polish

### 9.1 iOS
**a) Sheets and navigation feel**
- All modals use the native sheet presentation (`presentation: "formSheet"` with `sheetAllowedDetents` in react-native-screens / Expo Router), with a grabber visible and swipe-to-dismiss enabled.
- Large titles on top-level screens (Plans, Discover, Profile). They collapse on scroll.
- Respect the safe area and the home indicator; nothing interactive within 8pt of it.

**b) Live Activity: "Voting in progress"** (Lock Screen + Dynamic Island)
This starts when a plan is created and updates as members vote. It shows the voter ring (§4.4) in the Dynamic Island and ends at match or deadline. Native Swift, added via an Expo config plugin (`expo-apple-targets` or a custom plugin that adds a Widget Extension target).
```swift
// targets/widgets/VotingActivity.swift
import ActivityKit, WidgetKit, SwiftUI

struct VotingAttributes: ActivityAttributes {
  public struct ContentState: Codable, Hashable {
    var voted: Int; var total: Int; var waitingOn: [String]; var status: String // "open" | "matched" | "close"
    var winner: String?
  }
  var planTitle: String; var groupName: String; var planId: String
}

struct VotingLiveActivity: Widget {
  var body: some WidgetConfiguration {
    ActivityConfiguration(for: VotingAttributes.self) { ctx in
      HStack(spacing: 12) {
        Ring(voted: ctx.state.voted, total: ctx.state.total).frame(width: 44, height: 44)
        VStack(alignment: .leading, spacing: 2) {
          Text(ctx.attributes.planTitle).font(.headline)
          Text(ctx.state.status == "matched" ? "It's a plan: \(ctx.state.winner ?? "")"
               : "Waiting on \(ctx.state.waitingOn.joined(separator: ", "))")
            .font(.subheadline).foregroundStyle(.secondary).lineLimit(1)
        }
        Spacer()
      }.padding().activityBackgroundTint(Color("Surface")).widgetURL(URL(string: "datemeup://plan/\(ctx.attributes.planId)"))
    } dynamicIsland: { ctx in
      DynamicIsland {
        DynamicIslandExpandedRegion(.leading) { Ring(voted: ctx.state.voted, total: ctx.state.total).frame(width: 36, height: 36) }
        DynamicIslandExpandedRegion(.center) { Text(ctx.attributes.planTitle).font(.headline).lineLimit(1) }
        DynamicIslandExpandedRegion(.bottom) { Text("Waiting on \(ctx.state.waitingOn.joined(separator: ", "))").font(.caption) }
      } compactLeading: { Ring(voted: ctx.state.voted, total: ctx.state.total).frame(width: 18, height: 18) }
        compactTrailing: { Text("\(ctx.state.voted)/\(ctx.state.total)").font(.caption2).monospacedDigit() }
        minimal: { Ring(voted: ctx.state.voted, total: ctx.state.total) }
    }
  }
}
struct Ring: View { let voted: Int; let total: Int
  var body: some View { ZStack {
    Circle().stroke(Color.gray.opacity(0.25), lineWidth: 4)
    Circle().trim(from: 0, to: CGFloat(voted) / CGFloat(max(total, 1)))
      .stroke(Color("Teal500"), style: StrokeStyle(lineWidth: 4, lineCap: .round)).rotationEffect(.degrees(-90))
  } } }
```
**Server updates** via APNs (`apns-push-type: liveactivity`, topic `<bundleId>.push-type.liveactivity`). The app registers the activity's push token with `POST /api/live-activities {proposalId, token}`.
```ts
// api/src/push/liveActivity.ts — uses node:http2 + ES256 JWT (p8 key in Secret Manager)
const payload = { aps: { timestamp: Math.floor(Date.now()/1000), event: status === "open" ? "update" : "end",
  "content-state": { voted, total, waitingOn, status, winner },
  ...(status !== "open" ? { "dismissal-date": Math.floor(Date.now()/1000) + 3600 } : {}) } };
await apns.send({ token, topic: `${BUNDLE_ID}.push-type.liveactivity`, pushType: "liveactivity", priority: 10, payload });
```
Live Activities are optional for users and off by default for plans with more than 6 members. Store the push tokens in a `LiveActivityToken` table (§13).

**c) Home Screen widget: "Next plan"**
Small: the next decided plan's title, day and time, plus the group avatars. Medium: adds the "Waiting on you" count for open plans. It reads from an App Group shared container that the app writes on every plans sync (`expo-shared-preferences`-style native module or `react-native-shared-group-preferences`).

**d) Haptics everywhere per §2.1, plus SF Symbols** for system-ish icons (share, calendar, settings) via `expo-symbols`, so those feel native. The custom illustrator icons are for brand-ish icons (vote, categories).

**e) Sign in with Apple:** already in your store list.

### 9.2 Android
**a) Edge-to-edge + predictive back**
```json
// app.json (Expo SDK 52+)
{ "expo": { "android": { "edgeToEdgeEnabled": true, "predictiveBackGestureEnabled": true } } }
```
If the SDK version lacks these keys, use `react-native-edge-to-edge` and add `android:enableOnBackInvokedCallback="true"` to `<application>` via a config plugin. Test that every screen insets correctly under the gesture bar and that predictive back shows the previous screen peek (which depends on your M3 back-stack fix).

**b) Material motion, not iOS motion.** On Android, use shared-axis (X) transitions for forward/back navigation and fade-through for tab switches:
```ts
// Expo Router / React Navigation stack options, Android only
screenOptions={Platform.OS === "android" ? { animation: "fade_from_bottom" /* or "slide_from_right" with 300ms */, animationDuration: 300 } : undefined}
```
Ripples: on Android, `PressableScale` also sets `android_ripple={{ color: "rgba(18,163,158,0.12)", borderless: false }}`.

**c) Themed (monochrome) app icon** for Android 13+ themed icons:
```json
{ "expo": { "android": { "adaptiveIcon": { "foregroundImage": "./assets/icon-fg.png", "backgroundColor": "#0E8A86", "monochromeImage": "./assets/icon-mono.png" } } } }
```

**d) Home Screen widget (Jetpack Glance):** same content as the iOS widget. Kotlin, added via a config plugin (`react-native-android-widget` is a JS-driven alternative if native Kotlin is unwanted).
```kotlin
class NextPlanWidget : GlanceAppWidget() {
  override suspend fun provideGlance(context: Context, id: GlanceId) {
    val plan = PlanStore.read(context)            // written by the app via SharedPreferences on sync
    provideContent {
      GlanceTheme {
        Column(GlanceModifier.fillMaxSize().background(GlanceTheme.colors.surface).padding(16.dp)
          .clickable(actionStartActivity(Intent(Intent.ACTION_VIEW, Uri.parse("datemeup://plan/${plan?.id}"))))) {
          Text(plan?.title ?: "No plans yet", style = TextStyle(fontWeight = FontWeight.Bold, fontSize = 16.sp))
          Text(plan?.whenLabel ?: "Start one in DateMeUp", style = TextStyle(fontSize = 13.sp, color = GlanceTheme.colors.onSurfaceVariant))
        }
      }
    }
  }
}
```

**e) Notification channels:** §8.6.

**f) Text fields:** the keyboard action button ("Next"/"Done") matches the context. `returnKeyType="send"` on comments submits; `returnKeyType="done"` on titles dismisses. Testing showed the keyboard needed Back to close; fix that with `blurOnSubmit` and `Keyboard.dismiss()` on scroll (`keyboardDismissMode="on-drag"`).

### 9.3 Web: the front door for invitees
Invitees usually meet DateMeUp on the web first, through a shared link, so polish the web flows in this order:

**a) Public plan page `/p/:token`:** the first thing a non-user sees:
- Hero: the rendered invite card (§6) at the top, then the options as cards with the vote bar.
- **Vote as a guest** with first name only (`guestVotes` already exists in the tally). One tap per option, then "Get the app to see when it's decided" with store badges plus a "Text me the result" option (optional: needs SMS provider; skip if not wanted).
- Members' names appear only after you've voted (privacy plus curiosity).
- Above the fold on a 375×667 viewport: title, date, first option, and the vote buttons.

**b) Install & app handoff:** on iOS Safari, the `apple-itunes-app` smart banner (§6.3). On Android Chrome, a slim custom banner "Open in app" that uses an `intent://` URL with fallback.

**c) PWA basics** (makes the web feel like an app when saved):
```json
// web/public/manifest.webmanifest
{ "name": "DateMeUp", "short_name": "DateMeUp", "start_url": "/?src=pwa", "display": "standalone",
  "background_color": "#F6F5F2", "theme_color": "#0E8A86",
  "icons": [{ "src": "/icons/192.png", "sizes": "192x192", "type": "image/png" },
            { "src": "/icons/512.png", "sizes": "512x512", "type": "image/png" },
            { "src": "/icons/maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable" }] }
```
```html
<link rel="manifest" href="/manifest.webmanifest">
<meta name="theme-color" content="#0E8A86">
<link rel="apple-touch-icon" href="/icons/apple-180.png">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
```

**d) Page transitions:** use cross-document or SPA **View Transitions** for list → plan (the card morphs into the plan header):
```css
@view-transition { navigation: auto; }
.plan-card[data-id] { view-transition-name: var(--vt-name); }   /* set inline: style="--vt-name: plan-<id>" */
::view-transition-old(root), ::view-transition-new(root) { animation-duration: var(--motion-duration-base); }
@media (prefers-reduced-motion: reduce) { ::view-transition-group(*) { animation: none; } }
```

**e) Desktop layout:** the plan page uses a 2-column layout ≥ 1024px (options left, sticky sidebar right with the voter ring, deadline and discussion). Discussion moves to the sidebar on desktop and below the options on mobile. **Max content width 1120px.** Today the page is a narrow column in a wide grey field; center it with a gentle background texture or illustration margin art at ≥ 1440px.

**f) Hover and focus:** every card and button gets a hover state (§1.3), with focus-visible rings throughout and a skip link (`<a class="skip" href="#main">Skip to content</a>`).

**g) Empty and loading states:** skeletons (§11) for Plans, Groups, Discover and the plan page. Never a blank white panel or a spinner in the middle of the page.

---

## 10. Voice, copy & the string catalog

> **Provides the strings your G2 fix needs.** Your fix decides *when* each string is used; this decides *what it says*.

### 10.1 Voice
- **Warm, brief, slightly wry.** Like a friend who's good at planning, not a hype-man.
- Use people's **names**, not "a member" or "your partner".
- **No exclamation marks** except the match moment's title (and even that is optional; "It's a plan." reads more confident).
- **Sentence case** everywhere. No Title Case Buttons.
- **Verbs on buttons:** "Send to Trio Date Club", "Add to calendar", "Browse ideas". Never "OK" or "Submit".
- Errors say what happened plus what to do, and never "Something went wrong".

### 10.2 One vocabulary, every platform
| Concept | Use | Don't use |
|---|---|---|
| A proposal | **plan** | proposal, date plan, event |
| An option | **idea** (when choosing), **pick** (the winner) | activity, option |
| Vote values | **I'm in · Maybe · Not for me** | Yes/No (mobile), "Don't think so" (web), 👍🤔🙅 |
| Decided | **It's a plan** | It's a match, Locked in, Decided |
| Group | **group** (crew in casual copy is fine) | couple (unless type = couple) |

> "I'm in / Maybe / Not for me" keeps the playful web labels but makes "No" softer and clearer than "Don't think so". It's the same on all three platforms.

### 10.3 String catalog (ICU MessageFormat), `shared/i18n/en.json` (excerpt; Spanish mirrors keys)
```json
{
  "vote.groupLabel": "Your vote",
  "vote.APPROVE": "I'm in",
  "vote.MAYBE": "Maybe",
  "vote.REJECT": "Not for me",
  "vote.count": "{count, plural, =0 {No votes yet} one {# vote} other {# votes}}",

  "plan.waitingOn": "{count, plural, =0 {Everyone's voted} one {Waiting on {names}} other {Waiting on {names}}}",
  "plan.youreLast": "You're the last vote",
  "plan.everyoneIn": "{memberCount, plural, =2 {You're both in} other {Everyone's in}}",
  "plan.itsAPlan": "It's a plan.",
  "plan.itsAPlanSub": "{memberCount, plural, =2 {You're both in for {pick}} other {All {memberCount} of you are in for {pick}}} · {when}",
  "plan.soClose": "So close.",
  "plan.soCloseSub": "{pick} got the most love. Lock it in, or try a few new ideas?",
  "plan.sentBanner": "Sent to {group}. We'll ping you when everyone's voted.",

  "empty.noPlans.title": "No plans yet",
  "empty.noPlans.body": "Start with a few ideas. Your group votes, the app does the deciding.",
  "empty.noPlans.cta": "Browse ideas",
  "empty.noGroups.title": "Plans are better together",
  "empty.noGroups.body": "Make a group for your partner, your friends, or the Thursday crew.",
  "empty.noGroups.cta": "Make a group",
  "empty.discover.title": "Nothing nearby for that",
  "empty.discover.body": "Try a wider area or a different day.",

  "calendar.added": "In your calendar",
  "calendar.failTitle": "Couldn't reach your calendar",
  "calendar.failBody": "You can add it from the invite file instead. It works with any calendar app.",
  "calendar.downloadIcs": "Get the invite file",

  "perm.location.title": "Show me what's nearby?",
  "perm.location.body": "We use your location only to find things to do around you, never to share where you are.",
  "perm.location.cta": "Use my location",
  "perm.location.alt": "Choose a city instead",
  "perm.notif.title": "Want a heads-up when everyone's voted?",
  "perm.notif.cta": "Notify me",

  "error.network.title": "You're offline",
  "error.network.body": "We'll send your vote as soon as you're back.",
  "common.notNow": "Not now",
  "common.tryAgain": "Try again"
}
```
Use `@formatjs/intl` (web) and `react-intl` or `i18next` + `i18next-icu` (mobile), sharing the same JSON from a `shared/` package. Format names with `Intl.ListFormat` ("G R and Demo", "Jake, G R, and Demo").

### 10.4 Copy lint (CI)
```ts
// scripts/copy-lint.ts — fails CI on vibe-code tells in string catalogs
const banned = [/!{1}(?=\s|$)/, /something went wrong/i, /\bpartner\b/i, /\bsubmit\b/i, /[\u{1F300}-\u{1FAFF}]/u, /lorem|placeholder|TODO/i, /togetherplans/i];
const allowExclaim = new Set(["plan.itsAPlan"]);
for (const [k, v] of Object.entries(require("../shared/i18n/en.json") as Record<string,string>))
  for (const re of banned) if (re.test(v) && !(re.source.startsWith("!") && allowExclaim.has(k)))
    { console.error(`copy-lint: ${k} → ${v} (${re})`); process.exitCode = 1; }
```
`partner` is allowed only in keys prefixed `couple.`. Extend the allowlist as needed.

---

## 11. Perceived performance (fast *feels* premium)

### 11.1 Image placeholders with blurhash
At ingest (when an option or Discover item is saved), compute a blurhash and the dominant color, so cards paint instantly with a soft preview:
```ts
// services/image-pipeline (Cloud Run job or inline in API)
import sharp from "sharp"; import { encode } from "blurhash";
export async function hashImage(url: string) {
  const buf = Buffer.from(await (await fetch(url)).arrayBuffer());
  const { data, info } = await sharp(buf).resize(32, 32, { fit: "inside" }).ensureAlpha().raw().toBuffer({ resolveWithObject: true });
  const blurhash = encode(new Uint8ClampedArray(data), info.width, info.height, 4, 3);
  const { dominant } = await sharp(buf).stats();
  return { blurhash, dominant: `rgb(${dominant.r},${dominant.g},${dominant.b})` };
}
```
Mobile: `expo-image` with `placeholder={{ blurhash }}`, `transition={200}` and `contentFit="cover"`. Web: paint the dominant color as background, then fade the `<img>` in on `load`.

### 11.2 Image CDN and sizing
Ticketmaster and Places images vary wildly in crop and size. Proxy them through **one** resizer so every card gets a consistent 16:9 crop at the right density:
- **Option A (simplest, web is on Cloudflare):** Cloudflare Images "transform via URL" (`/cdn-cgi/image/width=640,height=360,fit=cover,format=auto/<src>`).
- **Option B (GCP):** a Cloud Run `image-proxy` (sharp) behind Cloud CDN, with an allowlist of source hosts (`s1.ticketm.net`, `places.googleapis.com` photo media, your GCS bucket).

Prefer **Option A** for web and the mobile apps alike (same URLs), and keep the GCS bucket for your own renders (§6).

For Places photos, respect the attribution requirement: render `authorAttributions` small on the card (or in the details view).

### 11.3 Skeletons, prefetch, lists
- Skeletons mirror the real layout exactly (same card heights), so nothing jumps when data arrives.
- **Prefetch** a plan's detail when its card scrolls into view (or on `onPressIn`, before the tap completes).
- Use **FlashList** (`@shopify/flash-list`) for Discover and Plans lists, with `estimatedItemSize` set.
- **Optimistic navigation:** push the plan screen immediately, using the card's data as an initial render, then hydrate.

### 11.4 Offline vote queue
Votes made offline queue locally (MMKV) and flush on reconnect. The chip shows a small clock badge until it's confirmed, and the `error.network` toast appears once.

### 11.5 Budgets (fail CI if exceeded)
| Metric | Budget |
|---|---|
| Web LCP (p75, 4G mobile) | ≤ 2.0 s |
| Web JS (initial, gzipped) | ≤ 180 KB |
| Web CLS | ≤ 0.02 |
| Mobile cold start → first plan list (mid-range Android) | ≤ 2.0 s |
| Vote tap → UI change | 1 frame (optimistic) |
| Any animation | 60 fps on Pixel 6a / iPhone 12 |

Lighthouse CI on the web (`/`, `/p/:token` fixture, plan page), and a Reassure or Flashlight run for Android performance.

---

## 12. Google Cloud components

### 12.1 Enable APIs
```bash
PROJECT=datemeup   # use the actual project ID
gcloud config set project $PROJECT
gcloud services enable run.googleapis.com cloudtasks.googleapis.com cloudscheduler.googleapis.com \
  artifactregistry.googleapis.com secretmanager.googleapis.com storage.googleapis.com compute.googleapis.com \
  routes.googleapis.com places.googleapis.com weather.googleapis.com
```

### 12.2 Card bucket + Cloud CDN
```bash
REGION=us-east4
gcloud storage buckets create gs://$PROJECT-cards --location=$REGION --uniform-bucket-level-access
# Public GET only, no LIST. roles/storage.objectViewer would also grant storage.objects.list and expose every card,
# and legacy roles can't be used with uniform bucket-level access, so use a custom role with get only:
gcloud iam roles create cardObjectGetOnly --project=$PROJECT --title="Card object get only" \
  --permissions=storage.objects.get --stage=GA
gcloud storage buckets add-iam-policy-binding gs://$PROJECT-cards --member=allUsers \
  --role=projects/$PROJECT/roles/cardObjectGetOnly
# Object paths contain unguessable hashes, so a card is reachable only by someone who was given its URL.
gcloud compute backend-buckets create cards-backend --gcs-bucket-name=$PROJECT-cards --enable-cdn \
  --cache-mode=CACHE_ALL_STATIC --default-ttl=86400 --max-ttl=31536000
gcloud compute url-maps create cards-map --default-backend-bucket=cards-backend
gcloud compute ssl-certificates create cards-cert --domains=cards.datemeup.app --global
gcloud compute target-https-proxies create cards-proxy --url-map=cards-map --ssl-certificates=cards-cert
gcloud compute addresses create cards-ip --global
gcloud compute forwarding-rules create cards-https --global --target-https-proxy=cards-proxy --ports=443 --address=cards-ip
# DNS: A record cards.datemeup.app → $(gcloud compute addresses describe cards-ip --global --format='value(address)')
```
> **Alternative if you'd rather not run a GCP load balancer** (≈$18/mo base): front the bucket with Cloudflare (R2 or a Cloudflare proxied CNAME to `storage.googleapis.com`). It's functionally equivalent. Pick one; don't do both.

### 12.3 Card renderer on Cloud Run (private)
```bash
gcloud artifacts repositories create services --repository-format=docker --location=$REGION
gcloud iam service-accounts create card-renderer
gcloud storage buckets add-iam-policy-binding gs://$PROJECT-cards \
  --member=serviceAccount:card-renderer@$PROJECT.iam.gserviceaccount.com --role=roles/storage.objectCreator
gcloud builds submit services/card-renderer --tag $REGION-docker.pkg.dev/$PROJECT/services/card-renderer:v1
gcloud run deploy card-renderer --image $REGION-docker.pkg.dev/$PROJECT/services/card-renderer:v1 \
  --region $REGION --service-account card-renderer@$PROJECT.iam.gserviceaccount.com \
  --no-allow-unauthenticated --cpu 1 --memory 1Gi --concurrency 8 --min-instances 0 --max-instances 10 \
  --set-env-vars CARD_BUCKET=$PROJECT-cards,CDN_BASE=https://cards.datemeup.app
# allow the API's service account to invoke:
gcloud run services add-iam-policy-binding card-renderer --region $REGION \
  --member=serviceAccount:<api-sa>@$PROJECT.iam.gserviceaccount.com --role=roles/run.invoker
```
`services/card-renderer/Dockerfile`:
```dockerfile
FROM node:20-slim
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev
COPY . .
RUN npm run build
ENV NODE_ENV=production
CMD ["node", "dist/index.js"]
```
API → renderer call with an ID token:
```ts
import { GoogleAuth } from "google-auth-library";
const auth = new GoogleAuth();
export async function callRenderer(body: unknown) {
  const client = await auth.getIdTokenClient(process.env.RENDERER_URL!);
  const r = await client.request({ url: `${process.env.RENDERER_URL}/render`, method: "POST", data: body, timeout: 15000 });
  return r.data as Record<string, string>;
}
```
> If the API itself is **not** on GCP, use a dedicated service account key stored in the API's secret store, or Workload Identity Federation, to mint the ID token.

### 12.4 Scheduled jobs & queues
```bash
gcloud tasks queues create notif-batch --location=$REGION --max-dispatches-per-second=20
gcloud scheduler jobs create http refresh-taste   --location=$REGION --schedule="15 4 * * *"  --time-zone="America/New_York" \
  --uri=https://api.datemeup.app/internal/jobs/refresh-taste --http-method=POST --oidc-service-account-email=scheduler@$PROJECT.iam.gserviceaccount.com
gcloud scheduler jobs create http weather-check   --location=$REGION --schedule="0 */3 * * *" --time-zone="America/New_York" \
  --uri=https://api.datemeup.app/internal/jobs/weather-check --http-method=POST --oidc-service-account-email=scheduler@$PROJECT.iam.gserviceaccount.com
gcloud scheduler jobs create http event-status    --location=$REGION --schedule="30 5 * * *" --time-zone="America/New_York" \
  --uri=https://api.datemeup.app/internal/jobs/refresh-event-status --http-method=POST --oidc-service-account-email=scheduler@$PROJECT.iam.gserviceaccount.com
```
`/internal/jobs/*` must verify the OIDC token (`aud` = the URL; `email` = the scheduler SA), and reject anything else.

### 12.5 Secrets & keys
```bash
printf '%s' "$APNS_P8" | gcloud secrets create apns-p8 --data-file=-
gcloud secrets create routes-key --data-file=<(printf '%s' "$ROUTES_KEY")
gcloud secrets create weather-key --data-file=<(printf '%s' "$WEATHER_KEY")
```
**API key separation:** create **server-only** keys for Routes, Weather and Places (server calls), restricted by **API** (only that API) and by **IP** (the API's egress) where possible. They must never ship in the app bundle. Client-side Maps keys stay separately restricted (as already in your store checklist).

### 12.6 Budgets
```bash
gcloud billing budgets create --billing-account=<ACCOUNT> --display-name="DateMeUp monthly" --budget-amount=150USD \
  --threshold-rule=percent=0.5 --threshold-rule=percent=0.9 --threshold-rule=percent=1.0
```
Also set **per-API quotas** in the console (APIs & Services → Routes API → Quotas): e.g., 2,000 matrix elements/day at launch.

---

## 13. Data model, flags & rollout

### 13.1 New Prisma models (consolidated)
```prisma
model ProposalMemberState { id String @id @default(cuid()) proposalId String userId String
  matchSeenAt DateTime? noConsensusSeenAt DateTime? lastViewedAt DateTime @default(now())
  @@unique([proposalId, userId]) @@index([userId]) }

model UserArea { userId String @id lat Float lng Float label String updatedAt DateTime @updatedAt }

model UserPrefs { userId String @id haptics Boolean @default(true) sounds Boolean @default(false)
  liveActivities Boolean @default(true) quietStart Int @default(22) quietEnd Int @default(8) tz String @default("America/New_York") }

model CardRender { id String @id @default(cuid()) proposalId String key String templateId String urls Json createdAt DateTime @default(now())
  @@unique([proposalId, key]) }

model LiveActivityToken { id String @id @default(cuid()) proposalId String userId String token String createdAt DateTime @default(now())
  @@unique([proposalId, userId]) }

model OptionEnrichment { optionId String @id blurhash String? dominant String? weather Json? eventStatus String? updatedAt DateTime @updatedAt }
```

### 13.2 New endpoints (summary)
| Method | Path | Purpose |
|---|---|---|
| POST | `/proposals/:id/moments/:moment/seen` | match / noConsensus seen |
| POST | `/cards/render` | render or fetch cached invite card |
| GET | `/public/plans/:token/preview` | OG data for link previews |
| GET/PUT | `/me/area` | opt-in home area for fairness ranking |
| GET/PUT | `/me/prefs` | haptics, sounds, quiet hours, live activities |
| POST | `/live-activities` | register a Live Activity push token |
| GET | `/discover?groupId=…` | adds `fairnessMinutes`, taste-ranked order |
| POST | `/internal/jobs/{refresh-taste,weather-check,refresh-event-status}` | scheduler-only |

### 13.3 Settings screen additions
Under Settings → **Experience**: Haptics, Sounds, Live Activities (iOS), Quiet hours, My area (with a "Used only to suggest fair meeting spots" explainer). Use your existing toggle component, styled per tokens.

### 13.4 Feature flags
Flags: `craft.voteBar`, `craft.matchReveal`, `craft.sentFlow`, `craft.illustrations`, `craft.cards.server`, `craft.fairness`, `craft.taste`, `craft.weather`, `craft.liveActivity`, `craft.widgets`, `craft.webPublicPlan`.

Serve them from `/me/flags` (static JSON in the API config is fine). Default **on** in internal builds; turn them on in production one at a time after the QA pass (§14). Illustrations fall back to the current visuals if `craft.illustrations` is off, so art arriving late doesn't block launch.

---

## 14. QA: the "is it still vibe-coded?" audit

Run on a real iPhone, a real Pixel and desktop plus mobile Safari and Chrome. Record a screen video of each flow and review it at 0.25× speed.

### 14.1 Flow checklist
- [ ] **Vote:** chip fills with a spring, glyph pops, haptic fires, count ticks, **no layout shift** (overlay the before/after frames to check).
- [ ] **Vote fails** (airplane mode mid-request): shake, error haptic, the vote shows a clock badge and then confirms on reconnect.
- [ ] **Note:** Save → "Saved ✓" morph → note appears in the breakdown under your name.
- [ ] **Send plan:** cards fly into avatars, you land on the plan with the banner, and your own vote section pulses.
- [ ] **Match:** full choreography once; reopening shows the calm decided view; a second device of the same user does **not** replay it (server `matchSeenAt`).
- [ ] **So close:** shown once; tone is gentle; actions from your C3 fix are present.
- [ ] **Calendar:** success morphs the button; failure shows a branded sheet with the `.ics` path (no system alert anywhere; check the ESLint rule passes).
- [ ] **Invite card:** identical in-app preview, shared PNG and link preview; no sample names or dates anywhere (contract test green).
- [ ] **Link preview:** pasting `/p/:token` into iMessage, WhatsApp and Slack shows the card image, title and description.
- [ ] **Web invitee:** open `/p/:token` logged out on a phone; vote as a guest in under 10 s; the smart banner offers the app.
- [ ] **Onboarding:** shown once per account (your A1); illustrations animate; Skip works; no permission prompts during onboarding.
- [ ] **Location primer** shows before the OS prompt; "Choose a city" fully works without location.
- [ ] **Discover from a group:** cards show "≤ N min for everyone"; ranking changes after votes (taste) on the next day.
- [ ] **Outdoor option with rain:** weather chip shown; no chip in good weather.
- [ ] **Notifications:** names-first copy, coalesced votes, rich match image, actions work, quiet hours respected, Android channels listed in system settings.
- [ ] **iOS:** Live Activity starts on plan creation and updates per vote; Dynamic Island compact view legible; widget shows the next plan.
- [ ] **Android:** edge-to-edge with correct insets on every screen; predictive back peek; themed icon; Glance widget.

### 14.2 Global sweeps
- [ ] `rg` emoji sweep (§1.6) returns zero hits in UI strings.
- [ ] Copy lint (§10.4) green; same vote labels on all three platforms.
- [ ] Every tappable element uses `PressableScale` (mobile) / `.btn` or `.card--interactive` (web).
- [ ] Every list and detail screen has a skeleton; there are no full-screen spinners.
- [ ] Every image has a blurhash or dominant-color placeholder and a consistent crop.
- [ ] Reduce Motion on (iOS/Android/OS-level for web): no flying, confetti or parallax; everything is still understandable.
- [ ] Largest Dynamic Type / 200% browser zoom: no clipped or overlapping text.
- [ ] VoiceOver/TalkBack: vote bar reads "Your vote, I'm in, radio button, 1 of 3, selected"; the match reveal announces "It's a plan, everyone's in for {pick}".
- [ ] Contrast ≥ 4.5:1 for text (run axe on web; Accessibility Inspector on iOS).
- [ ] Performance budgets (§11.5) green in CI.

### 14.3 Taste review (people, not checklists)
Show the build to **5 people who've never seen it**. Watch, don't explain, and note every moment of hesitation or "huh". Then do the inverse of Chris's test: show the app side-by-side with two well-crafted competitors (e.g., Partiful for invites, Airbnb for cards and motion). Anything that looks *obviously* less considered goes back into the queue.

---

## 15. Effort summary

| Area | Eng days | Notes |
|---|---|---|
| Tokens, fonts, icons, strings, lint rules (§1, §10) | 3 | Do first. |
| Haptics, press physics, sheets, toasts (§2, §3.6–3.7) | 2 | |
| Vote bar, option card, note states, web keyboard (§3.2–3.5) | 3 | |
| Match reveal, sent flow, so-close, voter ring (§4) | 5 | The "6 hours on an animation" work. Budget iteration time. |
| Illustration integration + Rive (§5) | 3 | Plus the artist: 2–3 weeks, ~$1.5–4k. |
| Card renderer + OG + share (§6, §12.2–12.3) | 4 | |
| Onboarding + permission primers (§7) | 3 | Waits on art for final polish. |
| Fairness, taste, weather, pairing, event status (§8.1–8.5) | 6 | |
| Notification copy, rich, actions, channels, batching (§8.6) | 3 | On top of your N1. |
| iOS Live Activity + widget (§9.1) | 4 | Native Swift targets via config plugins. |
| Android edge-to-edge, motion, icon, Glance widget (§9.2) | 3 | |
| Web front door, PWA, view transitions, desktop layout (§9.3) | 4 | |
| Perf: blurhash, image proxy, skeletons, offline queue (§11) | 3 | |
| QA audit + taste review + fixes (§14) | 4 | |
| **Total** | **≈ 50 eng days** | Parallelizable across 2 people in ~5 weeks. Art runs concurrently. |

---

*End of spec. Questions or decisions for the product owner are marked in context: font choice (§1.1), illustrator budget (§5.1), image CDN option (§11.2), load balancer vs. Cloudflare for cards (§12.2), SMS result option on web (§9.3a).*
