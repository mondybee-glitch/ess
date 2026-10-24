---
name: web-motion-accessibility
description: Web motion accessibility for meaningful transitions, reduced-motion preferences, focus/state continuity, and non-motion alternatives. Use when adding or reviewing CSS or UI animation in a web product.
version: 0.6.0
---

# Web Motion Accessibility

## Use when
Use when adding, reviewing, or debugging web animation, transitions, loading motion, modal transitions, attention cues, or state changes.

## Do not use when
Do not use for static visual design with no motion, video production, or a browser performance issue unrelated to animation.

## Required inputs
Require the user goal for the motion, affected states, keyboard and screen-reader behavior, motion sensitivity requirements, supported browsers, duration/repeat budget, and a static or reduced-motion alternative.

## Workflow
1. Name the product meaning of the motion: orient, confirm, reveal, or direct attention. Reject decorative motion with no user benefit.
2. Preserve the functional state independently of the animation. A user must receive the same content, focus, status, and action path when motion is reduced or unavailable.
3. Implement and test `prefers-reduced-motion: reduce` without overriding the user's preference. Replace large travel or repeated motion with an instant or low-motion state change when appropriate.
4. Check focus order, keyboard operation, screen-reader announcements, loading/error states, and whether motion causes disorientation, flashing, clipping, or unexpected scrollbars.
5. Avoid animating root documents and inline-only elements without a deliberate layout strategy. Keep entrance/exit semantics understandable and reversible.
6. Verify normal, reduced-motion, keyboard, narrow viewport, and interrupted-animation states.

## Pass/fail checks
Pass only when the motion has a stated purpose, reduced-motion behavior is present and tested, functional state and focus remain correct, repeated/flashing motion is bounded, and a non-motion path is documented.

Required commands or procedures: run accessibility checks; emulate reduced motion; exercise keyboard focus and screen-reader-visible state; inspect screenshots or recordings at relevant viewports; record any unverified assistive-technology limitation.

## Hand-offs
Hand off visual timing and composition to `ui-ux-design`, implementation to `frontend-development`, and browser evidence to browser testing. Do not duplicate their ownership.

## Evidence to report
Report the purpose, state diagram, reduced-motion result, focus behavior, viewport evidence, duration/repetition values, browser versions, commands, and unresolved accessibility limits.
