from manim import *
import numpy as np


class GraphMatrixRepresentation(Scene):

    # Basic graph data
    SLOTS = ("TL", "TR", "BL", "BR")
    NAMES = ("A", "B", "C", "D")

    NODE_COLORS = {
        "A": RED_C,
        "B": BLUE_C,
        "C": GREEN_C,
        "D": YELLOW_C,
    }

    SLOT_POSITIONS = {
        "TL": np.array([-1.3, 1.2, 0]),
        "TR": np.array([1.3, 1.2, 0]),
        "BL": np.array([-1.3, -1.2, 0]),
        "BR": np.array([1.3, -1.2, 0]),
    }

    ORIGINAL_NAMES = {
        "TL": "A",
        "TR": "B",
        "BL": "C",
        "BR": "D",
    }

    FLIPPED_NAMES = {
        "TL": "D",
        "TR": "C",
        "BL": "B",
        "BR": "A",
    }

    EDGE_DATA = [
        ("TL", "TR", 3),
        ("TL", "BL", 2),
        ("TR", "BL", 4),
        ("TR", "BR", 1),
        ("BL", "BR", 5),
    ]

    ORIGINAL_MATRIX = [
        [0, 3, 2, 0],
        [3, 0, 4, 1],
        [2, 4, 0, 5],
        [0, 1, 5, 0],
    ]

    NEW_MATRIX = [
        [0, 5, 1, 0],
        [5, 0, 4, 2],
        [1, 4, 0, 3],
        [0, 2, 3, 0],
    ]

    # Common layout functions

    def scene_title(self, text, color=WHITE, font_size=40):
        # Keep each scene title in the same position.
        title = Text(text, font_size=font_size, color=color)
        title.to_edge(UP, buff=0.22)
        return title

    def bottom_text(self, text, color=WHITE, font_size=24):
        # Put short explanations at the bottom of the screen.
        caption = Text(text, font_size=font_size, color=color)
        caption.to_edge(DOWN, buff=0.22)
        return caption

    def badge(self, text, color, center, width=2.75):
        # Create labels such as ORIGINAL GRAPH and NEW MATRIX.
        box = RoundedRectangle(
            width=width,
            height=0.52,
            corner_radius=0.12,
            stroke_color=color,
            stroke_width=3,
        )
        box.set_fill(color, opacity=0.15)

        label = Text(text, font_size=21, color=color)

        badge = VGroup(box, label)
        badge.move_to(center)

        return badge

    def comparison_panel(self, center, color):
        # Add a colored background around a comparison matrix.
        panel = RoundedRectangle(
            width=5.65,
            height=4.65,
            corner_radius=0.18,
            stroke_color=color,
            stroke_width=4,
        )
        panel.set_fill(color, opacity=0.08)
        panel.move_to(center)
        panel.set_z_index(-20)

        return panel

    def fade_out_all(self, *objects, run_time=1.2):
        # Remove several objects at once.
        self.play(
            *[FadeOut(obj) for obj in objects],
            run_time=run_time,
        )

    # Edge functions

    def make_edge(self, start_slot, end_slot, weight):
        # Create one edge and place its weight in the middle.
        start = self.SLOT_POSITIONS[start_slot]
        end = self.SLOT_POSITIONS[end_slot]
        direction = normalize(end - start)

        # Shorten the line so it stops at the outside of each node.
        edge = Line(
            start + direction * 0.43,
            end - direction * 0.43,
            color=WHITE,
            stroke_width=7,
        )
        edge.set_z_index(-5)

        weight_label = MathTex(str(weight), font_size=34, color=WHITE)
        weight_label.move_to(edge.get_center())

        # The dark background keeps the number visible over the line.
        weight_label.add_background_rectangle(
            color=BLACK,
            opacity=0.95,
            buff=0.09,
        )
        weight_label.set_z_index(30)

        return edge, weight_label

    def make_all_edges(self):
        # Build every edge and store them using their positions.
        edges = {}
        weights = {}

        for start, end, weight in self.EDGE_DATA:
            edge, number = self.make_edge(start, end, weight)
            key = f"{start}_{end}"

            edges[key] = edge
            weights[key] = number

        return edges, weights

    # Node models

    def make_circle_node(self, slot, name):
        # Create the basic mathematical node model.
        circle = Circle(radius=0.38)
        circle.set_fill(self.NODE_COLORS[name], opacity=1)
        circle.set_stroke(WHITE, width=3)
        circle.move_to(self.SLOT_POSITIONS[slot])
        circle.set_z_index(5)

        label = MathTex(name, font_size=34, color=WHITE)
        label.add_background_rectangle(
            color=BLACK,
            opacity=0.8,
            buff=0.06,
        )
        label.move_to(circle)
        label.set_z_index(25)

        return VGroup(circle, label)

    def make_house_node(self, slot, name):
        # Create a house for the neighborhood model.
        color = self.NODE_COLORS[name]

        body = Square(side_length=0.62)
        body.set_fill(color, opacity=1)
        body.set_stroke(WHITE, width=2)

        roof = Polygon(
            [-0.39, 0.29, 0],
            [0, 0.68, 0],
            [0.39, 0.29, 0],
        )
        roof.set_fill(color, opacity=1)
        roof.set_stroke(WHITE, width=2)

        door = Rectangle(width=0.16, height=0.29)
        door.set_fill(BLACK, opacity=0.8)
        door.set_stroke(WHITE, width=1)
        door.move_to([0, -0.165, 0])

        left_window = Square(side_length=0.11)
        left_window.set_fill(WHITE, opacity=1)
        left_window.set_stroke(BLACK, width=1)
        left_window.move_to([-0.18, 0.06, 0])

        right_window = left_window.copy()
        right_window.move_to([0.18, 0.06, 0])

        house = VGroup(
            body,
            roof,
            door,
            left_window,
            right_window,
        )
        house.move_to(self.SLOT_POSITIONS[slot])
        house.set_z_index(5)

        label = MathTex(name, font_size=32, color=WHITE)
        label.add_background_rectangle(
            color=BLACK,
            opacity=0.95,
            buff=0.07,
        )
        label.next_to(house, DOWN, buff=0.06)
        label.set_z_index(30)

        return VGroup(house, label)

    def make_person_node(self, slot, name):
        # Create a face for the social-network model.
        color = self.NODE_COLORS[name]

        face = Circle(radius=0.36)
        face.set_fill(color, opacity=1)
        face.set_stroke(WHITE, width=2)

        left_eye = Dot(
            point=[-0.11, 0.08, 0],
            radius=0.035,
            color=BLACK,
        )

        right_eye = Dot(
            point=[0.11, 0.08, 0],
            radius=0.035,
            color=BLACK,
        )

        smile = Arc(
            radius=0.15,
            start_angle=PI,
            angle=PI,
            color=BLACK,
            stroke_width=3,
        )
        smile.shift(DOWN * 0.04)

        person = VGroup(
            face,
            left_eye,
            right_eye,
            smile,
        )
        person.move_to(self.SLOT_POSITIONS[slot])
        person.set_z_index(5)

        label = MathTex(name, font_size=32, color=WHITE)
        label.add_background_rectangle(
            color=BLACK,
            opacity=0.95,
            buff=0.07,
        )
        label.next_to(person, DOWN, buff=0.08)
        label.set_z_index(30)

        return VGroup(person, label)

    def make_node(self, model, slot, name):
        # Pick the visual model used for each node.
        models = {
            "circle": self.make_circle_node,
            "house": self.make_house_node,
            "person": self.make_person_node,
        }

        if model not in models:
            raise ValueError(f"Unknown node model: {model}")

        return models[model](slot, name)

    def make_nodes(self, model, name_map):
        # Create all four nodes using the same model.
        return {
            slot: self.make_node(model, slot, name_map[slot])
            for slot in self.SLOTS
        }

    def transform_node_model(
        self,
        current_nodes,
        new_model,
        name_map,
        extra_animations=None,
        run_time=2,
    ):
        # Change all four nodes into a different model.
        new_nodes = self.make_nodes(new_model, name_map)

        animations = [
            ReplacementTransform(
                current_nodes[slot],
                new_nodes[slot],
            )
            for slot in self.SLOTS
        ]

        if extra_animations:
            animations.extend(extra_animations)

        self.play(
            *animations,
            run_time=run_time,
        )

        return new_nodes

    # Complete graph functions

    def make_graph_parts(self, name_map, model="house"):
        # Create the graph as separate edges, weights, and nodes.
        edges, weights = self.make_all_edges()
        nodes = self.make_nodes(model, name_map)

        return edges, weights, nodes

    def make_graph(
        self,
        name_map,
        model="house",
        center=ORIGIN,
        scale_factor=1,
    ):
        # Combine the whole graph into one movable group.
        edges, weights, nodes = self.make_graph_parts(
            name_map,
            model,
        )

        graph = VGroup(
            VGroup(*edges.values()),
            VGroup(*weights.values()),
            VGroup(*nodes.values()),
        )

        graph.scale(scale_factor)
        graph.move_to(center)

        return graph

    def animate_graph_build(self, edges, weights, nodes):
        # Show the nodes first, then the edges, then the weights.
        self.play(
            LaggedStart(
                *[
                    GrowFromCenter(nodes[slot])
                    for slot in self.SLOTS
                ],
                lag_ratio=0.18,
            ),
            run_time=1.8,
        )

        self.play(
            LaggedStart(
                *[
                    Create(edge)
                    for edge in edges.values()
                ],
                lag_ratio=0.14,
            ),
            run_time=2,
        )

        self.play(
            LaggedStart(
                *[
                    FadeIn(number, scale=0.6)
                    for number in weights.values()
                ],
                lag_ratio=0.12,
            ),
            run_time=1.5,
        )

    # Matrix functions

    def make_matrix(
        self,
        values,
        names,
        center,
        scale_factor=1,
        full_names=False,
        color_keys=None,
    ):
        # Create the matrix and its row and column labels.
        matrix = Matrix(
            values,
            element_to_mobject=lambda value: MathTex(
                str(value),
                font_size=32,
                color=WHITE,
            ),
            h_buff=0.72,
            v_buff=0.62,
            bracket_h_buff=0.13,
            bracket_v_buff=0.13,
        )

        matrix.scale(scale_factor)
        matrix.move_to(center)

        # Use gray for zeros and white for real edge weights.
        for index, entry in enumerate(matrix.get_entries()):
            row = index // 4
            column = index % 4
            value = values[row][column]

            entry.set_color(GRAY_B if value == 0 else WHITE)
            entry.set_z_index(15)

        color_keys = color_keys or list(self.NAMES)

        row_labels = VGroup()
        column_labels = VGroup()

        row_gap = 0.20
        column_gap = 0.20

        normal_size = max(18, int(30 * scale_factor))
        full_row_size = max(16, int(24 * scale_factor))
        full_column_size = max(15, int(22 * scale_factor))

        for index, name in enumerate(names):
            if full_names:
                row_label = Text(
                    name,
                    font_size=full_row_size,
                )

                column_label = Text(
                    name,
                    font_size=full_column_size,
                )
                column_label.rotate(PI / 4)

            else:
                row_label = MathTex(
                    name,
                    font_size=normal_size,
                )

                column_label = MathTex(
                    name,
                    font_size=normal_size,
                )

            color = self.NODE_COLORS[color_keys[index]]

            row_label.set_color(color)
            column_label.set_color(color)

            # Keep the visible space beside every row label equal.
            row_y = matrix.get_rows()[index].get_center()[1]
            row_x = (
                matrix.get_left()[0]
                - row_gap
                - row_label.width / 2
            )

            row_label.move_to([row_x, row_y, 0])

            # Keep the visible space above every column label equal.
            column_x = matrix.get_columns()[index].get_center()[0]
            column_y = (
                matrix.get_top()[1]
                + column_gap
                + column_label.height / 2
            )

            column_label.move_to([column_x, column_y, 0])

            row_label.set_z_index(20)
            column_label.set_z_index(20)

            row_labels.add(row_label)
            column_labels.add(column_label)

        return VGroup(
            matrix,
            row_labels,
            column_labels,
        )

    def make_dimension_guides(self, matrix_group):
        # Show that the matrix has four rows and four columns.
        matrix = matrix_group[0]

        top_line = DashedLine(
            matrix.get_corner(UL) + UP * 0.60,
            matrix.get_corner(UR) + UP * 0.60,
            dash_length=0.12,
            color=WHITE,
            stroke_width=4,
        )

        top_left_tick = Line(
            top_line.get_start() + DOWN * 0.13,
            top_line.get_start() + UP * 0.13,
            color=WHITE,
            stroke_width=4,
        )

        top_right_tick = Line(
            top_line.get_end() + DOWN * 0.13,
            top_line.get_end() + UP * 0.13,
            color=WHITE,
            stroke_width=4,
        )

        column_text = Text(
            "4 columns",
            font_size=21,
            color=WHITE,
        )
        column_text.next_to(top_line, UP, buff=0.08)

        side_line = DashedLine(
            matrix.get_corner(UL) + LEFT * 0.78,
            matrix.get_corner(DL) + LEFT * 0.78,
            dash_length=0.12,
            color=WHITE,
            stroke_width=4,
        )

        side_top_tick = Line(
            side_line.get_start() + LEFT * 0.13,
            side_line.get_start() + RIGHT * 0.13,
            color=WHITE,
            stroke_width=4,
        )

        side_bottom_tick = Line(
            side_line.get_end() + LEFT * 0.13,
            side_line.get_end() + RIGHT * 0.13,
            color=WHITE,
            stroke_width=4,
        )

        row_text = Text(
            "4 rows",
            font_size=21,
            color=WHITE,
        )
        row_text.rotate(PI / 2)
        row_text.next_to(side_line, LEFT, buff=0.08)

        return VGroup(
            top_line,
            top_left_tick,
            top_right_tick,
            column_text,
            side_line,
            side_top_tick,
            side_bottom_tick,
            row_text,
        )

    def show_matrix(self, matrix_group, guides=None):
        # Animate the brackets, labels, values, and guides.
        matrix = matrix_group[0]

        labels = VGroup(
            matrix_group[1],
            matrix_group[2],
        )

        self.play(
            Create(matrix.get_brackets()),
            FadeIn(labels),
            run_time=1,
        )

        self.play(
            LaggedStart(
                *[
                    Write(entry)
                    for entry in matrix.get_entries()
                ],
                lag_ratio=0.06,
            ),
            run_time=2.6,
        )

        if guides:
            self.play(
                Create(guides[0]),
                Create(guides[1]),
                Create(guides[2]),
                FadeIn(guides[3]),
                Create(guides[4]),
                Create(guides[5]),
                Create(guides[6]),
                FadeIn(guides[7]),
                run_time=1.4,
            )

    def make_changed_boxes(self, original_matrix, new_matrix):
        # Outline every matrix value that changed.
        original_entries = original_matrix[0].get_entries()
        new_entries = new_matrix[0].get_entries()

        original_boxes = VGroup()
        new_boxes = VGroup()

        for index in range(16):
            row = index // 4
            column = index % 4

            old_value = self.ORIGINAL_MATRIX[row][column]
            new_value = self.NEW_MATRIX[row][column]

            if old_value != new_value:
                original_boxes.add(
                    SurroundingRectangle(
                        original_entries[index],
                        color=YELLOW,
                        buff=0.08,
                        stroke_width=2,
                    )
                )

                new_boxes.add(
                    SurroundingRectangle(
                        new_entries[index],
                        color=YELLOW,
                        buff=0.08,
                        stroke_width=2,
                    )
                )

        return original_boxes, new_boxes

    # Reusable explanation sequences

    def explain_edges(self, edges, weights):
        # Explain what edges and edge weights represent.
        explanation = self.bottom_text(
            "An edge shows that two nodes are connected",
            font_size=26,
        )

        self.play(
            FadeIn(explanation, shift=UP * 0.2),
            Indicate(
                edges["TL_TR"],
                color=YELLOW,
                scale_factor=1.05,
            ),
            run_time=1.5,
        )

        self.wait(1.5)

        weight_text = self.bottom_text(
            "The number is the edge weight, or strength of the connection",
            font_size=25,
        )

        self.play(
            Transform(explanation, weight_text),
            Indicate(
                weights["TL_TR"],
                color=YELLOW,
                scale_factor=1.4,
            ),
            run_time=1.5,
        )

        self.wait(1.5)

        strength_text = self.bottom_text(
            "A larger weight means a stronger connection",
            color=YELLOW,
            font_size=26,
        )

        self.play(
            Transform(explanation, strength_text),
            run_time=1.2,
        )

        weak_label = Text(
            "1 = weaker connection",
            font_size=22,
            color=RED_A,
        )
        weak_label.next_to(
            weights["TR_BR"],
            RIGHT,
            buff=0.25,
        )

        self.play(
            FadeIn(weak_label),
            Indicate(
                edges["TR_BR"],
                color=RED_A,
                scale_factor=1.05,
            ),
            Indicate(
                weights["TR_BR"],
                color=RED_A,
                scale_factor=1.4,
            ),
            run_time=1.3,
        )

        self.wait(1)

        strong_label = Text(
            "5 = stronger connection",
            font_size=22,
            color=GREEN_A,
        )
        strong_label.next_to(
            weights["BL_BR"],
            DOWN,
            buff=0.25,
        )

        self.play(
            FadeIn(strong_label),
            Indicate(
                edges["BL_BR"],
                color=GREEN_A,
                scale_factor=1.05,
            ),
            Indicate(
                weights["BL_BR"],
                color=GREEN_A,
                scale_factor=1.4,
            ),
            run_time=1.3,
        )

        self.wait(1.5)

        self.fade_out_all(
            explanation,
            weak_label,
            strong_label,
            run_time=1,
        )

    def show_real_world_models(self, circle_nodes):
        # Show two different real-world meanings for the same graph.
        house_caption = self.bottom_text(
            "Neighborhood model: edges are roads and weights can show traffic flow",
            font_size=23,
        )

        house_nodes = self.transform_node_model(
            current_nodes=circle_nodes,
            new_model="house",
            name_map=self.ORIGINAL_NAMES,
            extra_animations=[
                FadeIn(
                    house_caption,
                    shift=UP * 0.2,
                )
            ],
        )

        self.wait(1.5)

        people_caption = self.bottom_text(
            "Social model: edges are relationships and weights show closeness",
            font_size=23,
        )

        people_nodes = self.transform_node_model(
            current_nodes=house_nodes,
            new_model="person",
            name_map=self.ORIGINAL_NAMES,
            extra_animations=[
                Transform(
                    house_caption,
                    people_caption,
                )
            ],
        )

        self.wait(1.5)

        final_caption = self.bottom_text(
            "The graph stays the same even when the real-world model changes",
            font_size=23,
        )

        final_houses = self.transform_node_model(
            current_nodes=people_nodes,
            new_model="house",
            name_map=self.ORIGINAL_NAMES,
            extra_animations=[
                Transform(
                    house_caption,
                    final_caption,
                )
            ],
        )

        self.wait(1.5)
        self.play(FadeOut(house_caption))

        return final_houses

    # Scene functions

    def show_intro_scene(self):
        # Introduce the graph, weights, and real-world models.
        main_title = Text(
            "Graph Representation with Matrices",
            font_size=48,
        )
        main_title.set_color_by_gradient(
            BLUE_A,
            GREEN_A,
        )

        self.play(
            Write(main_title),
            run_time=1.4,
        )

        self.wait(0.5)

        self.play(
            main_title.animate
            .scale(0.65)
            .to_edge(UP),
            run_time=0.8,
        )

        nodes_heading = Text(
            "Nodes",
            font_size=34,
            color=WHITE,
        )
        nodes_heading.next_to(
            main_title,
            DOWN,
            buff=0.28,
        )

        self.play(
            FadeIn(
                nodes_heading,
                shift=DOWN * 0.2,
            )
        )

        edges, weights, circle_nodes = self.make_graph_parts(
            self.ORIGINAL_NAMES,
            model="circle",
        )

        self.animate_graph_build(
            edges,
            weights,
            circle_nodes,
        )

        self.explain_edges(
            edges,
            weights,
        )

        final_houses = self.show_real_world_models(
            circle_nodes
        )

        graph = VGroup(
            VGroup(*edges.values()),
            VGroup(*weights.values()),
            VGroup(*final_houses.values()),
        )

        return main_title, nodes_heading, graph

    def show_graph_matrix_scene(
        self,
        main_title,
        nodes_heading,
        graph,
    ):
        # Place the original graph beside its matrix.
        title = self.scene_title(
            "Graph and Adjacency Matrix"
        )

        matrix = self.make_matrix(
            self.ORIGINAL_MATRIX,
            self.NAMES,
            RIGHT * 3.25 + DOWN * 0.35,
            scale_factor=0.90,
        )

        guides = self.make_dimension_guides(matrix)

        self.play(
            FadeOut(main_title),
            FadeOut(nodes_heading),
            FadeIn(title),
            graph.animate
            .scale(0.82)
            .move_to(
                LEFT * 3.35 + DOWN * 0.35
            ),
            run_time=1.4,
        )

        self.show_matrix(
            matrix,
            guides,
        )

        zero_note = self.bottom_text(
            "A zero means there is no direct connection",
            color=GRAY_A,
        )

        self.play(FadeIn(zero_note))
        self.wait(1.5)
        self.play(FadeOut(zero_note))

        return title, graph, matrix, guides

    def show_renamed_matrix_scene(
        self,
        old_title,
        graph,
        old_matrix,
        guides,
    ):
        # Show that simple renaming keeps the same matrix values.
        title = self.scene_title(
            "Same Matrix, Different Node Names"
        )

        original_matrix = self.make_matrix(
            self.ORIGINAL_MATRIX,
            self.NAMES,
            LEFT * 3.25 + DOWN * 0.45,
            scale_factor=0.76,
        )

        renamed_matrix = self.make_matrix(
            self.ORIGINAL_MATRIX,
            ["Oak", "Pine", "Maple", "Cedar"],
            RIGHT * 3.25 + DOWN * 0.45,
            scale_factor=0.70,
            full_names=True,
            color_keys=self.NAMES,
        )

        heading_y = max(
            original_matrix.get_top()[1],
            renamed_matrix.get_top()[1],
        ) + 0.58

        original_heading = Text(
            "Original labels",
            font_size=24,
            color=BLUE_A,
        )
        original_heading.move_to([
            original_matrix[0].get_center()[0],
            heading_y,
            0,
        ])

        renamed_heading = Text(
            "Same graph, different node names",
            font_size=24,
            color=ORANGE,
        )
        renamed_heading.move_to([
            renamed_matrix[0].get_center()[0],
            heading_y,
            0,
        ])

        self.fade_out_all(
            old_title,
            graph,
            old_matrix,
            guides,
        )

        self.play(FadeIn(title))

        self.play(
            FadeIn(original_matrix),
            FadeIn(renamed_matrix),
            FadeIn(original_heading),
            FadeIn(renamed_heading),
            run_time=1.6,
        )

        note = self.bottom_text(
            "Only the names changed, so the matrix values stay the same",
            color=GRAY_A,
        )

        self.play(FadeIn(note))
        self.wait(2)

        return (
            title,
            original_matrix,
            renamed_matrix,
            original_heading,
            renamed_heading,
            note,
        )

    def show_morph_scene(
        self,
        old_title,
        old_original_matrix,
        old_renamed_matrix,
        original_heading,
        renamed_heading,
        old_note,
    ):
        # Change the graph first, then update the matrix.
        title = self.scene_title(
            "Changing the Node Names"
        )

        graph = self.make_graph(
            self.ORIGINAL_NAMES,
            model="house",
            center=LEFT * 3.35 + DOWN * 0.45,
            scale_factor=0.82,
        )

        matrix = self.make_matrix(
            self.ORIGINAL_MATRIX,
            self.NAMES,
            RIGHT * 3.25 + DOWN * 0.45,
            scale_factor=0.88,
        )

        graph_badge = self.badge(
            "ORIGINAL GRAPH",
            BLUE_A,
            LEFT * 3.35 + UP * 2.05,
        )

        matrix_badge = self.badge(
            "ORIGINAL MATRIX",
            BLUE_A,
            RIGHT * 3.25 + UP * 2.05,
        )

        self.fade_out_all(
            old_title,
            old_original_matrix,
            old_renamed_matrix,
            original_heading,
            renamed_heading,
            old_note,
        )

        self.play(
            FadeIn(title),
            FadeIn(graph),
            FadeIn(matrix),
            FadeIn(graph_badge),
            FadeIn(matrix_badge),
            run_time=1.5,
        )

        self.wait(1)

        # Move the node identities first.
        new_graph = self.make_graph(
            self.FLIPPED_NAMES,
            model="house",
            center=LEFT * 3.35 + DOWN * 0.45,
            scale_factor=0.82,
        )

        new_graph_badge = self.badge(
            "NEW GRAPH",
            ORANGE,
            LEFT * 3.35 + UP * 2.05,
        )

        graph_note = self.bottom_text(
            "First, the names and colors move to new vertices",
            color=ORANGE,
            font_size=23,
        )

        self.play(
            Transform(graph, new_graph),
            Transform(
                graph_badge,
                new_graph_badge,
            ),
            FadeIn(
                graph_note,
                shift=UP * 0.15,
            ),
            run_time=2.5,
        )

        self.wait(1.5)
        self.play(FadeOut(graph_note))

        # Update the matrix after the graph changes.
        new_matrix = self.make_matrix(
            self.NEW_MATRIX,
            self.NAMES,
            RIGHT * 3.25 + DOWN * 0.45,
            scale_factor=0.88,
        )

        new_matrix_badge = self.badge(
            "NEW MATRIX",
            ORANGE,
            RIGHT * 3.25 + UP * 2.05,
        )

        matrix_note = self.bottom_text(
            "Next, the matrix updates to match the new graph",
            color=ORANGE,
            font_size=23,
        )

        self.play(
            Transform(matrix, new_matrix),
            Transform(
                matrix_badge,
                new_matrix_badge,
            ),
            FadeIn(
                matrix_note,
                shift=UP * 0.15,
            ),
            run_time=2.5,
        )

        self.wait(2)

        return (
            title,
            graph,
            matrix,
            graph_badge,
            matrix_badge,
            matrix_note,
        )

    def show_comparison_scene(
        self,
        old_title,
        graph,
        matrix,
        graph_badge,
        matrix_badge,
        old_note,
    ):
        # Compare the original and new matrices.
        title = self.scene_title(
            "Original Matrix vs. New Matrix"
        )

        subtitle = Text(
            "Yellow outlines show the values that changed",
            font_size=22,
            color=YELLOW,
        )
        subtitle.next_to(
            title,
            DOWN,
            buff=0.12,
        )

        original_panel = self.comparison_panel(
            LEFT * 3.25 + DOWN * 0.35,
            BLUE_A,
        )

        new_panel = self.comparison_panel(
            RIGHT * 3.25 + DOWN * 0.35,
            ORANGE,
        )

        original_badge = self.badge(
            "ORIGINAL MATRIX",
            BLUE_A,
            LEFT * 3.25 + UP * 1.55,
            width=2.9,
        )

        new_badge = self.badge(
            "NEW MATRIX",
            ORANGE,
            RIGHT * 3.25 + UP * 1.55,
            width=2.9,
        )

        original_matrix = self.make_matrix(
            self.ORIGINAL_MATRIX,
            self.NAMES,
            LEFT * 3.25 + DOWN * 0.45,
            scale_factor=0.82,
        )

        new_matrix = self.make_matrix(
            self.NEW_MATRIX,
            self.NAMES,
            RIGHT * 3.25 + DOWN * 0.45,
            scale_factor=0.82,
        )

        self.fade_out_all(
            old_title,
            graph,
            matrix,
            graph_badge,
            matrix_badge,
            old_note,
        )

        self.play(
            FadeIn(title),
            FadeIn(subtitle),
            FadeIn(original_panel),
            FadeIn(new_panel),
            FadeIn(original_badge),
            FadeIn(new_badge),
            FadeIn(original_matrix),
            FadeIn(new_matrix),
            run_time=1.8,
        )

        original_boxes, new_boxes = self.make_changed_boxes(
            original_matrix,
            new_matrix,
        )

        self.play(
            LaggedStart(
                *[
                    Create(box)
                    for box in [
                        *original_boxes,
                        *new_boxes,
                    ]
                ],
                lag_ratio=0.05,
            ),
            run_time=2.5,
        )

        self.wait(2)

        self.play(
            Circumscribe(
                original_panel,
                color=BLUE_A,
                buff=0.04,
            ),
            run_time=1,
        )

        self.play(
            Circumscribe(
                new_panel,
                color=ORANGE,
                buff=0.04,
            ),
            run_time=1,
        )

        self.wait(3)

    # Main animation

    def construct(self):
        # Scene 1 introduces the graph and its real-world models.
        main_title, nodes_heading, graph = self.show_intro_scene()

        # Scene 2 places the graph beside its matrix.
        graph_title, graph, matrix, guides = self.show_graph_matrix_scene(
            main_title,
            nodes_heading,
            graph,
        )

        # Scene 3 shows that basic renaming keeps the same values.
        renamed_scene = self.show_renamed_matrix_scene(
            graph_title,
            graph,
            matrix,
            guides,
        )

        # Scene 4 moves the node identities and updates the matrix.
        morph_scene = self.show_morph_scene(*renamed_scene)

        # Scene 5 compares the original and new matrices.
        self.show_comparison_scene(*morph_scene)