# imports manim, numpy, and the reusable graph tools
from manim import *
import numpy as np


from graphcommons import (
    adjacency_values_from_graph,
    animate_graph_build,
    animate_matrix_build,
    badge,
    bottom_text,
    comparison_panel,
    fade_out_all,
    make_adjacency_matrix,
    make_changed_boxes,
    make_dimension_guides,
    make_graph,
    make_graph_group,
    refresh_graph_group,
    scene_title,
    switch_node_icons,
)




class GraphMatrixRepresentation(Scene):


    # stores the names, colors, positions, and edges used in every section
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


    # calculates the matrix before the node names move
    ORIGINAL_MATRIX = adjacency_values_from_graph(
        node_order=NAMES,
        edge_data=EDGE_DATA,
        name_map=ORIGINAL_NAMES,
    )


    # calculates the matrix after the node names move
    NEW_MATRIX = adjacency_values_from_graph(
        node_order=NAMES,
        edge_data=EDGE_DATA,
        name_map=FLIPPED_NAMES,
    )


    # explains what graph edges and weights mean
    def explain_edges(self, edges, weights):
        # introduces what an edge means
        explanation = bottom_text(
            "An edge shows that two nodes are connected",
            font_size=26,
        )


        self.play(
            FadeIn(explanation, shift=UP * 0.2),
            Indicate(
                edges[("TL", "TR")],
                color=YELLOW,
                scale_factor=1.05,
            ),
            run_time=1.5,
        )


        self.wait(1.5)


        # explains that the number on an edge is its weight
        weight_text = bottom_text(
            "The number is the edge weight, or strength of the connection",
            font_size=25,
        )


        self.play(
            Transform(explanation, weight_text),
            Indicate(
                weights[("TL", "TR")],
                color=YELLOW,
                scale_factor=1.4,
            ),
            run_time=1.5,
        )


        self.wait(1.5)


        # compares a small weight with a large weight
        strength_text = bottom_text(
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
            weights[("TR", "BR")],
            RIGHT,
            buff=0.25,
        )


        self.play(
            FadeIn(weak_label),
            Indicate(
                edges[("TR", "BR")],
                color=RED_A,
                scale_factor=1.05,
            ),
            Indicate(
                weights[("TR", "BR")],
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
            weights[("BL", "BR")],
            DOWN,
            buff=0.25,
        )


        self.play(
            FadeIn(strong_label),
            Indicate(
                edges[("BL", "BR")],
                color=GREEN_A,
                scale_factor=1.05,
            ),
            Indicate(
                weights[("BL", "BR")],
                color=GREEN_A,
                scale_factor=1.4,
            ),
            run_time=1.3,
        )


        self.wait(1.5)


        # removes the explanation before the next section
        fade_out_all(
            self,
            explanation,
            weak_label,
            strong_label,
            run_time=1,
        )


    # switches between mathematical and real-world node icons
    def show_real_world_models(self, graph):
        # changes the circle nodes into houses
        house_caption = bottom_text(
            "Neighborhood model: edges are roads and weights can show traffic flow",
            font_size=23,
        )


        graph.nodes = switch_node_icons(
            scene=self,
            nodes=graph.nodes,
            new_icons="house",
            colors=self.NODE_COLORS,
            label_positions="below",
            extra_animations=[
                FadeIn(
                    house_caption,
                    shift=UP * 0.2,
                )
            ],
        )


        self.wait(1.5)


        # changes the houses into people
        people_caption = bottom_text(
            "Social model: edges are relationships and weights show closeness",
            font_size=23,
        )


        graph.nodes = switch_node_icons(
            scene=self,
            nodes=graph.nodes,
            new_icons="person",
            colors=self.NODE_COLORS,
            label_positions="below",
            extra_animations=[
                Transform(
                    house_caption,
                    people_caption,
                )
            ],
        )


        self.wait(1.5)


        # changes back to houses and explains that the graph structure stays the same
        final_caption = bottom_text(
            "The graph stays the same even when the real-world model changes",
            font_size=23,
        )


        graph.nodes = switch_node_icons(
            scene=self,
            nodes=graph.nodes,
            new_icons="circle",
            colors=self.NODE_COLORS,
            label_positions="below",
            extra_animations=[
                Transform(
                    house_caption,
                    final_caption,
                )
            ],
        )


        self.wait(1.5)
        self.play(FadeOut(house_caption))


        # updates the graph group so it uses the newest node objects
        refresh_graph_group(graph)
        return graph


    # introduces the graph weights and node models
    def show_intro_scene(self):
        # creates and moves the main title
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


        # adds the nodes heading below the title
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


        # creates the starting graph with circle nodes
        graph = make_graph(
            name_map=self.ORIGINAL_NAMES,
            positions=self.SLOT_POSITIONS,
            edge_data=self.EDGE_DATA,
            colors=self.NODE_COLORS,
            icons="circle",
            label_positions="center",
        )


        # shows the nodes, edges, and weights in order
        animate_graph_build(
            self,
            graph,
        )


        # explains the edges and their weights
        self.explain_edges(
            graph.edges,
            graph.weights,
        )


        # shows how the same graph can represent houses or people
        graph = self.show_real_world_models(graph)


        return main_title, nodes_heading, graph


    # places the graph next to its adjacency matrix
    def show_graph_matrix_scene(
        self,
        main_title,
        nodes_heading,
        graph,
    ):
        # creates the title and adjacency matrix for this section
        title = scene_title(
            "Graph and Adjacency Matrix"
        )


        matrix = make_adjacency_matrix(
            node_order=self.NAMES,
            edge_data=self.EDGE_DATA,
            name_map=self.ORIGINAL_NAMES,
            center=RIGHT * 3.25 + DOWN * 0.35,
            scale_factor=0.90,
            node_colors=self.NODE_COLORS,
        )


        # creates labels showing the number of rows and columns
        guides = make_dimension_guides(matrix)


        # removes the intro text and moves the graph to the left
        self.play(
            FadeOut(main_title),
            FadeOut(nodes_heading),
            FadeIn(title),
            graph.group.animate
            .scale(0.82)
            .move_to(
                LEFT * 3.35 + DOWN * 0.35
            ),
            run_time=1.4,
        )


        # builds the matrix and its row and column guides
        animate_matrix_build(
            self,
            matrix,
            guides,
        )


        # explains what a zero means in the matrix
        zero_note = bottom_text(
            "A zero means there is no direct connection",
            color=GRAY_A,
        )


        self.play(FadeIn(zero_note))
        self.wait(1.5)
        self.play(FadeOut(zero_note))


        return title, graph, matrix, guides


    # compares the same matrix with different display names
    def show_renamed_matrix_scene(
        self,
        old_title,
        graph,
        old_matrix,
        guides,
    ):
        # creates a new section comparing two label styles
        title = scene_title(
            "Same Matrix, Different Node Names"
        )


        # creates the matrix with the original A, B, C, and D labels
        original_matrix = make_adjacency_matrix(
            node_order=self.NAMES,
            edge_data=self.EDGE_DATA,
            name_map=self.ORIGINAL_NAMES,
            center=LEFT * 3.25 + DOWN * 0.45,
            scale_factor=0.76,
            node_colors=self.NODE_COLORS,
        )


        # creates the same matrix with longer display names
        renamed_matrix = make_adjacency_matrix(
            node_order=self.NAMES,
            edge_data=self.EDGE_DATA,
            name_map=self.ORIGINAL_NAMES,
            center=RIGHT * 3.25 + DOWN * 0.45,
            scale_factor=0.70,
            display_names=["Oak", "Pine", "Maple", "Cedar"],
            full_names=True,
            color_keys=self.NAMES,
            node_colors=self.NODE_COLORS,
        )


        # finds one height that works for both headings
        heading_y = max(
            original_matrix.group.get_top()[1],
            renamed_matrix.group.get_top()[1],
        ) + 0.58


        # creates headings above the two matrices
        original_heading = Text(
            "Original labels",
            font_size=24,
            color=BLUE_A,
        )
        original_heading.move_to([
            original_matrix.matrix.get_center()[0],
            heading_y,
            0,
        ])


        renamed_heading = Text(
            "Same graph, different node names",
            font_size=24,
            color=ORANGE,
        )
        renamed_heading.move_to([
            renamed_matrix.matrix.get_center()[0],
            heading_y,
            0,
        ])


        # removes the graph and matrix from the previous section
        fade_out_all(
            self,
            old_title,
            graph.group,
            old_matrix.group,
            guides,
        )


        self.play(FadeIn(title))


        self.play(
            FadeIn(original_matrix.group),
            FadeIn(renamed_matrix.group),
            FadeIn(original_heading),
            FadeIn(renamed_heading),
            run_time=1.6,
        )


        # explains that only the visible names changed
        note = bottom_text(
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


    # changes the graph identities before changing the matrix
    def show_morph_scene(
        self,
        old_title,
        old_original_matrix,
        old_renamed_matrix,
        original_heading,
        renamed_heading,
        old_note,
    ):
        # creates the original graph and matrix for the transformation
        title = scene_title(
            "Changing the Node Names"
        )


        graph = make_graph(
            name_map=self.ORIGINAL_NAMES,
            positions=self.SLOT_POSITIONS,
            edge_data=self.EDGE_DATA,
            colors=self.NODE_COLORS,
            icons="circle",
            label_positions="center",
            center=LEFT * 3.35 + DOWN * 0.45,
            scale_factor=0.82,
        )


        matrix = make_adjacency_matrix(
            node_order=self.NAMES,
            edge_data=self.EDGE_DATA,
            name_map=self.ORIGINAL_NAMES,
            center=RIGHT * 3.25 + DOWN * 0.45,
            scale_factor=0.88,
            node_colors=self.NODE_COLORS,
        )


        # creates labels above the original graph and matrix
        graph_badge = badge(
            "ORIGINAL GRAPH",
            BLUE_A,
            LEFT * 3.35 + UP * 2.05,
        )


        matrix_badge = badge(
            "ORIGINAL MATRIX",
            BLUE_A,
            RIGHT * 3.25 + UP * 2.05,
        )


        # removes the two renamed matrices from the previous section
        fade_out_all(
            self,
            old_title,
            old_original_matrix.group,
            old_renamed_matrix.group,
            original_heading,
            renamed_heading,
            old_note,
        )


        self.play(
            FadeIn(title),
            FadeIn(graph.group),
            FadeIn(matrix.group),
            FadeIn(graph_badge),
            FadeIn(matrix_badge),
            run_time=1.5,
        )


        self.wait(1)


        # creates the graph with the node names moved to new positions
        new_graph = make_graph(
            name_map=self.FLIPPED_NAMES,
            positions=self.SLOT_POSITIONS,
            edge_data=self.EDGE_DATA,
            colors=self.NODE_COLORS,
            icons="circle",
            label_positions="center",
            center=LEFT * 3.35 + DOWN * 0.45,
            scale_factor=0.82,
        )


        # creates the new graph label and explanation
        new_graph_badge = badge(
            "NEW GRAPH",
            ORANGE,
            LEFT * 3.35 + UP * 2.05,
        )


        graph_note = bottom_text(
            "First, the names and colors move to new vertices",
            color=ORANGE,
            font_size=23,
        )


        # changes the original graph into the flipped graph
        self.play(
            Transform(graph.group, new_graph.group),
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


        # creates the matrix that matches the flipped graph
        new_matrix = make_adjacency_matrix(
            node_order=self.NAMES,
            edge_data=self.EDGE_DATA,
            name_map=self.FLIPPED_NAMES,
            center=RIGHT * 3.25 + DOWN * 0.45,
            scale_factor=0.88,
            node_colors=self.NODE_COLORS,
        )


        # creates the new matrix label and explanation
        new_matrix_badge = badge(
            "NEW MATRIX",
            ORANGE,
            RIGHT * 3.25 + UP * 2.05,
        )


        matrix_note = bottom_text(
            "Next, the matrix updates to match the new graph",
            color=ORANGE,
            font_size=23,
        )


        # changes the original matrix into the new matrix
        self.play(
            Transform(matrix.group, new_matrix.group),
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
            graph.group,
            matrix.group,
            graph_badge,
            matrix_badge,
            matrix_note,
        )


    # compares the original and new matrices
    def show_comparison_scene(
        self,
        old_title,
        graph,
        matrix,
        graph_badge,
        matrix_badge,
        old_note,
    ):
        # creates the title and subtitle for the final comparison
        title = scene_title(
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


        # creates the colored background panels
        original_panel = comparison_panel(
            LEFT * 3.25 + DOWN * 0.35,
            BLUE_A,
        )


        new_panel = comparison_panel(
            RIGHT * 3.25 + DOWN * 0.35,
            ORANGE,
        )


        # creates labels above the two matrices
        original_badge = badge(
            "ORIGINAL MATRIX",
            BLUE_A,
            LEFT * 3.25 + UP * 1.55,
            width=2.9,
        )


        new_badge = badge(
            "NEW MATRIX",
            ORANGE,
            RIGHT * 3.25 + UP * 1.55,
            width=2.9,
        )


        # recreates the original and flipped matrices side by side
        original_matrix = make_adjacency_matrix(
            node_order=self.NAMES,
            edge_data=self.EDGE_DATA,
            name_map=self.ORIGINAL_NAMES,
            center=LEFT * 3.25 + DOWN * 0.45,
            scale_factor=0.82,
            node_colors=self.NODE_COLORS,
        )


        new_matrix = make_adjacency_matrix(
            node_order=self.NAMES,
            edge_data=self.EDGE_DATA,
            name_map=self.FLIPPED_NAMES,
            center=RIGHT * 3.25 + DOWN * 0.45,
            scale_factor=0.82,
            node_colors=self.NODE_COLORS,
        )


        # removes the graph transformation section
        fade_out_all(
            self,
            old_title,
            graph,
            matrix,
            graph_badge,
            matrix_badge,
            old_note,
        )


        # shows both matrices and their panels
        self.play(
            FadeIn(title),
            FadeIn(subtitle),
            FadeIn(original_panel),
            FadeIn(new_panel),
            FadeIn(original_badge),
            FadeIn(new_badge),
            FadeIn(original_matrix.group),
            FadeIn(new_matrix.group),
            run_time=1.8,
        )


        # finds every matrix position whose value changed
        original_boxes, new_boxes = make_changed_boxes(
            original_matrix,
            new_matrix,
        )


        # draws the yellow boxes one after another
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


        # highlights the original panel and then the new panel
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


    # runs the five scenes in order
    def construct(self):
        # runs each section in order and passes its objects to the next section
        main_title, nodes_heading, graph = self.show_intro_scene()


        graph_title, graph, matrix, guides = self.show_graph_matrix_scene(
            main_title,
            nodes_heading,
            graph,
        )


        renamed_scene = self.show_renamed_matrix_scene(
            graph_title,
            graph,
            matrix,
            guides,
        )


        morph_scene = self.show_morph_scene(*renamed_scene)


        self.show_comparison_scene(*morph_scene)