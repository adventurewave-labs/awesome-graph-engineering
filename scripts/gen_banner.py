#!/usr/bin/env python3
"""Generate assets/banner.svg — original hero banner for awesome-graph-engineering.
Deterministic (no randomness) hand-composed layout: a 'single looping agent' glyph on the
left, the README title centered, and a small 'orchestrator + workers' graph glyph on the
right — visually encoding the repo's thesis (one agent loops; many agents need a graph).
"""
import math

W, H = 1200, 300
BG_TOP = "#14151a"
BG_BOTTOM = "#1f2128"
CORAL = "#ff6b6b"
CORAL_SOFT = "#ff8f8f"
WHITE = "#f5f5f7"
MUTED = "#9296a3"
FAINT = "#2a2c34"

def dot_grid(spacing=28, r=1, opacity=0.055):
    dots = []
    for x in range(spacing, W, spacing):
        for y in range(spacing, H, spacing):
            dots.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#ffffff" opacity="{opacity}"/>')
    return "\n".join(dots)

def loop_glyph(cx, cy):
    """Single node with a self-loop arrow -> 'one agent, a loop'."""
    r = 15
    # self-loop arc: a circle path around the node, open on one side, with an arrowhead
    loop_r = 30
    return f'''
    <g>
      <circle cx="{cx}" cy="{cy}" r="{loop_r+16}" fill="none" stroke="{FAINT}" stroke-width="1"/>
      <path d="M {cx-loop_r} {cy} A {loop_r} {loop_r} 0 1 1 {cx+ (loop_r*0.15):.1f} {cy-loop_r*0.98:.1f}"
            fill="none" stroke="{MUTED}" stroke-width="2.5" stroke-linecap="round"/>
      <polygon points="{cx+ (loop_r*0.15)-7:.1f},{cy-loop_r*0.98-6:.1f} {cx+ (loop_r*0.15)+8:.1f},{cy-loop_r*0.98-2:.1f} {cx+ (loop_r*0.15)-3:.1f},{cy-loop_r*0.98+8:.1f}"
               fill="{MUTED}"/>
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="{CORAL}"/>
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#ffffff" stroke-width="1" opacity="0.25"/>
    </g>'''

def graph_glyph(cx, cy):
    """Central orchestrator node + worker nodes in a ring, with connecting edges -> 'a graph'."""
    outer_r = 62
    n = 6
    nodes = []
    for i in range(n):
        angle = -math.pi/2 + i * (2*math.pi/n)
        x = cx + outer_r*math.cos(angle)
        y = cy + outer_r*math.sin(angle)
        nodes.append((x, y))
    edges = []
    for (x, y) in nodes:
        edges.append(f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{x:.1f}" y2="{y:.1f}" stroke="{CORAL_SOFT}" stroke-width="1.6" opacity="0.55"/>')
    # a couple of cross-links between adjacent workers to read as a graph, not just a star
    for i in (0, 2, 4):
        x1, y1 = nodes[i]
        x2, y2 = nodes[(i+1) % n]
        edges.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{MUTED}" stroke-width="1" opacity="0.35"/>')
    worker_circles = [f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="{WHITE}" opacity="0.9"/>' for (x, y) in nodes]
    return f'''
    <g>
      {"".join(edges)}
      {"".join(worker_circles)}
      <circle cx="{cx}" cy="{cy}" r="16" fill="{CORAL}"/>
      <circle cx="{cx}" cy="{cy}" r="16" fill="none" stroke="#ffffff" stroke-width="1" opacity="0.3"/>
    </g>'''

svg = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{BG_TOP}"/>
      <stop offset="100%" stop-color="{BG_BOTTOM}"/>
    </linearGradient>
    <linearGradient id="edge-fade" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{CORAL}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{CORAL}" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="{CORAL}" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <rect x="0" y="0" width="{W}" height="{H}" rx="18" fill="url(#bg)"/>
  {dot_grid()}

  <!-- one agent, a loop -->
  {loop_glyph(130, 150)}

  <!-- many agents, a graph -->
  {graph_glyph(1060, 150)}

  <!-- center title block -->
  <text x="600" y="98" text-anchor="middle" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
        font-size="13" letter-spacing="4" fill="{MUTED}" font-weight="600">ADVENTURE WAVE LABS</text>

  <text x="600" y="155" text-anchor="middle" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
        font-size="40" letter-spacing="0.5" fill="{WHITE}" font-weight="800">AWESOME GRAPH ENGINEERING</text>

  <rect x="565" y="172" width="70" height="3" rx="1.5" fill="{CORAL}"/>

  <text x="600" y="205" text-anchor="middle" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
        font-size="17" fill="#c7c9d1" font-weight="400">Multi-agent topology &#183; orchestration &#183; handoffs &#183; state</text>

  <text x="600" y="255" text-anchor="middle" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
        font-size="11" letter-spacing="1" fill="{MUTED}" opacity="0.7">ONE AGENT LOOPS &#8212; MANY AGENTS NEED A GRAPH</text>

  <text x="1150" y="286" text-anchor="end" font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
        font-size="10" letter-spacing="0.5" fill="{MUTED}" opacity="0.5">github.com/adventurewave-labs</text>
</svg>'''

with open("assets/banner.svg", "w") as f:
    f.write(svg)

print("wrote assets/banner.svg", len(svg), "bytes")
