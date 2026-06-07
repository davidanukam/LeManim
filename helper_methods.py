"""
Manim Animation Helper Methods
"""

from manim import *

# - Color Palette - #
BG = "#141414"
REDIS_RED = "#f83645"
REDIS_PURP = "#7C3AED"
REDIS_PURP_DARK = "#6D28D9"
PURP_FILL = "#3B2A6E"
PURP_LIGHT = "#A78BFA"
BOX_FILL = "#1E1E1E"
BOX_FILL_ALT = "#232323"
BOX_STROKE = "#444444"
LABEL_GRAY = "#888888"
WHITE = "#FFFFFF"

# - Constants - #
MONO = "monospace"
ARIAL = "arial"


class Explainer(Scene):
    def setup(self):
        self.camera.background_color = BG

    # - Example Structure- #
    def construct(self):
        self.scene_01_name()
        self.scene_02_name()
        self.scene_03_name()
        self.scene_04_name()
        self.scene_05_name()

    # - Helper Methods - #

    def spaced_caps(self, text, size=20, color=LABEL_GRAY, weight=NORMAL):
        """Render text with spaced-caps effect."""
        spaced = " ".join(list(text.upper()))
        return Text(
            spaced,
            font_size=size,
            color=color,
            font="Monospace",
            weight=weight,
        )

    def make_label_box(
        self,
        label_text,
        main_text,
        stroke_color=BOX_STROKE,
        fill_color=BOX_FILL,
        label_color=LABEL_GRAY,
        width=4,
        height=2,
    ):
        """Box with small spaced-caps label and large main text."""
        box = RoundedRectangle(
            corner_radius=0.15,
            width=width,
            height=height,
            stroke_color=stroke_color,
            stroke_width=1.5,
            fill_color=fill_color,
            fill_opacity=1,
        )
        label = self.spaced_caps(label_text, size=14, color=label_color)
        main = Text(main_text, font_size=36, color=WHITE, weight=BOLD)
        content = VGroup(label, main).arrange(DOWN, buff=0.25)
        content.move_to(box.get_center())
        return VGroup(box, content)

    def make_numbered_row(self, number, label_text, active=False, width=8, height=0.9):
        """Horizontal numbered row like '01   PARSE SQL'."""
        num_color = REDIS_PURP if active else LABEL_GRAY
        fill_color = PURP_FILL if active else BOX_FILL
        stroke_col = REDIS_PURP if active else BOX_STROKE
        box = RoundedRectangle(
            corner_radius=0.12,
            width=width,
            height=height,
            stroke_color=stroke_col,
            stroke_width=1.5,
            fill_color=fill_color,
            fill_opacity=1,
        )
        num_text = Text(number, font_size=20, color=num_color, font="Monospace")
        lbl_text = Text(label_text, font_size=24, color=WHITE, weight=BOLD)
        num_text.move_to(box.get_left() + RIGHT * 0.7)
        lbl_text.move_to(box.get_center() + RIGHT * 0.3)
        return VGroup(box, num_text, lbl_text)

    def clear_scene(self, run_time=0.8):
        """Fade out everything on screen."""
        if self.mobjects:
            self.play(FadeOut(Group(*self.mobjects)), run_time=run_time)
        self.wait(0.3)

    def hold(self, seconds=2.0):
        """Pause on a finished composition before transitioning."""
        self.wait(seconds)

    def gap(self, seconds=10):
        """Black-screen pause between scenes (narrator pacing)."""
        self.wait(seconds)

    # --- Text & Typography ---

    def dot_label(self, text, dot_color=REDIS_PURP, size=16, text_color=LABEL_GRAY):
        """Inline dot + spaced-caps label: '• DEFAULT FOR DECADES'.
        Seen in the UUID video as scene context tags in the top-left or center."""
        dot = Text("•", font_size=size, color=dot_color)
        lbl = self.spaced_caps(text, size=size, color=text_color)
        return VGroup(dot, lbl).arrange(RIGHT, buff=0.18)

    def corner_label(self, text, color=LABEL_GRAY, size=16):
        """Small top-left scene label, pinned to upper-left edge.
        Used in UUID and render-text videos to name the current section."""
        lbl = Text(text, font_size=size, color=color, font="Monospace")
        lbl.to_corner(UL, buff=0.55)
        return lbl

    def two_tone_title(self, accent_word, rest, accent_color=REDIS_PURP, size=48):
        """Big centered title with one accent-colored word then white text.
        E.g. two_tone_title('SUBPIXEL', 'RENDERING') → purple + white caps."""
        part1 = Text(accent_word, font_size=size, color=accent_color, weight=BOLD)
        part2 = Text(rest, font_size=size, color=WHITE, weight=BOLD)
        return VGroup(part1, part2).arrange(RIGHT, buff=0.3)

    def narrator_line(self, text, size=38, color=WHITE, corner=DL, buff=1.2):
        """Lowercase italic-feel narrator sentence anchored to a corner.
        Mirrors the 'sounds almost insultingly simple' pattern in main.py."""
        t = Text(text, font_size=size, color=color)
        t.to_corner(corner, buff=buff)
        return t

    def mono_string(self, text, size=32, color=WHITE):
        """Plain monospace string — UUIDs, hashes, code values."""
        return Text(text, font_size=size, color=color, font="Monospace")

    def token_highlight(
        self,
        full_string,
        highlight_slice,
        base_color=LABEL_GRAY,
        accent_color=REDIS_PURP,
        size=36,
    ):
        """Render a monospace string with one segment colored differently.
        E.g. token_highlight('018f4a2b-...', slice(0,8)) for timestamp prefix.
        Returns a VGroup of Text objects arranged LEFT→RIGHT with no gap."""
        before = full_string[: highlight_slice.start] if highlight_slice.start else ""
        middle = full_string[highlight_slice]
        after = full_string[highlight_slice.stop :]
        parts = []
        if before:
            parts.append(
                Text(before, font_size=size, color=base_color, font="Monospace")
            )
        parts.append(Text(middle, font_size=size, color=accent_color, font="Monospace"))
        if after:
            parts.append(
                Text(after, font_size=size, color=base_color, font="Monospace")
            )
        return VGroup(*parts).arrange(RIGHT, buff=0)

    # --- Structural / Layout ---

    def make_db_table(
        self,
        headers,
        rows,
        col_widths=None,
        row_height=0.55,
        accent_col=0,
        accent_color=REDIS_PURP,
    ):
        """Database table with a header row and data rows.
        accent_col highlights that column's values (e.g. the ID column).
        headers: list of str. rows: list of list of str."""
        n_cols = len(headers)
        col_widths = col_widths or [2.0] * n_cols
        total_w = sum(col_widths) + 0.6

        def _row_bg(fill, stroke=BOX_STROKE):
            return RoundedRectangle(
                corner_radius=0.08,
                width=total_w,
                height=row_height,
                fill_color=fill,
                fill_opacity=1,
                stroke_color=stroke,
                stroke_width=1,
            )

        def _cell_text(val, col, is_header=False):
            color = (
                LABEL_GRAY
                if is_header
                else (accent_color if col == accent_col else WHITE)
            )
            size = 15 if is_header else 20
            weight = NORMAL
            font = "Monospace" if col == accent_col and not is_header else ARIAL
            return Text(str(val), font_size=size, color=color, font=font, weight=weight)

        def _build_row(vals, is_header=False):
            fill = BOX_FILL_ALT if is_header else BOX_FILL
            bg = _row_bg(fill)
            x_start = bg.get_left()[0] + 0.35
            cells = VGroup()
            x = x_start
            for i, (val, w) in enumerate(zip(vals, col_widths)):
                txt = _cell_text(val, i, is_header)
                txt.move_to([x + w / 2, 0, 0])
                cells.add(txt)
                x += w
            return VGroup(bg, cells)

        header_row = _build_row(headers, is_header=True)
        data_rows = VGroup(*[_build_row(r) for r in rows])
        all_rows = VGroup(header_row, *data_rows).arrange(DOWN, buff=0.04)
        return all_rows

    def make_tree_node(
        self,
        label="ROOT",
        width=4.5,
        height=0.85,
        stroke_color=BOX_STROKE,
        fill_color=BOX_FILL,
        label_color=LABEL_GRAY,
        active=False,
    ):
        """Single B-tree node box with a centered label.
        Set active=True to highlight it (purple stroke + fill)."""
        if active:
            stroke_color = REDIS_PURP
            fill_color = PURP_FILL
            label_color = PURP_LIGHT
        box = RoundedRectangle(
            corner_radius=0.1,
            width=width,
            height=height,
            stroke_color=stroke_color,
            stroke_width=1.5,
            fill_color=fill_color,
            fill_opacity=1,
        )
        lbl = self.spaced_caps(label, size=14, color=label_color)
        lbl.move_to(box.get_center())
        return VGroup(box, lbl)

    def make_tree(
        self,
        root_label,
        child_labels,
        grandchild_labels=None,
        node_width=3.5,
        v_gap=1.4,
        h_gap=0.45,
    ):
        """Two- or three-level tree: root → children → (optional) grandchildren.
        Returns (tree_VGroup, connector_VGroup) so you can animate separately."""
        root = self.make_tree_node(root_label, width=node_width + 1.5)
        root.move_to(ORIGIN)

        children = VGroup(
            *[self.make_tree_node(lbl, width=node_width) for lbl in child_labels]
        )
        children.arrange(RIGHT, buff=h_gap)
        children.next_to(root, DOWN, buff=v_gap)

        lines = VGroup()
        for child in children:
            line = Line(
                root.get_bottom(),
                child.get_top(),
                stroke_color=BOX_STROKE,
                stroke_width=1,
            )
            lines.add(line)

        nodes = VGroup(root, children)

        if grandchild_labels:
            grandchildren = VGroup(
                *[
                    self.make_tree_node(lbl, width=node_width - 0.5)
                    for lbl in grandchild_labels
                ]
            )
            grandchildren.arrange(RIGHT, buff=h_gap * 0.6)
            grandchildren.next_to(children, DOWN, buff=v_gap)
            for i, gc in enumerate(grandchildren):
                parent = children[min(i, len(children) - 1)]
                lines.add(
                    Line(
                        parent.get_bottom(),
                        gc.get_top(),
                        stroke_color=BOX_STROKE,
                        stroke_width=1,
                    )
                )
            nodes.add(grandchildren)

        return nodes, lines

    def make_pipeline(self, steps, width=2.8, height=0.85, gap=0.7, active_index=None):
        """Horizontal pipeline: [Step A] –– [Step B] –– [Step C].
        active_index highlights one box. Returns VGroup (boxes + arrows)."""
        boxes = VGroup()
        for i, label in enumerate(steps):
            active = i == active_index
            stroke = REDIS_PURP if active else BOX_STROKE
            fill = PURP_FILL if active else BOX_FILL
            color = WHITE if active else LABEL_GRAY
            box = RoundedRectangle(
                corner_radius=0.12,
                width=width,
                height=height,
                stroke_color=stroke,
                stroke_width=1.5,
                fill_color=fill,
                fill_opacity=1,
            )
            lbl = Text(
                label, font_size=20, color=color, weight=BOLD if active else NORMAL
            )
            lbl.move_to(box.get_center())
            boxes.add(VGroup(box, lbl))

        boxes.arrange(RIGHT, buff=gap)
        arrows = VGroup()
        for i in range(len(steps) - 1):
            a = DashedLine(
                boxes[i].get_right(),
                boxes[i + 1].get_left(),
                dash_length=0.12,
                dashed_ratio=0.5,
                stroke_color=BOX_STROKE,
                stroke_width=1.5,
            )
            arrows.add(a)
        return VGroup(boxes, arrows)

    def make_stat_callout(
        self,
        label,
        value,
        sub=None,
        width=5.5,
        height=2.4,
        stroke_color=BOX_STROKE,
        fill_color=BOX_FILL,
    ):
        """Large centered stat card: label above, huge value, optional sub-line.
        Matches the '1,200,000 ops per frame' card in the render-text video."""
        box = RoundedRectangle(
            corner_radius=0.2,
            width=width,
            height=height,
            stroke_color=stroke_color,
            stroke_width=1.5,
            fill_color=fill_color,
            fill_opacity=1,
        )
        lbl = self.spaced_caps(label, size=15, color=LABEL_GRAY)
        val = Text(value, font_size=56, color=WHITE, weight=BOLD)
        items = [lbl, val]
        if sub:
            sub_t = Text(sub, font_size=22, color=LABEL_GRAY)
            items.append(sub_t)
        content = VGroup(*items).arrange(DOWN, buff=0.2)
        content.move_to(box.get_center())
        return VGroup(box, content)

    def make_progress_bar(
        self,
        fill_ratio,
        width=5.0,
        height=0.18,
        fill_color=REDIS_PURP,
        track_color=BOX_STROKE,
    ):
        """Horizontal progress / bit-width bar.
        fill_ratio is 0.0–1.0. Used in UUID video for byte-size comparisons."""
        track = RoundedRectangle(
            corner_radius=0.09,
            width=width,
            height=height,
            stroke_color=track_color,
            stroke_width=1,
            fill_color=BOX_FILL,
            fill_opacity=1,
        )
        fill_w = max(0.01, width * fill_ratio)
        fill = RoundedRectangle(
            corner_radius=0.09,
            width=fill_w,
            height=height,
            stroke_width=0,
            fill_color=fill_color,
            fill_opacity=1,
        )
        fill.align_to(track, LEFT)
        return VGroup(track, fill)

    def make_vertical_bar(
        self,
        label,
        pct,
        bar_width=1.4,
        bar_height=3.5,
        fill_color=REDIS_PURP,
        label_color=REDIS_PURP,
        card_width=2.4,
        card_height=5.0,
    ):
        """Vertical fill bar inside a card (RAM / DISK style from UUID video).
        pct is 0.0–1.0. Returns a VGroup card."""
        card = RoundedRectangle(
            corner_radius=0.15,
            width=card_width,
            height=card_height,
            stroke_color=BOX_STROKE,
            stroke_width=1.5,
            fill_color=BOX_FILL,
            fill_opacity=1,
        )
        lbl = self.spaced_caps(label, size=14, color=label_color)
        lbl.move_to(card.get_top() + DOWN * 0.45)

        track = RoundedRectangle(
            corner_radius=0.08,
            width=bar_width,
            height=bar_height,
            stroke_color=BOX_STROKE,
            stroke_width=1,
            fill_color=BOX_FILL_ALT,
            fill_opacity=1,
        )
        fill_h = max(0.05, bar_height * pct)
        fill = RoundedRectangle(
            corner_radius=0.08,
            width=bar_width,
            height=fill_h,
            stroke_width=0,
            fill_color=fill_color,
            fill_opacity=1,
        )
        track.move_to(card.get_center() + UP * 0.15)
        fill.align_to(track, DOWN)

        pct_text = Text(f"{round(pct * 100)}%", font_size=28, color=WHITE, weight=BOLD)
        pct_text.move_to(card.get_bottom() + UP * 0.5)

        return VGroup(card, lbl, track, fill, pct_text)

    def make_editor_window(self, lines=None, width=7.0, height=3.5):
        """macOS-style dark editor window with traffic-light dots and line numbers.
        lines: list of str. Seen in the render-text video opening scene."""
        lines = lines or []
        frame = RoundedRectangle(
            corner_radius=0.2,
            width=width,
            height=height,
            stroke_color=BOX_STROKE,
            stroke_width=1.5,
            fill_color=BOX_FILL,
            fill_opacity=1,
        )
        # traffic lights
        tl_colors = ["#FF5F57", "#FEBC2E", "#28C840"]
        dots = VGroup(*[Dot(radius=0.1, color=c) for c in tl_colors]).arrange(
            RIGHT, buff=0.18
        )
        dots.move_to(frame.get_top() + DOWN * 0.35 + LEFT * (width / 2 - 0.5))

        # divider line under titlebar
        divider = Line(
            frame.get_left() + RIGHT * 0.01 + DOWN * 0.6,
            frame.get_right() + LEFT * 0.01 + DOWN * 0.6,
            stroke_color=BOX_STROKE,
            stroke_width=1,
        )

        code_lines = VGroup()
        for i, line_text in enumerate(lines):
            num = Text(str(i + 1), font_size=16, color=LABEL_GRAY, font="Monospace")
            code = Text(line_text, font_size=18, color=WHITE, font="Monospace")
            row = VGroup(num, code).arrange(RIGHT, buff=0.4)
            code_lines.add(row)
        code_lines.arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        code_lines.move_to(frame.get_center() + DOWN * 0.25 + RIGHT * 0.2)

        return VGroup(frame, dots, divider, code_lines)

    def make_pixel_grid(
        self,
        rows=8,
        cols=8,
        cell_size=0.55,
        filled_cells=None,
        fill_color=WHITE,
        stroke_color="#2a2a2a",
    ):
        """Pixel grid for bitmap / rasterization diagrams (render-text video).
        filled_cells: set of (row, col) tuples that are filled white."""
        filled_cells = filled_cells or set()
        grid = VGroup()
        for r in range(rows):
            for c in range(cols):
                rect = Square(
                    side_length=cell_size,
                    stroke_color=stroke_color,
                    stroke_width=1,
                    fill_color=fill_color if (r, c) in filled_cells else BG,
                    fill_opacity=1,
                )
                rect.move_to([c * cell_size, -r * cell_size, 0])
                grid.add(rect)
        grid.move_to(ORIGIN)
        return grid

    def make_annotation_bracket(
        self,
        target,
        label_text,
        direction=UP,
        color=REDIS_PURP,
        buff=0.25,
        label_size=16,
    ):
        """Bracket above (or below) a mobject with a label.
        Mirrors the 'TIMESTAMP / RANDOM' span labels in the UUID video."""
        brace = Brace(target, direction=direction, color=color, buff=buff)
        lbl = self.spaced_caps(label_text, size=label_size, color=color)
        if direction == UP:
            lbl.next_to(brace, UP, buff=0.1)
        else:
            lbl.next_to(brace, DOWN, buff=0.1)
        return VGroup(brace, lbl)

    def make_badge(
        self,
        text,
        fill_color=PURP_FILL,
        stroke_color=REDIS_PURP,
        text_color=PURP_LIGHT,
        size=18,
        h_pad=0.35,
        v_pad=0.18,
    ):
        """Small pill/badge: 'v4', 'V4 · 128-BIT · RANDOM'.
        Used in UUID video to annotate version tags inline."""
        lbl = self.spaced_caps(text, size=size, color=text_color)
        box = RoundedRectangle(
            corner_radius=0.18,
            width=lbl.width + h_pad * 2,
            height=lbl.height + v_pad * 2,
            stroke_color=stroke_color,
            stroke_width=1.5,
            fill_color=fill_color,
            fill_opacity=1,
        )
        lbl.move_to(box.get_center())
        return VGroup(box, lbl)

    # --- Animation Helpers ---

    def stagger_in(self, mobjects, shift=DOWN * 0.15, lag=0.18, run_time=2.0):
        """FadeIn a list/VGroup with a staggered downward drift.
        Replaces the repeated AnimationGroup + lag_ratio pattern."""
        self.play(
            AnimationGroup(
                *[FadeIn(m, shift=shift) for m in mobjects],
                lag_ratio=lag,
            ),
            run_time=run_time,
        )

    def walk_rows(
        self,
        rows,
        steps,
        active_fn,
        inactive_fn,
        pause=0.7,
        final_pause=1.2,
        run_time=0.8,
    ):
        """Step through a VGroup of rows, transforming the active + previous row.
        active_fn(i) and inactive_fn(i) return replacement mobjects for row i.
        Replaces the repetitive for-loop Transform pattern in main.py scenes."""
        for idx in range(len(steps)):
            active_row = active_fn(idx)
            active_row.move_to(rows[idx].get_center())
            if idx > 0:
                prev = inactive_fn(idx - 1)
                prev.move_to(rows[idx - 1].get_center())
                self.play(
                    Transform(rows[idx - 1], prev),
                    Transform(rows[idx], active_row),
                    run_time=run_time,
                )
            else:
                self.play(Transform(rows[idx], active_row), run_time=run_time)
            self.wait(pause if idx < len(steps) - 1 else final_pause)

    def reveal_stack(
        self, items, direction=DOWN, buff=0.5, item_pause=0.8, run_time=1.0
    ):
        """FadeIn a list of mobjects one at a time, already arranged.
        Good for building up a vertical list beat by beat."""
        for item in items:
            self.play(FadeIn(item), run_time=run_time)
            self.wait(item_pause)

    def write_then_hold(self, mobject, write_time=1.5, hold_time=2.0):
        """Write a single mobject then hold. Shorthand for the common pattern."""
        self.play(Write(mobject), run_time=write_time)
        self.hold(hold_time)

    def swap_highlight(self, old_mob, new_mob, run_time=0.6):
        """Transform old_mob into new_mob in place (reuse position).
        Used to toggle a row between active and inactive state."""
        new_mob.move_to(old_mob.get_center())
        self.play(Transform(old_mob, new_mob), run_time=run_time)
