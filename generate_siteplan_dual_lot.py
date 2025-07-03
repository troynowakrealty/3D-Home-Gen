import svgwrite
import json

SCALE = 4  # pixels per foot
MARGIN = 50

lot1_width = 46
lot2_width = 45.98
lot_widths = [lot1_width, lot2_width]
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
trash_width = 4
trash_depth = 9

# Calculated constants
canvas_width = sum(lot_widths) * SCALE + MARGIN * 2
canvas_height = lot_depth * SCALE + MARGIN * 2


dwg = svgwrite.Drawing('output/siteplan_dual_lot.svg', size=(canvas_width, canvas_height))
# Ensure exports have a white background instead of transparent
dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill='white'))

# Styles
lot_style = {
    'stroke': 'black',
    'stroke_width': 2,
    'stroke_dasharray': '4,4',
    'fill': 'none'
}
setback_fill_style = {
    'stroke': 'none',
    'fill': 'grey',
    'fill_opacity': 0.15
}
setback_line_style = {
    'stroke': 'black',
    'stroke_width': 1,
    'fill': 'none',
    'stroke_dasharray': '4,4'
}
building_style = {
    'stroke': 'black',
    'stroke_width': 2,
    'fill': '#dddddd'
}
parking_style = {
    'stroke': 'black',
    'stroke_width': 1,
    'fill': '#eeeeee'
}
trash_style = {
    'stroke': 'black',
    'stroke_width': 1,
    'stroke_dasharray': '2,2',
    'fill': 'none'
}

# Dimension arrow marker
arrow_marker = svgwrite.container.Marker(insert=(5,3), size=(6,6), orient='auto')
arrow_marker.add(svgwrite.path.Path('M0,0 L6,3 L0,6 Z', fill='black'))
dwg.defs.add(arrow_marker)

def dim_h(x1, x2, y, text):
    dwg.add(dwg.line((x1, y), (x2, y), stroke='black', stroke_width=1,
                     marker_start=arrow_marker.get_funciri(),
                     marker_end=arrow_marker.get_funciri()))
    dwg.add(dwg.text(text, insert=((x1 + x2) / 2, y - 5), text_anchor='middle', font_size=10, font_family='sans-serif'))

def dim_v(y1, y2, x, text):
    dwg.add(dwg.line((x, y1), (x, y2), stroke='black', stroke_width=1,
                     marker_start=arrow_marker.get_funciri(),
                     marker_end=arrow_marker.get_funciri()))
    dwg.add(dwg.text(text, insert=(x + 5, (y1 + y2) / 2), font_size=10,
                     transform=f"rotate(-90,{x + 5},{(y1 + y2) / 2})",
                     text_anchor='middle', font_family='sans-serif'))

layout = []

# Helper to convert feet to pixels
ft = lambda x: x * SCALE

lot_left = MARGIN
lot_right = lot_left + ft(sum(lot_widths))
lot_top = MARGIN
lot_bottom = lot_top + ft(lot_depth)

# Draw north arrow
arrow_start = (canvas_width - MARGIN, MARGIN + 40)
arrow_end = (canvas_width - MARGIN, MARGIN)
dwg.add(dwg.line(arrow_start, arrow_end, stroke='black', stroke_width=2))
dwg.add(dwg.polygon([
    (canvas_width - MARGIN - 5, MARGIN + 5),
    (canvas_width - MARGIN + 5, MARGIN + 5),
    (canvas_width - MARGIN, MARGIN - 5)
], fill='black'))
dwg.add(dwg.text('N', insert=(canvas_width - MARGIN, MARGIN + 15), font_size=12, font_weight='bold'))

# Starting x positions for each lot
lot1_origin = (MARGIN, MARGIN)
lot2_origin = (MARGIN + ft(lot1_width), MARGIN)

