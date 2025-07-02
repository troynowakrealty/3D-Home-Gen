import svgwrite
import json

SCALE = 4  # pixels per foot
MARGIN = 50

lot_width = 46
lot_depth = 124

front_setback = 18
rear_setback = 22

lot1_left_setback = 8
lot1_right_setback = 5

# mirrored for lot2
lot2_left_setback = 5
lot2_right_setback = 8

front_building_width = 33
front_building_depth = 28

adu_width = 30
adu_depth = 20

parking_width = 9
parking_depth = 20
parking_count = 3
trash_width = 6
trash_depth = 20

# Calculated constants
canvas_width = (lot_width * 2) * SCALE + MARGIN * 2
canvas_height = lot_depth * SCALE + MARGIN * 2

dwg = svgwrite.Drawing('output/siteplan_dual_lot.svg', size=(canvas_width, canvas_height))

# Styles
lot_style = {
    'stroke': 'black',
    'stroke_width': 3,
    'fill': 'none'
}
setback_style = {
    'stroke': 'none',
    'fill': 'grey',
    'fill_opacity': 0.15
}
building_style = {
    'stroke': 'black',
    'stroke_width': 1,
    'fill': '#cccccc'
}
parking_style = {
    'stroke': 'black',
    'stroke_width': 1,
    'fill': '#e0e0e0'
}

# Dimension arrow marker
arrow_marker = svgwrite.container.Marker(insert=(5,3), size=(6,6), orient='auto')
arrow_marker.add(svgwrite.path.Path('M0,0 L6,3 L0,6 Z', fill='black'))
dwg.defs.add(arrow_marker)

def dim_h(x1, x2, y, text):
    dwg.add(dwg.line((x1, y), (x2, y), stroke='black', stroke_width=1,
                     marker_start=arrow_marker.get_funciri(),
                     marker_end=arrow_marker.get_funciri()))
    dwg.add(dwg.text(text, insert=((x1 + x2) / 2, y - 5), text_anchor='middle', font_size=10))

def dim_v(y1, y2, x, text):
    dwg.add(dwg.line((x, y1), (x, y2), stroke='black', stroke_width=1,
                     marker_start=arrow_marker.get_funciri(),
                     marker_end=arrow_marker.get_funciri()))
    dwg.add(dwg.text(text, insert=(x + 5, (y1 + y2) / 2), font_size=10,
                     transform=f"rotate(-90,{x + 5},{(y1 + y2) / 2})",
                     text_anchor='middle'))

layout = []

# Helper to convert feet to pixels
ft = lambda x: x * SCALE

# Draw north arrow
arrow_start = (canvas_width - MARGIN, MARGIN + 40)
arrow_end = (canvas_width - MARGIN, MARGIN)
dwg.add(dwg.line(arrow_start, arrow_end, stroke='black', stroke_width=2))
dwg.add(dwg.polygon([
    (canvas_width - MARGIN - 5, MARGIN + 5),
    (canvas_width - MARGIN + 5, MARGIN + 5),
    (canvas_width - MARGIN, MARGIN - 5)
], fill='black'))
dwg.add(dwg.text('N', insert=(canvas_width - MARGIN - 10, MARGIN + 15), font_size=12, font_weight='bold'))

# Starting x positions for each lot
lot1_origin = (MARGIN, MARGIN)
lot2_origin = (MARGIN + ft(lot_width), MARGIN)

