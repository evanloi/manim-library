from manim import *
import numpy as np


class GraphEigenvalueAnimation(Scene):
    TEXT_FONT = "Segoe UI"

    SLOTS = ("L", "R")
    NAMES = ("A", "B")

    NODE_COLORS = {
        "A": BLUE_C,
        "B": GREEN_C,
    }

    POSITIONS = {
        "L": np.array([-1.25, 0.0, 0.0]),
        "R": np.array([1.25, 0.0, 0.0]),
    }

    NAME_MAP = {
        "L": "A",
        "R": "B",
    }

    EDGE_DATA = [
        ("L", "R", 2),
    ]

    MATRIX_VALUES = [
        [0, 2],
        [2, 0],
    ]

    def txt(
        self,
        content,
        font_size=24,
        color=WHITE,
        line_spacing=1.0,
    ):
        return Text(
            content,
            font=self.TEXT_FONT,
            font_size=font_size,
            color=color,
            line_spacing=line_spacing,
        )

    def make_title(self, content):
        title = self.txt(
            content,
            font_size=36,
        )

        title.to_edge(
            UP,
            buff=0.34,
        )

        return title

    def make_caption(
        self,
        content,
        font_size=20,
        color=WHITE,
    ):
        caption = self.txt(
            content,
            font_size=font_size,
            color=color,
            line_spacing=1.05,
        )

        caption.to_edge(
            DOWN,
            buff=0.22,
        )

        return caption

    def clear_screen(
        self,
        run_time=0.8,
    ):
        current_objects = list(
            self.mobjects
        )

        if current_objects:
            self.play(
                *[
                    FadeOut(obj)
                    for obj in current_objects
                ],
                run_time=run_time,
            )

        self.clear()

    def make_panel(
        self,
        center,
        color,
        width,
        height,
        opacity=0.06,
    ):
        panel = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.18,
            stroke_color=color,
            stroke_width=3,
        )

        panel.set_fill(
            color,
            opacity=opacity,
        )

        panel.move_to(center)

        return panel

    def make_text_box(
        self,
        content,
        center,
        color,
        width,
        font_size=18,
    ):
        label = self.txt(
            content,
            font_size=font_size,
            color=color,
        )

        box = RoundedRectangle(
            width=width,
            height=label.height + 0.36,
            corner_radius=0.12,
            stroke_color=color,
            stroke_width=2,
        )

        box.set_fill(
            color,
            opacity=0.10,
        )

        group = VGroup(
            box,
            label,
        )

        group.move_to(center)

        return group

    def make_math_badge(
        self,
        tex,
        center,
        color,
        width,
    ):
        box = RoundedRectangle(
            width=width,
            height=0.62,
            corner_radius=0.12,
            stroke_color=color,
            stroke_width=3,
        )

        box.set_fill(
            color,
            opacity=0.14,
        )

        label = MathTex(
            tex,
            font_size=30,
            color=color,
        )

        group = VGroup(
            box,
            label,
        )

        group.move_to(center)

        return group

    def make_equation_step(
        self,
        number,
        equation,
        color=BLUE_A,
        equation_size=28,
    ):
        number_circle = Circle(
            radius=0.21,
            stroke_color=color,
            stroke_width=3,
        )

        number_circle.set_fill(
            color,
            opacity=0.18,
        )

        number_text = self.txt(
            str(number),
            font_size=17,
        )

        number_badge = VGroup(
            number_circle,
            number_text,
        )

        equation_text = MathTex(
            equation,
            font_size=equation_size,
        )

        step = VGroup(
            number_badge,
            equation_text,
        )

        step.arrange(
            RIGHT,
            buff=0.28,
        )

        return step

    def make_symbol_row(
        self,
        symbol_tex,
        meaning,
        symbol_color,
        panel_center_x,
        y_position,
        symbol_size=31,
        meaning_size=17,
    ):
        symbol = MathTex(
            symbol_tex,
            font_size=symbol_size,
            color=symbol_color,
        )

        symbol.move_to([
            panel_center_x - 2.18,
            y_position,
            0,
        ])

        explanation = self.txt(
            meaning,
            font_size=meaning_size,
        )

        explanation.move_to([
            panel_center_x
            - 1.62
            + explanation.width / 2,
            y_position,
            0,
        ])

        return VGroup(
            symbol,
            explanation,
        )

    def make_edge(
        self,
        start_slot,
        end_slot,
        weight,
    ):
        start = self.POSITIONS[
            start_slot
        ]

        end = self.POSITIONS[
            end_slot
        ]

        direction = normalize(
            end - start
        )

        edge = Line(
            start + direction * 0.43,
            end - direction * 0.43,
            color=WHITE,
            stroke_width=7,
        )

        edge.set_z_index(-5)

        weight_label = MathTex(
            str(weight),
            font_size=34,
            color=WHITE,
        )

        weight_label.move_to(
            edge.get_center()
        )

        weight_label.add_background_rectangle(
            color=BLACK,
            opacity=0.95,
            buff=0.09,
        )

        weight_label.set_z_index(30)

        return (
            edge,
            weight_label,
        )

    def make_node(
        self,
        slot,
        name,
    ):
        circle = Circle(
            radius=0.38,
        )

        circle.set_fill(
            self.NODE_COLORS[name],
            opacity=1,
        )

        circle.set_stroke(
            WHITE,
            width=3,
        )

        circle.move_to(
            self.POSITIONS[slot]
        )

        circle.set_z_index(5)

        label = MathTex(
            name,
            font_size=34,
            color=WHITE,
        )

        label.move_to(circle)

        label.set_z_index(25)

        return VGroup(
            circle,
            label,
        )

    def make_graph(
        self,
        center=ORIGIN,
        scale_factor=1.0,
    ):
        edges = {}
        weights = {}

        for start, end, weight in self.EDGE_DATA:
            edge, number = self.make_edge(
                start,
                end,
                weight,
            )

            key = (
                start,
                end,
            )

            edges[key] = edge
            weights[key] = number

        nodes = {
            slot: self.make_node(
                slot,
                self.NAME_MAP[slot],
            )
            for slot in self.SLOTS
        }

        group = VGroup(
            VGroup(
                *edges.values()
            ),
            VGroup(
                *weights.values()
            ),
            VGroup(
                *nodes.values()
            ),
        )

        group.scale(
            scale_factor
        )

        group.move_to(
            center
        )

        return (
            group,
            edges,
            weights,
            nodes,
        )

    def animate_graph_build(
        self,
        edges,
        weights,
        nodes,
    ):
        self.play(
            LaggedStart(
                *[
                    GrowFromCenter(
                        nodes[slot]
                    )
                    for slot in self.SLOTS
                ],
                lag_ratio=0.20,
            ),
            run_time=1.5,
        )

        self.play(
            LaggedStart(
                *[
                    Create(edge)
                    for edge in edges.values()
                ],
                lag_ratio=0.15,
            ),
            run_time=1.4,
        )

        self.play(
            LaggedStart(
                *[
                    FadeIn(
                        weight,
                        scale=0.6,
                    )
                    for weight in weights.values()
                ],
                lag_ratio=0.15,
            ),
            run_time=1.0,
        )

    def make_labeled_matrix(
        self,
        center=ORIGIN,
        scale_factor=1.0,
    ):
        matrix = Matrix(
            self.MATRIX_VALUES,
            element_to_mobject=lambda value: MathTex(
                str(value),
                font_size=36,
                color=WHITE,
            ),
            h_buff=0.90,
            v_buff=0.80,
            bracket_h_buff=0.15,
            bracket_v_buff=0.15,
        )

        matrix.scale(
            scale_factor
        )

        matrix.move_to(
            center
        )

        for index, entry in enumerate(
            matrix.get_entries()
        ):
            row = index // 2
            column = index % 2

            value = self.MATRIX_VALUES[
                row
            ][
                column
            ]

            entry.set_color(
                GRAY_B
                if value == 0
                else WHITE
            )

        row_labels = VGroup()
        column_labels = VGroup()

        row_gap = 0.24
        column_gap = 0.24

        label_size = max(
            22,
            int(
                30 * scale_factor
            ),
        )

        for index, name in enumerate(
            self.NAMES
        ):
            row_label = MathTex(
                name,
                font_size=label_size,
                color=self.NODE_COLORS[name],
            )

            column_label = MathTex(
                name,
                font_size=label_size,
                color=self.NODE_COLORS[name],
            )

            row_y = (
                matrix
                .get_rows()[index]
                .get_center()[1]
            )

            row_x = (
                matrix.get_left()[0]
                - row_gap
                - row_label.width / 2
            )

            row_label.move_to([
                row_x,
                row_y,
                0,
            ])

            column_x = (
                matrix
                .get_columns()[index]
                .get_center()[0]
            )

            column_y = (
                matrix.get_top()[1]
                + column_gap
                + column_label.height / 2
            )

            column_label.move_to([
                column_x,
                column_y,
                0,
            ])

            row_labels.add(
                row_label
            )

            column_labels.add(
                column_label
            )

        return VGroup(
            matrix,
            row_labels,
            column_labels,
        )

    def show_graph_scene(self):
        title = self.txt(
            "From a Graph to Eigenvalues and Eigenvectors",
            font_size=40,
        )

        title.set_color_by_gradient(
            BLUE_A,
            GREEN_A,
        )

        subtitle = self.txt(
            "A beginner-friendly example",
            font_size=23,
            color=GRAY_A,
        )

        subtitle.next_to(
            title,
            DOWN,
            buff=0.24,
        )

        self.play(
            Write(title),
            run_time=1.4,
        )

        self.play(
            FadeIn(
                subtitle,
                shift=UP * 0.15,
            )
        )

        self.wait(0.8)

        small_title = self.make_title(
            "From a Graph to Eigenvalues and Eigenvectors"
        )

        self.play(
            Transform(
                title,
                small_title,
            ),
            FadeOut(
                subtitle
            ),
            run_time=1.0,
        )

        graph, edges, weights, nodes = self.make_graph(
            center=DOWN * 0.25,
            scale_factor=1.25,
        )

        self.animate_graph_build(
            edges,
            weights,
            nodes,
        )

        caption = self.make_caption(
            "The number 2 is the weight of the connection between A and B.",
            font_size=21,
        )

        self.play(
            FadeIn(
                caption,
                shift=UP * 0.15,
            ),
            Indicate(
                edges[("L", "R")],
                color=YELLOW,
                scale_factor=1.06,
            ),
            Indicate(
                weights[("L", "R")],
                color=YELLOW,
                scale_factor=1.4,
            ),
            run_time=1.5,
        )

        self.wait(1.5)

    def show_matrix_scene(self):
        self.clear_screen()

        title = self.make_title(
            "Graph and Adjacency Matrix"
        )

        self.play(
            FadeIn(title)
        )

        graph, _, _, _ = self.make_graph(
            center=LEFT * 3.75 + UP * 0.10,
            scale_factor=0.93,
        )

        matrix_group = self.make_labeled_matrix(
            center=RIGHT * 3.45 + UP * 0.10,
            scale_factor=1.02,
        )

        graph_label = self.make_text_box(
            "Weighted Graph",
            center=LEFT * 3.75 + UP * 1.5,
            color=BLUE_A,
            width=2.70,
            font_size=18,
        )

        matrix_label = self.make_text_box(
            "Adjacency Matrix",
            center=RIGHT * 3.45 + UP * 2.00,
            color=GREEN_A,
            width=3.00,
            font_size=18,
        )

        self.play(
            FadeIn(graph),
            FadeIn(matrix_group),
            FadeIn(graph_label),
            FadeIn(matrix_label),
            run_time=1.3,
        )

        guide_panel = self.make_panel(
            center=RIGHT * 3.45 + DOWN * 2.10,
            color=GRAY_A,
            width=4.15,
            height=1.45,
            opacity=0.05,
        )

        row_key = VGroup(
            Dot(
                radius=0.07,
                color=BLUE_A,
            ),
            self.txt(
                "Row labels: starting node",
                font_size=17,
                color=BLUE_A,
            ),
        )

        row_key.arrange(
            RIGHT,
            buff=0.16,
        )

        column_key = VGroup(
            Dot(
                radius=0.07,
                color=GREEN_A,
            ),
            self.txt(
                "Column labels: ending node",
                font_size=17,
                color=GREEN_A,
            ),
        )

        column_key.arrange(
            RIGHT,
            buff=0.16,
        )

        guide_text = VGroup(
            column_key,
            row_key,
        )

        guide_text.arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.22,
        )

        guide_text.move_to(
            guide_panel
        )

        self.play(
            FadeIn(guide_panel),
            FadeIn(guide_text),
        )

        self.play(
            Indicate(
                matrix_group[2],
                color=GREEN_A,
                scale_factor=1.08,
            ),
            run_time=1.1,
        )

        self.play(
            Indicate(
                matrix_group[1],
                color=BLUE_A,
                scale_factor=1.08,
            ),
            run_time=1.1,
        )

        entries = (
            matrix_group[0]
            .get_entries()
        )

        boxes = VGroup(
            SurroundingRectangle(
                entries[1],
                color=YELLOW,
                buff=0.10,
                stroke_width=3,
            ),
            SurroundingRectangle(
                entries[2],
                color=YELLOW,
                buff=0.10,
                stroke_width=3,
            ),
        )

        caption = self.make_caption(
            "The 2 appears twice because the connection works in both directions.",
            font_size=20,
        )

        self.play(
            Create(boxes),
            FadeIn(caption),
            run_time=1.3,
        )

        self.wait(1.5)

    def show_meaning_scene(self):
        self.clear_screen()

        title = self.make_title(
            "What Do Eigenvalues and Eigenvectors Mean?"
        )

        self.play(
            FadeIn(title)
        )

        equation = MathTex(
            r"A\vec{v}=\lambda\vec{v}",
            font_size=52,
        )

        equation.move_to(
            UP * 1.45
        )

        vector_panel = self.make_panel(
            center=LEFT * 3.20 + DOWN * 0.85,
            color=BLUE_A,
            width=5.65,
            height=1.95,
            opacity=0.08,
        )

        value_panel = self.make_panel(
            center=RIGHT * 3.20 + DOWN * 0.85,
            color=GREEN_A,
            width=5.65,
            height=1.95,
            opacity=0.08,
        )

        vector_content = VGroup(
            self.txt(
                "Eigenvector",
                font_size=27,
                color=BLUE_A,
            ),
            self.txt(
                "the special direction or pattern\n"
                "that remains on the same line",
                font_size=20,
                line_spacing=1.1,
            ),
        )

        vector_content.arrange(
            DOWN,
            buff=0.16,
        )

        vector_content.move_to(
            vector_panel
        )

        value_content = VGroup(
            self.txt(
                "Eigenvalue",
                font_size=27,
                color=GREEN_A,
            ),
            self.txt(
                "the number that tells us how much\n"
                "the vector stretches or flips",
                font_size=20,
                line_spacing=1.1,
            ),
        )

        value_content.arrange(
            DOWN,
            buff=0.16,
        )

        value_content.move_to(
            value_panel
        )

        caption = self.make_caption(
            "First find the eigenvalues. Then find one eigenvector for each eigenvalue.",
            font_size=20,
        )

        self.play(
            Write(equation)
        )

        self.play(
            FadeIn(vector_panel),
            FadeIn(value_panel),
            FadeIn(vector_content),
            FadeIn(value_content),
        )

        self.play(
            FadeIn(caption)
        )

        self.wait(2.5)

    def show_equation_explanation_scene(self):
        self.clear_screen()

        title = self.make_title(
            "Understanding the Equations"
        )

        self.play(
            FadeIn(title)
        )

        left_center_x = -3.35
        right_center_x = 3.35

        left_panel = self.make_panel(
            center=[
                left_center_x,
                -0.20,
                0,
            ],
            color=BLUE_A,
            width=6.05,
            height=5.35,
            opacity=0.06,
        )

        right_panel = self.make_panel(
            center=[
                right_center_x,
                -0.20,
                0,
            ],
            color=GREEN_A,
            width=6.05,
            height=5.35,
            opacity=0.06,
        )

        left_heading = self.txt(
            "Eigenvector Equation",
            font_size=24,
            color=BLUE_A,
        )

        left_heading.move_to([
            left_center_x,
            2.05,
            0,
        ])

        right_heading = self.txt(
            "Eigenvalue Condition",
            font_size=24,
            color=GREEN_A,
        )

        right_heading.move_to([
            right_center_x,
            2.05,
            0,
        ])

        eigenvector_equation = MathTex(
            r"A",
            r"\vec{v}",
            r"=",
            r"\lambda",
            r"\vec{v}",
            font_size=46,
        )

        eigenvector_equation[0].set_color(
            YELLOW
        )

        eigenvector_equation[1].set_color(
            BLUE_A
        )

        eigenvector_equation[3].set_color(
            GREEN_A
        )

        eigenvector_equation[4].set_color(
            BLUE_A
        )

        eigenvector_equation.move_to([
            left_center_x,
            1.25,
            0,
        ])

        eigenvalue_equation = MathTex(
            r"\det",
            r"(",
            r"A",
            r"-",
            r"\lambda",
            r"I",
            r")",
            r"=",
            r"0",
            font_size=40,
        )

        eigenvalue_equation[0].set_color(
            ORANGE
        )

        eigenvalue_equation[2].set_color(
            YELLOW
        )

        eigenvalue_equation[4].set_color(
            GREEN_A
        )

        eigenvalue_equation[5].set_color(
            PURPLE_A
        )

        eigenvalue_equation.move_to([
            right_center_x,
            1.25,
            0,
        ])

        left_divider = Line(
            [
                left_center_x - 2.35,
                0.67,
                0,
            ],
            [
                left_center_x + 2.35,
                0.67,
                0,
            ],
            color=GRAY_B,
            stroke_width=2,
        )

        right_divider = Line(
            [
                right_center_x - 2.35,
                0.67,
                0,
            ],
            [
                right_center_x + 2.35,
                0.67,
                0,
            ],
            color=GRAY_B,
            stroke_width=2,
        )

        left_rows = VGroup(
            self.make_symbol_row(
                r"A",
                "matrix that transforms the vector",
                YELLOW,
                left_center_x,
                0.15,
            ),
            self.make_symbol_row(
                r"\vec{v}",
                "eigenvector, or special direction",
                BLUE_A,
                left_center_x,
                -0.55,
            ),
            self.make_symbol_row(
                r"\lambda",
                "eigenvalue, or scale factor",
                GREEN_A,
                left_center_x,
                -1.25,
            ),
        )

        right_rows = VGroup(
            self.make_symbol_row(
                r"\det",
                "determinant",
                ORANGE,
                right_center_x,
                0.15,
            ),
            self.make_symbol_row(
                r"I",
                "identity matrix",
                PURPLE_A,
                right_center_x,
                -0.55,
            ),
        )


        self.play(
            FadeIn(left_panel),
            FadeIn(right_panel),
            FadeIn(left_heading),
            FadeIn(right_heading),
            run_time=1.0,
        )

        self.play(
            Write(
                eigenvector_equation
            ),
            Write(
                eigenvalue_equation
            ),
            run_time=1.5,
        )

        self.play(
            Create(left_divider),
            Create(right_divider),
        )

        for left_row, right_row in zip(
            left_rows,
            right_rows,
        ):
            self.play(
                FadeIn(
                    left_row,
                    shift=RIGHT * 0.10,
                ),
                FadeIn(
                    right_row,
                    shift=RIGHT * 0.10,
                ),
                run_time=0.85,
            )

        self.wait(2.5)

    def show_eigenvalue_scene(self):
        self.clear_screen()

        title = self.make_title(
            "Finding the Eigenvalues"
        )

        self.play(
            FadeIn(title)
        )

        steps = VGroup(
            self.make_equation_step(
                1,
                r"A="
                r"\begin{bmatrix}"
                r"0&2\\"
                r"2&0"
                r"\end{bmatrix}",
                equation_size=29,
            ),
            self.make_equation_step(
                2,
                r"A-\lambda I="
                r"\begin{bmatrix}"
                r"-\lambda&2\\"
                r"2&-\lambda"
                r"\end{bmatrix}",
                equation_size=27,
            ),
            self.make_equation_step(
                3,
                r"\det"
                r"\begin{bmatrix}"
                r"-\lambda&2\\"
                r"2&-\lambda"
                r"\end{bmatrix}"
                r"=0",
                equation_size=27,
            ),
            self.make_equation_step(
                4,
                r"(-\lambda)(-\lambda)-(2)(2)=0",
                equation_size=28,
            ),
            self.make_equation_step(
                5,
                r"\lambda^2-4=0",
                equation_size=31,
            ),
            self.make_equation_step(
                6,
                r"(\lambda-2)(\lambda+2)=0",
                equation_size=30,
            ),
            self.make_equation_step(
                7,
                r"\lambda_1=2"
                r"\qquad"
                r"\lambda_2=-2",
                color=GREEN_A,
                equation_size=33,
            ),
        )

        steps.arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.17,
        )

        steps.scale_to_fit_height(
            5.70
        )

        steps.move_to(
            DOWN * 0.25
        )

        for step in steps:
            self.play(
                FadeIn(
                    step[0],
                    scale=0.8,
                ),
                Write(
                    step[1]
                ),
                run_time=1.0,
            )

            self.wait(0.22)

        result_box = SurroundingRectangle(
            steps[-1][1],
            color=GREEN_A,
            buff=0.12,
            stroke_width=3,
        )

        self.play(
            Create(result_box),
            run_time=1.0,
        )

        self.wait(2)

    def show_eigenvector_scene(self):
        self.clear_screen()

        title = self.make_title(
            "Finding the Eigenvectors"
        )

        self.play(
            FadeIn(title)
        )

        left_panel = self.make_panel(
            center=LEFT * 3.35 + DOWN * 0.35,
            color=BLUE_A,
            width=6.15,
            height=5.55,
            opacity=0.06,
        )

        right_panel = self.make_panel(
            center=RIGHT * 3.35 + DOWN * 0.35,
            color=GREEN_A,
            width=6.15,
            height=5.55,
            opacity=0.06,
        )

        left_badge = self.make_math_badge(
            r"\lambda=2",
            center=LEFT * 3.35 + UP * 2.10,
            color=BLUE_A,
            width=2.2,
        )

        right_badge = self.make_math_badge(
            r"\lambda=-2",
            center=RIGHT * 3.35 + UP * 2.10,
            color=GREEN_A,
            width=2.4,
        )

        self.play(
            FadeIn(left_panel),
            FadeIn(right_panel),
            FadeIn(left_badge),
            FadeIn(right_badge),
        )

        left_steps = VGroup(
            self.make_equation_step(
                1,
                r"(A-2I)\vec{v}=\vec{0}",
                color=BLUE_A,
                equation_size=24,
            ),
            self.make_equation_step(
                2,
                r"\begin{bmatrix}"
                r"-2&2\\"
                r"2&-2"
                r"\end{bmatrix}"
                r"\begin{bmatrix}"
                r"x\\y"
                r"\end{bmatrix}"
                r"="
                r"\begin{bmatrix}"
                r"0\\0"
                r"\end{bmatrix}",
                color=BLUE_A,
                equation_size=20,
            ),
            self.make_equation_step(
                3,
                r"-2x+2y=0",
                color=BLUE_A,
                equation_size=25,
            ),
            self.make_equation_step(
                4,
                r"x=y",
                color=BLUE_A,
                equation_size=27,
            ),
            self.make_equation_step(
                5,
                r"\vec{v}_1="
                r"\begin{bmatrix}"
                r"1\\1"
                r"\end{bmatrix}",
                color=BLUE_A,
                equation_size=28,
            ),
        )

        right_steps = VGroup(
            self.make_equation_step(
                1,
                r"(A+2I)\vec{v}=\vec{0}",
                color=GREEN_A,
                equation_size=24,
            ),
            self.make_equation_step(
                2,
                r"\begin{bmatrix}"
                r"2&2\\"
                r"2&2"
                r"\end{bmatrix}"
                r"\begin{bmatrix}"
                r"x\\y"
                r"\end{bmatrix}"
                r"="
                r"\begin{bmatrix}"
                r"0\\0"
                r"\end{bmatrix}",
                color=GREEN_A,
                equation_size=20,
            ),
            self.make_equation_step(
                3,
                r"2x+2y=0",
                color=GREEN_A,
                equation_size=25,
            ),
            self.make_equation_step(
                4,
                r"x=-y",
                color=GREEN_A,
                equation_size=27,
            ),
            self.make_equation_step(
                5,
                r"\vec{v}_2="
                r"\begin{bmatrix}"
                r"1\\-1"
                r"\end{bmatrix}",
                color=GREEN_A,
                equation_size=28,
            ),
        )

        left_steps.arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.28,
        )

        right_steps.arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.28,
        )

        left_steps.scale_to_fit_height(
            4.35
        )

        right_steps.scale_to_fit_height(
            4.35
        )

        left_steps.move_to(
            LEFT * 3.35 + DOWN * 0.55
        )

        right_steps.move_to(
            RIGHT * 3.35 + DOWN * 0.55
        )

        for left_step, right_step in zip(
            left_steps,
            right_steps,
        ):
            self.play(
                FadeIn(
                    left_step[0],
                    scale=0.8,
                ),
                Write(
                    left_step[1]
                ),
                FadeIn(
                    right_step[0],
                    scale=0.8,
                ),
                Write(
                    right_step[1]
                ),
                run_time=1.25,
            )

            self.wait(0.22)

        left_result_box = SurroundingRectangle(
            left_steps[-1][1],
            color=BLUE_A,
            buff=0.10,
            stroke_width=3,
        )

        right_result_box = SurroundingRectangle(
            right_steps[-1][1],
            color=GREEN_A,
            buff=0.10,
            stroke_width=3,
        )

        self.play(
            Create(
                left_result_box
            ),
            Create(
                right_result_box
            ),
            run_time=1.2,
        )

        self.wait(2)

    def show_geometry_scene(self):
        self.clear_screen()

        title = self.make_title(
            "Geometric Meaning"
        )

        self.play(
            FadeIn(title)
        )

        plane = NumberPlane(
            x_range=[
                -3,
                3,
                1,
            ],
            y_range=[
                -3,
                3,
                1,
            ],
            x_length=6.2,
            y_length=5.7,
            background_line_style={
                "stroke_opacity": 0.35,
                "stroke_width": 1,
            },
            axis_config={
                "stroke_width": 2,
            },
        )

        plane.move_to(
            LEFT * 3.30 + DOWN * 0.35
        )

        info_panel = self.make_panel(
            center=RIGHT * 3.35 + DOWN * 0.30,
            color=GRAY_A,
            width=5.8,
            height=4.7,
            opacity=0.04,
        )

        info_content = VGroup(
            self.txt(
                "What to Watch",
                font_size=27,
                color=YELLOW,
            ),
            self.txt(
                "The arrow may stretch or flip.\n"
                "An eigenvector remains on the same line.",
                font_size=18,
                line_spacing=1.1,
            ),
            MathTex(
                r"A\vec{v}=\lambda\vec{v}",
                font_size=42,
            ),
        )

        info_content.arrange(
            DOWN,
            buff=0.30,
        )

        info_content.move_to(
            info_panel
        )

        self.play(
            Create(plane),
            FadeIn(info_panel),
            FadeIn(info_content),
            run_time=1.5,
        )

        line_1 = DashedLine(
            plane.c2p(
                -2.4,
                -2.4,
            ),
            plane.c2p(
                2.4,
                2.4,
            ),
            color=BLUE_A,
            stroke_opacity=0.65,
        )

        vector_1 = Arrow(
            plane.c2p(
                0,
                0,
            ),
            plane.c2p(
                1,
                1,
            ),
            buff=0,
            color=BLUE_A,
            stroke_width=7,
        )

        vector_1_label = MathTex(
            r"\vec{v}_1",
            color=BLUE_A,
            font_size=28,
        )

        vector_1_label.next_to(
            vector_1.get_end(),
            RIGHT,
            buff=0.10,
        )

        scaled_1 = Arrow(
            plane.c2p(
                0,
                0,
            ),
            plane.c2p(
                2,
                2,
            ),
            buff=0,
            color=YELLOW,
            stroke_width=8,
        )

        scaled_1_label = MathTex(
            r"2\vec{v}_1",
            color=YELLOW,
            font_size=28,
        )

        scaled_1_label.next_to(
            scaled_1.get_end(),
            LEFT,
            buff=0.10,
        )

        caption_1 = self.make_caption(
            "Eigenvalue 2: the direction stays the same and the length doubles.",
            font_size=19,
            color=BLUE_A,
        )

        self.play(
            Create(line_1),
            GrowArrow(vector_1),
            FadeIn(vector_1_label),
            FadeIn(caption_1),
        )

        self.wait(1)

        self.play(
            Transform(
                vector_1,
                scaled_1,
            ),
            Transform(
                vector_1_label,
                scaled_1_label,
            ),
            run_time=2,
        )

        self.wait(1.4)

        self.play(
            FadeOut(line_1),
            FadeOut(vector_1),
            FadeOut(vector_1_label),
            FadeOut(caption_1),
        )

        line_2 = DashedLine(
            plane.c2p(
                -2.4,
                2.4,
            ),
            plane.c2p(
                2.4,
                -2.4,
            ),
            color=GREEN_A,
            stroke_opacity=0.65,
        )

        vector_2 = Arrow(
            plane.c2p(
                0,
                0,
            ),
            plane.c2p(
                1,
                -1,
            ),
            buff=0,
            color=GREEN_A,
            stroke_width=7,
        )

        vector_2_label = MathTex(
            r"\vec{v}_2",
            color=GREEN_A,
            font_size=28,
        )

        vector_2_label.next_to(
            vector_2.get_end(),
            RIGHT,
            buff=0.10,
        )

        scaled_2 = Arrow(
            plane.c2p(
                0,
                0,
            ),
            plane.c2p(
                -2,
                2,
            ),
            buff=0,
            color=ORANGE,
            stroke_width=8,
        )

        scaled_2_label = MathTex(
            r"-2\vec{v}_2",
            color=ORANGE,
            font_size=28,
        )

        scaled_2_label.next_to(
            scaled_2.get_end(),
            RIGHT,
            buff=0.10,
        )

        caption_2 = self.make_caption(
            "Eigenvalue -2: the vector flips direction and doubles in length.",
            font_size=19,
            color=GREEN_A,
        )

        self.play(
            Create(line_2),
            GrowArrow(vector_2),
            FadeIn(vector_2_label),
            FadeIn(caption_2),
        )

        self.wait(1)

        self.play(
            Transform(
                vector_2,
                scaled_2,
            ),
            Transform(
                vector_2_label,
                scaled_2_label,
            ),
            run_time=2,
        )

        self.wait(2)

    def show_recap_scene(self):
        self.clear_screen()

        title = self.make_title(
            "Final Summary"
        )

        self.play(
            FadeIn(title)
        )

        graph_panel = self.make_panel(
            center=LEFT * 4.45 + DOWN * 0.15,
            color=BLUE_A,
            width=3.15,
            height=3.15,
            opacity=0.05,
        )

        matrix_panel = self.make_panel(
            center=LEFT * 0.75 + DOWN * 0.15,
            color=GREEN_A,
            width=3.30,
            height=3.15,
            opacity=0.05,
        )

        results_panel = self.make_panel(
            center=RIGHT * 3.85 + DOWN * 0.15,
            color=YELLOW,
            width=4.35,
            height=4.55,
            opacity=0.05,
        )

        graph_heading = self.txt(
            "1. Graph",
            font_size=23,
            color=BLUE_A,
        )

        graph_heading.move_to(
            graph_panel.get_top()
            + DOWN * 0.38
        )

        matrix_heading = self.txt(
            "2. Matrix",
            font_size=23,
            color=GREEN_A,
        )

        matrix_heading.move_to(
            matrix_panel.get_top()
            + DOWN * 0.38
        )

        results_heading = self.txt(
            "3. Results",
            font_size=23,
            color=YELLOW,
        )

        results_heading.move_to(
            results_panel.get_top()
            + DOWN * 0.38
        )

        self.play(
            FadeIn(graph_panel),
            FadeIn(matrix_panel),
            FadeIn(results_panel),
            FadeIn(graph_heading),
            FadeIn(matrix_heading),
            FadeIn(results_heading),
            run_time=1.0,
        )

        graph, _, _, _ = self.make_graph(
            center=(
                graph_panel.get_center()
                + DOWN * 0.18
            ),
            scale_factor=0.52,
        )

        matrix = self.make_labeled_matrix(
            center=(
                matrix_panel.get_center()
                + DOWN * 0.05
            ),
            scale_factor=0.55,
        )

        self.play(
            FadeIn(graph),
            FadeIn(matrix),
            run_time=1.2,
        )

        arrow_1 = Arrow(
            graph_panel.get_right()
            + RIGHT * 0.06,
            matrix_panel.get_left()
            + LEFT * 0.06,
            buff=0.05,
            color=GRAY_A,
            stroke_width=5,
        )

        arrow_2 = Arrow(
            matrix_panel.get_right()
            + RIGHT * 0.06,
            results_panel.get_left()
            + LEFT * 0.06,
            buff=0.05,
            color=GRAY_A,
            stroke_width=5,
        )

        self.play(
            GrowArrow(arrow_1),
            GrowArrow(arrow_2),
            run_time=1.0,
        )

        eigenvalues_title = self.txt(
            "Eigenvalues",
            font_size=21,
            color=GREEN_A,
        )

        eigenvalues_equation = MathTex(
            r"\lambda_1=2"
            r"\qquad"
            r"\lambda_2=-2",
            font_size=29,
        )

        divider = Line(
            LEFT * 1.45,
            RIGHT * 1.45,
            color=GRAY_B,
            stroke_width=2,
        )

        eigenvectors_title = self.txt(
            "Eigenvectors",
            font_size=21,
            color=BLUE_A,
        )

        eigenvectors_equation = MathTex(
            r"\vec{v}_1="
            r"\begin{bmatrix}"
            r"1\\1"
            r"\end{bmatrix}"
            r"\qquad"
            r"\vec{v}_2="
            r"\begin{bmatrix}"
            r"1\\-1"
            r"\end{bmatrix}",
            font_size=27,
        )

        results_content = VGroup(
            eigenvalues_title,
            eigenvalues_equation,
            divider,
            eigenvectors_title,
            eigenvectors_equation,
        )

        results_content.arrange(
            DOWN,
            buff=0.22,
        )

        results_content.move_to(
            results_panel.get_center()
            + DOWN * 0.12
        )

        self.play(
            FadeIn(
                results_content,
                shift=UP * 0.15,
            ),
            run_time=1.2,
        )

        caption = self.make_caption(
            "Graph to matrix, then matrix to eigenvalues and eigenvectors.",
            font_size=20,
            color=YELLOW,
        )

        self.play(
            FadeIn(caption)
        )

        self.wait(3)

    def construct(self):
        self.show_graph_scene()
        self.show_matrix_scene()
        self.show_meaning_scene()
        self.show_equation_explanation_scene()
        self.show_eigenvalue_scene()
        self.show_eigenvector_scene()
        self.show_geometry_scene()
        self.show_recap_scene()