for idx, origin in enumerate([lot1_origin, lot2_origin], start=1):
    lot_x, lot_y = origin
    lot_width = lot1_width if idx == 1 else lot2_width
    lot_left_setback = lot1_left_setback if idx == 1 else lot2_left_setback
    lot_right_setback = lot1_right_setback if idx == 1 else lot2_right_setback

    # Lot rectangle
    lot_rect = dwg.rect((lot_x, lot_y), (ft(lot_width), ft(lot_depth)), **lot_style)
    dwg.add(lot_rect)
    layout.append({'type': 'rectangle', 'name': f'Lot{idx}', 'x': lot_x, 'y': lot_y, 'width': ft(lot_width), 'height': ft(lot_depth)})

    dwg.add(dwg.text(f'Lot {idx}', insert=(lot_x + 5, lot_y + ft(lot_depth) + 30), font_size=12, font_family='sans-serif'))

    # Lot dimensions
    dim_h(lot_x, lot_x + ft(lot_width), lot_y + ft(lot_depth) + 20, f"{lot_width}'")
    dim_v(lot_y, lot_y + ft(lot_depth), lot_x + ft(lot_width) + 20, f"{lot_depth}'")

    # Shade setbacks
    # Front
    dwg.add(dwg.rect((lot_x, lot_y + ft(lot_depth - front_setback)), (ft(lot_width), ft(front_setback)), **setback_fill_style))
    # Rear
    dwg.add(dwg.rect((lot_x, lot_y), (ft(lot_width), ft(rear_setback)), **setback_fill_style))
    # Left
    dwg.add(dwg.rect((lot_x, lot_y), (ft(lot_left_setback), ft(lot_depth)), **setback_fill_style))
    # Right
    dwg.add(dwg.rect((lot_x + ft(lot_width - lot_right_setback), lot_y), (ft(lot_right_setback), ft(lot_depth)), **setback_fill_style))

    front_line_y = lot_y + ft(lot_depth - front_setback)
    rear_line_y = lot_y + ft(rear_setback)
    left_line_x = lot_x + ft(lot_left_setback)
    right_line_x = lot_x + ft(lot_width - lot_right_setback)
    dwg.add(dwg.line((lot_x, front_line_y), (lot_x + ft(lot_width), front_line_y), **setback_line_style))
    dwg.add(dwg.line((lot_x, rear_line_y), (lot_x + ft(lot_width), rear_line_y), **setback_line_style))
    dwg.add(dwg.line((left_line_x, lot_y), (left_line_x, lot_y + ft(lot_depth)), **setback_line_style))
    dwg.add(dwg.line((right_line_x, lot_y), (right_line_x, lot_y + ft(lot_depth)), **setback_line_style))

    dim_v(front_line_y, lot_y + ft(lot_depth), left_line_x - 15, f"{front_setback}'")
    dim_v(lot_y, rear_line_y, left_line_x - 15, f"{rear_setback}'")
    dim_h(lot_x, left_line_x, front_line_y + 15, f"{lot_left_setback}'")
    dim_h(right_line_x, lot_x + ft(lot_width), front_line_y + 15, f"{lot_right_setback}'")

    # Front building position
    bld_x = lot_x + ft(lot_left_setback)
    bld_y = lot_y + ft(lot_depth - front_setback - front_building_depth)
    front_rect = dwg.rect((bld_x, bld_y), (ft(front_building_width), ft(front_building_depth)), **building_style)
    dwg.add(front_rect)

    divider_x = bld_x + ft(front_building_width / 2)
    dwg.add(dwg.line((divider_x, bld_y), (divider_x, bld_y + ft(front_building_depth)), stroke='black', stroke_width=1))

    labels = ['Unit 1', 'Unit 2'] if idx == 1 else ['Unit 3', 'Unit 4']
    dwg.add(dwg.text(labels[0], insert=(bld_x + ft(front_building_width / 4), bld_y + ft(front_building_depth/2)),
                     text_anchor='middle', alignment_baseline='middle', font_size=12, font_family='sans-serif'))
    dwg.add(dwg.text(labels[1], insert=(bld_x + ft(3 * front_building_width / 4), bld_y + ft(front_building_depth/2)),
                     text_anchor='middle', alignment_baseline='middle', font_size=12, font_family='sans-serif'))

    layout.append({'type': 'rectangle', 'name': f'FrontUnit{idx}', 'x': bld_x, 'y': bld_y, 'width': ft(front_building_width), 'height': ft(front_building_depth)})

    # Front building dimensions
    dim_h(bld_x, bld_x + ft(front_building_width), bld_y - 10, f"{front_building_width}'")
    dim_v(bld_y, bld_y + ft(front_building_depth), bld_x - 10, f"{front_building_depth}'")

    # ADU position
    adu_x = lot_x + ft((lot_width - adu_width)/2)
    adu_y = lot_y + ft(rear_setback)
    adu_rect = dwg.rect((adu_x, adu_y), (ft(adu_width), ft(adu_depth)), **building_style)
    dwg.add(adu_rect)
    dwg.add(dwg.text('Garage/ADU', insert=(adu_x + ft(adu_width/2), adu_y + ft(adu_depth/2)), text_anchor='middle', alignment_baseline='middle', font_size=12, font_family='sans-serif'))

    layout.append({'type': 'rectangle', 'name': f'GarageADU{idx}', 'x': adu_x, 'y': adu_y, 'width': ft(adu_width), 'height': ft(adu_depth)})

    # ADU dimensions
    dim_h(adu_x, adu_x + ft(adu_width), adu_y - 10, f"{adu_width}'")
    dim_v(adu_y, adu_y + ft(adu_depth), adu_x - 10, f"{adu_depth}'")

    # Separation between structures
    sep_start = adu_y + ft(adu_depth)
    sep_end = bld_y
    dim_v(sep_start, sep_end, adu_x + ft(adu_width) + 20, "20'")

    # Parking and trash behind ADU
    parking_y = lot_y
    interior_width = lot_width - lot_left_setback - lot_right_setback
    group_width = parking_width * parking_count + trash_width
    parking_x = lot_x + ft(lot_left_setback + (interior_width - group_width) / 2)

    for p in range(parking_count):
        px = parking_x + ft(p * parking_width)
        rect = dwg.rect((px, parking_y), (ft(parking_width), ft(parking_depth)), **parking_style)
        dwg.add(rect)
        dwg.add(dwg.text('P', insert=(px + ft(parking_width/2), parking_y + 12), text_anchor='middle', font_size=10, font_family='sans-serif'))
        layout.append({'type': 'rectangle', 'name': f'Parking{idx}_{p+1}', 'x': px, 'y': parking_y, 'width': ft(parking_width), 'height': ft(parking_depth)})

        if p < parking_count:
            divider_x = px + ft(parking_width)
            dwg.add(dwg.line((divider_x, parking_y), (divider_x, parking_y + ft(parking_depth)), stroke='black', stroke_width=1))

    trash_x = parking_x + ft(parking_width * parking_count)
    trash_rect = dwg.rect((trash_x, parking_y), (ft(trash_width), ft(trash_depth)), **trash_style)
    dwg.add(trash_rect)
    dwg.add(dwg.text('T', insert=(trash_x + ft(trash_width/2), parking_y + 12), text_anchor='middle', font_size=10, font_family='sans-serif'))
    layout.append({'type': 'rectangle', 'name': f'TrashPad{idx}', 'x': trash_x, 'y': parking_y, 'width': ft(trash_width), 'height': ft(trash_depth)})

    divider_x = trash_x + ft(trash_width)
    dwg.add(dwg.line((divider_x, parking_y), (divider_x, parking_y + ft(parking_depth)), stroke='black', stroke_width=1))

    # Parking dimension line
    dim_h(parking_x, trash_x + ft(trash_width), parking_y - 10, f"{group_width}'")
    dim_v(parking_y, parking_y + ft(parking_depth), parking_x - 10, f"{parking_depth}'")

