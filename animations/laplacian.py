from manim import *
import numpy as np


A_COLOR = BLUE_C
D_COLOR = GREEN_C
L_COLOR = ORANGE
X_COLOR = RED_C
RESULT_COLOR = PURPLE_C


class GraphSignalLaplacian(Scene):
    def node_fill_color(self, number):
        # fixed colors for the four nodes
        palette = {
            1: RED_C,
            2: YELLOW_D,
            3: BLUE_C,
            4: GREEN_C,
        }
        return palette[number]

    def make_signal_node(self, position, number, value):
        # create one colored graph node
        fill_color = self.node_fill_color(number)

        circle = Circle(radius=0.48, color=WHITE, stroke_width=3)
        circle.set_fill(fill_color, opacity=1)
        circle.move_to(position)

        label = MathTex(str(number), color=BLACK).scale(0.72)
        label.move_to(circle)

        value_label = MathTex(f"x_{number}={value}").scale(0.55)
        value_label.next_to(circle, DOWN, buff=0.14)

        return VGroup(circle, label, value_label)

    def make_sensor_house(self, position, number, value):
        # create a simple house that represents a real sensor location
        fill_color = self.node_fill_color(number)

        body = Square(side_length=0.78, color=WHITE, stroke_width=2)
        body.set_fill(fill_color, opacity=0.9)

        roof = Polygon(
            np.array([-0.50, 0.39, 0]),
            np.array([0.00, 0.86, 0]),
            np.array([0.50, 0.39, 0]),
            color=WHITE,
            stroke_width=2,
        )
        roof.set_fill(fill_color, opacity=0.9)

        door = Rectangle(height=0.35, width=0.20, color=WHITE, stroke_width=1.5)
        door.set_fill(BLACK, opacity=0.35)
        door.shift(DOWN * 0.215)

        sensor = Dot(radius=0.07, color=GOLD)
        sensor.shift(UP * 0.12)

        number_label = MathTex(str(number), color=WHITE).scale(1)
        number_label.next_to(roof, UP, buff=0.12)

        # keep the value white so it shows clearly even for the yellow house
        value_label = MathTex(f"{value}", color=WHITE).scale(0.58)
        value_label.next_to(body, DOWN, buff=0.14)

        house = VGroup(body, roof, door, sensor, number_label, value_label)
        house.move_to(position)
        return house

    def make_graph(self, positions, values):
        # create the path graph 1-2-3-4
        edge_pairs = [(0, 1), (1, 2), (2, 3)]
        edges = VGroup()

        for start, end in edge_pairs:
            edge = Line(
                positions[start],
                positions[end],
                color=GREY_B,
                stroke_width=5,
                buff=0.48,
            )
            edges.add(edge)

        nodes = VGroup(
            *[
                self.make_signal_node(positions[i], i + 1, values[i])
                for i in range(4)
            ]
        )

        return edges, nodes

    def color_math(self, expr):
        # color MathTex objects directly, or each MathTex child inside a VGroup
        if isinstance(expr, MathTex):
            math_objects = [expr]
        else:
            math_objects = [
                mob for mob in expr.get_family()
                if isinstance(mob, MathTex)
            ]

        for math_object in math_objects:
            math_object.set_color_by_tex("A", A_COLOR)
            math_object.set_color_by_tex("D", D_COLOR)
            math_object.set_color_by_tex("L", L_COLOR)
            math_object.set_color_by_tex("x", X_COLOR)

        return expr

    def construct(self):
        values = [1, 3, 5, 2]
        positions = [
            np.array([-4.2, -0.7, 0]),
            np.array([-1.5, 1.0, 0]),
            np.array([1.5, 1.0, 0]),
            np.array([4.2, -0.7, 0]),
        ]

        # scene 1: introduce the graph signal
        title = Text("A Graph Signal", font_size=44).to_edge(UP)
        subtitle = MathTex(r"x=[1,3,5,2]^T").scale(0.8)
        self.color_math(subtitle)
        subtitle.next_to(title, DOWN, buff=0.18)

        edges, nodes = self.make_graph(positions, values)
        graph = VGroup(edges, nodes)

        self.play(Write(title), FadeIn(subtitle, shift=UP * 0.2))
        self.play(LaggedStart(*[Create(edge) for edge in edges], lag_ratio=0.2))
        self.play(LaggedStart(*[FadeIn(node, scale=0.7) for node in nodes], lag_ratio=0.18))
        self.wait(1)

        graph_explanation = Text(
            "Each color stores a value on a node.",
            font_size=28,
        ).to_edge(DOWN)
        self.play(FadeIn(graph_explanation, shift=UP * 0.15))
        self.wait(1)

        # scene 2: transform the abstract nodes into a real-life example
        real_title = Text("Real example: connected air-quality sensors", font_size=38)
        real_title.to_edge(UP)

        houses = VGroup(
            *[
                self.make_sensor_house(positions[i], i + 1, values[i])
                for i in range(4)
            ]
        )

        self.play(
            ReplacementTransform(title, real_title),
            FadeOut(subtitle),
            FadeOut(graph_explanation),
        )
        self.play(
            LaggedStart(
                *[
                    ReplacementTransform(nodes[i], houses[i])
                    for i in range(4)
                ],
                lag_ratio=0.15,
            )
        )

        real_explanation = VGroup(
            Text("Nodes = sensor locations", font_size=27),
            Text("Edges = communication links", font_size=27),
            Text("Values = pollution reading", font_size=27),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        real_explanation.to_edge(DOWN)

        self.play(LaggedStart(*[Write(line) for line in real_explanation], lag_ratio=0.2))
        self.wait(1.5)

        # transform the real example back into graph nodes
        abstract_title = Text("The same information as a graph signal", font_size=38)
        abstract_title.to_edge(UP)

        nodes_back = VGroup(
            *[
                self.make_signal_node(positions[i], i + 1, values[i])
                for i in range(4)
            ]
        )

        self.play(
            ReplacementTransform(real_title, abstract_title),
            FadeOut(real_explanation),
        )
        self.play(
            LaggedStart(
                *[
                    ReplacementTransform(houses[i], nodes_back[i])
                    for i in range(4)
                ],
                lag_ratio=0.15,
            )
        )
        graph = VGroup(edges, nodes_back)
        self.wait(1)

        # scene 3: project the signal onto a normal coordinate plot
        projection_title = Text("Projection of the graph signal", font_size=38)
        projection_title.to_edge(UP)

        self.play(ReplacementTransform(abstract_title, projection_title))
        self.play(graph.animate.scale(0.62).shift(UP * 1.55))

        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 6, 1],
            x_length=7.2,
            y_length=2.8,
            tips=False,
            axis_config={"include_numbers": True},
        ).shift(DOWN * 1.55)

        axis_labels = axes.get_axis_labels(MathTex("i"), MathTex("x_i"))
        self.color_math(axis_labels)
        stems = VGroup()
        dots = VGroup()

        for i, value in enumerate(values, start=1):
            stem_color = self.node_fill_color(i)
            stem = Line(
                axes.c2p(i, 0),
                axes.c2p(i, value),
                color=stem_color,
                stroke_width=6,
            )
            dot = Dot(
                axes.c2p(i, value),
                radius=0.11,
                color=stem_color,
            )
            stems.add(stem)
            dots.add(dot)

        self.play(Create(axes), FadeIn(axis_labels, shift=UP * 0.1))
        self.play(
            LaggedStart(
                *[GrowFromPoint(stems[i], stems[i].get_start()) for i in range(4)],
                lag_ratio=0.16,
            ),
            LaggedStart(*[FadeIn(dot, scale=0.5) for dot in dots], lag_ratio=0.16),
        )
        self.wait(1.5)

        # scene 4: build the adjacency matrix
        matrix_title = Text("The adjacency matrix describes the connections", font_size=36)
        matrix_title.to_edge(UP)

        self.play(
            ReplacementTransform(projection_title, matrix_title),
            FadeOut(VGroup(axes, axis_labels, stems, dots)),
            graph.animate.scale(0.86).move_to(LEFT * 3.55 + UP * 0.35),
        )

        adjacency = MathTex(
            r"A=\begin{bmatrix}"
            r"0&1&0&0\\"
            r"1&0&1&0\\"
            r"0&1&0&1\\"
            r"0&0&1&0"
            r"\end{bmatrix}"
        ).scale(0.82).move_to(RIGHT * 3.15 + UP * 0.3)
        self.color_math(adjacency)

        adjacency_note = VGroup(
            MathTex(r"A_{ij}=1\quad\text{when nodes share an edge}"),
            MathTex(r"A_{ij}=0\quad\text{when there is no shared edge}"),
        ).arrange(DOWN, buff=0.18).scale(0.63)
        self.color_math(adjacency_note)
        adjacency_note.next_to(adjacency, DOWN, buff=0.38)

        self.play(Write(adjacency), run_time=1.4)
        self.play(Circumscribe(adjacency, color=A_COLOR), run_time=1)
        self.play(LaggedStart(*[FadeIn(line, shift=UP * 0.1) for line in adjacency_note], lag_ratio=0.25))
        self.play(Indicate(edges[1], color=A_COLOR), run_time=0.8)
        self.wait(1.2)

        # scene 5: show how L = D - A changes each matrix entry
        laplacian_title = Text("The graph Laplacian compares neighboring values", font_size=36)
        laplacian_title.to_edge(UP)

        degree_matrix = Matrix(
            [
                ["1", "0", "0", "0"],
                ["0", "2", "0", "0"],
                ["0", "0", "2", "0"],
                ["0", "0", "0", "1"],
            ],
            h_buff=0.75,
            v_buff=0.55,
        ).scale(0.62)
        degree_label = MathTex("D=", color=D_COLOR).scale(0.82)
        degree_group = VGroup(degree_label, degree_matrix).arrange(RIGHT, buff=0.16)
        degree_group.move_to(LEFT * 3.0 + UP * 0.75)

        adjacency_matrix = Matrix(
            [
                ["0", "1", "0", "0"],
                ["1", "0", "1", "0"],
                ["0", "1", "0", "1"],
                ["0", "0", "1", "0"],
            ],
            h_buff=0.75,
            v_buff=0.55,
        ).scale(0.62)
        adjacency_label = MathTex("A=", color=A_COLOR).scale(0.82)
        adjacency_group = VGroup(adjacency_label, adjacency_matrix).arrange(RIGHT, buff=0.16)
        adjacency_group.move_to(RIGHT * 3.0 + UP * 0.75)

        subtraction_rule = MathTex("L", "=", "D", "-", "A").scale(0.9)
        subtraction_rule[0].set_color(L_COLOR)
        subtraction_rule[2].set_color(D_COLOR)
        subtraction_rule[4].set_color(A_COLOR)
        subtraction_rule.move_to(DOWN * 0.55)

        subtraction_matrix = Matrix(
            [
                [r"1-0", r"0-1", r"0-0", r"0-0"],
                [r"0-1", r"2-0", r"0-1", r"0-0"],
                [r"0-0", r"0-1", r"2-0", r"0-1"],
                [r"0-0", r"0-0", r"0-1", r"1-0"],
            ],
            h_buff=1.18,
            v_buff=0.62,
        ).scale(0.48)
        subtraction_label = MathTex("L=", color=L_COLOR).scale(0.78)
        subtraction_display = VGroup(subtraction_label, subtraction_matrix).arrange(RIGHT, buff=0.18)
        subtraction_display.move_to(DOWN * 1.95)

        final_laplacian_matrix = Matrix(
            [
                ["1", "-1", "0", "0"],
                ["-1", "2", "-1", "0"],
                ["0", "-1", "2", "-1"],
                ["0", "0", "-1", "1"],
            ],
            h_buff=0.85,
            v_buff=0.58,
        ).scale(0.68)
        final_laplacian_label = MathTex("L=", color=L_COLOR).scale(0.86)
        final_laplacian_display = VGroup(
            final_laplacian_label,
            final_laplacian_matrix,
        ).arrange(RIGHT, buff=0.18)
        final_laplacian_display.move_to(DOWN * 0.25)

        self.play(
            ReplacementTransform(matrix_title, laplacian_title),
            FadeOut(graph),
            FadeOut(adjacency_note),
            ReplacementTransform(adjacency, adjacency_group),
        )
        self.play(FadeIn(degree_group, shift=RIGHT * 0.2), run_time=1.1)
        self.play(Write(subtraction_rule))
        self.wait(0.5)

        self.play(
            FadeIn(subtraction_label),
            Create(subtraction_matrix.get_brackets()),
        )

        degree_entries = degree_matrix.get_entries()
        adjacency_entries = adjacency_matrix.get_entries()
        subtraction_entries = subtraction_matrix.get_entries()

        for row in range(4):
            row_start = row * 4
            row_end = row_start + 4
            degree_row = VGroup(*degree_entries[row_start:row_end])
            adjacency_row = VGroup(*adjacency_entries[row_start:row_end])
            subtraction_row = VGroup(*subtraction_entries[row_start:row_end])

            self.play(
                Indicate(degree_row, color=D_COLOR),
                Indicate(adjacency_row, color=A_COLOR),
                run_time=0.65,
            )
            self.play(
                LaggedStart(
                    *[FadeIn(entry, shift=UP * 0.08) for entry in subtraction_row],
                    lag_ratio=0.12,
                ),
                run_time=0.75,
            )

        subtraction_explanation = VGroup(
            MathTex(r"\text{diagonal: }d_i-0=d_i"),
            MathTex(r"\text{edge: }0-1=-1\qquad\text{no edge: }0-0=0"),
        ).arrange(DOWN, buff=0.12).scale(0.58)
        subtraction_explanation.to_edge(DOWN, buff=0.12)
        subtraction_explanation[0].set_color(D_COLOR)
        subtraction_explanation[1].set_color(A_COLOR)

        self.play(FadeIn(subtraction_explanation, shift=UP * 0.12))
        self.wait(1.0)

        self.play(
            FadeOut(degree_group),
            FadeOut(adjacency_group),
            FadeOut(subtraction_rule),
            FadeOut(subtraction_explanation),
            subtraction_display.animate.move_to(DOWN * 0.25),
            run_time=1.0,
        )

        final_entries = final_laplacian_matrix.get_entries()
        self.play(
            Transform(subtraction_label, final_laplacian_label),
            Transform(
                subtraction_matrix.get_brackets(),
                final_laplacian_matrix.get_brackets(),
            ),
            *[
                Transform(subtraction_entries[i], final_entries[i])
                for i in range(16)
            ],
            run_time=1.6,
        )
        self.play(Circumscribe(subtraction_display, color=L_COLOR), run_time=1.0)

        laplacian_note = Text(
            "The diagonal keeps each degree; connected off-diagonal entries become -1.",
            font_size=20,
        )
        laplacian_note.next_to(subtraction_display, DOWN, buff=0.42)
        self.play(FadeIn(laplacian_note, shift=UP * 0.12))
        self.wait(2.0)

        # scene 6: calculate the Laplacian operator on the signal
        calculation_title = Text("Apply the Laplacian operator to the signal", font_size=38)
        calculation_title.to_edge(UP)

        calculation = MathTex(
            r"Lx="
            r"\begin{bmatrix}"
            r"1&-1&0&0\\"
            r"-1&2&-1&0\\"
            r"0&-1&2&-1\\"
            r"0&0&-1&1"
            r"\end{bmatrix}"
            r"\begin{bmatrix}1\\3\\5\\2\end{bmatrix}"
            r"="
            r"\begin{bmatrix}-2\\0\\5\\-3\end{bmatrix}"
        ).scale(0.67).move_to(UP * 0.45)
        calculation.set_color(WHITE)

        local_rule = MathTex(
            r"(Lx)_i=d_i x_i-\sum_{j\in N(i)}x_j"
            r"=\sum_{j\in N(i)}(x_i-x_j)"
        ).scale(0.72).next_to(calculation, DOWN, buff=0.45)
        self.color_math(local_rule)

        self.play(
            ReplacementTransform(laplacian_title, calculation_title),
            FadeOut(VGroup(subtraction_display, laplacian_note)),
        )
        self.play(Write(calculation), run_time=1.8)
        self.play(Flash(calculation.get_center(), color=L_COLOR, line_length=0.3, num_lines=16))
        self.play(FadeIn(local_rule, shift=UP * 0.12))
        self.wait(1.2)

        node_calculations = VGroup(
            MathTex(r"(Lx)_1=1-3=", r"-2"),
            MathTex(r"(Lx)_2=(3-1)+(3-5)=", r"0"),
            MathTex(r"(Lx)_3=(5-3)+(5-2)=", r"5"),
            MathTex(r"(Lx)_4=2-5=", r"-3"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).scale(0.67)
        node_calculations.move_to(DOWN * 1.95)

        calc_colors = [RED_C, YELLOW_D, BLUE_C, GREEN_C]
        answer_underlines = VGroup()

        for line, color in zip(node_calculations, calc_colors):
            self.color_math(line)
            # line[0] is a rendered math part, so color it directly
            line[0].set_color(color)
            line[1].set_color(RESULT_COLOR)

            answer_underlines.add(
                Underline(
                    line[1],
                    color=RESULT_COLOR,
                    buff=0.05,
                    stroke_width=3,
                )
            )

        calculation_details = VGroup(node_calculations, answer_underlines)

        self.play(
            FadeOut(local_rule),
            calculation.animate.scale(0.82).shift(UP * 0.65),
        )
        self.play(
            LaggedStart(
                *[FadeIn(line, shift=RIGHT * 0.18) for line in node_calculations],
                lag_ratio=0.22,
            )
        )
        self.play(
            LaggedStart(
                *[Create(underline) for underline in answer_underlines],
                lag_ratio=0.22,
            )
        )
        self.wait(1.5)

        # scene 7: explain what the result means on the original graph
        meaning_title = Text("What does the Laplacian output show?", font_size=40)
        meaning_title.to_edge(UP)

        final_edges, final_nodes = self.make_graph(positions, values)
        laplacian_values = [-2, 0, 5, -3]

        result_labels = VGroup()
        for i, result in enumerate(laplacian_values):
            if result > 0:
                result_color = GREEN_C
                result_text = f"+{result}"
            elif result < 0:
                result_color = RED_C
                result_text = str(result)
            else:
                result_color = WHITE
                result_text = "0"

            label = MathTex(result_text, color=result_color).scale(0.76)
            label.next_to(final_nodes[i][0], UP, buff=0.13)
            result_labels.add(label)

        meaning = VGroup(
            Text("Positive: the node is higher than its neighbors overall.", font_size=23),
            Text("Negative: the node is lower than its neighbors overall.", font_size=23),
            Text("Near zero: the surrounding differences balance.", font_size=23),
            Text("Large magnitude: there is a sharp local change in the signal.", font_size=23),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.11)
        meaning.to_edge(DOWN, buff=0.12)

        self.play(
            ReplacementTransform(calculation_title, meaning_title),
            FadeOut(calculation),
            FadeOut(calculation_details),
        )
        final_graph = VGroup(final_edges, final_nodes).shift(UP * 0.35)
        result_labels.shift(UP * 0.35)

        self.play(Create(final_edges))
        self.play(LaggedStart(*[FadeIn(node, scale=0.7) for node in final_nodes], lag_ratio=0.15))
        self.play(LaggedStart(*[FadeIn(label, shift=DOWN * 0.15) for label in result_labels], lag_ratio=0.15))
        self.play(Write(meaning[0]))
        self.play(Circumscribe(final_nodes[2][0], color=GREEN_C), run_time=1)
        self.play(Write(meaning[1]))
        self.play(Circumscribe(final_nodes[3][0], color=RED_C), run_time=1)
        self.play(Write(meaning[2]))
        self.play(Circumscribe(final_nodes[1][0], color=WHITE), run_time=1)
        self.play(Write(meaning[3]))
        self.wait(2)

        final_formula = MathTex(
            r"Lx\text{ measures local differences across the graph.}"
        ).scale(0.78).to_edge(DOWN)
        self.color_math(final_formula)

        self.play(FadeOut(meaning), FadeIn(final_formula, shift=UP * 0.15))
        self.wait(2)