for idx, origin in enumerate([lot1_origin, lot2_origin], start=1):
    lot_x, lot_y = origin
    lot_left_setback = lot1_left_setback if idx == 1 else lot2_left_setback
    lot_right_setback = lot1_right_setback if idx == 1 else lot2_right_setback

    # Lot rectangle
    lot_rect = dwg.rect((lot_x, lot_y), (ft(lot_width), ft(lot_depth)), **lot_style)
    dwg.add(lot_rect)
    layout.append({'type': 'rectangle', 'name': f'Lot{idx}', 'x': lot_x, 'y': lot_y, 'width': ft(lot_width), 'height': ft(lot_depth)})

    # Lot dimensions
    dim_h(lot_x, lot_x + ft(lot_width), lot_y + ft(lot_depth) + 20, f"{lot_width}'")
    dim_v(lot_y, lot_y + ft(lot_depth), lot_x + ft(lot_width) + 20, f"{lot_depth}'")

    # Shade setbacks
    # Front
    dwg.add(dwg.rect((lot_x, lot_y + ft(lot_depth - front_setback)), (ft(lot_width), ft(front_setback)), **setback_style))
    # Rear
    dwg.add(dwg.rect((lot_x, lot_y), (ft(lot_width), ft(rear_setback)), **setback_style))
    # Left
    dwg.add(dwg.rect((lot_x, lot_y), (ft(lot_left_setback), ft(lot_depth)), **setback_style))
    # Right
    dwg.add(dwg.rect((lot_x + ft(lot_width - lot_right_setback), lot_y), (ft(lot_right_setback), ft(lot_depth)), **setback_style))

    # Front building position
    bld_x = lot_x + ft(lot_left_setback)
    bld_y = lot_y + ft(lot_depth - front_setback - front_building_depth)
    front_rect = dwg.rect((bld_x, bld_y), (ft(front_building_width), ft(front_building_depth)), **building_style)
    dwg.add(front_rect)
    dwg.add(dwg.text('Front Unit', insert=(bld_x + ft(front_building_width/2), bld_y + ft(front_building_depth/2)), text_anchor='middle', alignment_baseline='middle', font_size=12))

    layout.append({'type': 'rectangle', 'name': f'FrontUnit{idx}', 'x': bld_x, 'y': bld_y, 'width': ft(front_building_width), 'height': ft(front_building_depth)})

    # Front building dimensions
    dim_h(bld_x, bld_x + ft(front_building_width), bld_y - 10, f"{front_building_width}'")
    dim_v(bld_y, bld_y + ft(front_building_depth), bld_x - 10, f"{front_building_depth}'")

    # ADU position
    adu_x = lot_x + ft((lot_width - adu_width)/2)
    adu_y = lot_y + ft(rear_setback)
    adu_rect = dwg.rect((adu_x, adu_y), (ft(adu_width), ft(adu_depth)), **building_style)
    dwg.add(adu_rect)
    dwg.add(dwg.text('Garage/ADU', insert=(adu_x + ft(adu_width/2), adu_y + ft(adu_depth/2)), text_anchor='middle', alignment_baseline='middle', font_size=12))

    layout.append({'type': 'rectangle', 'name': f'GarageADU{idx}', 'x': adu_x, 'y': adu_y, 'width': ft(adu_width), 'height': ft(adu_depth)})

    # ADU dimensions
    dim_h(adu_x, adu_x + ft(adu_width), adu_y - 10, f"{adu_width}'")
    dim_v(adu_y, adu_y + ft(adu_depth), adu_x - 10, f"{adu_depth}'")

    # Parking and trash behind ADU
    parking_y = lot_y
    parking_x = lot_x + ft(lot_left_setback)
    for p in range(parking_count):
        px = parking_x + ft(p * parking_width)
        rect = dwg.rect((px, parking_y), (ft(parking_width), ft(parking_depth)), **parking_style)
        dwg.add(rect)
        dwg.add(dwg.text(f'Parking {p+1}', insert=(px + ft(parking_width/2), parking_y + ft(parking_depth/2)), text_anchor='middle', alignment_baseline='middle', font_size=10))
        layout.append({'type': 'rectangle', 'name': f'Parking{idx}_{p+1}', 'x': px, 'y': parking_y, 'width': ft(parking_width), 'height': ft(parking_depth)})

    trash_x = parking_x + ft(parking_width * parking_count)
    trash_rect = dwg.rect((trash_x, parking_y), (ft(trash_width), ft(trash_depth)), **parking_style)
    dwg.add(trash_rect)
    dwg.add(dwg.text('Trash Pad', insert=(trash_x + ft(trash_width/2), parking_y + ft(trash_depth/2)), text_anchor='middle', alignment_baseline='middle', font_size=10))
    layout.append({'type': 'rectangle', 'name': f'TrashPad{idx}', 'x': trash_x, 'y': parking_y, 'width': ft(trash_width), 'height': ft(trash_depth)})

    # Parking dimension line
    dim_h(parking_x, trash_x + ft(trash_width), parking_y - 10, f"{parking_width*parking_count + trash_width}'")
    dim_v(parking_y, parking_y + ft(parking_depth), parking_x - 10, f"{parking_depth}'")

# Save SVG
dwg.save()

with open('output/layout.json', 'w') as f:
    json.dump(layout, f, indent=2)

print(json.dumps(layout, indent=2))