total_lot_width = ft(sum(lot_widths))

# Surrounding streets
alley_top = MARGIN - ft(16)
dwg.add(dwg.rect((MARGIN, alley_top), (total_lot_width, ft(16)), stroke='gray', fill='none', stroke_width=1))
dwg.add(dwg.text("Alley", insert=(MARGIN + total_lot_width/2, alley_top + ft(8)), text_anchor='middle', font_size=12, font_family='sans-serif'))
dim_v(alley_top, MARGIN, MARGIN + total_lot_width/2, "16'")

street_bottom = MARGIN + ft(lot_depth)
dwg.add(dwg.rect((MARGIN, street_bottom), (total_lot_width, ft(60)), stroke='gray', fill='none', stroke_width=1))
dwg.add(dwg.text("22nd Ave S", insert=(MARGIN + total_lot_width/2, street_bottom + ft(30)), text_anchor='middle', font_size=12, font_family='sans-serif'))
dim_v(street_bottom, street_bottom + ft(60), MARGIN + total_lot_width + 20, "60'")

street_right = MARGIN + total_lot_width
dwg.add(dwg.rect((street_right, MARGIN), (ft(50), ft(lot_depth)), stroke='gray', fill='none', stroke_width=1))
dwg.add(dwg.text("30th Street South", insert=(street_right + ft(25), MARGIN + ft(lot_depth/2)), text_anchor='middle', font_size=12, font_family='sans-serif', transform=f"rotate(-90,{street_right + ft(25)},{MARGIN + ft(lot_depth/2)})"))
dim_h(street_right, street_right + ft(50), MARGIN + ft(lot_depth) + 20, "50'")

