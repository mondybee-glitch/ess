#!/usr/bin/env python3
"""WCAG 2.x relative luminance contrast checker for #RRGGBB foreground/background."""
import argparse, re, sys
def linear(c):
    c=c/255
    return c/12.92 if c <= 0.04045 else ((c+0.055)/1.055)**2.4
def luminance(hex_color):
    if not re.fullmatch(r"#[0-9a-fA-F]{6}",hex_color): raise ValueError(f"invalid color: {hex_color}")
    rgb=[int(hex_color[i:i+2],16) for i in (1,3,5)]
    r,g,b=[linear(v) for v in rgb]
    return 0.2126*r+0.7152*g+0.0722*b
def ratio(fg,bg):
    a,b=sorted((luminance(fg),luminance(bg)),reverse=True)
    return (a+0.05)/(b+0.05)
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("foreground"); ap.add_argument("background")
    ap.add_argument("--large-text",action="store_true")
    args=ap.parse_args()
    r=ratio(args.foreground,args.background)
    required=3.0 if args.large_text else 4.5
    print(f"contrast_ratio={r:.2f}:1 required={required:.1f}:1 result={'PASS' if r>=required else 'FAIL'}")
    return 0 if r>=required else 1
if __name__=="__main__": raise SystemExit(main())
