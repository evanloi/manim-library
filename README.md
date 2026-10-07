# manim-library

A Python and Manim library for visualizing signal processing and graph signal processing concepts, including graphs, matrices, eigenvalues, eigenvectors, and graph Laplacians.

## Features

- Create customizable graph nodes and edges
- Create weighted and unweighted graphs
- Use circle, square, diamond, star, house, and person icons
- Change node icons and labels during animations
- Generate labeled adjacency matrices
- Calculate and display eigenvalues and eigenvectors
- Animate eigenvector transformations
- Calculate adjacency, degree, and Laplacian matrices
- Apply the graph Laplacian to graph signals
- Color positive, negative, and zero results differently

## Requirements

- Python 3.10 or newer
- Manim
- NumPy

## Basic Usage

Import Manim and GraphWave:

```python
from manim import *
from graphwave import *
```

Example:

```python
from manim import *
from graphwave import *


class QuickGraphDemo(Scene):
    def construct(self):
        graph = make_graph(
            name_map={
                "A": "A",
                "B": "B",
                "C": "C",
            },
            positions={
                "A": LEFT * 2,
                "B": UP * 1.5,
                "C": RIGHT * 2,
            },
            edge_data=[
                ("A", "B", 2),
                ("B", "C", 4),
                ("A", "C", 1),
            ],
            colors={
                "A": BLUE_C,
                "B": GREEN_C,
                "C": ORANGE,
            },
            icons="circle",
        )

        animate_graph_build(self, graph)
        self.wait()
```

Save the code as `quick_graph_demo.py` and render it with:

```bash
python -m manim -pql quick_graph_demo.py QuickGraphDemo
```

## Animations

The `animations` folder contains three complete animations.

### Graphs and Adjacency Matrices

```bash
python -m manim -pql animations/graphmatrix.py GraphMatrixRepresentation
```

### Eigenvalues and Eigenvectors

```bash
python -m manim -pql animations/eigenvector.py GraphEigenvectorAnimation
```

### Graph Laplacians

```bash
python -m manim -pql animations/laplacian.py GraphSignalLaplacian
```

Run these commands from the main `GraphWave` folder.

Use `-pqh` instead of `-pql` for a higher-quality render:

```bash
python -m manim -pqh animations/laplacian.py GraphSignalLaplacian
```

## Main Library File

`graphcommons.py` contains the reusable GraphWave functions and data classes.

The files inside `animations` use those functions to create complete Manim animations.

## License

GraphWave is available under the MIT License.