# Overall lot depth dimension just outside the second lot
overall_dim_x = lot_right + 7  # space for label at +12
dim_v(lot_top, lot_bottom, overall_dim_x, "124'")

# Legend
legend_x = lot_right - 120
legend_y = lot_bottom + 40
dwg.add(dwg.rect((legend_x, legend_y), (20, 12), **building_style))
dwg.add(dwg.text('Front Unit', insert=(legend_x + 25, legend_y + 10), font_size=10, font_family='sans-serif'))
dwg.add(dwg.rect((legend_x, legend_y + 18), (20, 12), **building_style))
dwg.add(dwg.text('Garage/ADU', insert=(legend_x + 25, legend_y + 28), font_size=10, font_family='sans-serif'))
dwg.add(dwg.rect((legend_x, legend_y + 36), (20, 12), **parking_style))
dwg.add(dwg.text('Parking', insert=(legend_x + 25, legend_y + 46), font_size=10, font_family='sans-serif'))
dwg.add(dwg.rect((legend_x, legend_y + 54), (20, 12), **trash_style))
dwg.add(dwg.text('Trash', insert=(legend_x + 25, legend_y + 64), font_size=10, font_family='sans-serif'))
dwg.add(dwg.text("P = Parking Stall (9' x 20')", insert=(legend_x, legend_y + 80), font_size=10, font_family='sans-serif'))
dwg.add(dwg.text("T = Trash Pad (4' x 9')", insert=(legend_x, legend_y + 92), font_size=10, font_family='sans-serif'))
dwg.add(dwg.text("F = Front Unit (2-story)", insert=(legend_x, legend_y + 104), font_size=10, font_family='sans-serif'))
dwg.add(dwg.text("A = Garage/ADU (1 bed over garage)", insert=(legend_x, legend_y + 116), font_size=10, font_family='sans-serif'))
dwg.add(dwg.text("D = Driveway", insert=(legend_x, legend_y + 128), font_size=10, font_family='sans-serif'))
dwg.add(dwg.text("Dashed Line = Setback", insert=(legend_x, legend_y + 140), font_size=10, font_family='sans-serif'))
dwg.add(dwg.text("Solid Line = Structure", insert=(legend_x, legend_y + 152), font_size=10, font_family='sans-serif'))

# Save SVG
dwg.save()

with open('output/layout.json', 'w') as f:
    json.dump(layout, f, indent=2)

print(json.dumps(layout, indent=2))
